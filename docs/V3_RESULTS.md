# Agent v3 (prompt v5): credit ratios

Design, freeze and success criteria: [V3_DESIGN.md](V3_DESIGN.md). Prompt: `prompts/agent_system_prompt_v5.txt`. Scoring: `evaluation/score.py` (original items) and `evaluation/score_credit.py` (new items, key in `evaluation/key_credit.json`).

## What changed
The agent now also reports gross interest expense and three credit ratios: interest coverage (operating income / interest expense), debt to equity and operating cash flow to debt. The rules decide the status before any number is given: a bank gets not_applicable; a company that prints only a net interest line (or none) gets not_in_report; negative equity makes debt to equity not_applicable. The tools, the sub-workflow and the other prompt rules are unchanged.

## Test on Haiku (3 companies, reduced from 6 to save budget)
BA, SBUX, AAPL: 11 of 12 new items right, 1 wrong (BA debt to equity, caused by the known Boeing finance-lease error in total debt). SBUX returned debt to equity as not_applicable (negative equity) and AAPL returned interest expense and coverage as not_in_report, as designed. No prompt change was made after seeing this.

## Final runs on Sonnet 5.5 (adaptive thinking), one execution per company
| Set | Companies | Original items: wrong or invented | New items: right / scored | New items wrong |
|---|---|---|---|---|
| Validation | MSFT, WMT, NKE, JPM | 0 (36/36 read, 16/16 computed) | 13 / 14 | 0 |
| Holdout | BAC, VZ, CAT, KO | 3 (34/36 read, 15/16 computed) | 13 / 14 | 1 |
| Total | 8 | 3 | 26 / 28 (93 %) | 1 |

Errors:
- VZ total debt, equity and net debt: the same three as v4b, caused by ambiguities in the frozen key (finance leases in debt; equity with or without noncontrolling interests). Not new.
- VZ debt to equity: follows from those two inputs (1.490 against the key 1.4956).
- NKE interest coverage: the agent said not_applicable (no operating income line), the key says not_in_report. No wrong figure, counted as not right.

## Against the success criteria
1. No regression on the original items: met (validation 0, holdout 3, the same three Verizon items).
2. At least 80 % of the 28 new items right and at most 2 wrong: met (26 right, 1 wrong).
3. Cost per report no more than 0.3 USD: met. The balance went from 4.62 to 3.38 USD (1.24 USD) over the 3 Haiku tests and the 8 Sonnet runs, so at most about 0.11 USD per report on average, and the Sonnet reports are below 0.16 USD each. The agent shows no token counts, so this is read from the balance.

## Caveats
- Hand-saved run files keep figures, statuses and computed values as returned; free text is shortened.
- The key for the new items was frozen before the runs, but interest expense for CAT and WMT is excluded from scoring because the income statement prints components rather than one line (the agent chose not_in_report for WMT and the sum 1,861 for CAT; both are reasonable and are flagged to the analyst in the notes).
- Haiku AAPL put one sentence before the JSON (valid only after extraction); Sonnet runs were all valid JSON.
- Eight Sonnet companies and three Haiku companies is a small sample; the ratios are simple arithmetic on figures the agent already reads, so the main risk is picking the wrong input (debt, equity), which the notes expose for the analyst to check.
