#!/usr/bin/env python3
"""
Simple JSONL -> MP3 converter

Reads a JSONL file where each line is a JSON object with an "id" field and
a "conversations" field (list of {"from": "human"|"gpt", "value": text}).

For each record it generates two MP3 files:
  - human_<id>.mp3  (joined text of all 'human' conversation items)
  - gpt_<id>.mp3    (joined text of all 'gpt' conversation items)

Requires: gTTS (pip install gTTS)

Usage:
  python scripts/convert_jsonl_to_mp3.py \
      --input ./text_convert_mp3.jsonl \
      --outdir ./mp3_output

"""
import argparse
import json
import os
from pathlib import Path

try:
    from gtts import gTTS
except Exception as e:
    raise SystemExit("Missing dependency: gTTS is required. Install with 'pip install gTTS'.")


def extract_texts(record):
    """Return (human_text, gpt_text) for a JSON record.

    The function collects all conversation entries whose "from" is
    'human' (case-insensitive) into a single string, and all whose "from"
    is 'gpt' into another string.
    """
    human_parts = []
    gpt_parts = []
    convs = record.get("conversations") or []
    for item in convs:
        who = (item.get("from") or "").strip().lower()
        text = (item.get("value") or "").strip()
        if not text:
            continue
        if who == "human":
            human_parts.append(text)
        elif who == "gpt":
            gpt_parts.append(text)
        else:
            # ignore unknown origins
            continue
    return " ".join(human_parts).strip(), " ".join(gpt_parts).strip()


def process_file(input_path, outdir, language="en", slow=False, overwrite=False):
    os.makedirs(outdir, exist_ok=True)
    created = []
    with open(input_path, "r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                rec = json.loads(raw)
            except Exception as exc:
                print(f"Skipping line {lineno}: invalid json ({exc})")
                continue

            rid = rec.get("id")
            if rid is None:
                print(f"Skipping line {lineno}: missing id")
                continue

            human_text, gpt_text = extract_texts(rec)

            if human_text:
                human_filename = os.path.join(outdir, f"human_{rid}.mp3")
                if not overwrite and os.path.exists(human_filename):
                    print(f"Skipping existing file: {human_filename}")
                else:
                    tts = gTTS(text=human_text, lang=language, slow=slow)
                    tts.save(human_filename)
                    created.append(human_filename)

            if gpt_text:
                gpt_filename = os.path.join(outdir, f"gpt_{rid}.mp3")
                if not overwrite and os.path.exists(gpt_filename):
                    print(f"Skipping existing file: {gpt_filename}")
                else:
                    tts = gTTS(text=gpt_text, lang=language, slow=slow)
                    tts.save(gpt_filename)
                    created.append(gpt_filename)

    return created


def main():
    p = argparse.ArgumentParser(prog="convert_jsonl_to_mp3")
    p.add_argument("--input", "-i", type=Path, default=Path("text_convert_mp3.jsonl"), help="Input JSONL file")
    p.add_argument("--outdir", "-o", type=Path, default=Path("mp3_output"), help="Output folder for MP3s")
    p.add_argument("--lang", "-l", default="en", help="Language code for TTS (default: en)")
    p.add_argument("--slow", action="store_true", help="Make the speech slow")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing mp3 files")

    args = p.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input file not found: {args.input}")

    print(f"Reading: {args.input}")
    print(f"Writing mp3 files to: {args.outdir}")

    created = process_file(str(args.input), str(args.outdir), language=args.lang, slow=args.slow, overwrite=args.overwrite)

    print(f"Created {len(created)} files")
    for x in created:
        print("  ", x)


if __name__ == "__main__":
    main()
