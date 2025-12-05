"""
Convert JSONL conversation lines into separate MP3 files for human and gpt texts.

Usage:
  python convert_jsonl_to_mp3.py --input text_convert_mp3.jsonl --output mp3_outputs

This script uses gTTS (Google Text-to-Speech) to generate MP3 files. Install requirements in
the project requirements.txt before use.
"""
import argparse
import json
from pathlib import Path
import sys

try:
    from gtts import gTTS
except Exception as e:
    print("Missing dependency gTTS. Install requirements with: python -m pip install -r requirements.txt", file=sys.stderr)
    raise

from tqdm import tqdm


def extract_texts(conv_list):
    human_texts = []
    gpt_texts = []
    for turn in conv_list:
        who = turn.get("from")
        text = turn.get("value", "")
        if not text:
            continue
        if who == "human":
            human_texts.append(text.strip())
        elif who == "gpt":
            gpt_texts.append(text.strip())
    return "\n".join(human_texts), "\n".join(gpt_texts)


def make_tts(text, out_path: Path, lang: str = "en"):
    if not text:
        return False
    tts = gTTS(text=text, lang=lang)
    tts.save(str(out_path))
    return True


def main():
    parser = argparse.ArgumentParser(description="Convert JSONL conversation records to MP3 files")
    parser.add_argument("--input", "-i", required=True, help="Path to the input JSONL file")
    parser.add_argument("--output", "-o", default="mp3_outputs", help="Output directory for MP3 files")
    parser.add_argument("--lang", default="en", help="Language code for TTS (default: en)")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(2)

    with input_path.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    for raw in tqdm(lines, desc="records"):
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            print("Skipping invalid JSON line:", raw[:120], file=sys.stderr)
            continue

        rec_id = obj.get("id") or obj.get("_id") or None
        if rec_id is None:
            print("Skipping record without 'id' field", file=sys.stderr)
            continue

        conv = obj.get("conversations") or obj.get("conversation") or []
        human_text, gpt_text = extract_texts(conv)

        human_path = out_dir / f"human_{rec_id}.mp3"
        gpt_path = out_dir / f"gpt_{rec_id}.mp3"

        made_h = make_tts(human_text, human_path, lang=args.lang)
        made_g = make_tts(gpt_text, gpt_path, lang=args.lang)

        if not made_h:
            # Remove file if created empty
            if human_path.exists():
                human_path.unlink()
        if not made_g:
            if gpt_path.exists():
                gpt_path.unlink()

    print(f"Finished. MP3 files written to: {out_dir}")


if __name__ == "__main__":
    main()
