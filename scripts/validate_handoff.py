#!/usr/bin/env python3
"""Handoff contract validator."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import guard_paths as gp

MANDATORY_CHECK_ROLES = {"builder", "qa", "security"}


def validate_handoff(handoff_data: dict, root: Path = ROOT) -> tuple[bool, list[str]]:
    errors = []
    # 1. Status check
    if handoff_data.get("status") != "complete":
        errors.append(f"Handoff status must be 'complete', got '{handoff_data.get('status')}'")

    # 2. Artifact check
    artifact_path = handoff_data.get("artifact")
    if not artifact_path:
        errors.append("Handoff missing 'artifact' field")
    elif not (root / artifact_path).exists():
        errors.append(f"Referenced artifact does not exist: {artifact_path}")

    # 3. Acceptance refs check against harness.md
    harness_file = root / "docs/harness.md"
    if harness_file.exists():
        harness_text = harness_file.read_text(encoding="utf-8")
        for ref in handoff_data.get("acceptance_refs", []):
            if not re.search(rf"\b{re.escape(ref)}\b", harness_text):
                errors.append(f"Acceptance ref '{ref}' not found in docs/harness.md")

    # 4. Files touched inside role allow-list
    role = handoff_data.get("from", "")
    files_touched = handoff_data.get("files_touched", [])
    violations = gp.check_paths(role, files_touched, root=root)
    if violations:
        errors.extend(violations)

    # 5. Checks run
    if role in MANDATORY_CHECK_ROLES:
        checks = handoff_data.get("checks_run", [])
        if not checks:
            errors.append(f"Role '{role}' must provide at least one check in 'checks_run'")
        for c in checks:
            if c.get("exit", 1) != 0:
                errors.append(f"Check '{c.get('cmd')}' failed with exit code {c.get('exit')}")

    return len(errors) == 0, errors


def main(argv=None):
    if len(sys.argv) < 2:
        print("Usage: python validate_handoff.py <path-to-handoff.json>")
        return 1
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"File not found: {p}", file=sys.stderr)
        return 1
    data = json.loads(p.read_text(encoding="utf-8"))
    ok, errors = validate_handoff(data)
    if not ok:
        for e in errors:
            print(f"REJECTED: {e}", file=sys.stderr)
        return 1
    print("Handoff validated: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
