"""Completed offline tool challenges; HTTP is mocked via fake_http."""
from __future__ import annotations
import pytest
from conftest import FakeResponse
from tools import TOOL_FUNCTIONS as T


def test_clarify_choice_returns_options_and_awaits_user():
    result = T['clarify'](question='Nguồn nào?', response_type='choice', options=['Web', 'X'])
    assert result['options'] == ['Web', 'X']
    assert result['response_type'] == 'choice'
    assert result['awaiting_user'] is True


def test_format_sections_groups_items_by_section():
    items = [{'title': name, 'section': section} for name, section in [('one', 'A'), ('two', 'B'), ('three', 'A')]]
    markdown = T['format'](items=items, template='sections')['markdown']
    assert markdown.count('## A') == markdown.count('## B') == 1
    assert markdown.index('one') < markdown.index('three') < markdown.index('## B')


def test_format_thread_numbers_items():
    result = T['format'](items=[{'title': 'First'}, {'title': 'Second'}], template='thread')
    assert result['markdown'].split('\n\n') == ['1/ First - ', '2/ Second - ']


@pytest.mark.parametrize('items', [None, []])
def test_format_empty_items_does_not_crash(items):
    result = T['format'](items=items)
    assert result['item_count'] == 0
    assert result['markdown'] == ''


def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http):
    monkeypatch.setenv('TELEGRAM_BOT_TOKEN', 'fake-token')
    monkeypatch.setenv('TELEGRAM_CHAT_ID', 'fake-channel')
    calls = fake_http(FakeResponse({'ok': True}))
    assert T['send'](text='Bản tin', confirmed=True)['status'] == 'sent'
    assert len(calls) == 1
    assert calls[0]['method'] == 'POST'
    assert calls[0]['url'] == 'https://api.telegram.org/botfake-token/sendMessage'
    assert calls[0]['json'] == {'chat_id': 'fake-channel', 'text': 'Bản tin', 'parse_mode': 'Markdown'}


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http):
    calls = fake_http(FakeResponse())
    assert T['send'](text='Bản tin', confirmed=True)['error'] == 'RuntimeError'
    assert calls == []


def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http):
    monkeypatch.setenv('TAVILY_API_KEY', 'fake-key')
    calls = fake_http(FakeResponse({'results': []}))
    result = T['lookup'](query='robotics', timeframe=None)
    assert calls[0]['json']['query'] == 'robotics'
    assert 'time_range' not in calls[0]['json']
    assert result['timeframe'] is None and result['items'] == []


def test_fetch_maps_firecrawl_response(monkeypatch, fake_http):
    monkeypatch.setenv('FIRECRAWL_API_KEY', 'fake-key')
    calls = fake_http(FakeResponse({'data': {'markdown': 'Article body', 'metadata': {'title': 'T', 'sourceURL': 'https://example.com/final'}}}))
    result = T['fetch'](url='https://example.com/start')
    assert calls[0]['json'] == {'url': 'https://example.com/start', 'formats': ['markdown']}
    assert result['items'] == [{'title': 'T', 'url': 'https://example.com/final', 'source': 'example.com', 'summary': 'Article body'}]


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http):
    monkeypatch.setenv('FIRECRAWL_API_KEY', 'fake-key')
    fake_http(FakeResponse({'data': {'markdown': 'x' * 5000}}))
    assert T['fetch'](url='https://example.com')['items'][0]['summary'] == 'x' * 4000


def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http):
    monkeypatch.setenv('RAPIDAPI_KEY', 'fake-key')
    raw = [{'text': 'Missing id'}] + [{'tweet_id': str(i), 'screen_name': 'sama', 'text': f'Post {i}'} for i in range(6)]
    calls = fake_http(FakeResponse({'timeline': raw}))
    items = T['timeline'](screenname='sama', limit=3)['items']
    assert calls[0]['params'] == {'screenname': 'sama'}
    assert [i['url'] for i in items] == [f'https://x.com/sama/status/{i}' for i in range(3)]


@pytest.mark.parametrize('search_type', ['Top', 'Latest'])
def test_social_search_passes_search_type(monkeypatch, fake_http, search_type):
    monkeypatch.setenv('RAPIDAPI_KEY', 'fake-key')
    calls = fake_http(FakeResponse({'timeline': []}))
    result = T['social_search'](query='AI', search_type=search_type)
    assert calls[0]['params'] == {'query': 'AI', 'search_type': search_type}
    assert result['search_type'] == search_type and result['items'] == []


def test_policy_empty_query_returns_no_results():
    assert T['policy'](query='')['results'] == []


def test_policy_area_filter_only_returns_that_area():
    result = T['policy'](query='privacy data', policy_area='data_privacy')
    assert result['results']
    assert all(hit['policy_area'] == 'data_privacy' for hit in result['results'])


def test_policy_instruction_like_lines_go_to_untrusted_text():
    hits = T['policy'](query='source citation', policy_area='source_citation', top_k=20)['results']
    assert any('ignore the citation policy' in line for hit in hits for line in hit['untrusted_text'])
    assert all('ignore the citation policy' not in hit['facts'] for hit in hits)


def test_deduplicate_happy_path_preserves_first_source_and_order():
    items = [{'url': 'https://example.com/a', 'title': 'first'}, {'url': 'https://example.com/a', 'title': 'duplicate'}, {'url': 'https://example.com/b'}]
    result = T['deduplicate'](items=items)
    assert result['items'] == [items[0], items[2]]
    assert result['removed_count'] == 1
    assert len(items) == 3


@pytest.mark.parametrize('items', [None, '', {}, [1]])
def test_deduplicate_bad_input_returns_error(items):
    assert T['deduplicate'](items=items)['error'] == 'invalid_input'


def test_deduplicate_invalid_url_returns_error_dict():
    result = T['deduplicate'](items=[{'url': ['not', 'a', 'string']}])
    assert result['error'] == 'invalid_input'
    assert 'url' in result['message']


def test_deduplicate_preserves_items_without_urls_and_does_not_strip_tracking():
    items = [{'title': 'No URL'}, {'url': ''}, {'url': 'https://example.com/a'}, {'url': 'https://example.com/a?utm_source=x'}]
    result = T['deduplicate'](items=items)
    assert result['items'] == items
    assert result['removed_count'] == 0
