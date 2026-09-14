#!/usr/bin/env python3
"""Check README and CLAUDE catalog blocks against actual skill directories.

Usage: python3 verify_docs.py
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
START = "<!-- SKILL-LIST:START -->"
END = "<!-- SKILL-LIST:END -->"


def main() -> int:
    actual = {path.parent.name for path in ROOT.glob("*/SKILL.md")}
    errors = []
    if not actual:
        errors.append("No skills found")
    for filename in ("README.md", "CLAUDE.md"):
        try:
            text = (ROOT / filename).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{filename}: {exc}")
            continue
        if text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END):
            errors.append(f"{filename}: exactly one ordered SKILL-LIST block is required")
            continue
        block = text.split(START, 1)[1].split(END, 1)[0]
        names = re.findall(r"^- `([a-z0-9-]+)`\s*$", block, flags=re.MULTILINE)
        listed = set(names)
        if len(names) != len(listed):
            errors.append(f"{filename}: duplicate catalog entries")
        if listed != actual:
            errors.append(
                f"{filename}: missing={sorted(actual - listed)}, stale={sorted(listed - actual)}"
            )
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Checked 2 catalogs against {len(actual)} skills; {len(errors)} errors.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
