---
name: {{ skill_name }}
description: {{ description }}
---

# {{ title }}

## 运营模型

以 {{ evidence_label }} 为控制层，以 {{ delivery_label }} 流水线为输出层。将 {{ input_summary }} 视为材料，在 {{ output_action }} 之前必须解析为结构化状态。

工作台有两个侧面：

- 治理侧：`{{ context_dir }}/` 存储工作流状态、{{ governance_items }}。
- 交付侧：`{{ output_dir }}/` 存储 {{ delivery_items }}。
- 用户可见性：`{{ context_dir }}/workflow/user-dashboard.md` 汇总当前进度、缺失材料、需要用户做的决策和下一步建议。`{{ context_dir }}/workflow/content-decisions.md` 记录可选内容的取舍决策。`{{ context_dir }}/workflow/blocker-report.md` 记录最新阻断、选项、建议和有限继续状态。`{{ context_dir }}/workflow/user-decisions.md` 记录用户已批准的选择。

## 必需工作流

按以下顺序运行工作流，除非用户仅要求执行一个狭义任务：

{% for phase in phases %}
{{ phase.order }}. `{{ phase.name }}`：{{ phase.description }}
{% endfor %}

`stop_and_report` 是全局阻断机制，不是单一步骤。每当继续执行可能需要猜测时，阅读 `references/workflow/stop-and-report.md`。

## 阶段 + 状态模型

在 `{{ context_dir }}/workflow/workflow-status.md` 中使用此双层状态模型，并将用户可见摘要镜像到 `{{ context_dir }}/workflow/user-dashboard.md`：

| 字段 | 允许值 |
| --- | --- |
| `phase` | {% for phase in phases %}`{{ phase.name }}`{% if not loop.last %}、{% endif %}{% endfor %} |
| `status` | `pending`（未开始）、`in_progress`（进行中）、`blocked`（已阻断）、`needs_review`（待审查）、`done`（完成）、`deprecated`（已废弃） |

当状态变为 `blocked` 时，在状态文件中写入 `blocked_reason`、`missing_materials`、`next_action` 和 `can_continue_with_limitations`。不要仅在聊天中隐藏阻断。

在任何有意义的阶段、阻断、材料或交付范围变更后，更新 `user-dashboard.md` 以便用户可以看到：

- 当前阶段和状态
- 已完成的工作
- 等待用户确认的决策
- 缺失材料及其影响
- 下一步建议
- 有限继续选项（如有）

## 决策树

{% for decision in decision_tree %}
{{ decision.order }}. {{ decision.condition }}
{% endfor %}

## 硬规则

{% for rule in hard_rules %}
- {{ rule }}
{% endfor %}

## 资源映射

| 需求 | 资源 |
| --- | --- |
{% for resource in resource_map %}
| {{ resource.need }} | {{ resource.location }} |
{% endfor %}

## 质量门禁

在声称交付质量之前，检查：

{% for gate in quality_gates %}
- {{ gate }}
{% endfor %}

## 交付合约

在 `{{ output_dir }}/` 下交付产物：

{% for deliverable in deliverables %}
- {{ deliverable }}
{% endfor %}

报告验证了什么、什么无法验证、什么仍需要人工确认。如果无法运行验证，说明命令和原因。
