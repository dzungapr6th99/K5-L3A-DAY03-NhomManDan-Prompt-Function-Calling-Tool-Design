"""Unit tests for the `wikipedia` tool. HTTP is mocked via fake_http (offline, free)."""
from __future__ import annotations

import pytest
import requests
from conftest import FakeResponse

from tools import TOOL_FUNCTIONS as T

PAGE = {
    "type": "standard",
    "title": "Anthropic",
    "description": "American artificial intelligence company",
    "extract": "Anthropic PBC is an American artificial intelligence company.",
    "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Anthropic"}},
}


def test_wikipedia_maps_summary_and_builds_url(fake_http):
    calls = fake_http(FakeResponse(PAGE))
    result = T["wikipedia"](title="Transformer (deep learning)", lang="en")
    assert calls[0]["url"] == "https://en.wikipedia.org/api/rest_v1/page/summary/Transformer_%28deep_learning%29"
    assert "User-Agent" in calls[0]["headers"]
    assert result["summary"] == PAGE["extract"]
    assert result["url"] == "https://en.wikipedia.org/wiki/Anthropic"
    assert result["ambiguous"] is False


def test_wikipedia_404_is_not_found_error(fake_http):
    fake_http(FakeResponse(status_code=404))
    result = T["wikipedia"](title="Không có trang này", lang="vi")
    assert result["error"] == "not_found"
    assert "en" in result["message"]


def test_wikipedia_disambiguation_page_is_flagged(fake_http):
    fake_http(FakeResponse({**PAGE, "type": "disambiguation"}))
    assert T["wikipedia"](title="Mercury", lang="en")["ambiguous"] is True


@pytest.mark.parametrize("title, lang", [("", "vi"), ("   ", "en"), (None, "vi"), ("Anthropic", "fr")])
def test_wikipedia_bad_input_returns_error_without_request(fake_http, title, lang):
    calls = fake_http(FakeResponse(PAGE))
    assert T["wikipedia"](title=title, lang=lang)["error"] == "invalid_input"
    assert calls == []


def test_wikipedia_network_error_returns_error_dict(fake_http):
    fake_http(requests.ConnectionError("down"))
    assert T["wikipedia"](title="Anthropic")["error"] == "ConnectionError"
