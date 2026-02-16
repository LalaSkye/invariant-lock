"""CLI for invariant-lock."""

import argparse
import sys

from invariant_lock.core import LockError, compute_sha256, init_lock, verify


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="invariant-lock",
        description="Prevent silent drift in invariants.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="Create lock file from invariants.")
    p_init.add_argument("--invariants", required=True, help="Path to invariants JSON.")
    p_init.add_argument("--lock", required=True, help="Path to write lock file.")

    # verify
    p_verify = sub.add_parser("verify", help="Verify invariants against lock.")
    p_verify.add_argument("--invariants", required=True, help="Path to invariants JSON.")
    p_verify.add_argument("--lock", required=True, help="Path to lock file.")

    # hash
    p_hash = sub.add_parser("hash", help="Print SHA-256 of a file.")
    p_hash.add_argument("--file", required=True, help="Path to file.")

    args = parser.parse_args()

    try:
        if args.command == "init":
            lock = init_lock(args.invariants, args.lock)
            print(f"OK: lock created (version={lock['version']} sha256={lock['sha256'][:12]}...)")
        elif args.command == "verify":
            result = verify(args.invariants, args.lock)
            print(result)
        elif args.command == "hash":
            print(compute_sha256(args.file))
    except LockError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
