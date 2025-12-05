# JSONL to MP3 converter

This small utility converts each JSONL record in `text_convert_mp3.jsonl` into two MP3 files:
- `human_<id>.mp3` for the human text
- `gpt_<id>.mp3` for the GPT text

Requirements
-----------
Install Python packages with:

```
python -m pip install -r requirements.txt
```

Usage
-----
Run the script with the input JSONL and a target output folder:

```
python convert_jsonl_to_mp3.py --input text_convert_mp3.jsonl --output mp3_outputs
```

The script reads the `conversations` list on each line and joins multiple `human` or `gpt` turns into single MP3 files per id.

Notes
-----
- The script uses gTTS (Google Text-to-Speech) and requires an Internet connection.
- If a record lacks either a human or a gpt message, the corresponding MP3 file will not be created.
