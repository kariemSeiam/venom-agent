"""
SIPHON — Session death and rebirth.

The octopus's optic gland triggers death after spawning.
VENOM's SIPHON extracts knowledge at session death,
so the next session is born with memory.

Protocol:
  1. Session runs → work happens
  2. SIPHON extracts structured fields from transcript
  3. Extraction appends to MEMORY.md (append-only, never edit)
  4. Next session reads MEMORY.md first → rebirth
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import httpx
import yaml


# ── Extraction Schema (v1 — 7 fields) ───────────────────────────────────

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
  blocks:
    - "things that blocked progress and are NOT fixed yet"
  artifacts:
    - "files, patterns, skills, or outputs created this session"
  energy_state: building

Rules:
- decisions: only explicit choices, not observations
- corrections: only things that were WRONG and got FIXED
- next_action: concrete, not philosophical
- current_truth: the single most important fact right now
- blocks: active impediments still open — empty [] if none
- artifacts: tangible outputs (paths, skill names, docs) — empty [] if none
- energy_state: exactly one of: building, debugging, researching, idle, blocked
- If a list field has nothing, use []. If a string field has nothing, use ""
"""


ENERGY_STATES = frozenset({"building", "debugging", "researching", "idle", "blocked"})


def _normalize_energy_state(value: object) -> str:
    s = str(value).strip().lower() if value not in (None, "") else "idle"
    return s if s in ENERGY_STATES else "idle"


@dataclass(frozen=True)
class Extraction:
    """A single SIPHON extraction — the unit of cross-session memory."""

    session_id: str
    date: str
    decisions: list[str]
    corrections: list[str]
    next_action: str
    current_truth: str
    blocks: list[str]
    artifacts: list[str]
    energy_state: str

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
                    "blocks": self.blocks,
                    "artifacts": self.artifacts,
                    "energy_state": self.energy_state,
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
            decisions=list(s.get("decisions", []) or []),
            corrections=list(s.get("corrections", []) or []),
            next_action=s.get("next_action", ""),
            current_truth=s.get("current_truth", ""),
            blocks=list(s.get("blocks", []) or []),
            artifacts=list(s.get("artifacts", []) or []),
            energy_state=_normalize_energy_state(s.get("energy_state", "idle")),
        )


# ── Extractor ────────────────────────────────────────────────────────────

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


# ── Memory I/O ───────────────────────────────────────────────────────────

SEPARATOR = "\n---\n"

CORRECTIONS_HEADER = "# corrections.yaml — auto-populated by SIPHON\n"


def append_extraction(extraction: Extraction, memory_path: Path) -> Path:
    """Append extraction to MEMORY.md. Returns the path written."""
    memory_path.parent.mkdir(parents=True, exist_ok=True)

    entry = f"{SEPARATOR}{extraction.to_yaml()}"
    with open(memory_path, "a", encoding="utf-8") as f:
        f.write(entry)

    return memory_path


def append_corrections(extraction: Extraction, corrections_path: Path) -> Path:
    """Append correction entries for this session to corrections.yaml."""
    if not extraction.corrections:
        return corrections_path

    corrections_path.parent.mkdir(parents=True, exist_ok=True)

    existing: list[dict] = []
    if corrections_path.exists():
        raw = corrections_path.read_text(encoding="utf-8")
        body = raw[len(CORRECTIONS_HEADER) :] if raw.startswith(CORRECTIONS_HEADER) else raw
        try:
            doc = yaml.safe_load(body) if body.strip() else {}
            if isinstance(doc, dict) and isinstance(doc.get("corrections"), list):
                existing = [x for x in doc["corrections"] if isinstance(x, dict)]
        except yaml.YAMLError:
            existing = []

    for text in extraction.corrections:
        existing.append(
            {
                "session_id": extraction.session_id,
                "date": extraction.date,
                "text": str(text),
            }
        )

    dump = yaml.dump(
        {"corrections": existing},
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )
    corrections_path.write_text(CORRECTIONS_HEADER + dump, encoding="utf-8")
    return corrections_path


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
        lines.append(f"**{ex.session_id}** ({ex.date}) — energy: {ex.energy_state}")
        if ex.current_truth:
            lines.append(f"  Truth: {ex.current_truth}")
        if ex.decisions:
            for d in ex.decisions:
                lines.append(f"  Decision: {d}")
        if ex.corrections:
            for c in ex.corrections:
                lines.append(f"  Correction: {c}")
        if ex.blocks:
            for b in ex.blocks:
                lines.append(f"  Blocked: {b}")
        if ex.artifacts:
            for a in ex.artifacts:
                lines.append(f"  Artifact: {a}")
        if ex.next_action:
            lines.append(f"  Next: {ex.next_action}")
        lines.append("")

    return "\n".join(lines)
