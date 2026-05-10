"""SIPHON CLI — run extraction from terminal."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ..core.config import VenomConfig
from .extractor import Extraction, append_extraction, build_rebirth_prompt, extract


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="siphon",
        description="SIPHON — session death and rebirth for VENOM Agent",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # extract — run extraction from transcript
    p_extract = sub.add_parser("extract", help="Extract session memory from transcript")
    p_extract.add_argument("transcript", type=Path, help="Path to session transcript")
    p_extract.add_argument("--output", "-o", type=Path, default=None, help="Output memory file")
    p_extract.add_argument("--session-id", "-s", default=None, help="Override session ID")
    p_extract.add_argument("--dry-run", action="store_true", help="Print extraction without writing")

    # rebirth — build rebirth prompt from memory
    p_rebirth = sub.add_parser("rebirth", help="Build rebirth prompt from MEMORY.md")
    p_rebirth.add_argument("--memory", "-m", type=Path, default=None, help="Path to MEMORY.md")
    p_rebirth.add_argument("--last", "-n", type=int, default=5, help="Number of sessions to include")

    args = parser.parse_args(argv)

    config = VenomConfig().siphon

    if args.command == "extract":
        transcript_path: Path = args.transcript
        if not transcript_path.exists():
            print(f"Error: {transcript_path} not found", file=sys.stderr)
            sys.exit(1)

        transcript = transcript_path.read_text(encoding="utf-8")
        print(f"SIPHON: Extracting from {transcript_path}...")

        try:
            extraction = extract(transcript, config)
        except Exception as e:
            print(f"Extraction failed: {e}", file=sys.stderr)
            sys.exit(1)

        if args.session_id:
            # Override session ID in the extraction
            extraction = Extraction(
                session_id=args.session_id,
                date=extraction.date,
                decisions=extraction.decisions,
                corrections=extraction.corrections,
                next_action=extraction.next_action,
                current_truth=extraction.current_truth,
                blocks=extraction.blocks,
                artifacts=extraction.artifacts,
                energy_state=extraction.energy_state,
            )

        yaml_output = extraction.to_yaml()
        print(yaml_output)

        if args.dry_run:
            print("(dry run — nothing written)")
            return

        memory_path = args.output or config.memory_path
        append_extraction(extraction, memory_path)
        print(f"Appended to {memory_path}")

    elif args.command == "rebirth":
        memory_path = args.memory or config.memory_path
        prompt = build_rebirth_prompt(memory_path, args.last)
        if prompt:
            print(prompt)
        else:
            print("(no memory found — first session)")
