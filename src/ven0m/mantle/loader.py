"""Load identity documents (PACT, VOICE) for Mantle / L1."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from ..core.config import MantleConfig

logger = logging.getLogger(__name__)


def _warn_missing(path: Path, label: str) -> None:
    logger.warning("Mantle: %s not found at %s — using empty string", label, path)


def _warn_invalid_yaml(path: Path, label: str, detail: str) -> None:
    logger.warning("Mantle: invalid YAML for %s at %s — %s", label, path, detail)


def _render_yaml_as_text(data: Any, indent: int = 0) -> str:
    """Turn parsed YAML into readable plain text for prompts and display."""
    if data is None:
        return ""
    if isinstance(data, str):
        return data.strip()
    if isinstance(data, (int, float, bool)):
        return str(data)
    if isinstance(data, list):
        pad = "  " * indent
        lines: list[str] = []
        for item in data:
            if isinstance(item, dict):
                lines.append(f"{pad}-")
                sub = _render_yaml_as_text(item, indent + 1)
                if sub:
                    lines.append(sub)
            else:
                lines.append(f"{pad}- {_render_yaml_as_text(item, indent)}")
        return "\n".join(lines).strip()
    if isinstance(data, dict):
        pad = "  " * indent
        lines = []
        for key, val in data.items():
            key_str = str(key).replace("_", " ").title()
            if isinstance(val, (dict, list)):
                lines.append(f"{pad}{key_str}:")
                sub = _render_yaml_as_text(val, indent + 1)
                if sub:
                    lines.append(sub)
            else:
                lines.append(f"{pad}{key_str}: {_render_yaml_as_text(val, indent)}")
        return "\n".join(lines).strip()
    return str(data).strip()


def _load_file_raw(path: Path, label: str) -> str:
    if not path.exists():
        _warn_missing(path, label)
        return ""
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8").strip()
    if suffix in (".md", ".markdown"):
        return text
    if suffix in (".yaml", ".yml"):
        if not text:
            _warn_invalid_yaml(path, label, "file is empty")
            return ""
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as e:
            _warn_invalid_yaml(path, label, str(e))
            return ""
        if data is None:
            _warn_invalid_yaml(path, label, "parsed to null")
            return ""
        return _render_yaml_as_text(data)
    logger.warning(
        "Mantle: unsupported extension for %s at %s — reading as plain text",
        label,
        path,
    )
    return text


class Mantle:
    """Identity layer: immutable pact + communication voice."""

    def __init__(self, config: MantleConfig | None = None) -> None:
        self._config = config if config is not None else MantleConfig()

    @property
    def pact_path(self) -> Path:
        return self._config.pact_path

    @property
    def voice_path(self) -> Path:
        return self._config.voice_path

    def load_pact(self) -> str:
        return _load_file_raw(self.pact_path, "PACT")

    def load_voice(self) -> str:
        return _load_file_raw(self.voice_path, "VOICE")

    def get_system_prompt(self) -> str:
        pact = self.load_pact()
        voice = self.load_voice()
        parts: list[str] = []
        if pact:
            parts.append("# PACT\n\n" + pact)
        if voice:
            parts.append("# VOICE\n\n" + voice)
        return "\n\n---\n\n".join(parts).strip()
