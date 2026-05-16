"""
Validate completeness and integrity of a generated workflow skill package.
"""
import sys
import yaml
import subprocess
from pathlib import Path


REQUIRED_SECTIONS = [
    "Operating Model",
    "Required Workflow",
    "Phase + Status State Model",
    "Decision Tree",
    "Hard Rules",
    "Resource Map",
    "Quality Gates",
    "Delivery Contract",
]

# references/ and assets/templates/ are always required.
# scripts/ and tests/ are conditional — only required when the workflow design needs them.
REQUIRED_DIRS = [
    "references",
    "assets/templates",
]
OPTIONAL_DIRS = [
    "scripts",
    "tests",
]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
]


def check_skill_md_sections(skill_path: Path) -> list[str]:
    """Check SKILL.md has all 8 required sections."""
    errors = []
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return ["SKILL.md not found"]

    content = skill_md.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if f"# {section}" not in content and f"## {section}" not in content:
            errors.append(f"SKILL.md missing section: {section}")
    return errors


def check_frontmatter(skill_path: Path) -> list[str]:
    """Check YAML frontmatter validity."""
    errors = []
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return ["SKILL.md missing YAML frontmatter"]

    parts = content.split("---", 2)
    if len(parts) < 3:
        return ["SKILL.md frontmatter not closed"]

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return [f"SKILL.md frontmatter YAML error: {e}"]

    if "name" not in fm:
        errors.append("SKILL.md frontmatter missing 'name'")
    if "description" not in fm:
        errors.append("SKILL.md frontmatter missing 'description'")
    if fm.get("description", "").startswith("This skill"):
        errors.append("Description should start with 'Use when...', not 'This skill...'")

    total_chars = len(parts[1])
    if total_chars > 1024:
        errors.append(f"Frontmatter too long: {total_chars} > 1024 chars")

    return errors


def check_directory_integrity(skill_path: Path) -> list[str]:
    """Check required directories and files exist."""
    errors = []
    for d in REQUIRED_DIRS:
        if not (skill_path / d).is_dir():
            errors.append(f"Missing directory: {d}/")
    for f in REQUIRED_FILES:
        if not (skill_path / f).is_file():
            errors.append(f"Missing file: {f}")
    return errors


def check_script_syntax(skill_path: Path) -> list[str]:
    """Check all .py files compile."""
    errors = []
    scripts_dir = skill_path / "scripts"
    if not scripts_dir.is_dir():
        return errors
    for py_file in scripts_dir.rglob("*.py"):
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(py_file)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            errors.append(f"Syntax error in {py_file.name}: {result.stderr.strip()}")
    return errors


def main():
    target = Path.cwd()
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])

    if not target.is_dir():
        print(f"ERROR: {target} is not a directory")
        sys.exit(1)

    all_errors = []
    all_errors.extend(check_skill_md_sections(target))
    all_errors.extend(check_frontmatter(target))
    all_errors.extend(check_directory_integrity(target))
    all_errors.extend(check_script_syntax(target))

    # Warn about missing optional directories but don't error
    warnings = []
    for d in OPTIONAL_DIRS:
        if not (target / d).is_dir():
            warnings.append(f"Optional directory not present: {d}/ (only needed if workflow design includes it)")

    if all_errors:
        print(f"FAILED: {len(all_errors)} issue(s) found:")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("PASSED: Generated skill package is valid.")
        print(f"  - All 8 SKILL.md sections present")
        print(f"  - YAML frontmatter valid")
        print(f"  - Directory structure complete")
        if (target / "scripts").is_dir():
            print(f"  - All scripts compile")
        if warnings:
            for w in warnings:
                print(f"  ⚠ {w}")


if __name__ == "__main__":
    main()
