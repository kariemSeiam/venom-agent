"""VENOM root CLI — SIPHON, Mantle, status."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .core.config import VenomConfig
from .mantle import Mantle


def _cmd_status() -> None:
    cfg = VenomConfig()
    mantle = Mantle(cfg.mantle)
    pact_ok = cfg.mantle.pact_path.exists()
    voice_ok = cfg.mantle.voice_path.exists()
    pact_loaded = bool(mantle.load_pact())
    voice_loaded = bool(mantle.load_voice())

    print(f"ven0m {__version__}")
    print("SIPHON:")
    print(f"  model: {cfg.siphon.model}")
    print(f"  api_key_set: {cfg.siphon.has_api_key}")
    print(f"  memory_path: {cfg.siphon.memory_path}")
    print("Mantle:")
    print(f"  pact_path: {cfg.mantle.pact_path} (exists={pact_ok}, loaded_non_empty={pact_loaded})")
    print(f"  voice_path: {cfg.mantle.voice_path} (exists={voice_ok}, loaded_non_empty={voice_loaded})")


def _cmd_mantle_show(mantle: Mantle) -> None:
    pact = mantle.load_pact()
    voice = mantle.load_voice()
    print("=== PACT ===")
    print(pact if pact else "(empty)")
    print()
    print("=== VOICE ===")
    print(voice if voice else "(empty)")


def _cmd_mantle_inject(mantle: Mantle) -> None:
    prompt = mantle.get_system_prompt()
    print(prompt if prompt else "(empty system prompt — missing or unreadable identity files)")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="ven0m",
        description="VENOM Agent — unshelled.ai (SIPHON, Mantle, status)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status", help="Print package, SIPHON, and Mantle status")
    p_status.set_defaults(handler="status")

    p_mantle = sub.add_parser("mantle", help="Identity layer (PACT + VOICE)")
    mantle_sub = p_mantle.add_subparsers(dest="mantle_cmd", required=True)
    p_show = mantle_sub.add_parser("show", help="Print loaded PACT and VOICE")
    p_show.set_defaults(handler="mantle_show")
    p_inject = mantle_sub.add_parser("inject", help="Print combined system prompt for LLM injection")
    p_inject.set_defaults(handler="mantle_inject")

    p_siphon = sub.add_parser("siphon", help="Session death and rebirth")
    siphon_sub = p_siphon.add_subparsers(dest="siphon_cmd", required=True)

    p_extract = siphon_sub.add_parser("extract", help="Extract session memory from transcript")
    p_extract.add_argument("transcript", type=Path, help="Path to session transcript")
    p_extract.add_argument("--output", "-o", type=Path, default=None, help="Output memory file")
    p_extract.add_argument("--session-id", "-s", default=None, help="Override session ID")
    p_extract.add_argument("--dry-run", action="store_true", help="Print extraction without writing")
    p_extract.set_defaults(handler="siphon_extract")

    p_rebirth = siphon_sub.add_parser("rebirth", help="Build rebirth prompt from MEMORY.md")
    p_rebirth.add_argument("--memory", "-m", type=Path, default=None, help="Path to MEMORY.md")
    p_rebirth.add_argument("--last", "-n", type=int, default=5, help="Number of sessions to include")
    p_rebirth.set_defaults(handler="siphon_rebirth")

    args = parser.parse_args(argv)

    mantle = Mantle(VenomConfig().mantle)

    if args.handler == "status":
        _cmd_status()
    elif args.handler == "mantle_show":
        _cmd_mantle_show(mantle)
    elif args.handler == "mantle_inject":
        _cmd_mantle_inject(mantle)
    elif args.handler == "siphon_extract":
        from .siphon.cli import main as siphon_main

        siphon_argv = ["extract", str(args.transcript)]
        if args.output is not None:
            siphon_argv.extend(["--output", str(args.output)])
        if args.session_id is not None:
            siphon_argv.extend(["--session-id", args.session_id])
        if args.dry_run:
            siphon_argv.append("--dry-run")
        siphon_main(siphon_argv)
    elif args.handler == "siphon_rebirth":
        from .siphon.cli import main as siphon_main

        siphon_argv = ["rebirth"]
        if args.memory is not None:
            siphon_argv.extend(["--memory", str(args.memory)])
        siphon_argv.extend(["--last", str(args.last)])
        siphon_main(siphon_argv)
    else:
        parser.error("unknown command")


if __name__ == "__main__":
    main()
