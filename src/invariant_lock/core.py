"""Core logic for invariant-lock."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


class LockError(Exception):
    """Raised when invariant lock validation fails."""


def compute_sha256(file_path: str) -> str:
    """Compute SHA-256 hash of a file's contents."""
    path = Path(file_path)
    if not path.exists():
        raise LockError(f"FAIL: file not found: {file_path}")
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def load_json(file_path: str) -> dict:
    """Load and parse a JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise LockError(f"FAIL: file not found: {file_path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise LockError(f"FAIL: invalid JSON in {file_path}: {e}") from e


def validate_invariants(data: dict, file_path: str) -> None:
    """Check that invariants file has required fields."""
    if "version" not in data:
        raise LockError(
            f"FAIL: missing required field 'version' in {file_path}"
        )


def validate_lock(data: dict, file_path: str) -> None:
    """Check that lock file has required fields."""
    for field in ("version", "sha256"):
        if field not in data:
            raise LockError(
                f"FAIL: lockfile missing required field '{field}'"
            )


def init_lock(
    invariants_path: str,
    lock_path: str,
) -> dict:
    """Create a lock file from an invariants file."""
    data = load_json(invariants_path)
    validate_invariants(data, invariants_path)
    sha = compute_sha256(invariants_path)
    lock = {
        "version": data["version"],
        "sha256": sha,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    Path(lock_path).write_text(
        json.dumps(lock, indent=2) + "\n", encoding="utf-8"
    )
    return lock


def verify(
    invariants_path: str,
    lock_path: str,
) -> str:
    """Verify invariants against lock file. Returns 'OK' or raises."""
    inv_data = load_json(invariants_path)
    validate_invariants(inv_data, invariants_path)
    lock_data = load_json(lock_path)
    validate_lock(lock_data, lock_path)
    current_sha = compute_sha256(invariants_path)
    if inv_data["version"] != lock_data["version"]:
        raise LockError(
            f"FAIL: version mismatch "
            f"(invariants={inv_data['version']} "
            f"lock={lock_data['version']})"
        )
    if current_sha != lock_data["sha256"]:
        raise LockError("FAIL: invariant drift (sha256 mismatch)")
    return "OK"
