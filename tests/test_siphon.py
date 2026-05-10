"""Tests for SIPHON extraction, memory I/O, and rebirth."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest
import yaml

from ven0m.core.config import SiphonConfig, VenomConfig
from ven0m.siphon.extractor import (
    Extraction,
    append_extraction,
    build_rebirth_prompt,
    read_memory,
)


# ── Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def tmp_memory(tmp_path: Path) -> Path:
    return tmp_path / "MEMORY.md"


@pytest.fixture
def sample_extraction() -> Extraction:
    return Extraction(
        session_id="session-001",
        date="2026-05-10",
        decisions=["Built SIPHON v0 in Python", "Scraped old Claude Code artifacts"],
        corrections=["Old siphon.ts used Z.AI endpoint wrong — fixed model name"],
        next_action="Run siphon for 20 sessions before expanding",
        current_truth="VENOM is a Python package, not a Claude Code workspace.",
    )


# ── Extraction dataclass ───────────────────────────────────────────────

class TestExtraction:
    def test_to_yaml_produces_valid_yaml(self, sample_extraction: Extraction):
        out = sample_extraction.to_yaml()
        data = yaml.safe_load(out)
        assert data["session"]["id"] == "session-001"
        assert data["session"]["date"] == "2026-05-10"
        assert len(data["session"]["decisions"]) == 2

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
        assert ex.current_truth == ""  # missing fields default to empty

    def test_from_dict_no_session_key_reads_top_level(self):
        """Without 'session' wrapper, reads id from top-level dict."""
        data = {"id": "session-042", "date": "2026-01-01"}
        ex = Extraction.from_dict(data)
        # Falls through: s = data.get("session", data) → uses data itself
        assert ex.session_id == "session-042"


# ── Memory I/O ─────────────────────────────────────────────────────────

class TestMemoryIO:
    def test_append_creates_file(self, tmp_memory: Path, sample_extraction: Extraction):
        append_extraction(sample_extraction, tmp_memory)
        assert tmp_memory.exists()

    def test_append_adds_separator(self, tmp_memory: Path, sample_extraction: Extraction):
        append_extraction(sample_extraction, tmp_memory)
        content = tmp_memory.read_text()
        assert "\n---\n" in content
        assert "session-001" in content

    def test_append_multiple_extractions(self, tmp_memory: Path, sample_extraction: Extraction):
        ex2 = Extraction(
            session_id="session-002",
            date="2026-05-11",
            decisions=["Added tests"],
            corrections=[],
            next_action="Ship it",
            current_truth="Tests pass.",
        )
        append_extraction(sample_extraction, tmp_memory)
        append_extraction(ex2, tmp_memory)
        extractions = read_memory(tmp_memory)
        assert len(extractions) == 2
        assert extractions[0].session_id == "session-001"
        assert extractions[1].session_id == "session-002"

    def test_read_memory_respects_last_n(self, tmp_memory: Path):
        for i in range(10):
            ex = Extraction(
                session_id=f"session-{i:03d}",
                date="2026-05-10",
                decisions=[f"Decision {i}"],
                corrections=[],
                next_action="",
                current_truth="",
            )
            append_extraction(ex, tmp_memory)

        last_3 = read_memory(tmp_memory, last_n=3)
        assert len(last_3) == 3
        assert last_3[0].session_id == "session-007"
        assert last_3[2].session_id == "session-009"

    def test_read_memory_empty_file(self, tmp_memory: Path):
        tmp_memory.write_text("")
        assert read_memory(tmp_memory) == []

    def test_read_memory_nonexistent(self, tmp_memory: Path):
        assert read_memory(tmp_memory) == []

    def test_read_memory_skips_garbage(self, tmp_memory: Path, sample_extraction: Extraction):
        append_extraction(sample_extraction, tmp_memory)
        # Append garbage
        with open(tmp_memory, "a") as f:
            f.write("\n---\nthis is not yaml at all\n")
        extractions = read_memory(tmp_memory)
        assert len(extractions) == 1


# ── Rebirth prompt ─────────────────────────────────────────────────────

class TestRebirthPrompt:
    def test_empty_memory_returns_empty(self, tmp_memory: Path):
        assert build_rebirth_prompt(tmp_memory) == ""

    def test_rebirth_includes_current_truth(self, tmp_memory: Path, sample_extraction: Extraction):
        append_extraction(sample_extraction, tmp_memory)
        prompt = build_rebirth_prompt(tmp_memory)
        assert "Truth: VENOM is a Python package" in prompt

    def test_rebirth_includes_decisions(self, tmp_memory: Path, sample_extraction: Extraction):
        append_extraction(sample_extraction, tmp_memory)
        prompt = build_rebirth_prompt(tmp_memory)
        assert "Decision: Built SIPHON v0" in prompt

    def test_rebirth_includes_corrections(self, tmp_memory: Path, sample_extraction: Extraction):
        append_extraction(sample_extraction, tmp_memory)
        prompt = build_rebirth_prompt(tmp_memory)
        assert "Correction: Old siphon.ts" in prompt

    def test_rebirth_includes_next_action(self, tmp_memory: Path, sample_extraction: Extraction):
        append_extraction(sample_extraction, tmp_memory)
        prompt = build_rebirth_prompt(tmp_memory)
        assert "Next: Run siphon for 20 sessions" in prompt


# ── Config ─────────────────────────────────────────────────────────────

class TestConfig:
    def test_default_config(self):
        config = VenomConfig()
        assert config.siphon.model == "glm-5-turbo"
        assert "z.ai" in config.siphon.api_url

    def test_config_without_api_key(self, monkeypatch):
        monkeypatch.delenv("ZAI_API_KEY", raising=False)
        config = SiphonConfig()
        assert not config.has_api_key
