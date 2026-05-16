"""
为生成的工作流 Skill 包创建目录骨架。
仅创建 Skill 包结构——generator-context/ 由生成器自行管理。
"""
import sys
from pathlib import Path


def main():
    """入口函数：创建生成 Skill 包的目录骨架。"""
    if len(sys.argv) < 2:
        print("用法：python scaffold_directories.py <Skill包目录>")
        sys.exit(1)

    base = Path(sys.argv[1])

    # Skill 包必需目录
    required_dirs = [
        "references/workflow",
        "references/standards",
        "references/evidence",
        "references/writing",
        "references/delivery",
        "assets/templates",
    ]

    # 可选目录（仅在工作流包含脚本/测试时创建）
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

    print(f"目录骨架已创建：{base}")
    for d in created:
        print(f"  {d}/")

    # 如果 scripts/ 存在，创建 __init__.py
    scripts_dir = base / "scripts"
    if scripts_dir.is_dir():
        (scripts_dir / "__init__.py").touch(exist_ok=True)

    tests_dir = base / "tests"
    if tests_dir.is_dir():
        (tests_dir / "__init__.py").touch(exist_ok=True)


if __name__ == "__main__":
    main()
