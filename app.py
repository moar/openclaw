from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dax_dashboard.analytics import DashboardMetrics, compute_dashboard_metrics
from dax_dashboard.config import DEFAULT_CONFIG
from dax_dashboard.data import fetch_market_data


st.set_page_config(page_title="FDAX Dashboard", layout="wide")

st.title("FDAX Decision Dashboard")
st.caption("Prototype v1: statistical stretch, drawdown, seasonality, and directional bias")

config = DEFAULT_CONFIG

@st.cache_data(ttl=300)
def load_data():
    return fetch_market_data(config)

try:
    market = load_data()
    df = market.frame
    metrics: DashboardMetrics = compute_dashboard_metrics(df, config)
except Exception as exc:
    st.error(f"Data load failed: {exc}")
    st.stop()

with st.sidebar:
    st.header("Data source")
    st.write(f"**Active symbol:** `{market.symbol}`")
    st.write(f"**Interval:** `{config.interval}`")
    st.write(f"**Period:** `{config.period}`")
    st.write(f"**Timezone:** `{config.timezone}`")
    st.info("If FDAX.EX is unavailable, the app falls back to configured proxy symbols.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Current price", f"{metrics.current_price:,.2f}")
col2.metric("Last 5m change", f"{metrics.intraday_change_pct:+.2f}%")
col3.metric("Signal", metrics.decision.action)
col4.metric("Confidence", f"{metrics.decision.confidence:.0f}%")

st.subheader("Decision summary")
summary_color = {
    "BUY": "green",
    "SELL": "red",
    "NEUTRAL": "gray",
}.get(metrics.decision.action, "gray")
st.markdown(f"### :{summary_color}[{metrics.decision.action}] — {metrics.decision.confidence:.0f}% confidence")
for reason in metrics.decision.rationale:
    st.write(f"- {reason}")


def snapshot_table(metrics: DashboardMetrics) -> pd.DataFrame:
    rows = []
    for snap in [metrics.current_day, metrics.current_week, metrics.current_month]:
        rows.append(
            {
                "Horizon": snap.name.title(),
                "Current Return %": round(snap.current_return_pct, 2),
                "Historical Mean %": round(snap.mean_pct, 2),
                "Std Dev %": round(snap.std_pct, 2),
                "Percentile": round(snap.percentile, 1),
                "Z-Score": round(snap.zscore, 2),
                "Current Max Drawdown %": round(snap.max_drawdown_pct, 2),
            }
        )
    return pd.DataFrame(rows)

st.subheader("Current stretch and drawdown")
st.dataframe(snapshot_table(metrics), use_container_width=True, hide_index=True)

st.subheader("Price action")
price_fig = go.Figure()
price_fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price",
    )
)
price_fig.update_layout(height=500, xaxis_rangeslider_visible=False)
st.plotly_chart(price_fig, use_container_width=True)

season_col1, season_col2 = st.columns(2)
with season_col1:
    st.subheader("Weekday seasonality")
    fig_weekday = px.bar(metrics.seasonality_weekday, title="Average daily return by weekday")
    fig_weekday.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_weekday, use_container_width=True)

with season_col2:
    st.subheader("Monthly seasonality")
    fig_month = px.bar(metrics.seasonality_month, title="Average monthly return")
    fig_month.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_month, use_container_width=True)

st.subheader("Intraday seasonality (5m slots)")
fig_intraday = px.line(metrics.seasonality_intraday, title="Average return by time-of-day")
fig_intraday.update_layout(height=350)
st.plotly_chart(fig_intraday, use_container_width=True)

st.caption("This prototype is a decision-support tool, not financial advice. It currently uses automatic data retrieval and a mean-reversion-biased scoring model.")
