import os
import json
import sys
from pathlib import Path

try:
    from gtts import gTTS
except Exception:
    gTTS = None


INPUT = Path(__file__).resolve().parent.parent / 'text_convert_mp3.jsonl'
OUT_DIR = Path(__file__).resolve().parent.parent / 'mp3_outputs'


def ensure_deps():
    if gTTS is None:
        print('The `gTTS` package is required. Install with: pip install -r requirements.txt')
        sys.exit(1)


def make_tts(text: str, out_path: Path, lang: str = 'en'):
    tts = gTTS(text=text, lang=lang)
    tts.save(str(out_path))


def main():
    ensure_deps()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT.exists():
        print(f"Input file not found: {INPUT}")
        sys.exit(1)

    with INPUT.open('r', encoding='utf-8') as fh:
        for idx, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON on line {idx}")
                continue

            record_id = obj.get('id') or obj.get('uid') or str(idx)

            human_text = None
            gpt_text = None

            # Support conversation arrays with {from, value}
            convs = obj.get('conversations') or obj.get('conversation') or []
            if isinstance(convs, list):
                for turn in convs:
                    if not isinstance(turn, dict):
                        continue
                    who = (turn.get('from') or '').lower()
                    val = turn.get('value') or turn.get('text') or ''
                    if who in ('human', 'user') and val:
                        human_text = val.strip()
                    if who in ('gpt', 'assistant') and val:
                        gpt_text = val.strip()

            # Fallbacks for simple fields
            if not human_text:
                human_text = obj.get('human') or obj.get('human_text') or obj.get('humanText') or obj.get('user')
            if not gpt_text:
                gpt_text = obj.get('gpt') or obj.get('gpt_text') or obj.get('gptText') or obj.get('assistant')

            if human_text:
                out_h = OUT_DIR / f'human_{record_id}.mp3'
                print(f'Generating {out_h.name}')
                make_tts(human_text, out_h)
            else:
                print(f'No human text for record {record_id}, skipping human_{record_id}.mp3')

            if gpt_text:
                out_g = OUT_DIR / f'gpt_{record_id}.mp3'
                print(f'Generating {out_g.name}')
                make_tts(gpt_text, out_g)
            else:
                print(f'No GPT text for record {record_id}, skipping gpt_{record_id}.mp3')


if __name__ == '__main__':
    main()
