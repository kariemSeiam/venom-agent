"""VENOM root CLI — SIPHON, Mantle, status."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from . import __version__
from .core.config import VenomConfig
from .mantle import Mantle, Wallet


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
    print(f"  memory_dir: {cfg.siphon.memory_dir}")
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


def _cmd_mantle_status(mantle: Mantle) -> None:
    wallet = Wallet.load()
    pact = mantle.load_pact()
    voice = mantle.load_voice()
    print("=== Mantle Identity Status ===")
    print(f"  pact_loaded: {bool(pact)}")
    print(f"  voice_loaded: {bool(voice)}")
    print(f"  wallet_path: {wallet.path}")
    print(f"  sessions_recorded: {wallet.session_count}")
    print(f"  corrections_count: {len(wallet.corrections)}")
    print(f"  active_pact_version: {wallet.active.get('pact_version')}")
    print(f"  active_voice_version: {wallet.active.get('voice_version')}")
    cond = wallet.get_conditioning()
    print(f"  conditioning_keys: {list(cond.keys()) if cond else '(none)'}")
    # Last 3 corrections
    recent = wallet.corrections[-3:]
    if recent:
        print("  recent_corrections:")
        for c in recent:
            ts = datetime.fromtimestamp(c["ts"], tz=timezone.utc).isoformat()
            print(f"    [{ts}] {c['field']}: {c['old_value']!r} → {c['new_value']!r} ({c.get('reason', '')})")


def _cmd_mantle_history() -> None:
    wallet = Wallet.load()
    sessions = wallet.sessions[-20:]
    if not sessions:
        print("(no sessions recorded)")
        return
    print(f"=== Last {len(sessions)} Session(s) ===")
    for s in sessions:
        ts = datetime.fromtimestamp(s["ts"], tz=timezone.utc).isoformat()
        print(f"  {ts}  model={s.get('model', '?')}  pact={s.get('pact_version')}  voice={s.get('voice_version')}")


def _cmd_mantle_correct(field: str, value: str, reason: str, wallet_path: Path | None = None) -> None:
    wallet = Wallet.load(wallet_path)
    wallet.apply_correction(field, "", value, reason)
    wallet.save()
    print(f"Correction recorded: {field}={value!r} reason={reason!r}")


def _cmd_mantle_export(mantle: Mantle) -> None:
    wallet = Wallet.load()
    outer, inner = mantle.get_system_prompt_dual(wallet)
    export = wallet.export_identity()
    export["outer_prompt_length"] = len(outer)
    export["inner_prompt_length"] = len(inner)
    print(json.dumps(export, indent=2, default=str))


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
    p_mantle_status = mantle_sub.add_parser("status", help="Show identity state, session count, last corrections")
    p_mantle_status.set_defaults(handler="mantle_status")
    p_mantle_history = mantle_sub.add_parser("history", help="Show last 20 sessions from wallet")
    p_mantle_history.set_defaults(handler="mantle_history")
    p_mantle_correct = mantle_sub.add_parser("correct", help="Apply a correction to identity field")
    p_mantle_correct.add_argument("field", help="Identity field to correct")
    p_mantle_correct.add_argument("value", help="New value")
    p_mantle_correct.add_argument("--reason", "-r", default="", help="Reason for correction")
    p_mantle_correct.add_argument("--wallet", type=Path, default=None, help="Path to wallet.json")
    p_mantle_correct.set_defaults(handler="mantle_correct")
    p_mantle_export = mantle_sub.add_parser("export", help="Dump full identity to stdout as JSON")
    p_mantle_export.set_defaults(handler="mantle_export")

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

    p_watch = siphon_sub.add_parser(
        "watch",
        help="Watch Hermes session JSON files and auto-extract into MEMORY/",
    )
    p_watch.add_argument(
        "--watch-dir",
        type=Path,
        default=None,
        help="Directory to watch (default: ~/.hermes/sessions)",
    )
    p_watch.add_argument(
        "--memory-dir",
        type=Path,
        default=None,
        help="MEMORY folder containing MEMORY.md (default: ./MEMORY)",
    )
    p_watch.add_argument(
        "--poll-interval",
        type=float,
        default=None,
        help="Polling interval in seconds (default: 30)",
    )
    p_watch.set_defaults(handler="siphon_watch")

    args = parser.parse_args(argv)

    mantle = Mantle(VenomConfig().mantle)

    if args.handler == "status":
        _cmd_status()
    elif args.handler == "mantle_show":
        _cmd_mantle_show(mantle)
    elif args.handler == "mantle_inject":
        _cmd_mantle_inject(mantle)
    elif args.handler == "mantle_status":
        _cmd_mantle_status(mantle)
    elif args.handler == "mantle_history":
        _cmd_mantle_history()
    elif args.handler == "mantle_correct":
        _cmd_mantle_correct(args.field, args.value, args.reason, args.wallet)
    elif args.handler == "mantle_export":
        _cmd_mantle_export(mantle)
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
    elif args.handler == "siphon_watch":
        from .siphon.daemon import run_watch

        base = VenomConfig().siphon
        overrides = {}
        if args.watch_dir is not None:
            overrides["watch_dir"] = args.watch_dir.expanduser().resolve()
        if args.memory_dir is not None:
            overrides["memory_dir"] = args.memory_dir.expanduser().resolve()
        if args.poll_interval is not None:
            overrides["poll_interval"] = args.poll_interval
        cfg = replace(base, **overrides) if overrides else base
        run_watch(cfg)
    else:
        parser.error("unknown command")


if __name__ == "__main__":
    main()
