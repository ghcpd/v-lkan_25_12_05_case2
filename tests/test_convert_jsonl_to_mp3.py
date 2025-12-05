import io
from pathlib import Path
import json
import pytest

import convert_jsonl_to_mp3 as module


class FakeTTS:
    def __init__(self, text, lang="en"):
        self.text = text
        self.lang = lang

    def save(self, path):
        # write simple bytes to simulate an mp3 file
        Path(path).write_bytes(b"FAKE_MP3_BYTES_" + self.text.encode("utf-8"))


def test_generate_mp3s_creates_files(tmp_path, monkeypatch):
    # prepare a small jsonl
    jsonl = tmp_path / "sample.jsonl"
    lines = [
        {"id": "1", "conversations": [{"from": "human", "value": "Hello"}, {"from": "gpt", "value": "Hi"}]},
        {"id": "2", "conversations": [{"from": "human", "value": "Q2"}, {"from": "gpt", "value": "A2"}]},
    ]
    with jsonl.open("w", encoding="utf-8") as fh:
        for obj in lines:
            fh.write(json.dumps(obj, ensure_ascii=False) + "\n")

    outdir = tmp_path / "out"

    # monkeypatch gTTS in the module to avoid network calls
    monkeypatch.setattr(module, "gTTS", FakeTTS)

    module.generate_mp3s(str(jsonl), str(outdir))

    # assert files exist and non-empty
    for id_ in ["1", "2"]:
        h = outdir / f"human_{id_}.mp3"
        g = outdir / f"gpt_{id_}.mp3"
        assert h.exists() and h.stat().st_size > 0
        assert g.exists() and g.stat().st_size > 0


def test_missing_fields_create_placeholders(tmp_path, monkeypatch):
    jsonl = tmp_path / "sample2.jsonl"
    obj = {"id": "3", "conversations": [{"from": "human", "value": ""}, {"from": "gpt", "value": ""}]}
    jsonl.write_text(json.dumps(obj, ensure_ascii=False) + "\n", encoding="utf-8")

    outdir = tmp_path / "out2"
    monkeypatch.setattr(module, "gTTS", FakeTTS)
    module.generate_mp3s(str(jsonl), str(outdir))

    h = outdir / "human_3.mp3"
    g = outdir / "gpt_3.mp3"
    # even empty texts should produce files (placeholders)
    assert h.exists()
    assert g.exists()

