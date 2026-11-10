import io
import sys

from chat import console_print, run_model_tool_loop
from providers.base import ModelResponse, ToolCall


def test_tool_call_runs_on_cp1252_console_without_changing_unicode_result(monkeypatch):
    buffer = io.BytesIO()
    stream = io.TextIOWrapper(buffer, encoding="cp1252", errors="strict")
    monkeypatch.setattr(sys, "stdout", stream)

    class Provider:
        def complete(self, *args, **kwargs):
            return ModelResponse(text=None, tool_calls=[ToolCall("clarify", {
                "question": "Bạn muốn đọc bài nào? 🔧", "response_type": "text",
            })])

    result = run_model_tool_loop(provider=Provider(), messages=[], tools=[], model=None, max_tool_rounds=1)
    stream.flush()
    assert result["status"] == "waiting_for_user"
    assert result["assistant_text"] == "Bạn muốn đọc bài nào? 🔧"
    assert result["tool_events"][0]["result"]["awaiting_user"] is True
    assert "[tool] clarify(" in buffer.getvalue().decode("cp1252")


def test_cli_output_escapes_unsupported_characters_without_crashing(monkeypatch):
    buffer = io.BytesIO()
    stream = io.TextIOWrapper(buffer, encoding="cp1252", errors="strict")
    monkeypatch.setattr(sys, "stdout", stream)
    console_print("Agent> Bạn muốn đọc bài nào? 🔧")
    stream.flush()
    output = buffer.getvalue().decode("cp1252")
    assert "Agent>" in output
    assert "\\U0001f527" in output
