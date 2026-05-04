![CI](https://github.com/LalaSkye/invariant-lock/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
![stdlib only](https://img.shields.io/badge/stdlib-only-green)
![~130 LOC](https://img.shields.io/badge/LOC-~130-lightgrey)

# invariant-lock

Refuse execution unless the invariant file's hash and version both match the lock. The simplest possible defence against silent drift on the demonstrated path.

**v0.1.0** | MIT License | Zero dependencies

---

## Why This Exists

Invariants that silently change between versions are not invariants — they are suggestions. Systems that rely on governance rules need a way to prove that those rules have not been quietly modified between the time they were declared and the time they are enforced. `invariant-lock` binds a hash of the invariants file to an explicit version increment: if either has changed without the other, execution is refused on the demonstrated path. No gradual drift, no silent regressions, no ambiguity inside that hash + version check surface.

---

## Architecture

```
  invariants.json  ──┐
                     ├──> compute_sha256()  ──> .lock.json
  version field   ──┘                             │
                                                  │
  Before execution:                               │
                                                  v
  invariants.json  ──┐                    ┌─────────────┐
                     ├──> verify()  ──>   │ hash match? │ ──> OK / LockError
  .lock.json      ──┘                     │ ver match?  │
                                          └─────────────┘
```

**Fail-closed on the demonstrated path:** any mismatch blocks execution. No silent fallbacks inside the lock check.

---

## Quickstart

```bash
git clone https://github.com/LalaSkye/invariant-lock.git
cd invariant-lock
pip install .

# 1. Define your invariants
cat > invariants.json << 'EOF'
{
  "version": "1.0.0",
  "rules": [
    "execution requires explicit authority",
    "halt is a structural capability"
  ]
}
EOF

# 2. Create the lock file
invariant-lock init --invariants invariants.json --lock invariants.lock.json

# 3. Verify before execution (returns 0 on success)
invariant-lock verify --invariants invariants.json --lock invariants.lock.json
# OK

# 4. Tamper with the invariants (without bumping version)
echo '"sneaky_rule"' >> invariants.json

# 5. Verify again — execution refused
invariant-lock verify --invariants invariants.json --lock invariants.lock.json
# LockError: FAIL: invariant drift (sha256 mismatch)
```

Compute a hash only:

```bash
invariant-lock hash --file invariants.json
# sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

---

## Invariants File Format

```json
{
  "version": "1.0.0",
  "rules": [
    "execution requires explicit authority",
    "halt is a structural capability"
  ]
}
```

The `version` field is required. All other fields are preserved but not validated. The entire file content is hashed — any byte change produces a different hash.

---

## Python API

```python
from invariant_lock.core import init_lock, verify, compute_sha256

# Create lock
lock = init_lock("invariants.json", "invariants.lock.json")
# lock == {"version": "1.0.0", "sha256": "e3b0c44..."}

# Verify (returns 'OK' or raises LockError)
result = verify("invariants.json", "invariants.lock.json")
# result == "OK"

# Hash a file
sha = compute_sha256("invariants.json")
# sha == "e3b0c44..."
```

---

## Failure Modes

| Condition | Error |
|---|---|
| File not found | `LockError: FAIL: file not found` |
| Invalid JSON | `LockError: FAIL: invalid JSON` |
| Missing version field | `LockError: FAIL: missing required field 'version'` |
| Version mismatch | `LockError: FAIL: version mismatch` |
| Content drift (hash) | `LockError: FAIL: invariant drift (sha256 mismatch)` |

---

## Constraints

- ~130 LOC (implementation + CLI)
- Zero dependencies (stdlib only)
- SHA-256 hashing
- Listed failures are explicit and typed
- Fail-closed within the lock check: no silent fallbacks
- Deterministic for the same input bytes

---

## What this does not prove

This repository does not prove adoption, certification, standardisation, production readiness, or path-universal deployment coverage.

It is a scoped primitive that demonstrates one property: content hash + version must match the lockfile exactly before execution is allowed on the demonstrated path.

Failures outside that surface are out of scope, including:

- semantic correctness of the rules inside the invariant file
- governance integration around the lock check
- runtime adoption in a larger system
- protection against mutation paths that do not call this verifier

---

## Part of the Execution Boundary Series

| Repo | Layer | What It Does |
|---|---|---|
| [interpretation-boundary-lab](https://github.com/LalaSkye/interpretation-boundary-lab) | Upstream boundary | 10-rule admissibility gate for interpretations |
| [dual-boundary-admissibility-lab](https://github.com/LalaSkye/dual-boundary-admissibility-lab) | Full corridor | Dual-boundary model with pressure monitoring and C-sector rotation |
| [execution-boundary-lab](https://github.com/LalaSkye/execution-boundary-lab) | Execution boundary | Demonstrates cascading failures without upstream governance |
| [stop-machine](https://github.com/LalaSkye/stop-machine) | Control primitive | Deterministic three-state stop controller |
| [constraint-workshop](https://github.com/LalaSkye/constraint-workshop) | Control primitives | Execution gate, invariant litmus, stop machine |
| [csgr-lab](https://github.com/LalaSkye/csgr-lab) | Measurement | Contracted stability and drift measurement |
| [invariant-lock](https://github.com/LalaSkye/invariant-lock) | Drift prevention | Refuse execution unless version increments |
| [policy-lint](https://github.com/LalaSkye/policy-lint) | Policy validation | Deterministic linter for governance statements |
| [deterministic-lexicon](https://github.com/LalaSkye/deterministic-lexicon) | Vocabulary | Fixed terms, exact matches, no inference |

---

## License

MIT. See `LICENSE`.

---

## Authorship & Rights

All architecture, methods, and system designs in this repository are the original work of **Ricky Dean Jones** unless otherwise stated.
No rights to use, reproduce, or implement are granted without explicit permission beyond the terms of the repository licence.

**Author:** Ricky Dean Jones
**Repository owner:** [LalaSkye](https://github.com/LalaSkye)
**Status:** Active research / architecture work
**Part of:** [Execution Boundary Series](https://github.com/LalaSkye) — TrinityOS / AlvianTech

---

This repository demonstrates deterministic control using standard engineering techniques. No proprietary frameworks or external implementations are used.

