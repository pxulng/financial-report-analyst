# Second holdout results: Goldman Sachs, Pfizer, NextEra Energy

Freeze (reports, key, decisions, hashes): [HOLDOUT2_FREEZE.md](HOLDOUT2_FREEZE.md). Agent v3 (prompt v5, tools v2, Sonnet 5.5, adaptive thinking), one execution per company (n8n executions 981, 989, 997), no reruns. Run files: `evaluation/runs/{GS,PFE,NEE}_agent_v5_sonnet-5-5_holdout2.json`.

## Results
| Set of items | Result |
|---|---|
| Original items (10 figures and 4 computed, per company) | 0 wrong or invented. Read 26/26, computed 11/11, absent questions 9/9 (NEE capex and free cash flow excluded from scoring by the frozen key) |
| New credit items (12 scored) | 8 right, 3 wrong or invented, 1 status mismatch |

| Company | Original items | Credit items | Notes |
|---|---|---|---|
| GS | 9/9 read, 4/4 computed, 0 wrong | 3/4, 1 wrong | Debt to equity returned as 2.85 for a bank; the rule says not_applicable |
| PFE | 9/9, 4/4, 0 wrong | 3/4, 0 wrong | Interest coverage status not_applicable instead of not_in_report (the weakness declared in the freeze) |
| NEE | 8/8, 3/3, 0 wrong | 2/4, 2 wrong | Interest expense 4,305 against the printed 4,572; coverage 1.92 against 1.81 as a result |

## Causes of the errors
- **NEE interest expense (agent error with a tool cause).** `read_statement("income")` returned an earnings-per-share note instead of the income statement (the statement finder picks the wrong table in this combined NEE and FPL filing). The agent then did not find the printed "Interest expense (4,572)" line by search and, instead of leaving the value empty, derived 4,305 by subtraction from the other income lines. It said so in the note and in "limits" and asked the analyst to verify, but it still put a number in the value field, which breaks the rule "never invent or estimate a figure". Interest coverage follows from it. Capex (summed from three lines, 24,053) and free cash flow were also judgements, but they are excluded from scoring and were flagged in the notes.
- **GS debt to equity (agent error).** The agent applied the bank rule to operating income, capex, cash, interest and cfo_to_debt but computed debt to equity. The prompt definition says "or for a bank: not_applicable"; the agent did not follow it. This is the same kind of slip as Sonnet's earlier ratio mistakes: a rule given in one place and not applied in a computed item.
- **PFE interest coverage (key weakness, not a wrong figure).** Pfizer has no operating income line and no interest line. The frozen key gives not_in_report (interest status first); the agent said not_applicable (operating income status first). Both are defensible. Same case as Nike in the first round.

## What worked
- Bank handling of the original items on a third bank type: all GS figures right, including the unsecured borrowings sum (the key's judgement call) and net earnings before preferred dividends.
- Pfizer's missing operating income and interest lines were reported as missing, not invented.
- NEE: the agent found the consolidated NEE figures (not FPL's) for revenue, operating income, net income, cash, debt and equity, even though the income statement tool returned the wrong table, and it listed every shortcut in "limits".

## What it means
- On the figures an analyst reads first (revenue, income, cash flow, debt, equity) the agent made no error on these three harder reports.
- The new credit ratios are where the errors are: 3 of 12 wrong here against 1 of 28 on the first eight companies. Taken together (40 credit items on 11 companies), 4 are wrong. The two sets are small and not comparable (this one was chosen to be hard), so the honest summary is: ratios are reliable on ordinary industrial companies, and fail on banks (a rule not applied) and on filings where the tool cannot find the statement.
- The notes and "limits" fields carried each uncertainty (derived interest, summed capex, debt judgement), so a reviewing analyst would have seen them. This supports the claim "aid with human review", not "autonomous".

## Not done (would need a new, untouched set to test)
- Fix the statement finder for combined filings (NEE) and add a rule "if a line cannot be found, leave the value empty; never derive it by subtraction".
- Restate the bank rule once for all computed items.
Both are plausible one-line changes, but any change made now would be tuned on these three reports and could not be scored on them cleanly.

## Cost
Balance went from 3.38 to 2.56 USD for the three runs: 0.82 USD, about 0.27 USD per report (more than the 0.11 USD average of the first eleven because these filings are larger and NEE needed 21 tool calls; still under the 0.3 USD ceiling).
