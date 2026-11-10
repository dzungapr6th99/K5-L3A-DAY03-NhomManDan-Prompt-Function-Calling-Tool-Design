"""Run the normal eval CLI with send simulated, never posting to Telegram.

All provider/read tools remain live. Each produced run explicitly records the
action simulation; this is routing evidence, not evidence of Telegram delivery.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import run_eval
from tools import TOOL_FUNCTIONS


def simulated_send(text="", confirmed=False):
    return {
        "tool": "send_telegram", "status": "dry_run_not_sent",
        "confirmed": confirmed, "text": text,
        "message": "Action simulated for eval; no Telegram request was made.",
    }


if __name__ == "__main__":
    # Scope metadata collection to the runs directory selected by the normal CLI.
    args = sys.argv[1:]
    runs_dir = Path(args[args.index('--runs-dir') + 1]) if '--runs-dir' in args else ROOT / 'runs'
    before = set(runs_dir.glob('*.json'))
    original = TOOL_FUNCTIONS['send']
    TOOL_FUNCTIONS['send'] = simulated_send
    try:
        run_eval.main()
    finally:
        TOOL_FUNCTIONS['send'] = original
        for path in set(runs_dir.glob('*.json')) - before:
            payload = json.loads(path.read_text(encoding='utf-8'))
            payload['execution_mode'] = 'live_provider_and_read_tools_with_simulated_send'
            payload['simulated_tools'] = ['send']
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
