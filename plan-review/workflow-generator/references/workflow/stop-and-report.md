# Stop And Report

## Mechanism Definition

`stop_and_report` is a global blocking mechanism. At any phase of workflow generation, stop and report when continuing would require guessing domain logic, inventing steps, or producing unverifiable output.

The report must be written into `generator-context/workflow/workflow-status.md` and `generator-context/workflow/blocker-report.md`, and the chat response must summarize the same blocker without weakening it.

## Blocker Type

| Type | Meaning | Handling |
| --- | --- | --- |
| `hard_blocker` | Continuing would require invented or unverifiable content | Stop until the user provides information or changes scope |
| `limited_continue` | Unaffected parts can continue, but a section must stay provisional | Continue only with visible limitations |
| `user_choice_needed` | Two valid approaches or configurations conflict | Ask the user to choose or approve the recommended path |

## Blocking Conditions By Phase

| Phase | Stop when |
| --- | --- |
| `intake_idea` | User description too vague to infer domain |
| `domain_analysis` | Domain cannot be determined or user disagrees without alternative |
| `gap_interview` | User cannot answer critical Layer 2 dimensions |
| `design_workflow` | Phase dependencies cannot be resolved |
| `generate_skll_md` | Template variables are missing or inconsistent |
| `generate_references` | Resource map references point to non-existent domains |
| `generate_scripts` | Tool chain or deliverable format is unsupported |
| `generate_tests` | Hard rules are too vague to derive test cases |
| `quality_gates` | A required verification fails |

## Recovery Flow

| New information | Return phase |
| --- | --- |
| User clarifies domain | `domain_analysis` |
| User provides missing input materials | `design_workflow` |
| User changes deliverable format | `design_workflow` |
| User adds quality gate | `generate_tests` |

## Chat Response Contract

When blocked, report:

1. Current phase and status
2. The blocker type
3. The exact missing information or decision
4. Which parts of the generated skill are affected
5. Whether limited continuation is allowed
6. Two or three options the user can choose from
7. The recommended option and reason
