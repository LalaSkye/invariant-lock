# invariant-lock
Prevent silent drift in invariants. Refuse execution unless version increments.

## Why this exists

Invariants that silently change between versions aren't invariants — they're suggestions. This primitive enforces version-locked execution: if the invariant definition has changed and the version hasn't been explicitly incremented, the system refuses to run. No gradual drift, no silent regressions, no ambiguity about which rules were in effect when something executed.
