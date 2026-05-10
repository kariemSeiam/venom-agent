"""Tests for Mantle identity loading and system prompt assembly."""

from __future__ import annotations

import logging
from pathlib import Path
import pytest

from ven0m.core.config import MantleConfig
from ven0m.mantle import Mantle


@pytest.fixture
def real_mantle_paths() -> Mantle:
    """Default package MantleConfig (pact.yaml / voice.yaml shipped under ven0m/mantle)."""
    return Mantle(MantleConfig())


class TestMantleLoadsYaml:
    def test_load_pact_non_empty(self, real_mantle_paths: Mantle):
        pact = real_mantle_paths.load_pact()
        assert pact
        assert "Document" in pact and "PACT" in pact

    def test_load_voice_non_empty(self, real_mantle_paths: Mantle):
        voice = real_mantle_paths.load_voice()
        assert voice
        assert "TESLA" in voice or "modes" in voice.lower()

    def test_get_system_prompt_combines(self, real_mantle_paths: Mantle):
        prompt = real_mantle_paths.get_system_prompt()
        assert "# PACT" in prompt
        assert "# VOICE" in prompt
        assert "---" in prompt


class TestMantleFallback:
    def test_missing_files_return_empty_with_warning(self, tmp_path: Path, caplog):
        caplog.set_level(logging.WARNING)
        missing_pact = tmp_path / "nope_pact.yaml"
        missing_voice = tmp_path / "nope_voice.yaml"
        m = Mantle(MantleConfig(pact_path=missing_pact, voice_path=missing_voice))
        assert m.load_pact() == ""
        assert m.load_voice() == ""
        assert "not found" in caplog.text.lower()

    def test_get_system_prompt_empty_when_both_missing(self, tmp_path: Path):
        m = Mantle(
            MantleConfig(
                pact_path=tmp_path / "a.yaml",
                voice_path=tmp_path / "b.yaml",
            )
        )
        assert m.get_system_prompt() == ""


class TestMantleYamlEdgeCases:
    def test_empty_yaml_file_warns_and_returns_empty(self, tmp_path: Path, caplog):
        caplog.set_level(logging.WARNING)
        p = tmp_path / "empty.yaml"
        p.write_text("", encoding="utf-8")
        m = Mantle(MantleConfig(pact_path=p, voice_path=p))
        assert m.load_pact() == ""
        assert "empty" in caplog.text.lower()

    def test_invalid_yaml_warns_and_returns_empty(self, tmp_path: Path, caplog):
        caplog.set_level(logging.WARNING)
        p = tmp_path / "bad.yaml"
        p.write_text("{broken\n", encoding="utf-8")
        m = Mantle(MantleConfig(pact_path=p, voice_path=p))
        assert m.load_pact() == ""
        assert "invalid yaml" in caplog.text.lower()

    def test_yaml_null_document_returns_empty(self, tmp_path: Path, caplog):
        caplog.set_level(logging.WARNING)
        p = tmp_path / "null.yaml"
        p.write_text("# comment only\n", encoding="utf-8")
        m = Mantle(MantleConfig(pact_path=p, voice_path=p))
        assert m.load_pact() == ""
        assert "null" in caplog.text.lower()

    def test_markdown_loaded_raw(self, tmp_path: Path):
        pact_md = tmp_path / "pact.md"
        voice_md = tmp_path / "voice.md"
        pact_md.write_text("## Hello\nBody.", encoding="utf-8")
        voice_md.write_text("Voice **here**.", encoding="utf-8")
        m = Mantle(MantleConfig(pact_path=pact_md, voice_path=voice_md))
        assert m.load_pact() == "## Hello\nBody."
        assert m.load_voice() == "Voice **here**."
        sp = m.get_system_prompt()
        assert "## Hello" in sp
        assert "Voice **here**" in sp
