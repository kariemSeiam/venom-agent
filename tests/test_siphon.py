"""Tests for SIPHON extraction, memory I/O, rebirth, daemon, and corrections."""

from __future__ import annotations

import json
import time
from dataclasses import replace
from pathlib import Path

import httpx
import pytest
import yaml
from pydantic import ValidationError

from ven0m.core.config import SiphonConfig, VenomConfig
from ven0m.siphon.backoff import BackoffController
from ven0m.siphon.daemon import (
    ensure_memory_and_watch_dirs,
    process_session_json_file,
)
from ven0m.siphon.extractor import (
    CORRECTIONS_HEADER,
    Extraction,
    append_corrections,
    append_extraction,
    append_siphon_error,
    build_rebirth_prompt,
    extract,
    read_memory,
)

from ven0m.siphon.schema import ExtractionResult, ExtractionSeverity


# ── Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def tmp_memory(tmp_path: Path) -> Path:
    return tmp_path / "MEMORY" / "MEMORY.md"


@pytest.fixture
def sample_extraction() -> Extraction:
    return Extraction(
        session_id="session-001",
        date="2026-05-10",
        decisions=["Built SIPHON v0 in Python", "Scraped old Claude Code artifacts"],
        corrections=["Old siphon.ts used Z.AI endpoint wrong — fixed model name"],
        next_action="Run siphon for 20 sessions before expanding",
        current_truth="VENOM is a Python package, not a Claude Code workspace.",
        blocks=["Waiting on API quota"],
        artifacts=["src/ven0m/siphon/extractor.py"],
        energy_state="building",
    )


# ── Extraction dataclass ───────────────────────────────────────────────

class TestExtraction:
    def test_schema_7_fields(self, sample_extraction: Extraction):
        assert sample_extraction.blocks == ["Waiting on API quota"]
        assert sample_extraction.artifacts == ["src/ven0m/siphon/extractor.py"]
        assert sample_extraction.energy_state == "building"

    def test_to_yaml_produces_valid_yaml(self, sample_extraction: Extraction):
        out = sample_extraction.to_yaml()
        data = yaml.safe_load(out)
        assert data["session"]["id"] == "session-001"
        assert data["session"]["date"] == "2026-05-10"
        assert len(data["session"]["decisions"]) == 2
        assert data["session"]["energy_state"] == "building"
        assert data["session"]["blocks"]

    def test_from_dict_roundtrip(self, sample_extraction: Extraction):
        data = yaml.safe_load(sample_extraction.to_yaml())
        reconstructed = Extraction.from_dict(data)
        assert reconstructed == sample_extraction

    def test_from_dict_handles_missing_fields(self):
        data = {"session": {"id": "session-099"}}
        ex = Extraction.from_dict(data)
        assert ex.session_id == "session-099"
        assert ex.decisions == []
        assert ex.corrections == []
        assert ex.next_action == ""
        assert ex.current_truth == ""
        assert ex.blocks == []
        assert ex.artifacts == []
        assert ex.energy_state == "idle"

    def test_from_dict_no_session_key_reads_top_level(self):
        """Without 'session' wrapper, reads id from top-level dict."""
        data = {"id": "session-042", "date": "2026-01-01"}
        ex = Extraction.from_dict(data)
        assert ex.session_id == "session-042"


# ── Memory I/O ─────────────────────────────────────────────────────────

class TestMemoryIO:
    def test_append_creates_file(self, tmp_memory: Path, sample_extraction: Extraction):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        append_extraction(sample_extraction, tmp_memory)
        assert tmp_memory.exists()

    def test_append_adds_separator(self, tmp_memory: Path, sample_extraction: Extraction):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        append_extraction(sample_extraction, tmp_memory)
        content = tmp_memory.read_text()
        assert "\n---\n" in content
        assert "session-001" in content

    def test_append_multiple_extractions(self, tmp_memory: Path, sample_extraction: Extraction):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        ex2 = Extraction(
            session_id="session-002",
            date="2026-05-11",
            decisions=["Added tests"],
            corrections=[],
            next_action="Ship it",
            current_truth="Tests pass.",
            blocks=[],
            artifacts=[],
            energy_state="idle",
        )
        append_extraction(sample_extraction, tmp_memory)
        append_extraction(ex2, tmp_memory)
        extractions = read_memory(tmp_memory)
        assert len(extractions) == 2
        assert extractions[0].session_id == "session-001"
        assert extractions[1].session_id == "session-002"

    def test_read_memory_respects_last_n(self, tmp_memory: Path):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        for i in range(10):
            ex = Extraction(
                session_id=f"session-{i:03d}",
                date="2026-05-10",
                decisions=[f"Decision {i}"],
                corrections=[],
                next_action="",
                current_truth="",
                blocks=[],
                artifacts=[],
                energy_state="idle",
            )
            append_extraction(ex, tmp_memory)

        last_3 = read_memory(tmp_memory, last_n=3)
        assert len(last_3) == 3
        assert last_3[0].session_id == "session-007"
        assert last_3[2].session_id == "session-009"

    def test_read_memory_empty_file(self, tmp_memory: Path):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        tmp_memory.write_text("")
        assert read_memory(tmp_memory) == []

    def test_read_memory_nonexistent(self, tmp_memory: Path):
        assert read_memory(tmp_memory) == []

    def test_read_memory_skips_garbage(self, tmp_memory: Path, sample_extraction: Extraction):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        append_extraction(sample_extraction, tmp_memory)
        with open(tmp_memory, "a") as f:
            f.write("\n---\nthis is not yaml at all\n")
        extractions = read_memory(tmp_memory)
        assert len(extractions) == 1


# ── Rebirth prompt ─────────────────────────────────────────────────────

class TestRebirthPrompt:
    def test_empty_memory_returns_empty(self, tmp_memory: Path):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        assert build_rebirth_prompt(tmp_memory) == ""

    def test_rebirth_includes_current_truth(self, tmp_memory: Path, sample_extraction: Extraction):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        append_extraction(sample_extraction, tmp_memory)
        prompt = build_rebirth_prompt(tmp_memory)
        assert "Truth: VENOM is a Python package" in prompt

    def test_rebirth_includes_decisions(self, tmp_memory: Path, sample_extraction: Extraction):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        append_extraction(sample_extraction, tmp_memory)
        prompt = build_rebirth_prompt(tmp_memory)
        assert "Decision: Built SIPHON v0" in prompt

    def test_rebirth_includes_corrections(self, tmp_memory: Path, sample_extraction: Extraction):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        append_extraction(sample_extraction, tmp_memory)
        prompt = build_rebirth_prompt(tmp_memory)
        assert "Correction: Old siphon.ts" in prompt

    def test_rebirth_includes_next_action(self, tmp_memory: Path, sample_extraction: Extraction):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        append_extraction(sample_extraction, tmp_memory)
        prompt = build_rebirth_prompt(tmp_memory)
        assert "Next: Run siphon for 20 sessions" in prompt

    def test_build_rebirth_prompt_with_new_fields(self, tmp_memory: Path):
        tmp_memory.parent.mkdir(parents=True, exist_ok=True)
        ex = Extraction(
            session_id="session-x",
            date="2026-05-12",
            decisions=["Ship daemon"],
            corrections=[],
            next_action="Monitor watch",
            current_truth="Daemon live.",
            blocks=["Flaky network"],
            artifacts=["daemon.py", "skills/foo"],
            energy_state="debugging",
        )
        append_extraction(ex, tmp_memory)
        prompt = build_rebirth_prompt(tmp_memory)
        assert "energy: debugging" in prompt
        assert "Blocked: Flaky network" in prompt
        assert "Artifact: daemon.py" in prompt
        assert "Artifact: skills/foo" in prompt


# ── corrections.yaml ───────────────────────────────────────────────────

class TestCorrectionsYaml:
    def test_corrections_yaml_population(self, tmp_path: Path):
        corr_path = tmp_path / "corrections.yaml"
        ex = Extraction(
            session_id="session-001",
            date="2026-05-10",
            decisions=[],
            corrections=["Don't hardcode colors", "Use theme tokens"],
            next_action="",
            current_truth="",
            blocks=[],
            artifacts=[],
            energy_state="idle",
        )
        append_corrections(ex, corr_path)
        text = corr_path.read_text(encoding="utf-8")
        assert text.startswith(CORRECTIONS_HEADER)
        data = yaml.safe_load(text[len(CORRECTIONS_HEADER) :])
        assert len(data["corrections"]) == 2
        assert data["corrections"][0]["session_id"] == "session-001"
        assert data["corrections"][0]["text"] == "Don't hardcode colors"

        ex2 = replace(ex, session_id="session-002", corrections=["Third fix"])
        append_corrections(ex2, corr_path)
        data2 = yaml.safe_load(corr_path.read_text(encoding="utf-8")[len(CORRECTIONS_HEADER) :])
        assert len(data2["corrections"]) == 3
        assert data2["corrections"][2]["text"] == "Third fix"


# ── Daemon ─────────────────────────────────────────────────────────────

class TestDaemon:
    def test_daemon_skips_already_extracted(self, tmp_path: Path, monkeypatch):
        calls: list[str] = []

        def fake_extract(*args, **kwargs):
            calls.append("extract")
            return Extraction(
                session_id="fake",
                date="2026-01-01",
                decisions=[],
                corrections=[],
                next_action="",
                current_truth="",
                blocks=[],
                artifacts=[],
                energy_state="idle",
            )

        monkeypatch.setattr("ven0m.siphon.daemon.extract", fake_extract)

        mem = tmp_path / "MEMORY"
        watch = tmp_path / "sessions"
        watch.mkdir()
        mem.mkdir()
        cfg = replace(
            SiphonConfig(),
            watch_dir=watch,
            memory_dir=mem,
            api_key="fake-key-for-test",
        )

        session_file = watch / "session_test.json"
        session_file.write_text(
            '{"session_id":"abc","messages":[{"role":"user","content":"hello world enough chars"}]}',
            encoding="utf-8",
        )

        assert process_session_json_file(session_file, cfg) is True
        assert calls == ["extract"]

        assert process_session_json_file(session_file, cfg) is False
        assert calls == ["extract"]

    def test_daemon_watch_dir_creation(self, tmp_path: Path):
        wd = tmp_path / "watch_here"
        md = tmp_path / "MEMORY_here"
        cfg = replace(SiphonConfig(), watch_dir=wd, memory_dir=md)
        ensure_memory_and_watch_dirs(cfg)
        assert wd.is_dir()
        assert md.is_dir()


# ── Config ─────────────────────────────────────────────────────────────

class TestConfig:
    def test_default_config(self):
        config = VenomConfig()
        assert config.siphon.model == "glm-5-turbo"
        assert "z.ai" in config.siphon.api_url
        assert config.siphon.memory_path == config.siphon.memory_dir / "MEMORY.md"

    def test_config_without_api_key(self, monkeypatch):
        monkeypatch.delenv("ZAI_API_KEY", raising=False)
        config = SiphonConfig()
        assert not config.has_api_key


# ── Pydantic schema ────────────────────────────────────────────────────────


class TestPydanticExtractionSchema:
    def test_valid_extraction_result(self):
        data = {
            "session_id": "s-1",
            "extracted_at": "2026-05-11T12:00:00",
            "entries": [
                {
                    "timestamp": "2026-05-11T12:00:00",
                    "summary": "Worked",
                    "decision": "Pick A",
                    "correction": "",
                    "pattern": "",
                    "memory_worthy": True,
                    "severity": "info",
                }
            ],
            "total_tokens": 10,
            "model_used": "glm",
        }
        r = ExtractionResult.model_validate(data)
        assert r.session_id == "s-1"
        assert r.entries[0].severity == ExtractionSeverity.info

    def test_invalid_severity_rejected(self):
        data = {
            "session_id": "s-1",
            "entries": [
                {
                    "timestamp": "t",
                    "summary": "x",
                    "severity": "not-a-level",
                }
            ],
        }
        with pytest.raises(ValidationError):
            ExtractionResult.model_validate(data)


class TestBackoffController:
    def test_sleep_seconds_after_failure_scales(self, monkeypatch):
        monkeypatch.setattr("random.uniform", lambda lo, hi: (lo + hi) / 2)
        bc = BackoffController(base_interval=5.0, max_interval=120.0, jitter_fraction=0.2)
        assert bc.sleep_seconds_after_failure() == pytest.approx(5.0)
        assert bc.sleep_seconds_after_failure() == pytest.approx(10.0)
        assert bc.sleep_seconds_after_failure() == pytest.approx(20.0)

    def test_reset_restores_base(self, monkeypatch):
        monkeypatch.setattr("random.uniform", lambda lo, hi: (lo + hi) / 2)
        bc = BackoffController()
        bc.sleep_seconds_after_failure()
        bc.reset()
        assert bc.sleep_seconds_after_failure() == pytest.approx(5.0)


class TestExtractHardening:
    def test_extract_uses_json_schema_path(self, tmp_path, monkeypatch):
        monkeypatch.setattr(time, "sleep", lambda _: None)
        cfg = replace(SiphonConfig(), memory_dir=tmp_path, api_key="key")

        payload = {
            "session_id": "json-session",
            "extracted_at": "2026-05-11T00:00:00",
            "entries": [
                {
                    "timestamp": "2026-05-11T00:00:00",
                    "summary": "Built tests",
                    "decision": "Use pydantic",
                    "correction": "",
                    "pattern": "",
                    "memory_worthy": True,
                    "severity": "minor",
                }
            ],
            "total_tokens": 0,
            "model_used": "",
        }

        class OkResp:
            status_code = 200
            request = None

            def raise_for_status(self):
                return None

            def json(self):
                return {
                    "choices": [{"message": {"content": json.dumps(payload)}}],
                    "usage": {"total_tokens": 42},
                }

        monkeypatch.setattr("ven0m.siphon.extractor.httpx.post", lambda *a, **k: OkResp())

        ex = extract("transcript body", cfg)
        assert ex.session_id == "json-session"
        assert "Use pydantic" in ex.decisions
        assert ex.energy_state == "building"

    def test_extract_legacy_yaml_fallback(self, tmp_path, monkeypatch):
        monkeypatch.setattr(time, "sleep", lambda _: None)
        cfg = replace(SiphonConfig(), memory_dir=tmp_path, api_key="key")
        yaml_body = (
            "session:\n"
            "  id: legacy-s\n"
            "  date: 2026-02-02\n"
            "  decisions: ['Legacy decision']\n"
            "  corrections: []\n"
            "  next_action: ''\n"
            "  current_truth: 'Still works'\n"
            "  blocks: []\n"
            "  artifacts: []\n"
            "  energy_state: idle\n"
        )

        class OkResp:
            status_code = 200
            request = None

            def raise_for_status(self):
                return None

            def json(self):
                return {"choices": [{"message": {"content": yaml_body}}], "usage": {}}

        monkeypatch.setattr("ven0m.siphon.extractor.httpx.post", lambda *a, **k: OkResp())

        ex = extract("tr", cfg)
        assert ex.session_id == "legacy-s"
        assert ex.current_truth == "Still works"

    def test_extract_retries_http_on_503(self, tmp_path, monkeypatch):
        monkeypatch.setattr(time, "sleep", lambda _: None)
        cfg = replace(SiphonConfig(), memory_dir=tmp_path, api_key="key")
        req = httpx.Request("POST", "https://api.example/v1")

        calls = {"n": 0}
        payload = {
            "session_id": "retry-ok",
            "extracted_at": "2026-05-11T00:00:00",
            "entries": [
                {
                    "timestamp": "2026-05-11T00:00:00",
                    "summary": "ok",
                    "severity": "info",
                }
            ],
        }

        class OkResp:
            status_code = 200
            request = req

            def raise_for_status(self):
                return None

            def json(self):
                return {"choices": [{"message": {"content": json.dumps(payload)}}], "usage": {}}

        def fake_post(*a, **k):
            calls["n"] += 1
            if calls["n"] == 1:
                return httpx.Response(503, request=req)
            return OkResp()

        monkeypatch.setattr("ven0m.siphon.extractor.httpx.post", fake_post)

        ex = extract("t", cfg)
        assert ex.session_id == "retry-ok"
        assert calls["n"] == 2
        assert (tmp_path / ".siphon_errors.jsonl").exists()

    def test_extract_http_exhausted_writes_errors(self, tmp_path, monkeypatch):
        monkeypatch.setattr(time, "sleep", lambda _: None)
        cfg = replace(SiphonConfig(), memory_dir=tmp_path, api_key="key")
        req = httpx.Request("POST", "https://api.example/v1")

        monkeypatch.setattr(
            "ven0m.siphon.extractor.httpx.post",
            lambda *a, **k: httpx.Response(503, request=req),
        )

        with pytest.raises(ValueError, match="HTTP extraction failed"):
            extract("t", cfg)

        lines = (tmp_path / ".siphon_errors.jsonl").read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) >= 3

    def test_memory_append_separator_format(self, tmp_path):
        mem = tmp_path / "MEMORY.md"
        mem.parent.mkdir(parents=True, exist_ok=True)
        ex = Extraction(
            session_id="fmt",
            date="2026-05-11",
            decisions=["d"],
            corrections=[],
            next_action="",
            current_truth="truth",
            blocks=[],
            artifacts=[],
            energy_state="idle",
        )
        append_extraction(ex, mem)
        text = mem.read_text(encoding="utf-8")
        assert text.startswith("\n---\n")
        assert "session:" in text
        assert "id: fmt" in text


class TestSiphonErrorLog:
    def test_append_siphon_error_jsonl(self, tmp_path):
        append_siphon_error(tmp_path, {"kind": "unit", "ok": True})
        line = (tmp_path / ".siphon_errors.jsonl").read_text(encoding="utf-8").strip()
        assert json.loads(line)["kind"] == "unit"
