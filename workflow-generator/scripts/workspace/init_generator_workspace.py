"""
Initialize generator-context/ with workflow state files.
"""
import sys
from pathlib import Path
from datetime import datetime


WORKFLOW_FILES = {
    "user-dashboard.md": """# User Dashboard

## Current Status
- Phase: intake_idea
- Status: pending

## Completed
(None yet)

## Waiting For
- User to describe their workflow idea

## Missing Information
- Workflow idea description

## Next Action
Describe your workflow idea in natural language.
""",
    "workflow-status.md": f"""# Workflow Status

- phase: intake_idea
- status: pending
- created_at: {datetime.now().isoformat()}
""",
    "progress-log.md": f"""# Progress Log

## {datetime.now().strftime("%Y-%m-%d %H:%M")} — Workspace Initialized
- Created generator-context/workflow/
""",
    "domain-analysis.md": """# Domain Analysis

(Not yet started)
""",
    "interview-answers.yaml": """# Interview Answers
# Filled during Layer 2 interview
layers: {}
""",
    "blocker-report.md": """# Blocker Report

No active blockers.
""",
    "user-decisions.md": """# User Decisions

(No decisions recorded yet)
""",
}


def main():
    target = Path.cwd()
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])

    workflow_dir = target / "generator-context" / "workflow"
    workflow_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in WORKFLOW_FILES.items():
        filepath = workflow_dir / filename
        if not filepath.exists():
            filepath.write_text(content, encoding="utf-8")
            print(f"  Created: {filepath}")

    print(f"\nGenerator workspace initialized at: {workflow_dir}")


if __name__ == "__main__":
    main()
