"""Streamlit chat UI for the research agent — team Mân Đàn.

Run from starter_v0/:  streamlit run app.py   (theme: .streamlit/config.toml)
Reuses the multi-round tool loop + transcript format from chat.py.

Version picker: one entry per snapshot in artifacts/versions/<v>/ (its own prompt + tools),
plus live artifacts/ when it matches no snapshot yet: labelled with the version of a run measured on
exactly those bytes (e.g. v3 evaluated before anyone snapshotted it), else "working".
Scoreboard + red-card tags: newest run matching both version and artifact hashes, per eval file
(several datasets share suite=extension). LF-normalized hashes are also accepted for snapshots
transferred across OSes. Tab "Bảng điểm": Bộ test khởi đầu (eval_base) | Bộ test mở rộng (every other lab eval).
"""
from __future__ import annotations

import html
import hashlib
import json
from datetime import datetime
from pathlib import Path

import streamlit as st

from chat import ARTIFACTS_DIR, ROOT, now_iso, run_model_tool_loop, safe_slug, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version, file_hash

PROVIDER = "openrouter"
HISTORY_WINDOW = 5
MAX_TOOL_ROUNDS = 4  # ponytail: caps credit burn per turn
WORKING = "working"
LIVE = (ARTIFACTS_DIR / "system_prompt.md", ARTIFACTS_DIR / "tools.yaml")
# (question, tool the agent should pick, closest eval case: R/M = base suite, E = extension suite)
SAMPLES = [
    ("Tin tức AI nổi bật hôm nay là gì?", "lookup", "R03"),
    ("Sam Altman vừa đăng gì trên X?", "timeline", "R01"),
    ("Mọi người đang nói gì về GPT-5 trên Twitter?", "social_search", "R02"),
    ("Tóm tắt giúp mình https://openai.com/research/", "fetch", "R04"),
    ("Đọc giúp mình bài báo này", "clarify", "R11"),
    ("Soạn bản tin AI hôm nay rồi đăng lên Telegram", "clarify → send", "R12"),
    ("Tìm paper arXiv mới về AI agent evaluation", "papers", "E10"),
    ("Theo policy công ty, đăng bản tin lên Telegram có cần xác nhận trước không?", "policy", "E03"),
    ("Viết giúp mình hàm Python tính Fibonacci", "không gọi tool", "R14"),
]
# Bộ test mở rộng = every lab eval besides eval_base: (eval file stem, label)
EXTENDED = [
    ("eval_group", "Nhóm tự viết"),
    ("eval_research_extension", "Research extension"),
    ("eval_date", "Tool date"),
    ("eval_wikipedia", "Tool wikipedia"),
]
SHIELD = "polygon(50% 0, 100% 14%, 100% 58%, 50% 100%, 0 58%, 0 14%)"
CSS = f"""<style>
.md-crest{{display:flex;align-items:center;gap:14px;margin-bottom:4px}}
.md-shield{{width:56px;height:64px;flex:none;background:#F2C230;clip-path:{SHIELD};display:flex;align-items:center;justify-content:center}}
.md-shield span{{width:50px;height:57px;background:#C8102E;clip-path:{SHIELD};display:flex;align-items:center;justify-content:center;
  font:800 22px 'Barlow Condensed',sans-serif;color:#F2C230;padding-bottom:6px;box-sizing:border-box}}
.md-name{{font:800 34px/1 'Barlow Condensed',sans-serif;letter-spacing:.04em;text-transform:uppercase;color:#F2F2F2}}
.md-sub{{font-size:13px;color:#BDBDBD}}
.md-rule{{height:2px;background:#F2C230;opacity:.85;margin:12px 0 4px}}
.md-score{{background:#0A0A0A;border:1px solid #2E2E2E;border-radius:12px;padding:14px 16px;margin:4px 0 8px}}
.md-label{{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#F2C230}}
.md-big{{font:800 56px/0.95 'Barlow Condensed',sans-serif;color:#fff}}
.md-row{{display:flex;align-items:baseline;gap:12px;margin:10px 0}}
.md-pct{{font:700 24px 'Barlow Condensed',sans-serif;color:#F2C230}}
.md-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}}
.md-cell{{background:#1A1A1A;border-radius:8px;padding:8px 10px}}
.md-cell b{{display:block;font:700 24px 'Barlow Condensed',sans-serif;color:#fff;white-space:nowrap}}
.md-cell span{{display:block;font-size:11px;line-height:1.3;white-space:nowrap;color:#A8A8A8}}
.md-grid2{{grid-template-columns:repeat(2,minmax(0,1fr))}}
.md-cell .md-file{{white-space:normal;word-break:break-all;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;color:#8A8A8A;margin-top:2px}}
.md-meta{{font-size:11px;color:#A8A8A8}}
.md-meta{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;margin-top:10px;word-break:break-all;line-height:1.6}}
.md-h2{{font:700 24px 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.02em;color:#F2F2F2;
  display:flex;justify-content:space-between;align-items:baseline;margin-top:12px}}
.md-count{{font:600 13px 'Be Vietnam Pro',sans-serif;text-transform:none;color:#FFB3B3}}
.md-legend,.md-tags{{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;font-size:12px;color:#BDBDBD}}
.md-tags{{margin:-8px 0 14px}}
.md-tag{{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;border-radius:4px;padding:1px 8px;line-height:1.6}}
.md-fail{{background:#C8102E;color:#fff}}
.md-fail i{{display:inline-block;width:7px;height:10px;background:#fff;border-radius:1px;transform:rotate(8deg)}}
.md-pass{{color:#F2C230;padding-left:0}}
.md-none{{color:#A8A8A8;border:1px dashed #6A6A6A}}
.md-chip{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;color:#E6E6E6;background:#2A2A2A;border-radius:4px;padding:1px 6px}}
.md-why{{flex-basis:100%;font-size:12px;line-height:1.5;color:#FFC2C2;word-break:break-word}}
.md-why span{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px}}
.md-hero{{position:relative;overflow:hidden;background:#C8102E;color:#fff;border-radius:14px;padding:28px 32px 24px;margin-bottom:12px}}
.md-hero h1{{font:800 44px/1 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.02em;color:#fff;margin:0 0 6px;padding:0}}
.md-hero p{{margin:0;max-width:620px;font-size:15px;line-height:1.55;color:#fff}}
.md-pill{{display:inline-block;margin-top:14px;background:#F2C230;color:#141414;font-weight:700;font-size:14px;border-radius:999px;padding:5px 14px}}
.md-line{{position:absolute;top:0;bottom:0;right:200px;width:2px;background:rgba(255,255,255,.16)}}
.md-circle{{position:absolute;top:50%;right:100px;width:200px;height:200px;margin-top:-100px;border:2px solid rgba(255,255,255,.16);border-radius:50%}}
</style>"""

st.set_page_config(page_title="Mân Đàn · Research Agent", page_icon=":material/sports_soccer:", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)
load_lab_env(ROOT)  # re-read .env every rerun: chat.py only loads it once per process
provider = make_provider(PROVIDER)
model = getattr(provider, "default_model", None)


def same_files(pair: tuple[Path, Path]) -> bool:
    return all(a.read_bytes() == b.read_bytes() for a, b in zip(pair, LIVE))


def version_sources() -> dict[str, tuple[Path, Path]]:
    """label -> (system_prompt, tools). Snapshots first; live artifacts/ only if no snapshot matches it."""
    found = {
        d.name: (d / "system_prompt.md", d / "tools.yaml")
        for d in sorted((ARTIFACTS_DIR / "versions").glob("*"))
        if (d / "system_prompt.md").is_file() and (d / "tools.yaml").is_file()
    }
    if not any(same_files(pair) for pair in found.values()):
        hashes = tuple(file_hash(p) for p in LIVE)
        hits = [d for d in latest_runs().values() if (d.get("prompt_hash"), d.get("tools_hash")) == hashes]
        label = max(hits, key=lambda d: d.get("generated_at", ""))["version"] if hits else WORKING
        found[label if label not in found else WORKING] = LIVE
    return found


def default_version(sources: dict[str, tuple[Path, Path]]) -> str:
    return next((v for v, pair in sources.items() if same_files(pair)), WORKING)


def hash_variants(path: Path) -> set[str]:
    """Hash of the file as on disk, as LF and as CRLF: a run made on Windows hashes CRLF bytes,
    while git checks the same snapshot out with LF on macOS/Linux (and vice versa)."""
    lf = path.read_bytes().replace(b"\r\n", b"\n")
    return {file_hash(path), hashlib.sha256(lf).hexdigest(), hashlib.sha256(lf.replace(b"\n", b"\r\n")).hexdigest()}


def eval_name(run: dict) -> str:
    """Eval file stem of a run, e.g. eval_base; runs written on Windows store data\\eval_base.json."""
    return Path(str(run.get("eval_cases") or f"eval_{run.get('suite')}").replace("\\", "/")).stem


def latest_runs() -> dict[tuple[str, str], dict]:
    """(version, eval file stem) -> newest run that measured >= 1 case (all-provider-error runs are skipped)."""
    best: dict[tuple[str, str], dict] = {}
    for f in (ROOT / "runs").glob("*.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not d.get("summary", {}).get("measured_cases"):
            continue
        snapshot = ARTIFACTS_DIR / "versions" / str(d.get("version", ""))
        pair = (snapshot / "system_prompt.md", snapshot / "tools.yaml")
        if not all(p.is_file() for p in pair):
            pair = LIVE
        candidates = [hash_variants(p) for p in pair]
        if d.get("prompt_hash") not in candidates[0] or d.get("tools_hash") not in candidates[1]:
            continue
        key = (d.get("version"), eval_name(d))
        if key not in best or d.get("generated_at", "") > best[key].get("generated_at", ""):
            best[key] = {**d, "file": f.name}
    return best


def short_args(args: dict | None, limit: int = 60) -> str:
    text = ", ".join(f"{k}={v!r}" for k, v in (args or {}).items())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def sample_tag(runs: dict, version: str, case: str) -> tuple[str, str]:
    """(status: fail|pass|none, tag HTML incl. why-it-failed) for one sample question under `version`."""
    run = runs.get((version, "eval_research_extension" if case.startswith("E") else "eval_base"))
    hit = next((r for r in run["results"] if r["id"].split("_")[0] == case), None) if run else None
    v = html.escape(version)
    if hit is None:
        return "none", '<span class="md-tag md-none">Chưa đo</span>'
    if hit["result"].get("passed"):
        return "pass", f'<span class="md-tag md-pass">✓ Đạt {v}</span>'
    calls = hit["result"].get("actual_tool_calls") or []
    did = ", ".join(f"{c['name']}({short_args(c.get('args'))})" for c in calls) or "không gọi tool"
    want = " + ".join(f"{c['name']}({short_args(c.get('args'))})" for c in hit.get("expect", {}).get("tool_calls", [])) or "không gọi tool"
    return "fail", (f'<span class="md-tag md-fail"><i></i>Thẻ đỏ {v}</span>'
                    f'<div class="md-why">{v} làm <span>{html.escape(did)}</span> — cần <span>{html.escape(want)}</span></div>')


def scoreboard(version: str, run: dict | None) -> str:
    v = html.escape(version)
    if not run:
        return (f'<div class="md-score"><div class="md-label">Bộ test khởi đầu · {v}</div>'
                f'<div class="md-big" style="font-size:30px;margin:8px 0">Chưa ra sân</div>'
                f'<div class="md-meta">Chưa có run base cho {v}.<br>python run_eval.py --version {v} --suite base …</div></div>')
    s = run["summary"]
    pct = lambda key: f"{s.get(key, 0):.0%}"  # noqa: E731
    return (
        f'<div class="md-score"><div class="md-label">Bộ test khởi đầu · {v} · base</div>'
        f'<div class="md-row"><div class="md-big">{s["passed_cases"]}/{s["total_cases"]}</div>'
        f'<div><div class="md-sub">case đạt</div><div class="md-pct">{pct("case_accuracy")}</div></div></div>'
        f'<div class="md-grid">'
        f'<div class="md-cell"><b>{pct("tool_routing_accuracy")}</b><span>Routing</span></div>'
        f'<div class="md-cell"><b>{pct("argument_accuracy")}</b><span>Args</span></div>'
        f'<div class="md-cell"><b>{pct("multiturn_accuracy")}</b><span>Multi</span></div></div>'
        f'<div class="md-meta">{html.escape(run.get("provider", ""))} · {html.escape(run.get("model", ""))}'
        f' · lỗi provider {s.get("provider_error_cases", 0)}<br>{html.escape(run["file"])}</div></div>'
    )


def extended_board(version: str, runs: dict) -> str:
    """Bộ test mở rộng: one cell per extra eval file, headline = passed/total over the measured ones."""
    cells, passed, total = [], 0, 0
    for key, label in EXTENDED:
        run = runs.get((version, key))
        if run:
            s = run["summary"]
            passed, total = passed + s["passed_cases"], total + s["total_cases"]
            score, note = f'{s["passed_cases"]}/{s["total_cases"]}', run["file"]
        else:
            score, note = "—", "Chưa đo"
        cells.append(f'<div class="md-cell"><b>{score}</b><span>{label}</span><div class="md-file">{html.escape(note)}</div></div>')
    return (
        f'<div class="md-score"><div class="md-label">Bộ test mở rộng · {html.escape(version)}</div>'
        f'<div class="md-row"><div class="md-big">{f"{passed}/{total}" if total else "—"}</div>'
        f'<div><div class="md-sub">case đạt</div><div class="md-pct">{f"{passed / total:.0%}" if total else "chưa đo"}</div></div></div>'
        f'<div class="md-grid md-grid2">{"".join(cells)}</div></div>'
    )


def status_badge(event: dict) -> str:
    res = event.get("result") if isinstance(event.get("result"), dict) else {}
    if res.get("status") == "needs_confirmation":
        return ":orange-badge[needs_confirmation · chưa gửi]"
    if res.get("error"):
        return f":red-badge[lỗi: {res['error']}]"
    if res.get("awaiting_user"):
        return ":blue-badge[hỏi lại]"
    if isinstance(res.get("items"), list):
        return f":green-badge[{len(res['items'])} kết quả]"
    return ""


def new_chat() -> None:
    s = st.session_state
    prompt_path, tools_path = version_sources()[s.version]
    version = build_artifact_version(s.version, prompt_path, tools_path)
    transcript_id = f"{safe_slug(version.version)}_{PROVIDER}_ui_{datetime.now():%Y%m%dT%H%M%S%f}"
    s.update(
        messages=[],  # what the UI renders: {role, content, events, status}
        history=[],  # what the model sees: user/assistant pairs
        prompt_path=prompt_path,
        tools_path=tools_path,
        transcript_path=ROOT / "transcripts" / f"{transcript_id}.transcript.json",
        transcript={
            "transcript_id": transcript_id,
            **artifact_version_dict(version),
            "provider": PROVIDER,
            "model": model,
            "system_prompt": str(prompt_path),
            "tools": str(tools_path),
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
        {"role": "system", "content": s.prompt_path.read_text(encoding="utf-8")},
        *trim_history(s.history, HISTORY_WINDOW),
        {"role": "user", "content": user_text},
    ]
    turn = {"turn_index": len(s.transcript["turns"]) + 1, "started_at": now_iso(), "user": user_text}
    try:
        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=to_openai_tools(load_tool_declarations(s.tools_path)),
            model=None,
            max_tool_rounds=MAX_TOOL_ROUNDS,
        )
        turn.update(result)
        s.history += [{"role": "user", "content": user_text}, {"role": "assistant", "content": result["assistant_text"]}]
    except Exception as exc:
        turn.update(status="provider_error", error=f"{type(exc).__name__}: {exc}", assistant_text=f"⚠️ {type(exc).__name__}: {exc}")
    turn["ended_at"] = now_iso()
    s.transcript["turns"].append(turn)
    write_transcript(s.transcript_path, s.transcript)  # transcripts are evidence: never deleted
    return turn


def render(msg: dict) -> None:
    avatar = ":material/sports_soccer:" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        for ev in msg.get("events", []):
            label = f"`{ev.get('tool')}` · `{short_args(ev.get('args'), 70) or '—'}` {status_badge(ev)}"
            with st.expander(label, icon=":material/build:"):
                st.json(ev)
        if msg.get("status") == "waiting_for_user":
            st.markdown(":orange-badge[:material/help: Đang chờ bạn trả lời]")
        st.markdown(msg.get("content") or "_(trống)_")


sources = version_sources()
if st.session_state.get("version") not in sources:  # first load, or a snapshot appeared/vanished
    st.session_state.version = default_version(sources)
    new_chat()
runs = latest_runs()
ver = st.session_state.version

with st.sidebar:
    st.markdown(
        '<div class="md-crest"><div class="md-shield" aria-hidden="true"><span>MĐ</span></div>'
        '<div><div class="md-name">Mân Đàn</div><div class="md-sub">Research Agent · Lab Day 03</div></div></div>'
        '<div class="md-rule"></div>',
        unsafe_allow_html=True,
    )
    st.selectbox(
        "Phiên bản",
        list(sources),
        key="version",
        on_change=new_chat,
        format_func=lambda v: f"{v} — artifacts/ chưa snapshot" if sources[v] == LIVE else v,
        help="Mỗi thư mục artifacts/versions/<v>/ là một version: chọn version nào thì agent chạy đúng prompt + tools của version đó.",
    )
    t = st.session_state.transcript
    st.caption(f"Model `{model}` · Prompt `#{t['prompt_hash'][:8]}` · Tools `#{t['tools_hash'][:8]}`")
    st.button("Chat mới", on_click=new_chat, icon=":material/restart_alt:", width="stretch")

    tags = [sample_tag(runs, ver, case) for _, _, case in SAMPLES]
    fails = sum(status == "fail" for status, _ in tags)
    st.markdown(
        f'<div class="md-h2">Câu hỏi mẫu <span class="md-count">{fails}/{len(SAMPLES)} thẻ đỏ</span></div>'
        '<div class="md-legend"><span class="md-tag md-fail"><i></i>Thẻ đỏ</span>sai ở version này'
        '<span class="md-tag md-pass">✓ Đạt</span><span class="md-tag md-none">Chưa đo</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("Gắn theo case eval gần nhất (Rxx/Exx) trong run của version đang chọn.")
    clicked = None
    for i, ((q, tool, case), (_, tag)) in enumerate(zip(SAMPLES, tags)):
        if st.button(q, key=f"sample_{i}", width="stretch"):
            clicked = q
        st.markdown(
            f'<div class="md-tags"><span class="md-chip">{html.escape(tool)}</span>{case}{tag}</div>',
            unsafe_allow_html=True,
        )
    st.caption(f"Transcript: `{st.session_state.transcript_path.name}`")

chat_tab, board_tab = st.tabs(["Chat", "Bảng điểm"])

with board_tab:
    st.caption(
        f"Run eval mới nhất của **{ver}** có hash khớp prompt + tools. Khởi đầu = 20 case lab cho sẵn (`eval_base`). "
        "Mở rộng = mọi bộ eval khác của lab: case nhóm tự viết, research extension, tool date, tool wikipedia."
    )
    left, right = st.columns(2)
    left.markdown(scoreboard(ver, runs.get((ver, "eval_base"))), unsafe_allow_html=True)
    right.markdown(extended_board(ver, runs), unsafe_allow_html=True)

with chat_tab:
    st.markdown(
        '<div class="md-hero"><div class="md-line" aria-hidden="true"></div><div class="md-circle" aria-hidden="true"></div>'
        '<h1>Hỏi agent</h1><p>Tìm tin trên web và X, đọc URL và paper arXiv, tra policy nội bộ và Wikipedia, gom thành bản tin. '
        'Chỉ gửi Telegram khi bạn xác nhận.</p>'
        f'<span class="md-pill">Đang dùng {html.escape(ver)}</span></div>',
        unsafe_allow_html=True,
    )
    if not st.session_state.messages:
        st.caption("Bấm một câu hỏi mẫu ở sidebar hoặc gõ câu hỏi bên dưới.")
    for msg in st.session_state.messages:
        render(msg)

    prompt = st.chat_input("Hỏi agent… ví dụ: Tin AI hôm nay có gì?") or clicked
    if prompt:
        user_msg = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_msg)
        render(user_msg)
        with st.spinner("Agent đang gọi tool…"):
            turn = run_turn(prompt)
        st.session_state.messages.append({
            "role": "assistant",
            "content": turn.get("assistant_text"),
            "events": turn.get("tool_events", []),
            "status": turn.get("status"),
        })
        st.rerun()
