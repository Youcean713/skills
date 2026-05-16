"""
Generate SKILL.md from interview answers using Jinja2 template.
First-pass template fill; AI polishes afterwards.
"""
import sys
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def load_interview_answers(answers_path: Path) -> dict:
    """Load and parse interview-answers.yaml."""
    with open(answers_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_template_context(answers: dict) -> dict:
    """Transform interview answers into template context."""
    layers = answers.get("layers", {})

    # Extract Layer 1 data
    l1 = layers.get("domain_positioning", {})
    l1_dims = {d["name"]: d.get("value", "") for d in l1.get("dimensions", [])}

    # Extract Layer 2 data
    l2 = layers.get("workflow_structure", {})
    l2_dims = {d["name"]: d.get("value", d.get("items", [])) for d in l2.get("dimensions", [])}

    phases = l2_dims.get("workflow_phases", [])
    deliverables = l2_dims.get("core_deliverables", [])
    quality_gates = l2_dims.get("quality_gates", [])

    # Derive values
    skill_name = l1_dims.get("domain_label", "custom-workflow")
    context_dir = l2_dims.get("context_dir_name", "context")
    output_dir = l2_dims.get("output_dir_name", "output")

    # Build decision tree from phases
    decision_tree = []
    for i, phase in enumerate(phases):
        if i == 0:
            decision_tree.append({
                "order": i + 1,
                "condition": f"If there is no workspace, run `scripts/workspace/init_workspace.py`."
            })
        else:
            prev = phases[i - 1]
            decision_tree.append({
                "order": i + 1,
                "condition": f"If `{prev['name']}` is not complete, do not start `{phase['name']}`."
            })

    # Build hard rules from quality gates
    hard_rules = []
    for gate in quality_gates:
        hard_rules.append(f"Do not claim delivery complete if {gate['description']}.")
    hard_rules.append("Do not silently skip log updates after changing workflow state.")
    hard_rules.append("Do not hide blockers in chat only; write them to blocker-report.md.")
    hard_rules.append("Output filenames must be descriptive, not generic.")

    # Build resource map
    resource_map = [
        {"need": "Intake and workflow start", "location": "`references/workflow/intake.md`"},
        {"need": "Workflow state, blockers", "location": "`references/workflow/workflow-state-management.md`, `references/workflow/stop-and-report.md`"},
    ]
    for phase in phases:
        resource_map.append({
            "need": phase.get("description", phase["name"]),
            "location": f"`references/workflow/{phase['name']}.md`"
        })

    return {
        "skill_name": skill_name,
        "description": f"Use when the user asks to {l1_dims.get('domain_purpose', 'run this workflow')}",
        "title": f"{l1_dims.get('domain_label', 'Workflow').replace('-', ' ').title()} Workbench",
        "evidence_label": "materials",
        "delivery_label": "output",
        "input_summary": ", ".join([m.get("name", "") for m in l2_dims.get("input_materials", [])]),
        "output_action": "producing deliverables",
        "context_dir": context_dir,
        "output_dir": output_dir,
        "governance_items": "workflow state, material inventory, blocker reports, user decisions",
        "delivery_items": ", ".join([d.get("filename", "") for d in deliverables]),
        "phases": phases,
        "decision_tree": decision_tree,
        "hard_rules": hard_rules,
        "resource_map": resource_map,
        "quality_gates": [g["description"] for g in quality_gates],
        "deliverables": [f"`{d['filename']}`" for d in deliverables],
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_skill_md.py <interview-answers.yaml> <output-dir>")
        sys.exit(1)

    answers_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not answers_path.exists():
        print(f"ERROR: {answers_path} not found")
        sys.exit(1)

    answers = load_interview_answers(answers_path)
    context = build_template_context(answers)

    templates_dir = Path(__file__).parent.parent.parent / "assets" / "templates"
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template("skill-md-template.md")

    output = template.render(**context)
    output_path = output_dir / "SKILL.md"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")

    print(f"SKILL.md generated at: {output_path}")
    print("\nReview needed:")
    print("  - Verify all template variables were filled")
    print("  - Check hard rules are domain-specific")
    print("  - Confirm decision tree covers all phases")
    print("  - Polish descriptions to natural language")


if __name__ == "__main__":
    main()
