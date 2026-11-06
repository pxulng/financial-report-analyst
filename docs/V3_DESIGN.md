# Agent v3 (prompt v5): credit ratios. Design and freeze, 6 November 2026

Goal: add what a credit or equity analyst reads first after the figures: interest burden and leverage. The agent keeps its tools; only the prompt and the fact sheet change.

## New items (definitions are in `prompts/agent_system_prompt_v5.txt`)
| Item | Rule |
|---|---|
| interest_expense | The gross interest expense line printed on the consolidated income statement. A net-only line or none gives not_in_report (the notes are not used). Banks: not_applicable. |
| interest_coverage | operating_income / interest_expense, in times. Takes the status of its inputs. |
| debt_to_equity | total_financial_debt / shareholders_equity. Not applicable if equity is zero or negative, and for banks. |
| cfo_to_debt | operating_cash_flow / total_financial_debt. Not applicable for banks. |

The key is `evaluation/key_credit.json`, built by `evaluation/build_key_credit.py` from `key.json` plus the interest lines found in the statements. Scored by `evaluation/score_credit.py`, separately from `score.py` (so earlier scores stay reproducible). Known limits of the key, fixed before running:
- Walmart prints interest as components (debt, finance lease, income, net), and Caterpillar splits interest between Financial Products and the rest: both are **excluded** from the interest items (not scored).
- Apple, Microsoft and Nike print no gross interest line on the income statement, so the key is not_in_report for them even though the notes give a figure. This tests whether the agent obeys the rule; an analyst may find the rule too strict.
- JNJ and XOM publish no operating income, so their interest coverage is not_applicable.
- 28 items are scored on the validation and holdout companies (MSFT 4, WMT 2, NKE 4, JPM 4, BAC 4, VZ 4, CAT 2, KO 4).

## Frozen items
| Item | Value |
|---|---|
| Agent prompt | `prompts/agent_system_prompt_v5.txt` (v4b plus the four definitions and the new lists of 10 figures and 7 computed items). One allowed correction after the test set, declared in LOG.md. |
| Tools | unchanged (`workflow/report_tools_v2.js`) |
| Models, settings | Haiku 5.5 thinking disabled for the test set; Sonnet 5.5 adaptive for the final runs; step limit 15; one company per execution |
| Test set (debugging) | AAPL, JNJ, XOM, BA, SBUX, TSLA on Haiku, about 0.1 USD |
| Final runs | Sonnet on MSFT, WMT, NKE, JPM (validation) and BAC, VZ, CAT, KO (holdout), about 0.2 USD each |
| Budget | about 2.2 USD of the 4.62 USD balance; stop and report if the balance falls below 1.5 USD |

## Success criteria (decided now)
1. No regression: on the original items, the Sonnet v5 agent makes no more wrong figures than v4b on the same companies (validation 0, holdout 3, the three being Verizon's key ambiguities).
2. New items: at least 80 % of the 28 scored items right and at most 2 wrong or invented.
3. Cost per report no more than 0.3 USD.
Not claimed: the validation companies were seen by the earlier prompt versions; only the new items are new. The holdout companies were not used to tune v5, so they are the cleaner check of the new items.
