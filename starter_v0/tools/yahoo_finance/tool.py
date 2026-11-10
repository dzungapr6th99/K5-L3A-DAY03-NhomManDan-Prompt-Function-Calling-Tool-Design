"""Read the latest available Yahoo quote; never place orders or invent prices."""
from __future__ import annotations

from datetime import datetime, timezone
import math
import re
from typing import Any
from urllib.parse import quote

import requests

from tools._shared import TIMEOUT, err


def get_yahoo_finance_data(ticker: str = "") -> dict[str, Any]:
    tool = "get_yahoo_finance_data"
    if not isinstance(ticker, str) or not re.fullmatch(r"[A-Za-z0-9^][A-Za-z0-9^=._-]{0,39}", ticker.strip()):
        return {"tool": tool, "error": "invalid_input", "message": "Provide one Yahoo ticker, e.g. NVDA, GC=F or ^GSPC; not a URL."}
    ticker = ticker.strip().upper()
    try:
        response = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{quote(ticker, safe='')}",
            params={"range": "1d", "interval": "1d"},
            headers={"User-Agent": "Mozilla/5.0 (ResearchAgent-Day03)"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        chart = response.json().get("chart") or {}
        if chart.get("error"):
            return {"tool": tool, "ticker": ticker, "error": "provider_error", "message": str(chart["error"].get("description") or chart["error"])}
        results = chart.get("result") or []
        meta = (results[0].get("meta") or {}) if results else {}
        price, timestamp, currency = meta.get("regularMarketPrice"), meta.get("regularMarketTime"), meta.get("currency")
        if (isinstance(price, bool) or not isinstance(price, (int, float)) or not math.isfinite(price)
                or isinstance(timestamp, bool) or not isinstance(timestamp, (int, float))
                or not math.isfinite(timestamp) or timestamp <= 0 or not isinstance(currency, str) or not currency):
            return {"tool": tool, "ticker": ticker, "error": "no_data", "message": "Yahoo did not return a usable price, currency and quote timestamp."}
        as_of = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
        url = f"https://finance.yahoo.com/quote/{quote(ticker, safe='')}/"
        name = meta.get("longName") or meta.get("shortName") or ticker
        summary = f"{ticker}: {price} {currency}; quote timestamp {as_of}. Latest available quote; may be delayed or from a previous session."
        return {
            "tool": tool, "ticker": ticker, "price": price, "currency": currency,
            "as_of": as_of, "exchange": meta.get("exchangeName"),
            "instrument_type": meta.get("instrumentType"), "url": url,
            "freshness": "latest_available_not_guaranteed_realtime",
            "items": [{"title": str(name), "url": url, "source": "finance.yahoo.com", "summary": summary}],
        }
    except Exception as exc:
        return {**err(tool, exc), "ticker": ticker}
