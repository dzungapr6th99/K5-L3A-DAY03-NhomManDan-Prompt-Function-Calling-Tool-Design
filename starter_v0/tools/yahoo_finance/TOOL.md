---
name: get_yahoo_finance_data
track: bonus
kind: live_api
provider: Yahoo Finance chart endpoint
requires_env: []
inputs: [ticker]
outputs: [ticker, price, currency, as_of, exchange, instrument_type, url, freshness, items]
side_effect: false
---

# Latest available Yahoo quote

Use for an explicitly provided Yahoo symbol: `NVDA`, `GC=F`, `^GSPC`, `BTC-USD`.
Ask for the symbol when ambiguous. Not for news, trade execution or recommendations.
`GC=F` is gold futures, not a Vietnamese retail gold/spot quote.

Returns a price, original currency and UTC quote timestamp from Yahoo metadata.
Always show timestamp/currency. The latest quote can be delayed or from a previous
session; do not describe it as today's live price solely because it was fetched today.
No fabricated fallback: missing data, malformed response, timeout and HTTP failures
return error dictionaries. This public endpoint can rate-limit or change; no key is
required by this implementation. Network access is required for live use.

Endpoint reference: upstream yfinance chart implementation:
https://github.com/ranaroussi/yfinance/blob/main/yfinance/scrapers/history.py

Example: `get_yahoo_finance_data(ticker="NVDA")`.
Unit tests mock requests and never fetch real market data.
