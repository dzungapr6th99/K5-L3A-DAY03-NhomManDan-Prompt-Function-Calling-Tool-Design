"""Exercise Streamlit rendering/session behavior without provider/network calls."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

import chat
import providers
from providers.base import ModelResponse

ROOT = Path(__file__).resolve().parents[1]


class OfflineProvider:
    default_model = "offline-ui-check"

    def complete(self, *args, **kwargs):
        return ModelResponse(text="Tôi hỗ trợ tìm kiếm và tổng hợp nguồn nghiên cứu.", tool_calls=[])


def make_app(monkeypatch, tmp_path):
    monkeypatch.setattr(chat, 'ROOT', tmp_path)
    monkeypatch.setattr(providers, 'make_provider', lambda _: OfflineProvider())
    app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=20)
    assert not app.exception
    return app


def test_ui_loads_final_snapshot_and_switches_version(monkeypatch, tmp_path):
    app = make_app(monkeypatch, tmp_path)
    assert app.selectbox[0].value == 'v3'
    app.selectbox[0].select('v1').run(timeout=20)
    assert not app.exception
    assert app.session_state['transcript']['version'] == 'v1'
    assert Path(app.session_state['prompt_path']).parent.name == 'v1'


def test_ui_chat_writes_a_transcript_and_new_chat_clears_history(monkeypatch, tmp_path):
    app = make_app(monkeypatch, tmp_path)
    app.chat_input[0].set_value('Bạn làm được gì?').run(timeout=20)
    assert not app.exception
    assert len(app.chat_message) == 2
    assert len(app.session_state['history']) == 2
    assert len(app.session_state['transcript']['turns']) == 1
    assert app.session_state['transcript']['turns'][0]['status'] == 'answered'
    assert list((tmp_path / 'transcripts').glob('*.transcript.json'))
    next(b for b in app.button if b.label == 'Chat mới').click().run(timeout=20)
    assert not app.exception
    assert app.session_state['history'] == []
    assert app.session_state['transcript']['turns'] == []
