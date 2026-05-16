# Script Generation Rules

## Goal

Generate `scripts/` directory with executable Python scripts based on deliverable formats and tool chain requirements.

## Standard Scripts (Always Generated)

| Script | Purpose |
| --- | --- |
| `workspace/init_workspace.py` | Initialize the governance side directory structure |
| `workspace/check_workspace.py` | Validate workspace integrity |

## Domain-Specific Scripts (Generated from Deliverable Formats)

### Format-to-Library Mapping

| Deliverable Format | Python Library | Script Template |
| --- | --- | --- |
| `.xlsx` | `openpyxl` | Data → pandas DataFrame → styled Excel with sheets |
| `.docx` | `python-docx` | Markdown → python-docx with heading/paragraph styles |
| `.json` | `json` (stdlib) | Dict/List → json.dump with indent |
| `.html` | `jinja2` | Data → Jinja2 template → HTML file |
| `.csv` | `csv` (stdlib) | Data → csv.writer |
| `.png`/`.jpg` | `matplotlib` or `Pillow` | Data → chart/image → file |

### Script Naming Convention

`scripts/<domain>/<verb>_<object>.py`

Examples:
- `scripts/coverage/calculate_coverage.py`
- `scripts/evidence/extract_requirements.py`
- `scripts/report/generate_report_xlsx.py`

## Script Skeleton Template

Every generated script must have:

```python
"""
<one-line purpose>
"""
import sys
from pathlib import Path


def main():
    """Entry point."""
    pass


if __name__ == "__main__":
    main()
```

## Generation Rules

1. Scripts must be syntactically valid Python (pass `python -m py_compile`)
2. Each script does ONE thing (single responsibility)
3. Scripts use stdlib + packages from `requirements.txt` only
4. Scripts accept paths as arguments, do not hardcode paths
5. Scripts print progress to stdout, errors to stderr
