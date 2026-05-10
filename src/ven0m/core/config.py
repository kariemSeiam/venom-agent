"""Core configuration for VENOM Agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SiphonConfig:
    """SIPHON extraction configuration."""

    api_url: str = "https://api.z.ai/api/coding/paas/v4/chat/completions"
    model: str = "glm-5-turbo"
    api_key: str = field(default_factory=lambda: os.environ.get("ZAI_API_KEY", ""))
    temperature: float = 0.1
    memory_dir: Path = field(default_factory=lambda: Path.cwd() / "MEMORY")
    watch_dir: Path = field(default_factory=lambda: Path.home() / ".hermes" / "sessions")
    poll_interval: float = 30.0

    @property
    def memory_path(self) -> Path:
        return self.memory_dir / "MEMORY.md"

    @property
    def corrections_path(self) -> Path:
        return self.memory_dir / "corrections.yaml"

    @property
    def siphon_index_path(self) -> Path:
        return self.memory_dir / ".siphon_index.json"

    @property
    def siphon_errors_log_path(self) -> Path:
        return self.memory_dir / ".siphon_errors.jsonl"

    @property
    def has_api_key(self) -> bool:
        return bool(self.api_key)


@dataclass(frozen=True)
class MantleConfig:
    """Identity and behavioral configuration."""

    pact_path: Path = field(default_factory=lambda: Path(__file__).parent.parent / "mantle" / "pact.yaml")
    voice_path: Path = field(default_factory=lambda: Path(__file__).parent.parent / "mantle" / "voice.yaml")


@dataclass(frozen=True)
class VenomConfig:
    """Master configuration — single source of truth."""

    siphon: SiphonConfig = field(default_factory=SiphonConfig)
    mantle: MantleConfig = field(default_factory=MantleConfig)
    project_root: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent.parent)
