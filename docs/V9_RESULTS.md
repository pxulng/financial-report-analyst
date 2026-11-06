# Prompt v9: results on the same 7 reports (Boeing, Honeywell, Verizon, Exxon, Home Depot, Walmart, Caterpillar)

v9 = v7 plus three rules decided before this run (see docs/V8_VALIDATION.md and docs/DESIGN.md):
1. Total financial debt is taken from the balance-sheet captions as printed. The agent checks the debt note and states in the note any finance-lease amount included in the captions, but subtracts it only when a caption itself names finance leases.
2. Revenue is the last total-of-revenues line of the income statement (Exxon: "Total revenues and other income").
3. Equity is the printed line; if only one total equity line is printed, it is used and the note says it includes non-controlling interests; the agent must not compute the attributable amount (Verizon).

The key was not changed. Cost about 1 USD (7 runs).

| | v8 | v9 |
|---|---|---|
| Figures read | 56/63 | 62/63 |
| Computed items | 22/28 | 27/28 |
| Absent questions | 20/20 | 20/20 |
| Wrong or invented figures | 13 | 2 |
| Credit ratios right | 16/22 | 21/22 |

Home Depot, Honeywell, Verizon, Exxon, Walmart and Caterpillar: 0 wrong figures, every debt note states what the captions contain (for example Home Depot: "the captions include 2,963 of finance leases", Verizon: equity 105,741 "includes noncontrolling interests of 1,281, the attributable amount was not computed").

Remaining errors (2 figures plus the ratios that depend on them), all Boeing: total financial debt 54,098 against the key's 53,848, and net debt. The agent followed the new rule (captions as printed: 8,461 + 45,637, which include 361 of finance leases, and it says so). The key entry for Boeing was written under the OLD definition ("debt excluding finance lease obligations") on 5 November. It is not changed here so that the test stays fair; it is reported as a known inconsistency of the key. Under the new convention the key value would be 54,098.

Honest limits:
- These 7 reports were also used to find the problem (v8 test), so this score is optimistic. A confirmation on reports the agent has never seen is still needed.
- One run per company; model answers vary a little between runs.
- Risks (keyword proxy) are not a quality measure.

Run files: `evaluation/runs/*_agent_v9_sonnet-5-5_validation7.json`. The workflow uses v9.
