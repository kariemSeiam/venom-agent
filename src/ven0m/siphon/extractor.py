"""
SIPHON — Session death and rebirth.

The octopus's optic gland triggers death after spawning.
VENOM's SIPHON extracts knowledge at session death,
so the next session is born with memory.

Protocol:
  1. Session runs → work happens
  2. SIPHON extracts 4 fields from transcript
  3. Extraction appends to MEMORY.md (append-only, never edit)
  4. Next session reads MEMORY.md first → rebirth
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import httpx
import yaml


# ── Extraction Schema (v0 — 4 fields, no more) ────────────────────────

SYSTEM_PROMPT = """\
You are SIPHON. Extract the session transcript into exactly this YAML.
Output ONLY raw YAML. No markdown fences. No commentary.

session:
  id: "session-NNN"
  date: YYYY-MM-DD
  decisions:
    - "what changed"
  corrections:
    - "what was wrong and got fixed"
  next_action: "first thing to do next session"
  current_truth: "one sentence the next session inherits"

Rules:
- decisions: only explicit choices, not observations
- corrections: only things that were WRONG and got FIXED
- next_action: concrete, not philosophical
- current_truth: the single most important fact right now
- If a field has nothing, use empty list [] or empty string ""
"""


@dataclass(frozen=True)
class Extraction:
    """A single SIPHON extraction — the unit of cross-session memory."""

    session_id: str
    date: str
    decisions: list[str]
    corrections: list[str]
    next_action: str
    current_truth: str

    def to_yaml(self) -> str:
        return yaml.dump(
            {
                "session": {
                    "id": self.session_id,
                    "date": self.date,
                    "decisions": self.decisions,
                    "corrections": self.corrections,
                    "next_action": self.next_action,
                    "current_truth": self.current_truth,
                }
            },
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    @classmethod
    def from_dict(cls, data: dict) -> Extraction:
        s = data.get("session", data)
        return cls(
            session_id=s.get("id", "session-unknown"),
            date=s.get("date", date.today().isoformat()),
            decisions=s.get("decisions", []),
            corrections=s.get("corrections", []),
            next_action=s.get("next_action", ""),
            current_truth=s.get("current_truth", ""),
        )


# ── Extractor ──────────────────────────────────────────────────────────

def extract(transcript: str, config) -> Extraction:
    """
    Send transcript to LLM, parse extraction YAML.
    Raises ValueError on parse failure.
    """
    if not config.has_api_key:
        raise ValueError("ZAI_API_KEY not set. Cannot extract.")

    response = httpx.post(
        config.api_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.api_key}",
        },
        json={
            "model": config.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": transcript},
            ],
            "temperature": config.temperature,
        },
        timeout=60.0,
    )
    response.raise_for_status()

    raw = response.json()
    content = raw["choices"][0]["message"]["content"]

    # Strip markdown fences if model ignores instruction
    content = re.sub(r"^```(?:yaml)?\n?", "", content.strip())
    content = re.sub(r"\n?```\s*$", "", content)

    data = yaml.safe_load(content)
    if not isinstance(data, dict) or "session" not in data:
        raise ValueError(f"Invalid extraction format: {content[:200]}")

    return Extraction.from_dict(data)


# ── Memory I/O ─────────────────────────────────────────────────────────

SEPARATOR = "\n---\n"

def append_extraction(extraction: Extraction, memory_path: Path) -> Path:
    """Append extraction to MEMORY.md. Returns the path written."""
    memory_path.parent.mkdir(parents=True, exist_ok=True)

    entry = f"{SEPARATOR}{extraction.to_yaml()}"
    with open(memory_path, "a", encoding="utf-8") as f:
        f.write(entry)

    return memory_path


def read_memory(memory_path: Path, last_n: int = 5) -> list[Extraction]:
    """Read the last N extractions from MEMORY.md for rebirth."""
    if not memory_path.exists():
        return []

    text = memory_path.read_text(encoding="utf-8")
    blocks = re.split(r"\n---\n", text)

    # Parse from the end (newest first)
    extractions: list[Extraction] = []
    for block in reversed(blocks):
        block = block.strip()
        if not block or not block.startswith("session:"):
            continue
        try:
            data = yaml.safe_load(block)
            if isinstance(data, dict) and "session" in data:
                extractions.append(Extraction.from_dict(data))
        except yaml.YAMLError:
            continue
        if len(extractions) >= last_n:
            break

    extractions.reverse()  # chronological order
    return extractions


def build_rebirth_prompt(memory_path: Path, last_n: int = 5) -> str:
    """Build the rebirth prompt from recent memory — injected at session start."""
    extractions = read_memory(memory_path, last_n)
    if not extractions:
        return ""

    lines = ["## Previous Sessions (SIPHON rebirth)\n"]
    for ex in extractions:
        lines.append(f"**{ex.session_id}** ({ex.date})")
        if ex.current_truth:
            lines.append(f"  Truth: {ex.current_truth}")
        if ex.decisions:
            for d in ex.decisions:
                lines.append(f"  Decision: {d}")
        if ex.corrections:
            for c in ex.corrections:
                lines.append(f"  Correction: {c}")
        if ex.next_action:
            lines.append(f"  Next: {ex.next_action}")
        lines.append("")

    return "\n".join(lines)
