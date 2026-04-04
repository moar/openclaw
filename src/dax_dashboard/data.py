from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import yfinance as yf

from .config import DashboardConfig


@dataclass
class MarketDataResult:
    symbol: str
    frame: pd.DataFrame
    source: str = "yfinance"


REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    return df


def fetch_market_data(config: DashboardConfig) -> MarketDataResult:
    candidates = (config.symbol, *config.fallback_symbols)
    last_error: Exception | None = None

    for symbol in candidates:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=config.period, interval=config.interval, auto_adjust=False)
            df = _normalize_columns(df)
            if df.empty:
                raise ValueError(f"No data returned for {symbol}")
            missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
            if missing:
                raise ValueError(f"Missing columns for {symbol}: {missing}")
            df = df[REQUIRED_COLUMNS].copy()
            df.index = pd.to_datetime(df.index, utc=True).tz_convert(config.tzinfo)
            return MarketDataResult(symbol=symbol, frame=df)
        except Exception as exc:  # pragma: no cover - network path
            last_error = exc
            continue

    raise RuntimeError(f"Unable to fetch market data from any configured symbol: {last_error}")
