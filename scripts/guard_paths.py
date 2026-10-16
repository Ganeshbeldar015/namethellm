#!/usr/bin/env python3
"""Path/lane guard. Given role and touched files, exit non-zero if outside allow-list."""
import argparse
import fnmatch
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Default role allow-lists (can also be read from harness/roles/<role>.md)
ROLE_ALLOW_LISTS = {
    "orchestrator": [
        "harness/**", "docs/**", "scripts/**", "tests/**", "AGENTS.md", "CLAUDE.md",
        ".mcp.json", ".github/**", ".cursor/**"
    ],
    "po-spec": [
        "harness/artifacts/*/01-spec.md",
        "harness/artifacts/*/handoff-*.json",
    ],
    "designer": [
        "harness/artifacts/*/02-design.md",
        "harness/artifacts/*/handoff-*.json",
        "docs/adr/**",
    ],
    "tech-lead": [
        "harness/artifacts/*/03-plan.md",
        "harness/artifacts/*/handoff-*.json",
        "docs/adr/**",
    ],
    "test-author": [
        "tests/**",
        "harness/artifacts/*/04-tests.md",
        "harness/artifacts/*/handoff-*.json",
    ],
    "builder": [
        "src/**",
        "harness/artifacts/*/05-build*.md",
        "harness/artifacts/*/handoff-*.json",
    ],
    "reviewer": [
        "harness/artifacts/*/06-review.md",
        "harness/artifacts/*/handoff-*.json",
    ],
    "security": [
        "harness/artifacts/*/06b-security.md",
        "harness/artifacts/*/handoff-*.json",
    ],
    "qa": [
        "harness/artifacts/*/07-qa.md",
        "harness/artifacts/*/handoff-*.json",
    ],
    "scribe": [
        "docs/**",
        "harness/artifacts/*/08-docs.md",
        "harness/artifacts/*/handoff-*.json",
        "README.md",
        "CHANGELOG.md",
    ],
    "librarian": [
        "docs/memory/**",
        "AGENTS.md",
        "harness/artifacts/*/handoff-*.json",
    ],
}


def is_path_allowed(path_str: str, allow_patterns: list) -> bool:
    normalized = path_str.replace("\\", "/").lstrip("./")
    for pattern in allow_patterns:
        norm_pat = pattern.replace("\\", "/").lstrip("./")
        if norm_pat.endswith("/**"):
            prefix = norm_pat[:-3]
            if normalized == prefix or normalized.startswith(prefix + "/"):
                return True
        elif fnmatch.fnmatch(normalized, norm_pat):
            return True
    return False


def check_paths(role: str, files: list, root: Path = ROOT) -> list:
    role_lower = role.lower()
    allowed_patterns = ROLE_ALLOW_LISTS.get(role_lower, [])

    # Also inspect lock files if role is builder
    violations = []
    for f in files:
        f_norm = f.replace("\\", "/").lstrip("./")
        if not is_path_allowed(f_norm, allowed_patterns):
            violations.append(f"File '{f_norm}' is outside allow-list for role '{role}'")

    return violations


def main(argv=None):
    parser = argparse.ArgumentParser(description="Guard file writes by role allow-list")
    parser.add_argument("--role", required=True, help="Role name")
    parser.add_argument("--files", nargs="*", default=[], help="Files to check")
    parser.add_argument("--stdin", action="store_true", help="Read file paths from stdin")
    args = parser.parse_args(argv)

    files = list(args.files)
    if args.stdin:
        files.extend([line.strip() for line in sys.stdin if line.strip()])

    violations = check_paths(args.role, files)
    if violations:
        for v in violations:
            print(f"GUARD VIOLATION: {v}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
