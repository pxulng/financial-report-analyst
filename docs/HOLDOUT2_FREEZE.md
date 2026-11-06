# Second holdout: Goldman Sachs, Pfizer, NextEra Energy (frozen before running)

Purpose: test agent v3 (prompt v5, Sonnet 5.5) on three cases the 14 earlier reports cover poorly: an investment bank, a company with no operating income line and no interest line, and a heavily indebted utility whose filing holds two sets of statements (NEE and FPL). The prompt, tools and scorers are not changed after seeing these reports. McDonald's was proposed but its PDF could not be read reliably (OCR loses total lines), so it is not included.

## Files and hashes (data/10k/, sha256)
- GS_10-K_FY2025.md: 92862d96c8ff72c61312022880b8b32ed5b6ab43f0f6d88905fb27615c30db4c
- PFE_10-K_FY2025.md: b67625916a3761fb4f9d8890a637e117bd793efba458c8d83e22350bcb23db3e
- NEE_10-K_FY2025.md: 805d684d71cb5e96d642e0009436e6408d80316eb49802c010477bbca52cbeda (draft marked "confidential draft 2/3/2026" on its first page, as supplied)

## Frozen files (sha256)
- evaluation/key.json: ac335bc74cfd91c64f4e68c2fb0952ecbebf189b694af386e66513be14a01eed (the 14 earlier entries are unchanged; GS, PFE, NEE added)
- evaluation/key_credit.json: 656cd651141d6c1c735e93983c4721afe124ef602ac74ef48d7815409bd156db (earlier entries unchanged)
- evaluation/score.py: 555ff842de9c8cf90ba6ab03713b3c33db713d91f81f100b717766f0e889c28d (only change: items the key marks "excluded" are skipped; earlier scores re-checked and identical)
- evaluation/score_credit.py: 24c5955531ccc71fc6e351a98335f85069fb731bb215835ba1333a14ede84dd8 (unchanged)
- prompts/agent_system_prompt_v5.txt: 76f617ac5d7d657f23d0d62fffe5d8ef9c69954b694013377b8f2953f9529d80 (unchanged)

## Key decisions made before any run
| Company | Choices in the key |
|---|---|
| GS | Treated as a bank like JPM and BAC: operating income, capex, cash, interest expense and the four dependent items are not_applicable. Revenue = Total net revenues 58,283 (prev 53,512). Net income = "Net earnings" 17,176 (before preferred dividends of 876; the line "applicable to common" is 16,300). Debt = unsecured short-term borrowings 70,459 + unsecured long-term borrowings 285,500 = 355,959, excluding deposits, repos and other secured financings (the balance sheet has no plain "short-term borrowings" and "long-term debt" lines, so this is a judgement). Equity 124,972 (includes preferred stock 15,153, as for JPM). |
| PFE | No operating income line and no interest line on the income statement (interest is inside "Other (income)/deductions"): operating income not_applicable, interest expense not_in_report. Net income 7,771 (attributable to Pfizer), diluted EPS 1.36, operating cash flow 11,704, capex 2,629, cash 1,142 (short-term investments excluded), debt 3,154 + 61,641 = 64,795, equity 86,476 (Pfizer shareholders, excluding noncontrolling interests 299). Interest coverage follows the existing precedence (interest expense status first): not_in_report. Known weakness: the agent may say not_applicable (as it did for Nike); that is a status mismatch, not a wrong figure. |
| NEE | Consolidated NEE statements, not FPL's. Revenue 27,412 (prev 24,753), operating income 8,280, net income attributable to NEE 6,835, diluted EPS 3.30, operating cash flow 12,485, cash 2,812, interest expense 4,572 (printed gross line), equity = total common shareholders' equity 54,608 (excluding noncontrolling interests 11,871). Debt = commercial paper 1,955 + other short-term debt 608 + current portion 3,500 + long-term debt 89,556 = 95,619. Capex and free cash flow are excluded from scoring: the cash-flow statement has no single purchases-of-PP&E line (FPL capital expenditures 8,719, independent power investments 15,332, nuclear fuel 553, other 2), so any total is a judgement. |

Guidance question: none of the three reports gives next-year earnings guidance (Pfizer's text mentions "financial guidance" only as a risk reference), so all three keep the guidance question as an absent item.

## Seen before the runs
- I read the three reports' statements (to build the key) and ran the statement tool on PFE and NEE. The tool returns the wrong table for NEE's income statement (an earnings-per-share note); the agent has to find the real statement another way. I did not change the tool.
- Risks: no reference keywords are defined for these three companies, so the keyword proxy for risks is not reported.

## Plan and rules
- Agent v3 (prompt v5, tools v2, Sonnet 5.5, adaptive thinking), one execution per company, no reruns except an infrastructure failure before any model call (declared in the log).
- Descriptive results only: no pass/fail threshold. Every wrong figure is listed with its cause (agent error, key judgement, or tool limit).
- Cost read from the account balance (3.38 USD before the runs).
