# McDonald's (MCD) test: results

Agent v3 (prompt v5, Sonnet 5.5), one run (execution 1011), 13 tool calls, key frozen beforehand (`docs/MCD_FREEZE.md`).

| Check | Result |
|---|---|
| Original items read | 9/9 right |
| Original computed items | 4/4 right |
| Wrong or invented figures | 0 |
| Credit items (interest expense, debt/equity, CFO/debt, coverage) | 4/4 right |

The case tested the negative-equity rule: the agent returned `not_applicable` for debt_to_equity (equity of -1,791) and still gave CFO/debt (0.264) and interest coverage (7.83). It used the long-term debt line only and said so in the note. It took the three risks from search snippets because `read_section` did not find the risk factors section, and said this in its limits (the risk-factor lookup is a known weak spot, not scored here).

Limit: one company, so it confirms the rule works; it does not change the earlier totals. The run file is `evaluation/runs/MCD_agent_v5_sonnet-5-5_holdout3.json` (free text shortened, figures as returned).
