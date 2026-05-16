# 参考文档生成规则

## 目标

基于资源映射和工作流阶段，为 Skill 生成 `references/` 目录。

## 目录结构

每个生成的工作流都有这些参考子目录：

```
references/
  workflow/       # 摄入、状态管理、阻断、质量门禁
  standards/      # 领域标准和约束
  evidence/       # 证据/数据收集规则
  writing/        # 执行/撰写规则
  delivery/       # 输出交付规则
```

## 标准文件（始终生成）

这些文件从生成器自身的 references 改编而来，填充领域特定内容：

| 文件 | 改编来源 | 定制内容 |
| --- | --- | --- |
| `workflow/intake.md` | 生成器的 `intake.md` | 将"工作流思路"替换为领域特定的材料 |
| `workflow/stop-and-report.md` | 生成器的 `stop-and-report.md` | 将阻断条件替换为领域特定的条件 |
| `workflow/workflow-state-management.md` | 生成器的 `workflow-state-management.md` | 替换阶段词汇、治理目录名 |
| `workflow/quality-gates.md` | 生成器的 `quality-gates.md` | 将门禁替换为领域特定的验证 |

## 领域特定文件（从采访生成）

资源映射中的每个条目生成一个参考文件：

1. **如果需求与证据/数据相关**：创建 `evidence/<topic>.md`
2. **如果需求与标准/约束相关**：创建 `standards/<topic>.md`
3. **如果需求与执行/撰写相关**：创建 `writing/<topic>.md`
4. **如果需求与输出/交付相关**：创建 `delivery/<topic>.md`

## 文件模板

每个参考文件使用此结构（来自 `assets/templates/reference-template.md`）：

```markdown
# {{ reference_title }}

用于 {{ purpose }}。

硬约束：
- 约束 1
- 约束 2

必须确认：
1. 事项 1
2. 事项 2
```

## 生成规则

1. 只为资源映射中有对应条目的文件创建
2. 不创建空文件或占位文件
3. 每个文件至少有一条硬约束和一个必须确认的事项
4. 文件内容必须领域特定，不能是通用的
