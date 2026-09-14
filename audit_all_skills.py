#!/usr/bin/env python3
"""Validate the checked-in skill catalog and Python syntax without dependencies.

Usage: python3 audit_all_skills.py
"""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SUPPORT_DIRS = {"tests", "public", "dist", "build", "__pycache__", "venv", "env", "ENV"}


def main() -> int:
    spec = importlib.util.spec_from_file_location(
        "quick_validate", ROOT / "skill-creator/scripts/quick_validate.py"
    )
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    candidates = sorted(
        path for path in ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".") and path.name not in SUPPORT_DIRS
    )
    errors = []
    script_count = 0
    if not candidates:
        errors.append("No skill directories found")
    for path in candidates:
        valid, message = validator.validate_skill(path)
        if not valid:
            errors.append(f"{path.name}: {message}")
        for script in sorted((path / "scripts").rglob("*.py")):
            script_count += 1
            try:
                ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
            except (SyntaxError, UnicodeError, OSError) as exc:
                errors.append(f"{script.relative_to(ROOT)}: {exc}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Audited {len(candidates)} skills and {script_count} Python scripts; {len(errors)} errors.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
