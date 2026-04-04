from __future__ import annotations

from dataclasses import dataclass
from math import isnan

import numpy as np
import pandas as pd
from scipy.stats import percentileofscore

from .config import DashboardConfig


@dataclass
class HorizonSnapshot:
    name: str
    current_return_pct: float
    percentile: float
    zscore: float
    mean_pct: float
    std_pct: float
    max_drawdown_pct: float


@dataclass
class SignalDecision:
    action: str
    confidence: float
    rationale: list[str]


@dataclass
class DashboardMetrics:
    intraday_change_pct: float
    current_price: float
    current_day: HorizonSnapshot
    current_week: HorizonSnapshot
    current_month: HorizonSnapshot
    seasonality_weekday: pd.Series
    seasonality_month: pd.Series
    seasonality_intraday: pd.Series
    decision: SignalDecision


def _max_drawdown_from_returns(return_series: pd.Series) -> float:
    equity = (1 + return_series.fillna(0) / 100.0).cumprod()
    rolling_max = equity.cummax()
    drawdown = equity / rolling_max - 1.0
    return float(drawdown.min() * 100)


def _safe_zscore(value: float, mean: float, std: float) -> float:
    if std == 0 or isnan(std):
        return 0.0
    return float((value - mean) / std)


def _percentile(value: float, sample: pd.Series) -> float:
    clean = sample.dropna()
    if clean.empty:
        return 50.0
    return float(percentileofscore(clean, value, kind="mean"))


def _period_returns(df: pd.DataFrame, freq: str) -> pd.Series:
    close = df["Close"].resample(freq).last().dropna()
    return close.pct_change() * 100


def _current_period_return(df: pd.DataFrame, period: str) -> float:
    close = df["Close"]
    if period == "day":
        bucket = close.index.normalize()
    elif period == "week":
        iso = close.index.isocalendar()
        bucket = pd.Index([f"{y}-W{w:02d}" for y, w in zip(iso.year, iso.week)], dtype="object")
    elif period == "month":
        bucket = close.index.tz_localize(None).to_period("M")
    else:
        raise ValueError(period)

    current_bucket = bucket[-1]
    current = close[bucket == current_bucket]
    if current.empty:
        return 0.0
    return float((current.iloc[-1] / current.iloc[0] - 1.0) * 100)


def _historical_same_period_returns(df: pd.DataFrame, period: str) -> pd.Series:
    close = df["Close"]
    if period == "day":
        grouped = close.groupby(close.index.normalize())
    elif period == "week":
        iso = close.index.isocalendar()
        keys = [f"{y}-W{w:02d}" for y, w in zip(iso.year, iso.week)]
        grouped = close.groupby(keys)
    elif period == "month":
        grouped = close.groupby(close.index.tz_localize(None).to_period("M"))
    else:
        raise ValueError(period)

    returns = grouped.apply(lambda s: (s.iloc[-1] / s.iloc[0] - 1.0) * 100 if len(s) > 1 else np.nan)
    return pd.Series(returns).dropna()


def _historical_drawdowns(df: pd.DataFrame, period: str) -> pd.Series:
    returns = df["Close"].pct_change() * 100
    if period == "day":
        grouped = returns.groupby(df.index.normalize())
    elif period == "week":
        iso = df.index.isocalendar()
        keys = [f"{y}-W{w:02d}" for y, w in zip(iso.year, iso.week)]
        grouped = returns.groupby(keys)
    elif period == "month":
        grouped = returns.groupby(df.index.tz_localize(None).to_period("M"))
    else:
        raise ValueError(period)
    return grouped.apply(_max_drawdown_from_returns).dropna()


def build_horizon_snapshot(df: pd.DataFrame, period: str) -> HorizonSnapshot:
    current_return = _current_period_return(df, period)
    history = _historical_same_period_returns(df, period)
    drawdowns = _historical_drawdowns(df, period)
    mean = float(history.mean()) if not history.empty else 0.0
    std = float(history.std(ddof=1)) if len(history) > 1 else 0.0
    percentile = _percentile(current_return, history)
    zscore = _safe_zscore(current_return, mean, std)
    current_drawdown = float(drawdowns.iloc[-1]) if not drawdowns.empty else 0.0
    return HorizonSnapshot(
        name=period,
        current_return_pct=current_return,
        percentile=percentile,
        zscore=zscore,
        mean_pct=mean,
        std_pct=std,
        max_drawdown_pct=current_drawdown,
    )


def _seasonality_intraday(df: pd.DataFrame) -> pd.Series:
    intraday_returns = df["Close"].pct_change() * 100
    key = df.index.strftime("%H:%M")
    return intraday_returns.groupby(key).mean().sort_index()


def _seasonality_weekday(df: pd.DataFrame) -> pd.Series:
    daily_close = df["Close"].resample("1D").last().dropna()
    daily_returns = daily_close.pct_change() * 100
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data = daily_returns.groupby(daily_returns.index.day_name()).mean()
    return data.reindex(order).dropna()


def _seasonality_month(df: pd.DataFrame) -> pd.Series:
    monthly_close = df["Close"].resample("1ME").last().dropna()
    monthly_returns = monthly_close.pct_change() * 100
    order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    data = monthly_returns.groupby(monthly_returns.index.month_name()).mean()
    return data.reindex(order).dropna()


def derive_signal(day: HorizonSnapshot, week: HorizonSnapshot, month: HorizonSnapshot) -> SignalDecision:
    rationale: list[str] = []
    score = 0.0

    for snapshot, weight in [(day, 0.5), (week, 0.3), (month, 0.2)]:
        if snapshot.zscore > 1.0:
            score -= weight * min(snapshot.zscore, 3.0)
            rationale.append(f"{snapshot.name} return is stretched high (z={snapshot.zscore:.2f}, pctile={snapshot.percentile:.0f})")
        elif snapshot.zscore < -1.0:
            score += weight * min(abs(snapshot.zscore), 3.0)
            rationale.append(f"{snapshot.name} return is stretched low (z={snapshot.zscore:.2f}, pctile={snapshot.percentile:.0f})")

    if abs(day.current_return_pct) > abs(day.mean_pct) + day.std_pct:
        rationale.append("intraday move is outside its typical daily range")

    if score > 0.35:
        action = "BUY"
    elif score < -0.35:
        action = "SELL"
    else:
        action = "NEUTRAL"
        rationale.append("returns are not far enough from historical norms to force a directional call")

    confidence = min(95.0, max(15.0, abs(score) * 30 + 35))
    return SignalDecision(action=action, confidence=confidence, rationale=rationale)


def compute_dashboard_metrics(df: pd.DataFrame, config: DashboardConfig) -> DashboardMetrics:
    day = build_horizon_snapshot(df, "day")
    week = build_horizon_snapshot(df, "week")
    month = build_horizon_snapshot(df, "month")
    decision = derive_signal(day, week, month)

    intraday_change = float(df["Close"].pct_change().iloc[-1] * 100) if len(df) > 1 else 0.0
    current_price = float(df["Close"].iloc[-1])

    return DashboardMetrics(
        intraday_change_pct=intraday_change,
        current_price=current_price,
        current_day=day,
        current_week=week,
        current_month=month,
        seasonality_weekday=_seasonality_weekday(df),
        seasonality_month=_seasonality_month(df),
        seasonality_intraday=_seasonality_intraday(df),
        decision=decision,
    )
