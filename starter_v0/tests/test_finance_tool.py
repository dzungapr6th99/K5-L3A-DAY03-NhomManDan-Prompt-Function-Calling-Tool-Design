"""Yahoo Finance tool tests: offline HTTP fixtures, no live market data."""
import pytest
import requests

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS


finance = TOOL_FUNCTIONS["get_yahoo_finance_data"]


def quote_payload(**updates):
    meta = {
        "symbol": "NVDA", "longName": "NVIDIA Corporation",
        "regularMarketPrice": 123.45, "regularMarketTime": 1700000000,
        "currency": "USD", "exchangeName": "NMS", "instrumentType": "EQUITY",
    }
    meta.update(updates)
    return {"chart": {"error": None, "result": [{"meta": meta}]}}


def test_finance_sends_request_and_maps_quote(fake_http):
    calls = fake_http(FakeResponse(quote_payload()))

    result = finance(ticker=" nvda ")

    assert len(calls) == 1
    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == "https://query1.finance.yahoo.com/v8/finance/chart/NVDA"
    assert calls[0]["params"] == {"interval": "1d", "range": "1d"}
    assert calls[0]["timeout"] > 0
    assert result["ticker"] == "NVDA"
    assert result["price"] == 123.45
    assert result["currency"] == "USD"
    assert result["name"] == "NVIDIA Corporation"
    assert result["market_time"] == "2023-11-14T22:13:20+00:00"
    assert result["source_url"] == "https://finance.yahoo.com/quote/NVDA/"
    assert result["instrument_type"] == "EQUITY"


def test_finance_encodes_futures_symbol(fake_http):
    calls = fake_http(FakeResponse(quote_payload(symbol="GC=F", instrumentType="FUTURE")))

    result = finance(ticker="GC=F")

    assert calls[0]["url"].endswith("/GC%3DF")
    assert result["ticker"] == "GC=F"
    assert result["instrument_type"] == "FUTURE"


@pytest.mark.parametrize("ticker", [None, 12, [], "", "  ", "NVIDIA Corporation", "https://example.com", "../NVDA"])
def test_finance_bad_ticker_returns_error_without_http(fake_http, ticker):
    calls = fake_http(FakeResponse({}))

    result = finance(ticker=ticker)

    assert result["error"] == "invalid_input"
    assert calls == []


@pytest.mark.parametrize("response,error", [
    (FakeResponse(status_code=429), "HTTPError"),
    (requests.Timeout("test timeout"), "Timeout"),
    (requests.ConnectionError("offline"), "ConnectionError"),
])
def test_finance_network_failure_returns_error(fake_http, response, error):
    calls = fake_http(response)

    result = finance(ticker="NVDA")

    assert len(calls) == 1
    assert result["error"] == error
    assert "price" not in result


@pytest.mark.parametrize("payload", [
    {"chart": {"error": {"description": "Not Found"}, "result": None}},
    {"chart": {"result": []}},
    quote_payload(regularMarketPrice=None),
    quote_payload(regularMarketPrice="123.45"),
    quote_payload(regularMarketPrice=float("nan")),
    quote_payload(regularMarketTime=None),
])
def test_finance_missing_or_invalid_quote_returns_error(fake_http, payload):
    fake_http(FakeResponse(payload))

    result = finance(ticker="NVDA")

    assert result["error"] == "ValueError"
    assert "price" not in result


def test_registered_deduplicate_executes_through_agent():
    from agent import ResearchAgent
    from providers.base import ModelResponse, ToolCall

    class FakeProvider:
        def complete(self, *args, **kwargs):
            return ModelResponse(tool_calls=[ToolCall("deduplicate", {
                "items": [{"url": "https://example.com"}, {"url": "https://example.com"}],
            })])

    run = ResearchAgent(FakeProvider(), system_prompt="test").run([
        {"role": "user", "content": "Remove duplicate links"},
    ])

    result = run.tool_results[0]["result"]
    assert result["removed_count"] == 1
    assert result["items"] == [{"url": "https://example.com"}]
