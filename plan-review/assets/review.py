#!/usr/bin/env python3
"""
方案互审脚本 — 调用 Claude Code (`claude -p`) 作为独立审查方。
支持多轮迭代：自动追踪轮次、保存历史、后续轮次自动附带上轮反馈。

用法:
    python review.py --file plan.md              # 从文件读取方案
    python review.py --text "方案内容"            # 直接传入文本
    echo "方案内容" | python review.py --stdin    # 从 stdin 读取

    python review.py --file plan.md --workspace .plan-review  # 指定工作目录（默认 .plan-review）
    python review.py --file plan.md --round 2                # 手动指定轮次（默认自动递增）
    python review.py --file plan.md --reset                  # 重置轮次，从第 1 轮开始

依赖: Claude Code CLI (`claude`) 已安装并在 PATH 中。
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WORKSPACE = ".plan-review"
TEMPLATE_PATH = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "references", "review-prompt.md"))


def ensure_workspace(workspace: str) -> str:
    """确保工作目录存在，返回绝对路径。"""
    ws = os.path.abspath(workspace)
    os.makedirs(ws, exist_ok=True)
    return ws


def get_current_round(workspace: str) -> int:
    """读取当前轮次（从 state.json）。"""
    state_file = os.path.join(workspace, "state.json")
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
        return state.get("current_round", 0)
    return 0


def save_state(workspace: str, round_num: int):
    """保存当前轮次到 state.json。"""
    state_file = os.path.join(workspace, "state.json")
    state = {
        "current_round": round_num,
        "updated_at": datetime.now().isoformat(),
    }
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def save_round(workspace: str, round_num: int, plan: str, review: str):
    """保存本轮方案和审查结果。"""
    round_dir = os.path.join(workspace, f"round-{round_num}")
    os.makedirs(round_dir, exist_ok=True)

    with open(os.path.join(round_dir, "plan.md"), "w", encoding="utf-8") as f:
        f.write(plan)

    with open(os.path.join(round_dir, "review.md"), "w", encoding="utf-8") as f:
        f.write(review)

    meta = {
        "round": round_num,
        "timestamp": datetime.now().isoformat(),
        "plan_chars": len(plan),
        "review_chars": len(review),
    }
    with open(os.path.join(round_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def get_previous_review(workspace: str, round_num: int) -> str | None:
    """获取上一轮的审查结果。"""
    if round_num <= 1:
        return None
    prev_review_file = os.path.join(workspace, f"round-{round_num - 1}", "review.md")
    if os.path.exists(prev_review_file):
        with open(prev_review_file, "r", encoding="utf-8") as f:
            return f.read()
    return None


def load_template() -> str:
    """加载审查提示词模板。"""
    if not os.path.exists(TEMPLATE_PATH):
        print(f"[错误] 找不到审查提示词模板: {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(template: str, plan: str, round_num: int, previous_review: str | None) -> str:
    """构建完整的审查提示词。"""
    # 构造"上轮反馈"区块
    if previous_review and round_num > 1:
        previous_review_section = f"""## 上轮审查结果（第 {round_num - 1} 轮）

以下是上一轮的审查反馈，请重点关注其中 🔴 和 ⚠️ 未解决 的问题：

---
{previous_review}
---"""
        iteration_instruction = f"""这是第 {round_num} 轮审查。生成方已根据上轮反馈修订了方案。
请重点检查：
1. 上轮 🔴 必须解决 的问题是否已修复
2. 修订是否引入了新问题
3. 在"上轮反馈跟踪"表格中逐条标注每条上轮反馈的解决状态"""
    else:
        previous_review_section = ""
        iteration_instruction = "这是首次审查，请全面审查方案的完整性、合理性和可行性。"

    # 替换模板中的占位符
    prompt = template.replace("{previous_review_section}", previous_review_section)
    prompt = prompt.replace("{iteration_instruction}", iteration_instruction)

    # 追加待审查方案
    prompt += f"""

---

## 待审查方案（第 {round_num} 轮）

{plan}
"""
    return prompt


def check_claude_cli() -> bool:
    """检查 claude CLI 是否可用。"""
    try:
        subprocess.run(["claude", "--version"], capture_output=True, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return True  # 存在但返回非零，仍可尝试


def call_claude(prompt: str) -> str:
    """调用 claude -p，返回审查结果。"""
    if not check_claude_cli():
        print(
            "[错误] 找不到 claude 命令。请确认 Claude Code CLI 已安装并在 PATH 中。\n"
            "安装方式: npm install -g @anthropic-ai/claude-code",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        result = subprocess.run(
            ["claude", "-p", "--output-format", "text"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        print("[错误] claude -p 调用超时（5 分钟），请检查网络或重试。", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        print(f"[错误] claude -p 返回错误:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    return result.stdout.strip()


def extract_verdict(review: str) -> str:
    """从审查结果中提取最终判断。"""
    if "方案通过，可执行" in review:
        return "PASS"
    if "结构性问题" in review and "重大修订" in review:
        return "MAJOR_REVISION"
    return "IMPROVE"


def main():
    parser = argparse.ArgumentParser(description="方案互审 — 多轮迭代审查")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="方案文件路径")
    group.add_argument("--text", type=str, help="直接传入方案文本")
    group.add_argument("--stdin", action="store_true", help="从 stdin 读取方案")
    parser.add_argument("--workspace", type=str, default=DEFAULT_WORKSPACE,
                        help=f"工作目录（默认: {DEFAULT_WORKSPACE}）")
    parser.add_argument("--round", type=int, default=None, help="手动指定轮次（默认自动递增）")
    parser.add_argument("--reset", action="store_true", help="重置轮次，从第 1 轮开始")
    parser.add_argument("--output", type=str, help="将审查结果额外写入文件")
    parser.add_argument("--verbose", action="store_true", help="显示详细信息")

    args = parser.parse_args()

    # 1. 读取方案
    if args.file:
        if not os.path.exists(args.file):
            print(f"[错误] 方案文件不存在: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            plan = f.read()
    elif args.text:
        plan = args.text
    else:
        plan = sys.stdin.read()

    if not plan.strip():
        print("[错误] 方案内容为空", file=sys.stderr)
        sys.exit(1)

    # 2. 初始化工作目录和轮次
    ws = ensure_workspace(args.workspace)

    if args.reset:
        save_state(ws, 0)

    if args.round is not None:
        round_num = args.round
    else:
        round_num = get_current_round(ws) + 1

    save_state(ws, round_num)

    if args.verbose:
        print(f"[信息] 轮次: {round_num}", file=sys.stderr)
        print(f"[信息] 工作目录: {ws}", file=sys.stderr)
        print(f"[信息] 方案长度: {len(plan)} 字符", file=sys.stderr)

    # 3. 获取上轮反馈
    previous_review = get_previous_review(ws, round_num)
    if previous_review and args.verbose:
        print(f"[信息] 已加载第 {round_num - 1} 轮审查反馈", file=sys.stderr)

    # 4. 构建提示词
    template = load_template()
    prompt = build_prompt(template, plan, round_num, previous_review)

    if args.verbose:
        print(f"[信息] 提示词总长度: {len(prompt)} 字符", file=sys.stderr)
        print("[信息] 正在调用 Claude Code 审查...", file=sys.stderr)

    # 5. 调用审查
    review = call_claude(prompt)

    # 6. 保存结果
    save_round(ws, round_num, plan, review)
    verdict = extract_verdict(review)

    # 7. 输出结果
    header = f"{'='*60}\n📋 方案互审 · 第 {round_num} 轮 · 判定: {verdict}\n{'='*60}\n"

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(header + "\n" + review)
        print(f"[完成] 审查结果已写入: {args.output}", file=sys.stderr)

    # 始终输出到 stdout
    print(header)
    print(review)

    # 8. 输出下一步提示
    if verdict == "PASS":
        print(f"\n✅ 审查通过！共经历 {round_num} 轮审查。")
    elif verdict == "MAJOR_REVISION":
        print(f"\n⚠️ 需要重大修订。请根据上述反馈修改方案后，再次运行 review.py（将自动进入第 {round_num + 1} 轮）。")
    else:
        print(f"\n📝 建议改进。请根据上述反馈修订方案后，再次运行 review.py（将自动进入第 {round_num + 1} 轮）。")

    # 非通过时返回非零退出码，方便脚本判断
    if verdict != "PASS":
        sys.exit(2)


if __name__ == "__main__":
    main()
