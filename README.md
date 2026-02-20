![CI](https://github.com/LalaSkye/invariant-lock/actions/workflows/ci.yml/badge.svg)

# invariant-lock

Prevent silent drift in invariants. Refuse execution unless version increments.

**v0.1.0** | MIT License | Zero dependencies

## Why this exists

Invariants that silently change between versions aren't invariants — they're suggestions. This primitive enforces version-locked execution: if the invariant definition has changed and the version hasn't been explicitly incremented, the system refuses to run. No gradual drift, no silent regressions, no ambiguity about which rules were in effect when something executed.

## What it does

`invariant-lock` hashes an invariants JSON file (SHA-256) and stores the hash alongside the declared version in a lock file. Before execution, the system verifies that:

- The current hash matches the locked hash
- The current version matches the locked version

If either check fails, execution is refused with a clear error.

## Quickstart

```bash
# Install
pip install .

# Create a lock file from invariants
invariant-lock init --invariants invariants.json --lock invariants.lock.json

# Verify before execution
invariant-lock verify --invariants invariants.json --lock invariants.lock.json

# Compute hash only
invariant-lock hash --file invariants.json
```

## Invariants file format

```json
{
  "version": "1.0.0",
  "rules": [
    "execution requires explicit authority",
    "halt is a structural capability"
  ]
}
```

The `version` field is required. All other fields are preserved but not validated.

## API

```python
from invariant_lock.core import init_lock, verify, compute_sha256

# Create lock
lock = init_lock("invariants.json", "invariants.lock.json")

# Verify (returns 'OK' or raises LockError)
result = verify("invariants.json", "invariants.lock.json")

# Hash a file
sha = compute_sha256("invariants.json")
```

## Failure modes

| Condition | Error |
|---|---|
| File not found | `LockError: FAIL: file not found` |
| Invalid JSON | `LockError: FAIL: invalid JSON` |
| Missing version field | `LockError: FAIL: missing required field 'version'` |
| Version mismatch | `LockError: FAIL: version mismatch` |
| Content drift (hash) | `LockError: FAIL: invariant drift (sha256 mismatch)` |

## Constraints

- ~130 LOC (implementation + CLI)
- Zero dependencies (stdlib only)
- SHA-256 hashing
- All failures are explicit and typed
- No silent fallbacks
- Deterministic: same inputs always produce same outputs

## License

MIT
