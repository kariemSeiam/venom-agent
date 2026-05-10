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

import json
import logging
import random
import re
import time
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import httpx
import yaml
from pydantic import ValidationError

from .schema import ExtractionResult, ExtractionSeverity

LOG = logging.getLogger(__name__)

# ── LLM prompts ───────────────────────────────────────────────────────────

JSON_SYSTEM_PROMPT = """\
You are SIPHON. Summarize the session transcript into ONE JSON object only.
Output ONLY raw JSON. No markdown fences. No commentary.

Schema:
{
  "session_id": "session-NNN or inferred id",
  "extracted_at": "<ISO-8601 datetime string>",
  "entries": [
    {
      "timestamp": "<ISO-8601 string>",
      "summary": "one-line summary",
      "decision": "",
      "correction": "",
      "pattern": "",
      "memory_worthy": false,
      "severity": "info"
    }
  ],
  "total_tokens": 0,
  "model_used": ""
}

Rules:
- Produce at least one entry when transcript has usable content.
- severity must be one of: critical, major, minor, info
- Fill correction only when something wrong was fixed; decision when an explicit choice was made.
- pattern: observable repetition / technique / path-worthy hook when relevant.
- memory_worthy true only for durable facts worth MEMORY.md.
- Omit unknown scalar fields as \"\" , false , or 0 as appropriate.

If transcript is empty of substance, return one entry with summary noting emptiness and severity info.
"""

LEGACY_YAML_PROMPT = """\
Fallback legacy YAML shape (only if JSON is impossible — prefer JSON):
Output ONLY raw YAML. No markdown fences.

session:
  id: "session-NNN"
  date: YYYY-MM-DD
  decisions: []
  corrections: []
  next_action: ""
  current_truth: ""
  blocks: []
  artifacts: []
  energy_state: idle

energy_state ∈ building | debugging | researching | idle | blocked
"""

COMBINED_SYSTEM_PROMPT = JSON_SYSTEM_PROMPT + "\n\n" + LEGACY_YAML_PROMPT


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


def extraction_result_to_extraction(result: ExtractionResult) -> Extraction:
    """Fold validated ExtractionResult into MEMORY-compatible Extraction."""
    entries = result.entries
    decisions: list[str] = []
    seen: set[str] = set()
    for e in entries:
        if e.decision.strip():
            d = e.decision.strip()
            if d not in seen:
                seen.add(d)
                decisions.append(d)
    for e in entries:
        if e.memory_worthy and e.summary.strip():
            s = e.summary.strip()
            if s not in seen:
                seen.add(s)
                decisions.append(s)

    corrections = []
    for e in entries:
        if e.correction.strip():
            corrections.append(e.correction.strip())

    blocks: list[str] = []
    artifacts: list[str] = []
    for e in entries:
        p = e.pattern.strip()
        if not p:
            continue
        if e.severity in (ExtractionSeverity.critical, ExtractionSeverity.major):
            blocks.append(p)
        else:
            artifacts.append(p)

    rank = {
        ExtractionSeverity.info: 0,
        ExtractionSeverity.minor: 1,
        ExtractionSeverity.major: 2,
        ExtractionSeverity.critical: 3,
    }
    worst = ExtractionSeverity.info
    for e in entries:
        if rank[e.severity] > rank[worst]:
            worst = e.severity
    energy_map = {
        ExtractionSeverity.critical: "blocked",
        ExtractionSeverity.major: "debugging",
        ExtractionSeverity.minor: "building",
        ExtractionSeverity.info: "idle",
    }
    energy_state = energy_map[worst]

    date_str = (
        result.extracted_at.date().isoformat()
        if isinstance(result.extracted_at, datetime)
        else date.today().isoformat()
    )
    truth = entries[0].summary.strip() if entries else ""
    next_act = ""
    for e in reversed(entries):
        if e.memory_worthy and e.summary.strip():
            next_act = e.summary.strip()
            break

    return Extraction(
        session_id=result.session_id.strip() or "session-unknown",
        date=date_str,
        decisions=decisions,
        corrections=corrections,
        next_action=next_act,
        current_truth=truth,
        blocks=blocks,
        artifacts=artifacts,
        energy_state=energy_state,
    )


def append_siphon_error(memory_dir: Path, record: dict[str, Any]) -> Path:
    """Append one JSON line to `.siphon_errors.jsonl`."""
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = memory_dir / ".siphon_errors.jsonl"
    line = json.dumps(record, default=str, ensure_ascii=False)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return path


def _strip_markdown_fences(content: str) -> str:
    content = content.strip()
    content = re.sub(r"^```(?:json|yaml)?\s*\n?", "", content)
    content = re.sub(r"\n?```\s*$", "", content)
    return content.strip()


def _parse_llm_content_to_extraction(
    content: str,
    *,
    config,
    usage_tokens: int,
    raw_snippet_max: int = 1200,
) -> Extraction:
    stripped = _strip_markdown_fences(content)

    # 1) JSON + Pydantic (preferred)
    try:
        data = json.loads(stripped)
        if isinstance(data, dict):
            result = ExtractionResult.model_validate(data)
            updates: dict[str, Any] = {}
            if not result.total_tokens and usage_tokens:
                updates["total_tokens"] = usage_tokens
            if not result.model_used:
                updates["model_used"] = config.model
            if updates:
                result = result.model_copy(update=updates)
            return extraction_result_to_extraction(result)
    except json.JSONDecodeError:
        pass
    except ValidationError as e:
        append_siphon_error(
            config.memory_dir,
            {
                "kind": "validation_error",
                "errors": e.errors(),
                "snippet": stripped[:raw_snippet_max],
            },
        )
        LOG.warning("SIPHON JSON validation failed: %s", e)

    # 2) Legacy YAML session block
    try:
        yml = yaml.safe_load(stripped)
        if isinstance(yml, dict) and "session" in yml:
            append_siphon_error(
                config.memory_dir,
                {"kind": "legacy_yaml_fallback", "snippet": stripped[:raw_snippet_max]},
            )
            return Extraction.from_dict(yml)
    except yaml.YAMLError:
        pass

    append_siphon_error(
        config.memory_dir,
        {"kind": "unparseable_response", "snippet": stripped[:raw_snippet_max]},
    )
    raise ValueError(f"Invalid extraction payload (not JSON schema nor legacy session YAML): {stripped[:200]}")


def _request_extraction_raw(transcript: str, config) -> tuple[str, int]:
    """POST with retries; returns (message_content, total_tokens)."""
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            response = httpx.post(
                config.api_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {config.api_key}",
                },
                json={
                    "model": config.model,
                    "messages": [
                        {"role": "system", "content": COMBINED_SYSTEM_PROMPT},
                        {"role": "user", "content": transcript},
                    ],
                    "temperature": config.temperature,
                },
                timeout=30.0,
            )
            if response.status_code in (429, 502, 503, 504):
                raise httpx.HTTPStatusError(
                    "retryable status",
                    request=response.request,
                    response=response,
                )
            response.raise_for_status()
            raw = response.json()
            if (
                not isinstance(raw.get("choices"), list)
                or not raw["choices"]
                or not isinstance(raw["choices"][0], dict)
                or "message" not in raw["choices"][0]
            ):
                raise KeyError("choices/message")
            content = raw["choices"][0]["message"]["content"]
            usage = raw.get("usage") or {}
            tokens = int(usage.get("total_tokens") or 0)
            return str(content), tokens
        except (httpx.TimeoutException, httpx.TransportError, httpx.HTTPStatusError, KeyError) as e:
            last_error = e
            append_siphon_error(
                config.memory_dir,
                {"kind": "http_attempt_failed", "attempt": attempt + 1, "error": repr(e)},
            )
            if attempt == 2:
                break
            backoff = (2**attempt) * random.uniform(0.8, 1.2)
            time.sleep(backoff)

    raise ValueError(f"SIPHON HTTP extraction failed after retries: {last_error}") from last_error


def extract(transcript: str, config) -> Extraction:
    """
    Send transcript to LLM, validate JSON via Pydantic when possible,
    fall back to legacy YAML session blocks, return MEMORY-compatible Extraction.
    """
    if not config.has_api_key:
        raise ValueError("ZAI_API_KEY not set. Cannot extract.")

    raw_content, usage_tokens = _request_extraction_raw(transcript, config)
    return _parse_llm_content_to_extraction(
        raw_content,
        config=config,
        usage_tokens=usage_tokens,
    )


# ── Memory I/O ─────────────────────────────────────────────────────────────

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
