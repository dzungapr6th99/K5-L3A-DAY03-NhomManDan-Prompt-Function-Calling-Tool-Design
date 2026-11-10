from __future__ import annotations

import pytest
import requests

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS as T


def payload():
    # Synthetic data for mapping tests, not a real market quote.
    return {'chart': {'result': [{'meta': {'symbol': 'NVDA', 'regularMarketPrice': 123.5,
        'regularMarketTime': 1700000000, 'currency': 'USD', 'shortName': 'Example equity',
        'exchangeName': 'NMS', 'instrumentType': 'EQUITY'}}], 'error': None}}


def test_finance_maps_quote_and_includes_timestamp_and_source(fake_http):
    calls = fake_http(FakeResponse(payload()))
    result = T['get_yahoo_finance_data'](ticker=' nvda ')
    assert len(calls) == 1
    assert calls[0]['url'] == 'https://query1.finance.yahoo.com/v8/finance/chart/NVDA'
    assert calls[0]['params'] == {'range': '1d', 'interval': '1d'}
    assert calls[0]['timeout'] > 0
    assert result['ticker'] == 'NVDA' and result['price'] == 123.5
    assert result['currency'] == 'USD'
    assert result['as_of'] == '2023-11-14T22:13:20+00:00'
    assert result['items'][0]['source'] == 'finance.yahoo.com'
    assert 'previous session' in result['items'][0]['summary']


def test_finance_encodes_futures_ticker(fake_http):
    calls = fake_http(FakeResponse(payload()))
    assert T['get_yahoo_finance_data'](ticker='GC=F')['ticker'] == 'GC=F'
    assert calls[0]['url'].endswith('/GC%3DF')


@pytest.mark.parametrize('ticker', ['', '  ', None, 123, 'https://example.com', 'NVDA AAPL', '../NVDA', 'X'*41])
def test_finance_bad_ticker_does_not_call_network(fake_http, ticker):
    calls = fake_http(FakeResponse(payload()))
    assert T['get_yahoo_finance_data'](ticker=ticker)['error'] == 'invalid_input'
    assert calls == []


@pytest.mark.parametrize('response,expected', [
    (FakeResponse(status_code=429), 'HTTPError'),
    (requests.Timeout('timeout'), 'Timeout'),
    (FakeResponse({'chart': {'result': [], 'error': None}}), 'no_data'),
    (FakeResponse({'chart': {'result': None, 'error': {'description': 'Unknown ticker'}}}), 'provider_error'),
    (FakeResponse(['invalid response']), 'AttributeError'),
])
def test_finance_failure_returns_error_dict(fake_http, response, expected):
    fake_http(response)
    result = T['get_yahoo_finance_data'](ticker='NVDA')
    assert result['error'] == expected
    assert 'price' not in result


@pytest.mark.parametrize('key,value', [('regularMarketPrice', None), ('regularMarketPrice', float('nan')),
    ('regularMarketPrice', True), ('regularMarketTime', None), ('regularMarketTime', 0), ('currency', None)])
def test_finance_missing_or_invalid_metadata_does_not_fabricate_quote(fake_http, key, value):
    data = payload()
    data['chart']['result'][0]['meta'][key] = value
    fake_http(FakeResponse(data))
    assert T['get_yahoo_finance_data'](ticker='NVDA')['error'] == 'no_data'
