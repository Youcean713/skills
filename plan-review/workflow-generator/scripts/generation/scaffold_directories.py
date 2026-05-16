"""
Create directory skeleton for a generated workflow skill package.
Only creates the skill package structure — generator-context/ is managed separately.
"""
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: python scaffold_directories.py <skill-package-dir>")
        sys.exit(1)

    base = Path(sys.argv[1])

    # Skill package directories (always required)
    required_dirs = [
        "references/workflow",
        "references/standards",
        "references/evidence",
        "references/writing",
        "references/delivery",
        "assets/templates",
    ]

    # Optional directories (only when workflow design includes scripts/tests)
    optional_dirs = [
        "scripts",
        "tests",
    ]

    for d in required_dirs:
        (base / d).mkdir(parents=True, exist_ok=True)

    created = list(required_dirs)

    for d in optional_dirs:
        if (base / d).is_dir():
            created.append(d)
        else:
            # Create only if explicitly opted-in via a marker file or arg
            pass

    print(f"Directory skeleton created at: {base}")
    for d in created:
        print(f"  {d}/")

    # If scripts/ already exists or was asked for, create __init__.py
    scripts_dir = base / "scripts"
    if scripts_dir.is_dir():
        (scripts_dir / "__init__.py").touch(exist_ok=True)

    tests_dir = base / "tests"
    if tests_dir.is_dir():
        (tests_dir / "__init__.py").touch(exist_ok=True)


if __name__ == "__main__":
    main()
