"""
验证生成的 Skill 包的完整性和一致性。
"""
import sys
import yaml
import subprocess
from pathlib import Path


REQUIRED_SECTIONS = [
    "运营模型",
    "必需工作流",
    "阶段 + 状态模型",
    "决策树",
    "硬规则",
    "资源映射",
    "质量门禁",
    "交付合约",
]

# references/ 和 assets/templates/ 始终必需。
# scripts/ 和 tests/ 仅在需要脚本或测试时生成。
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
    """检查 SKILL.md 是否包含全部必需部分。"""
    errors = []
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return ["SKILL.md 未找到"]

    content = skill_md.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if f"# {section}" not in content and f"## {section}" not in content:
            errors.append(f"SKILL.md 缺少部分：{section}")
    return errors


def check_frontmatter(skill_path: Path) -> list[str]:
    """检查 YAML 前置元数据有效性。"""
    errors = []
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return ["SKILL.md 缺少 YAML 前置元数据"]

    parts = content.split("---", 2)
    if len(parts) < 3:
        return ["SKILL.md 前置元数据未闭合"]

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return [f"SKILL.md 前置元数据 YAML 错误：{e}"]

    if "name" not in fm:
        errors.append("SKILL.md 前置元数据缺少 'name'")
    if "description" not in fm:
        errors.append("SKILL.md 前置元数据缺少 'description'")

    total_chars = len(parts[1])
    if total_chars > 1024:
        errors.append(f"前置元数据过长：{total_chars} > 1024 字符")

    return errors


def check_directory_integrity(skill_path: Path) -> list[str]:
    """检查必需目录和文件是否存在。"""
    errors = []
    for d in REQUIRED_DIRS:
        if not (skill_path / d).is_dir():
            errors.append(f"缺少目录：{d}/")
    for f in REQUIRED_FILES:
        if not (skill_path / f).is_file():
            errors.append(f"缺少文件：{f}")
    return errors


def check_script_syntax(skill_path: Path) -> list[str]:
    """检查所有 .py 文件能否编译。"""
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
            errors.append(f"语法错误 {py_file.name}：{result.stderr.strip()}")
    return errors


def main():
    """入口函数：验证生成的 Skill 包。"""
    target = Path.cwd()
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])

    if not target.is_dir():
        print(f"错误：{target} 不是目录")
        sys.exit(1)

    all_errors = []
    all_errors.extend(check_skill_md_sections(target))
    all_errors.extend(check_frontmatter(target))
    all_errors.extend(check_directory_integrity(target))
    all_errors.extend(check_script_syntax(target))

    # 缺失可选目录时仅警告，不阻断
    warnings = []
    for d in OPTIONAL_DIRS:
        if not (target / d).is_dir():
            warnings.append(f"可选目录未生成：{d}/（仅在工作流包含脚本/测试时需要）")

    if all_errors:
        print(f"验证失败：发现 {len(all_errors)} 个问题：")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("验证通过：生成的 Skill 包有效。")
        print("  - 全部需要的 SKILL.md 部分已包含")
        print("  - YAML 前置元数据有效")
        print("  - 目录结构完整")
        if (target / "scripts").is_dir():
            print("  - 所有脚本编译通过")
        if warnings:
            for w in warnings:
                print(f"  ⚠ {w}")


if __name__ == "__main__":
    main()
