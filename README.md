# FDAX Decision Dashboard

Prototype dashboard for DAX/FDAX decision support.

## Features in v1

- Automatic market data pull via Yahoo Finance
- Primary symbol: `FDAX.EX`
- Fallback symbol(s): `^GDAXI`
- 5-minute dashboard
- Current day/week/month return stretch
- Current max drawdown by day/week/month
- Weekday, monthly, and intraday seasonality
- Buy / Sell / Neutral score with confidence and rationale

## Run

```bash
cd /root/.openclaw/workspace
. .venv/bin/activate
streamlit run app.py
```

## Notes

- TradingView symbol target remains `FDAX1!`, but v1 uses automated proxy/free data.
- Current model is intentionally simple and interpretable.
- Next iteration can add Telegram alerts, TradingView alerts, richer regime filters, and better futures-accurate data sources.
