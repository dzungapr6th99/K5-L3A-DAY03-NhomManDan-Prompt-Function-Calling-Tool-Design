"""Streamlit chat UI for the research agent.

Run from starter_v0/:  streamlit run app.py
Reuses the multi-round tool loop + transcript format from chat.py.
"""
from __future__ import annotations

import json
from datetime import datetime

import streamlit as st

from chat import ARTIFACTS_DIR, ROOT, now_iso, run_model_tool_loop, safe_slug, trim_history, write_transcript
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

PROVIDER = "openai"
PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
HISTORY_WINDOW = 5
MAX_TOOL_ROUNDS = 4  # ponytail: caps credit burn per turn when other teams use the public link
SAMPLES = [
    "Tin tức AI nổi bật hôm nay là gì?",
    "Sam Altman vừa đăng gì trên X?",
    "Mọi người đang nói gì về GPT-5 trên Twitter?",
    "Tóm tắt giúp mình https://openai.com/research/",
    "Đọc giúp mình bài báo này",
    "Soạn bản tin AI hôm nay rồi đăng lên Telegram",
]

st.set_page_config(page_title="Research Agent", page_icon="🔎")
provider = make_provider(PROVIDER)
model = getattr(provider, "default_model", None)


def new_chat() -> None:
    version = build_artifact_version(st.session_state.get("version") or "v0", PROMPT_PATH, TOOLS_PATH)
    transcript_id = f"{safe_slug(version.version)}_{PROVIDER}_ui_{datetime.now():%Y%m%dT%H%M%S%f}"
    st.session_state.update(
        messages=[],  # what the UI renders: {role, content, events}
        history=[],  # what the model sees: user/assistant pairs
        transcript_path=ROOT / "transcripts" / f"{transcript_id}.transcript.json",
        transcript={
            "transcript_id": transcript_id,
            **artifact_version_dict(version),
            "provider": PROVIDER,
            "model": model,
            "system_prompt": str(PROMPT_PATH),
            "tools": str(TOOLS_PATH),
            "history_window": HISTORY_WINDOW,
            "max_tool_rounds": MAX_TOOL_ROUNDS,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "turns": [],
        },
    )


def run_turn(user_text: str) -> dict:
    s = st.session_state
    messages = [
        {"role": "system", "content": PROMPT_PATH.read_text(encoding="utf-8")},
        *trim_history(s.history, HISTORY_WINDOW),
        {"role": "user", "content": user_text},
    ]
    turn = {"turn_index": len(s.transcript["turns"]) + 1, "started_at": now_iso(), "user": user_text}
    try:
        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=to_openai_tools(load_tool_declarations(TOOLS_PATH)),
            model=None,
            max_tool_rounds=MAX_TOOL_ROUNDS,
        )
        turn.update(result)
        s.history += [{"role": "user", "content": user_text}, {"role": "assistant", "content": result["assistant_text"]}]
    except Exception as exc:
        turn.update(status="provider_error", error=f"{type(exc).__name__}: {exc}", assistant_text=f"⚠️ {type(exc).__name__}: {exc}")
    turn["ended_at"] = now_iso()
    s.transcript["turns"].append(turn)
    write_transcript(s.transcript_path, s.transcript)
    return turn


def render(msg: dict) -> None:
    with st.chat_message(msg["role"]):
        for ev in msg.get("events", []):
            args = json.dumps(ev.get("args", {}), ensure_ascii=False)
            with st.expander(f"🔧 {ev['tool']}({args[1:-1][:80]})"):
                st.json(ev)
        st.markdown(msg["content"] or "_(trống)_")


if "transcript" not in st.session_state:
    new_chat()

with st.sidebar:
    st.header("🔎 Research Agent")
    st.text_input("Version", value="v0", key="version", on_change=new_chat)
    t = st.session_state.transcript
    st.caption(f"Model: `{model}`  \nPrompt `#{t['prompt_hash'][:8]}` · Tools `#{t['tools_hash'][:8]}`")
    st.button("🗑 Chat mới", on_click=new_chat, width="stretch")
    st.subheader("Câu hỏi mẫu")
    clicked = None
    for q in SAMPLES:
        if st.button(q, width="stretch"):
            clicked = q
    st.caption(f"Transcript: `{st.session_state.transcript_path.name}`")

for msg in st.session_state.messages:
    render(msg)

prompt = st.chat_input("Hỏi agent…") or clicked
if prompt:
    user_msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_msg)
    render(user_msg)
    with st.spinner("Agent đang gọi tool…"):
        turn = run_turn(prompt)
    st.session_state.messages.append(
        {"role": "assistant", "content": turn.get("assistant_text"), "events": turn.get("tool_events", [])}
    )
    st.rerun()
