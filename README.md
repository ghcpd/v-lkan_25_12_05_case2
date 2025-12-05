Usage
-----

This repo contains a small script to convert each line in `text_convert_mp3.jsonl` into two MP3 files: `human_<id>.mp3` and `gpt_<id>.mp3`.

Setup

1. Create a virtual environment (recommended).

   On Windows (cmd.exe):

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run

```
python scripts\generate_mp3.py
```

Outputs are written to `mp3_outputs/`.
