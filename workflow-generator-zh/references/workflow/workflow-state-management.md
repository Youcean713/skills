# 工作流状态管理

## 目标

在 `generator-context/workflow/` 下创建生成器工作台，使智能体可以恢复工作而无需猜测。

## 初始化

运行：

```powershell
python scripts/workspace/init_generator_workspace.py .
```

## 生成的文件

| 文件 | 用途 |
| --- | --- |
| `user-dashboard.md` | 面向用户的进度快照、待决决策、缺失信息和下一步行动 |
| `workflow-status.md` | 当前阶段、下一步行动、总体状态 |
| `progress-log.md` | 按时间顺序的生成会话日志 |
| `domain-analysis.md` | 第一层采访的领域定位结果 |
| `interview-answers.yaml` | 第二层采访的结构化答案 |
| `blocker-report.md` | 最新阻断、影响范围、用户选项、建议 |
| `user-decisions.md` | 影响工作流设计、命名、交付物、质量门禁的用户确认选择 |

## 更新规则

在生成任务开始时：

1. 读取 `workflow-status.md`
2. 读取 `user-dashboard.md`
3. 当状态为 blocked 时读取 `blocker-report.md`
4. 当请求依赖之前的用户选择时读取 `user-decisions.md`

在生成任务结束时：

1. 用用户可见的进度更新 `user-dashboard.md`
2. 当工作被阻断时更新 `blocker-report.md`
3. 当用户批准选择时更新 `user-decisions.md`
4. 向 `progress-log.md` 追加一条记录
5. 更新 `workflow-status.md` 的阶段和状态

## 状态词汇

- `pending`：未开始
- `in_progress`：正在进行中
- `blocked`：无法继续，需要信息或决策
- `needs_review`：已生成但需要用户审查
- `done`：对当前阶段而言已经足够验证
- `deprecated`：不再使用

## 阶段词汇

- `intake_idea`
- `domain_analysis`
- `gap_interview`
- `design_workflow`
- `generate_skll_md`
- `review_skll`
- `generate_references`
- `generate_scripts`
- `generate_assets`
- `generate_tests`
- `generate_readme`
- `quality_gates`
- `delivery_report`
- `archive_generation`

## 合法回退表

| 当前阶段 | 触发事件 | 目标阶段 |
| --- | --- | --- |
| `review_skll` | 用户变更工作流阶段 | `design_workflow` |
| `generate_references` | 用户变更资源映射 | `design_workflow` |
| `generate_scripts` | 用户变更交付物格式 | `design_workflow` |
| `generate_tests` | 用户添加/变更硬规则 | `generate_skll_md` |
| `quality_gates` | 验证失败 | 受影响的生成阶段 |

## 不可协商的规则

不要在更改生成状态后偷偷跳过日志更新。工作台是生成项目的记忆。

## 用户仪表盘规则

保持 `user-dashboard.md` 足够简短，让用户在做决定前可以快速浏览。

它应回答五个问题：

1. 我们在生成过程的什么位置？
2. 已经生成了什么？
3. 用户需要做什么决策？
4. 缺失什么信息，影响什么？
5. 下一步建议是什么？
