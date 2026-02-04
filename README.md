# JSONL → MP3 converter

This small utility converts each record from the `text_convert_mp3.jsonl` file into two MP3 files:

- `human_<id>.mp3` — contains all `human` messages joined together for the record
- `gpt_<id>.mp3` — contains all `gpt` messages joined together for the record

Getting started

1. Install dependencies (recommended in a virtualenv):

```
pip install -r requirements.txt
```

2. Run the converter (defaults to `text_convert_mp3.jsonl` in repo root):

```
python scripts/convert_jsonl_to_mp3.py --input text_convert_mp3.jsonl --outdir mp3_output
```

3. The MP3 files will be created in `mp3_output/`.

Notes

- The script uses `gTTS` (Google Text-to-Speech). An internet connection is required while converting.
- You can pass `--lang` to select the language, `--slow` for slower speech and `--overwrite` to force regenerate.
