from __future__ import annotations

import math
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

import requests

from tools._shared import TIMEOUT, err


def get_yahoo_finance_data(ticker: str = "") -> dict[str, Any]:
    """Return the latest regular-session quote supplied by Yahoo, not a forecast."""
    if not isinstance(ticker, str) or not re.fullmatch(r"[A-Za-z0-9^][A-Za-z0-9.^=\-]{0,31}", ticker.strip()):
        return {
            "tool": "get_yahoo_finance_data", "error": "invalid_input",
            "message": "Provide a Yahoo Finance ticker such as AAPL, NVDA or GC=F.",
        }
    symbol = ticker.strip().upper()
    try:
        response = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{quote(symbol, safe='')}",
            params={"interval": "1d", "range": "1d"},
            headers={"User-Agent": "ResearchAgentLab/1.0"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        chart = response.json().get("chart") or {}
        if chart.get("error"):
            raise ValueError(f"Yahoo Finance error: {chart['error']}")
        results = chart.get("result") or []
        if not results:
            raise ValueError("Yahoo Finance returned no quote for this ticker.")
        meta = results[0].get("meta") or {}
        price = meta.get("regularMarketPrice")
        timestamp = meta.get("regularMarketTime")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or not math.isfinite(price):
            raise ValueError("Yahoo Finance returned no valid market price.")
        if isinstance(timestamp, bool) or not isinstance(timestamp, (int, float)):
            raise ValueError("Yahoo Finance returned no market timestamp.")
        return {
            "tool": "get_yahoo_finance_data",
            "ticker": meta.get("symbol") or symbol,
            "name": meta.get("longName") or meta.get("shortName") or symbol,
            "price": price,
            "currency": meta.get("currency"),
            "exchange": meta.get("exchangeName"),
            "instrument_type": meta.get("instrumentType"),
            "market_time": datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
            "source": "Yahoo Finance",
            "source_url": f"https://finance.yahoo.com/quote/{quote(symbol, safe='')}/",
            "freshness": "Latest regular-session quote from provider; may be delayed or from a previous session.",
        }
    except Exception as exc:
        return err("get_yahoo_finance_data", exc)
