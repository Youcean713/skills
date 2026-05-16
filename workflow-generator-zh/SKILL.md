---
name: workflow-generator-zh
description: >
  当用户想要将思路、概念或工作流需求转化为完整的产品级工作流 Skill 包时使用。
  触发词包括："把这个变成工作流"、"为X创建一个工作流"、"我有一个工作流的想法"、
  "构建一个工作台"、"根据这个思路生成Skill"、或将任何流程系统化为具备治理侧
  和交付侧的结构化工作台的请求。
---

# 工作流生成器

## 运营模型

以三层采访为发现层，以模板驱动生成为输出层。将用户的自然语言思路视为初始材料，必须先细化为结构化参数，然后才能生成任何代码。

生成器有两个侧面：

- 治理侧：`generator-context/` 存储采访状态、领域分析、工作流设计、阻断报告和用户决策。
- 交付侧：`<workflow-name>/` 存储生成的 Skill 包 —— SKILL.md、references/、scripts/、assets/、tests/ 和 README.md。
- 用户可见性：`generator-context/workflow/user-dashboard.md` 汇总当前进度、待决事项、缺失信息和下一步建议。`generator-context/workflow/blocker-report.md` 记录最新阻断、选项、建议和有限继续状态。`generator-context/workflow/user-decisions.md` 记录用户已确认的工作流设计选择。

## 必需工作流

按以下顺序运行工作流：

1. `intake_idea`：收集用户的自然语言思路描述。
2. `domain_analysis`：分析领域特征——输入、输出、步骤、约束、工具。将领域推断呈现给用户确认。
3. `gap_interview`：执行三层采访（领域定位 → 工作流结构 → 细节填充）。AI 建议，用户选择。
4. `design_workflow`：设计工作流骨架——阶段序列、决策树、硬规则、资源映射。
5. `generate_skll_md`：从采访答案生成核心 SKILL.md。**硬阻断点——用户必须在继续之前确认。**
6. `review_skll`：用户审查并调整 SKILL.md。
7. `generate_references`：基于资源映射生成 references/ 参考文档框架。
8. `generate_scripts`：基于交付物格式和工具链生成 scripts/ 关键脚本。
9. `generate_assets`：生成 assets/ 模板和配置。
10. `generate_tests`：从硬规则和质量门禁生成 tests/ 合约测试。
11. `generate_readme`：生成 README.md 使用文档。
12. `quality_gates`：运行 check_generated_skill.py 验证完整性、一致性和语法。
13. `delivery_report`：报告产出、限制、剩余人工决策和验证证据。
14. `archive_generation`：归档生成记录到 generator-context/。

`stop_and_report` 是全局阻断机制，不是单一步骤。每当继续执行可能需要猜测时，阅读 `references/workflow/stop-and-report.md`。

## 阶段 + 状态模型

在 `generator-context/workflow/workflow-status.md` 中使用此双层状态模型，并将用户可见摘要镜像到 `generator-context/workflow/user-dashboard.md`：

| 字段 | 允许值 |
| --- | --- |
| `phase` | `intake_idea`、`domain_analysis`、`gap_interview`、`design_workflow`、`generate_skll_md`、`review_skll`、`generate_references`、`generate_scripts`、`generate_assets`、`generate_tests`、`generate_readme`、`quality_gates`、`delivery_report`、`archive_generation` |
| `status` | `pending`、`in_progress`、`blocked`、`needs_review`、`done`、`deprecated` |

当状态变为 `blocked` 时，在状态文件中写入 `blocked_reason`、`missing_information`、`next_action` 和 `can_continue_with_limitations`。不要仅在聊天中隐藏阻断。

在任何有意义的阶段、阻断、决策或交付范围变更后，更新 `user-dashboard.md` 以便用户可以看到：

- 当前阶段和状态
- 已完成的工作
- 等待用户确认的决策
- 缺失信息及其影响
- 下一步建议
- 有限继续选项（如有）

## 决策树

1. 如果没有 `generator-context/`，运行 `scripts/workspace/init_generator_workspace.py`。
2. 如果用户的思路描述过于模糊（缺少领域、输入、输出中至少两项），先做第一层采访。
3. 如果第一层领域未确认，不要开始第二层工作流结构采访。
4. 如果第二层采访答案不完整，不要开始 SKILL.md 生成。
5. 如果 `interview-answers.yaml` 未确认，不要生成 SKILL.md。
6. 如果 SKILL.md 未经用户批准，不要生成 references/、scripts/ 或 tests/。
7. 如果资源映射引用不存在的领域，停止并重新设计工作流。
8. 如果在未确认交付物格式的情况下被要求生成脚本，停止并返回到 `design_workflow`。
9. 如果质量门禁失败，返回到受影响的生成阶段。
10. 如果被要求最终交付，先运行质量门禁并生成交付报告。

## 硬规则

- AI 始终先建议，用户确认或修改。绝不呈现空白表单。
- 在三层采访完成或用户明确确认没有更多问题之前，不要生成 SKILL.md。
- 在摄入阶段，将每个输入材料分类为 `required`、`strongly_recommended` 或 `optional`，并解释缺失每个必需或强烈推荐材料的影响。
- 将用户确认的决策记录在 `user-decisions.md` 中。
- 用户可见的工作流文件仅为决策辅助。它们不得弱化质量门禁或交付检查。
- 在领域分析和采访完成之前不要生成工作流文件。
- 信息不足时，触发 `stop_and_report`；不要猜测用户意图。
- 当被阻断时，将问题分类为 `hard_blocker`、`limited_continue` 或 `user_choice_needed`，然后提供用户选项和推荐路径。
- `interview-answers.yaml` 是工作流生成参数的唯一入口。
- `SKILL.md` 生成是硬阻断点——必须在继续任何进一步生成之前得到用户确认。
- 不要发明用户未描述或批准的功能、步骤、工具或约束。
- 所有生成的文件路径必须使用正斜杠，并相对于 Skill 包根目录。
- 输出文件名必须具有描述性，不能是通用的（`需求覆盖率报告.xlsx` 而非 `report.xlsx`）。
- 如果生成的包中包含 Python 脚本，在声称完成之前必须通过 `python -m py_compile`。

## 资源映射

| 需求 | 资源 |
| --- | --- |
| 摄入和思路收集 | `references/workflow/intake.md` |
| 三层采访 | `references/workflow/interview-engine.md` |
| 阻断和停止/报告 | `references/workflow/stop-and-report.md` |
| 生成状态管理 | `references/workflow/workflow-state-management.md` |
| 交付前验证 | `references/workflow/quality-gates.md` |
| SKILL.md 生成规则 | `references/generation/skill-template.md` |
| 参考文档生成 | `references/generation/reference-generation.md` |
| 脚本生成 | `references/generation/script-generation.md` |
| 测试生成 | `references/generation/test-generation.md` |
| 工作区初始化 | `scripts/workspace/init_generator_workspace.py` |
| Skill 验证 | `scripts/workspace/check_generated_skill.py` |
| SKILL.md 生成工具 | `scripts/generation/generate_skill_md.py` |
| 目录骨架生成 | `scripts/generation/scaffold_directories.py` |
| SKILL.md 模板 | `assets/templates/skill-md-template.md` |
| 采访 schema | `assets/templates/interview-schema.yaml` |
| README 模板 | `assets/templates/readme-template.md` |
| 参考文档模板 | `assets/templates/reference-template.md` |

## 质量门禁

在声称交付质量之前，检查：

- `interview-answers.yaml` 已填写所有第二层维度并已确认。
- SKILL.md 具备全部 8 个必需部分，且内容领域特定。
- YAML 前置元数据有效：`name` 使用连字符，`description` 以"当……时使用"开头，总计不超过 1024 字符。
- 每个资源映射条目指向 `references/`、`scripts/` 或 `assets/` 中的现有文件。
- 每条硬规则至少由一个质量门禁或阻断条件支撑。
- 生成的包包含必需目录：`references/`、`assets/templates/`；`scripts/` 和 `tests/` 仅在工作流设计需要时生成。
- 如果 `scripts/` 包含 `.py` 文件，则必须通过 `python -m py_compile`。
- 如果 `tests/` 存在，则必须通过 `python -m pytest`。
- README.md 存在，包含快速开始、架构和验证部分。
- `user-dashboard.md` 反映当前阶段、待决决策和下一步行动。
- 如果状态为 blocked，`blocker-report.md` 反映最新的阻断。

## 交付合约

在用户项目目录下交付生成的 Skill 包：

- `<workflow-name>/SKILL.md`
- `<workflow-name>/README.md`
- `<workflow-name>/requirements.txt`
- `<workflow-name>/references/workflow/`
- `<workflow-name>/references/standards/`
- `<workflow-name>/references/evidence/`
- `<workflow-name>/references/writing/`
- `<workflow-name>/references/delivery/`
- `<workflow-name>/scripts/`（如工作流设计包含脚本）
- `<workflow-name>/assets/templates/`
- `<workflow-name>/tests/`（如工作流设计包含测试）

同时在 `generator-context/` 下交付生成记录：

- `generator-context/workflow/user-dashboard.md`
- `generator-context/workflow/workflow-status.md`
- `generator-context/workflow/domain-analysis.md`
- `generator-context/workflow/interview-answers.yaml`
- `generator-context/workflow/blocker-report.md`
- `generator-context/workflow/user-decisions.md`
- `generator-context/workflow/progress-log.md`

报告生成了什么、验证了什么、什么无法验证、什么仍需要人工确认。如果无法运行验证，说明命令和原因。
