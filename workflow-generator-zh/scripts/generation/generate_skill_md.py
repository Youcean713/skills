"""
从采访答案使用 Jinja2 模板生成 SKILL.md。
第一轮模板填充；之后由 AI 润色。
"""
import sys
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def load_interview_answers(answers_path: Path) -> dict:
    """加载并解析 interview-answers.yaml。"""
    with open(answers_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_template_context(answers: dict) -> dict:
    """将采访答案转换为模板上下文。"""
    layers = answers.get("layers", {})

    # 提取第一层数据
    l1 = layers.get("domain_positioning", {})
    l1_dims = {d["name"]: d.get("value", "") for d in l1.get("dimensions", [])}

    # 提取第二层数据
    l2 = layers.get("workflow_structure", {})
    l2_dims = {d["name"]: d.get("value", d.get("items", [])) for d in l2.get("dimensions", [])}

    phases = l2_dims.get("workflow_phases", [])
    deliverables = l2_dims.get("core_deliverables", [])
    quality_gates = l2_dims.get("quality_gates", [])

    # 推导值
    skill_name = l1_dims.get("domain_label", "custom-workflow")
    context_dir = l2_dims.get("context_dir_name", "context")
    output_dir = l2_dims.get("output_dir_name", "output")

    # 从阶段推导决策树
    decision_tree = []
    for i, phase in enumerate(phases):
        if i == 0:
            decision_tree.append({
                "order": i + 1,
                "condition": "如果工作区不存在，运行 `scripts/workspace/init_workspace.py`。"
            })
        else:
            prev = phases[i - 1]
            decision_tree.append({
                "order": i + 1,
                "condition": f"如果 `{prev['name']}` 未完成，不要开始 `{phase['name']}`。"
            })

    # 从质量门禁构建硬规则
    hard_rules = []
    for gate in quality_gates:
        hard_rules.append(f"如果 {gate['description']}，不要声称交付完成。")
    hard_rules.append("在更改工作流状态后不要偷偷跳过日志更新。")
    hard_rules.append("不要仅在聊天中隐藏阻断；将其写入 blocker-report.md。")
    hard_rules.append("输出文件名必须具有描述性，不能是通用的。")

    # 构建资源映射
    resource_map = [
        {"need": "摄入和工作流启动", "location": "`references/workflow/intake.md`"},
        {"need": "工作流状态、阻断", "location": "`references/workflow/workflow-state-management.md`、`references/workflow/stop-and-report.md`"},
    ]
    for phase in phases:
        resource_map.append({
            "need": phase.get("description", phase["name"]),
            "location": f"`references/workflow/{phase['name']}.md`"
        })

    return {
        "skill_name": skill_name,
        "description": f"当用户要求 {l1_dims.get('domain_purpose', '运行此工作流')} 时使用",
        "title": f"{l1_dims.get('domain_label', 'Workflow').replace('-', ' ').title()} 工作台",
        "evidence_label": "材料",
        "delivery_label": "输出",
        "input_summary": "、".join([m.get("name", "") for m in l2_dims.get("input_materials", [])]),
        "output_action": "产出交付物",
        "context_dir": context_dir,
        "output_dir": output_dir,
        "governance_items": "工作流状态、材料清单、阻断报告、用户决策",
        "delivery_items": "、".join([d.get("filename", "") for d in deliverables]),
        "phases": phases,
        "decision_tree": decision_tree,
        "hard_rules": hard_rules,
        "resource_map": resource_map,
        "quality_gates": [g["description"] for g in quality_gates],
        "deliverables": [f"`{d['filename']}`" for d in deliverables],
    }


def main():
    """入口函数：从采访答案生成 SKILL.md。"""
    if len(sys.argv) < 3:
        print("用法：python generate_skill_md.py <interview-answers.yaml> <输出目录>")
        sys.exit(1)

    answers_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not answers_path.exists():
        print(f"错误：{answers_path} 未找到")
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

    print(f"SKILL.md 已生成：{output_path}")
    print("\n需要审查：")
    print("  - 验证所有模板变量是否已填充")
    print("  - 检查硬规则是否为领域特定")
    print("  - 确认决策树覆盖了所有阶段")
    print("  - 润色描述为自然语言")


if __name__ == "__main__":
    main()
