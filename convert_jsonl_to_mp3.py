import json
from pathlib import Path
from gtts import gTTS


def generate_mp3s(jsonl_path: str, output_dir: str):
    """Read a JSONL file and generate two MP3s per line: human_<id>.mp3 and gpt_<id>.mp3

    Args:
        jsonl_path: path to the JSONL file
        output_dir: directory where MP3s will be saved
    """
    jsonl_path = Path(jsonl_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with jsonl_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            id_ = obj.get("id")
            if id_ is None:
                # skip entries without id
                continue

            # find human and gpt text
            human_text = None
            gpt_text = None
            for turn in obj.get("conversations", []) or []:
                if turn.get("from") == "human" and human_text is None:
                    human_text = turn.get("value", "")
                elif turn.get("from") == "gpt" and gpt_text is None:
                    gpt_text = turn.get("value", "")

            human_text = (human_text or "").strip()
            gpt_text = (gpt_text or "").strip()

            # generate files
            if human_text:
                out_h = output_dir / f"human_{id_}.mp3"
                tts = gTTS(text=human_text, lang="en")
                tts.save(str(out_h))
            else:
                # create empty placeholder file to keep naming consistent
                out_h = output_dir / f"human_{id_}.mp3"
                out_h.write_bytes(b"")

            if gpt_text:
                out_g = output_dir / f"gpt_{id_}.mp3"
                tts = gTTS(text=gpt_text, lang="en")
                tts.save(str(out_g))
            else:
                out_g = output_dir / f"gpt_{id_}.mp3"
                out_g.write_bytes(b"")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert JSONL lines to two MP3 files each")
    parser.add_argument("jsonl", help="Path to JSONL file")
    parser.add_argument("outdir", help="Directory to save MP3 files")
    args = parser.parse_args()
    generate_mp3s(args.jsonl, args.outdir)
