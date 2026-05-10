"""Tests for SIPHON extraction, memory I/O, rebirth, daemon, and corrections."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from ven0m.core.config import SiphonConfig, VenomConfig
from ven0m.siphon.daemon import (
    ensure_memory_and_watch_dirs,
    process_session_json_file,
)
from ven0m.siphon.extractor import (
    CORRECTIONS_HEADER,
    Extraction,
    append_corrections,
    append_extraction,
    build_rebirth_prompt,
    read_memory,
)


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
