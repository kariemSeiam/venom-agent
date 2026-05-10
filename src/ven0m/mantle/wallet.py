"""Identity Wallet — persistent identity that survives session restarts.

The wallet stores:
- Active pact/voice versions (which files are loaded)
- Session history (when identity was loaded, by which model)
- Identity mutations (user corrections to pact/voice)
- Conditioning bundles (accumulated behavioral adjustments)

Stored at: ~/.ven0m/wallet.json
"""

from __future__ import annotations

import fcntl
import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_WALLET_PATH = Path.home() / ".ven0m" / "wallet.json"
MAX_SESSIONS = 100


class Wallet:
    """JSON-backed identity store with file-level locking."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path if path is not None else DEFAULT_WALLET_PATH
        self._data: dict[str, Any] = {
            "version": 1,
            "active": {"pact_version": None, "voice_version": None},
            "sessions": [],
            "corrections": [],
            "conditioning": {},
        }

    # ── load / save ──────────────────────────────────────────────

    @classmethod
    def load(cls, path: Path | None = None) -> Wallet:
        """Read from disk; create fresh wallet if file is missing."""
        wallet = cls(path)
        if wallet.path.exists():
            try:
                text = wallet.path.read_text(encoding="utf-8")
                data = json.loads(text)
                # Merge loaded data into default structure so new keys survive.
                for key in wallet._data:
                    if key in data:
                        wallet._data[key] = data[key]
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Wallet: failed to read %s — starting fresh (%s)", wallet.path, exc)
        return wallet

    def save(self) -> None:
        """Write to disk with directory creation and file locking."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        try:
            fd = open(tmp, "w", encoding="utf-8")  # noqa: SIM115
            try:
                fcntl.flock(fd, fcntl.LOCK_EX)
                json.dump(self._data, fd, indent=2, ensure_ascii=False)
                fd.flush()
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
                fd.close()
            tmp.replace(self.path)
        except OSError:
            if tmp.exists():
                tmp.unlink()
            raise

    # ── session recording ────────────────────────────────────────

    def record_session(
        self,
        model: str,
        pact_version: str | None = None,
        voice_version: str | None = None,
    ) -> None:
        """Log a session and auto-compact when over limit."""
        entry = {
            "ts": time.time(),
            "model": model,
            "pact_version": pact_version,
            "voice_version": voice_version,
        }
        self._data["sessions"].append(entry)
        if pact_version is not None:
            self._data["active"]["pact_version"] = pact_version
        if voice_version is not None:
            self._data["active"]["voice_version"] = voice_version
        self._compact_sessions()

    def _compact_sessions(self) -> None:
        """Keep last MAX_SESSIONS entries, drop older ones."""
        sessions = self._data["sessions"]
        if len(sessions) > MAX_SESSIONS:
            self._data["sessions"] = sessions[-MAX_SESSIONS:]

    # ── corrections ──────────────────────────────────────────────

    def apply_correction(
        self,
        field: str,
        old_value: str,
        new_value: str,
        reason: str = "",
    ) -> None:
        """Record a user correction to the identity."""
        entry = {
            "ts": time.time(),
            "field": field,
            "old_value": old_value,
            "new_value": new_value,
            "reason": reason,
        }
        self._data["corrections"].append(entry)

    @property
    def corrections(self) -> list[dict[str, Any]]:
        return list(self._data["corrections"])

    # ── conditioning ─────────────────────────────────────────────

    def add_conditioning(self, key: str, value: Any) -> None:
        """Accumulate a behavioral adjustment."""
        self._data["conditioning"][key] = value

    def get_conditioning(self) -> dict[str, Any]:
        """Return accumulated conditioning as a dict."""
        return dict(self._data["conditioning"])

    # ── export / introspection ───────────────────────────────────

    def export_identity(self) -> dict[str, Any]:
        """Full identity dump for debugging."""
        return {
            "wallet_path": str(self.path),
            "active": dict(self._data["active"]),
            "session_count": len(self._data["sessions"]),
            "correction_count": len(self._data["corrections"]),
            "conditioning": dict(self._data["conditioning"]),
            "last_session": self._data["sessions"][-1] if self._data["sessions"] else None,
            "recent_corrections": self._data["corrections"][-5:],
        }

    @property
    def session_count(self) -> int:
        return len(self._data["sessions"])

    @property
    def active(self) -> dict[str, Any]:
        return dict(self._data["active"])

    @property
    def sessions(self) -> list[dict[str, Any]]:
        return list(self._data["sessions"])
