"""Exercise Streamlit rendering/session behavior without provider/network calls."""
import hashlib
import json
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
    assert app.selectbox[0].value == 'v5'
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


def test_board_counts_a_run_hashed_with_the_other_line_endings(monkeypatch, tmp_path):
    """Runs made on Windows hash CRLF bytes; the LF checkout on macOS/Linux must still match them."""
    snap = ROOT / 'artifacts' / 'versions' / 'v3'
    crlf = lambda p: hashlib.sha256(p.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')).hexdigest()  # noqa: E731
    (tmp_path / 'runs').mkdir()
    run = {'version': 'v3', 'suite': 'group', 'eval_cases': 'data\\eval_group.json', 'generated_at': '2099-01-01',
           'prompt_hash': crlf(snap / 'system_prompt.md'), 'tools_hash': crlf(snap / 'tools.yaml'),
           'summary': {'measured_cases': 10, 'passed_cases': 7, 'total_cases': 10}}
    (tmp_path / 'runs' / 'v3_B_group_test.json').write_text(json.dumps(run), encoding='utf-8')
    app = make_app(monkeypatch, tmp_path)
    app.selectbox[0].select('v3').run(timeout=20)
    assert not app.exception
    board = next(m.value for m in app.markdown if 'Bộ test mở rộng' in m.value)
    assert '7/10' in board and 'Nhóm tự viết' in board
