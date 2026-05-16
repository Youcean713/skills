"""
初始化 generator-context/ 并创建工作流状态文件。
"""
import sys
from pathlib import Path
from datetime import datetime


WORKFLOW_FILES = {
    "user-dashboard.md": """# 用户仪表盘

## 当前状态
- 阶段：intake_idea
- 状态：pending

## 已完成
（暂无）

## 等待中
- 用户描述其工作流思路

## 缺失信息
- 工作流思路描述

## 下一步
用自然语言描述你的工作流思路。
""",
    "workflow-status.md": f"""# 工作流状态

- phase: intake_idea
- status: pending
- created_at: {datetime.now().isoformat()}
""",
    "progress-log.md": f"""# 进度日志

## {datetime.now().strftime("%Y-%m-%d %H:%M")} — 工作区已初始化
- 已创建 generator-context/workflow/
""",
    "domain-analysis.md": """# 领域分析

（尚未开始）
""",
    "interview-answers.yaml": """# 采访答案
# 在第二层采访中填写
layers: {}
""",
    "blocker-report.md": """# 阻断报告

当前没有活动阻断。
""",
    "user-decisions.md": """# 用户决策

（尚未记录任何决策）
""",
}


def main():
    """入口函数：在工作目录下初始化生成器工作台。"""
    target = Path.cwd()
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])

    workflow_dir = target / "generator-context" / "workflow"
    workflow_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in WORKFLOW_FILES.items():
        filepath = workflow_dir / filename
        if not filepath.exists():
            filepath.write_text(content, encoding="utf-8")
            print(f"  已创建：{filepath}")

    print(f"\n生成器工作区已初始化：{workflow_dir}")


if __name__ == "__main__":
    main()
