#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "models/backup-policy.json")
    data = json.loads(path.read_text())
    policies = data.get("policies", [])
    if not policies:
        raise SystemExit("No backup policies defined")

    failed = False
    for policy in policies:
        name = policy.get("name", "unnamed")
        freq = policy.get("backup_frequency_hours")
        retention = policy.get("retention_days")
        immutable = policy.get("immutable_copy")
        secondary = policy.get("secondary_copy")

        if not isinstance(freq, (int, float)) or freq <= 0:
            print(f"FAIL {name}: invalid backup frequency")
            failed = True
        if not isinstance(retention, int) or retention <= 0:
            print(f"FAIL {name}: invalid retention")
            failed = True
        if name == "critical" and immutable is not True:
            print("FAIL critical: immutable copy is required in this reference model")
            failed = True
        if secondary is not True:
            print(f"WARN {name}: no secondary copy defined")

        if not failed:
            print(f"PASS {name}: every {freq}h, retain {retention}d")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
