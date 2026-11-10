"""Use chat.py's real multi-round CLI; simulate only Telegram delivery."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import chat
from tools import TOOL_FUNCTIONS
from scripts.eval_group_safe import simulated_send


if __name__ == "__main__":
    args = sys.argv[1:]
    directory = Path(args[args.index('--transcripts-dir') + 1]) if '--transcripts-dir' in args else ROOT / 'transcripts'
    before = set(directory.glob('*.transcript.json'))
    original = TOOL_FUNCTIONS['send']
    TOOL_FUNCTIONS['send'] = simulated_send
    try:
        chat.main()
    finally:
        TOOL_FUNCTIONS['send'] = original
        for path in set(directory.glob('*.transcript.json')) - before:
            payload = json.loads(path.read_text(encoding='utf-8'))
            payload['execution_mode'] = 'live_provider_and_read_tools_with_simulated_send'
            payload['simulated_tools'] = ['send']
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
