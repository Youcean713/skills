# 停止并报告

## 机制定义

`stop_and_report` 是全局阻断机制。在工作流生成的任何阶段，当继续执行需要猜测领域逻辑、编造步骤或生成无法验证的输出时，停止并报告。

报告必须写入 `generator-context/workflow/workflow-status.md` 和 `generator-context/workflow/blocker-report.md`，聊天回复必须总结同样的阻断，不得弱化。

## 阻断类型

| 类型 | 含义 | 处理方式 |
| --- | --- | --- |
| `hard_blocker` | 继续执行需要编造或无法验证的内容 | 停止，直到用户提供信息或变更范围 |
| `limited_continue` | 未受影响的部分可以继续，但某部分必须保持临时状态 | 仅在可见限制下继续 |
| `user_choice_needed` | 两种有效方法或配置存在冲突 | 请用户选择或批准推荐路径 |

## 各阶段阻断条件

| 阶段 | 停止条件 |
| --- | --- |
| `intake_idea` | 用户描述过于模糊，无法推断领域 |
| `domain_analysis` | 领域无法确定，或用户不同意且无替代方案 |
| `gap_interview` | 用户无法回答关键的第二层维度 |
| `design_workflow` | 阶段依赖关系无法解决 |
| `generate_skll_md` | 模板变量缺失或不一致 |
| `generate_references` | 资源映射引用指向不存在的领域 |
| `generate_scripts` | 工具链或交付物格式不受支持 |
| `generate_tests` | 硬规则过于模糊，无法推导测试用例 |
| `quality_gates` | 必需验证失败 |

## 恢复流程

| 新信息 | 返回阶段 |
| --- | --- |
| 用户澄清领域 | `domain_analysis` |
| 用户提供缺失的输入材料 | `design_workflow` |
| 用户更改交付物格式 | `design_workflow` |
| 用户添加质量门禁 | `generate_tests` |

## 聊天回复约定

当被阻断时，报告：

1. 当前阶段和状态
2. 阻断类型
3. 确切缺失的信息或需要做的决策
4. 生成的 Skill 的哪些部分受影响
5. 是否允许有限继续
6. 用户可选择的两个或三个选项
7. 推荐选项及原因
