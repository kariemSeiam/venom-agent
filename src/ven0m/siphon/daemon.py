"""SIPHON daemon — watch Hermes session files and auto-extract to MEMORY."""

from __future__ import annotations

import json
import logging
import signal
import threading
import time
from pathlib import Path
from typing import Any

from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

from ..core.config import SiphonConfig, VenomConfig
from .backoff import BackoffController
from .extractor import append_corrections, append_extraction, append_siphon_error, extract

LOG = logging.getLogger(__name__)

INDEX_PROCESSED_KEY = "processed"
_PATH_BACKOFF: dict[str, BackoffController] = {}


def ensure_memory_and_watch_dirs(config: SiphonConfig) -> None:
    """Create MEMORY dir and watch dir if missing."""
    config.memory_dir.mkdir(parents=True, exist_ok=True)
    config.watch_dir.mkdir(parents=True, exist_ok=True)


def load_siphon_index(config: SiphonConfig) -> dict[str, Any]:
    path = config.siphon_index_path
    if not path.exists():
        return {INDEX_PROCESSED_KEY: []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {INDEX_PROCESSED_KEY: []}
    if INDEX_PROCESSED_KEY not in data or not isinstance(data[INDEX_PROCESSED_KEY], list):
        data[INDEX_PROCESSED_KEY] = []
    return data


def save_siphon_index(config: SiphonConfig, data: dict[str, Any]) -> None:
    config.memory_dir.mkdir(parents=True, exist_ok=True)
    path = config.siphon_index_path
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def is_processable_session_path(path: Path) -> bool:
    if path.suffix.lower() != ".json":
        return False
    name = path.name
    if name == "sessions.json":
        return False
    if name.startswith("request_dump_"):
        return False
    return True


def transcript_from_hermes_session(data: dict[str, Any]) -> str:
    """Build a plain-text transcript from Hermes session JSON."""
    lines: list[str] = []
    sid = data.get("session_id") or data.get("id")
    if sid:
        lines.append(f"[meta session_id={sid}]")

    messages = data.get("messages")
    if not isinstance(messages, list):
        return "\n".join(lines)

    for msg in messages:
        if not isinstance(msg, dict):
            continue
        role = msg.get("role", "?")
        content = _message_content(msg)
        if content.strip():
            lines.append(f"[{role}]: {content}")
        elif role == "assistant" and msg.get("tool_calls"):
            tc = msg.get("tool_calls")
            lines.append(f"[{role}]: [tool_calls: {len(tc) if isinstance(tc, list) else 0}]")

    return "\n".join(lines)


def _message_content(msg: dict[str, Any]) -> str:
    c = msg.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts: list[str] = []
        for block in c:
            if isinstance(block, dict):
                if block.get("type") == "text" and isinstance(block.get("text"), str):
                    parts.append(block["text"])
                elif isinstance(block.get("content"), str):
                    parts.append(block["content"])
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return ""


def _backoff_for(path_key: str) -> BackoffController:
    if path_key not in _PATH_BACKOFF:
        _PATH_BACKOFF[path_key] = BackoffController()
    return _PATH_BACKOFF[path_key]


def process_session_json_file(path: Path, config: SiphonConfig) -> bool:
    """
    If path is a new Hermes session JSON, extract and persist.
    Returns True if extraction ran successfully.
    """
    path = path.resolve()
    if not is_processable_session_path(path):
        return False

    index_data = load_siphon_index(config)
    processed: list[str] = list(index_data.get(INDEX_PROCESSED_KEY, []))
    key = str(path)
    if key in processed:
        LOG.debug("SIPHON daemon: skip already indexed %s", path)
        return False

    try:
        raw_json = path.read_text(encoding="utf-8")
        data = json.loads(raw_json)
    except (OSError, json.JSONDecodeError) as e:
        LOG.warning("SIPHON daemon: unreadable json %s — %s", path, e)
        return False

    if not isinstance(data, dict):
        return False

    transcript = transcript_from_hermes_session(data)
    if len(transcript.strip()) < 10:
        LOG.debug("SIPHON daemon: skip empty transcript %s", path)
        return False

    if not config.has_api_key:
        LOG.warning("SIPHON daemon: ZAI_API_KEY not set; cannot extract %s", path)
        return False

    bc = _backoff_for(key)
    extraction = None
    for attempt in range(3):
        try:
            extraction = extract(transcript, config)
            bc.reset()
            break
        except Exception as e:
            append_siphon_error(
                config.memory_dir,
                {
                    "kind": "daemon_extract_failed",
                    "path": key,
                    "attempt": attempt + 1,
                    "error": repr(e),
                },
            )
            LOG.exception("SIPHON daemon: extract failed for %s (attempt %s)", path, attempt + 1)
            if attempt == 2:
                return False
            delay = bc.sleep_seconds_after_failure()
            LOG.info("SIPHON daemon: backoff %.2fs before retry", delay)
            time.sleep(delay)

    if extraction is None:
        return False

    append_extraction(extraction, config.memory_path)
    if extraction.corrections:
        append_corrections(extraction, config.corrections_path)

    processed.append(key)
    index_data[INDEX_PROCESSED_KEY] = processed
    save_siphon_index(config, index_data)

    LOG.info(
        "SIPHON daemon: extracted %s → MEMORY (%s decisions, %s corrections)",
        extraction.session_id,
        len(extraction.decisions),
        len(extraction.corrections),
    )
    return True


class _SessionFileHandler(FileSystemEventHandler):
    def __init__(self, config: SiphonConfig) -> None:
        self._config = config

    def on_created(self, event):  # noqa: ANN001
        self._handle(event)

    def on_modified(self, event):  # noqa: ANN001
        self._handle(event)

    def _handle(self, event) -> None:
        if getattr(event, "is_directory", False):
            return
        src = getattr(event, "src_path", None)
        if not src:
            return
        path = Path(src)
        # Brief settle for writers still flushing
        time.sleep(0.3)
        process_session_json_file(path, self._config)


def run_watch(config: SiphonConfig | None = None) -> None:
    """
    Poll watch_dir for Hermes session JSON files; extract new sessions into MEMORY/.
    Handles SIGINT/SIGTERM for graceful shutdown.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    cfg = config or VenomConfig().siphon
    ensure_memory_and_watch_dirs(cfg)

    stop = threading.Event()

    def handle_signal(signum: int, frame: object | None) -> None:  # noqa: ARG001
        LOG.info("SIPHON daemon: signal %s — shutting down", signum)
        stop.set()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    timeout = max(1.0, float(cfg.poll_interval))
    observer = PollingObserver(timeout=timeout)
    handler = _SessionFileHandler(cfg)
    observer.schedule(handler, str(cfg.watch_dir.resolve()), recursive=True)
    observer.start()
    LOG.info(
        "SIPHON daemon: watching %s (poll %.1fs), memory dir %s",
        cfg.watch_dir,
        timeout,
        cfg.memory_dir,
    )

    try:
        while not stop.is_set():
            time.sleep(0.5)
    finally:
        observer.stop()
        observer.join(timeout=10.0)
        LOG.info("SIPHON daemon: stopped")
