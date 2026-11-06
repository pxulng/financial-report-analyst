# Holdout freeze (6 November 2026)

Round 2 of the study (agent v2) was tuned after the round-1 errors were seen on the validation set, so those four companies are no longer a clean holdout. This document fixes a new holdout of four reports **before any model is run on them**. Nothing below changes after a result is seen.

## Companies and how they were chosen
Bank of America (BAC), Verizon (VZ), Caterpillar (CAT), Coca-Cola (KO), all FY2025 10-Ks supplied by the project owner (`data/10k/`). They were **chosen on purpose, not drawn at random** (unlike the first 10), to cover the weak points seen so far: a second bank (JPMorgan was the source of most errors), a heavily indebted group with finance leases (Boeing and Apple errors), an industrial with a finance arm (ambiguous debt), and a plain corporate as a control. This makes the holdout harder than a random draw, which works against the agent if anything.

## Frozen items
| Item | Value |
|---|---|
| Agent prompt | `prompts/agent_system_prompt_v4b.txt`, sha256 `66cae5c5585b3c44b17b20e2e66f1591dcb95b6498041a1c71d8799c94c2086c` |
| Single prompt | `prompts/reference2_system_prompt.txt`, sha256 `7a7d5b55b2e176876161343dfb1b540c1a7c637be708c8e41f8554b280a8971d` |
| Tool code | `workflow/report_tools_v2.js`, sha256 `807f0236426767574afc88962c786687ef5f68e791a3ce6500959ca61a2a08a6` (the only change allowed: adding the four tickers to the file list of the sub-workflow) |
| Key | `evaluation/key.json`, sha256 `486bd16c85d48da56292e356ef4e93808a237d7f21bf7d2bea353f44bca4386c`; entries for the other ten companies are unchanged |
| Scorer | `evaluation/score.py` (one addition, below) |
| Models, settings | claude-haiku-5-5 (thinking disabled) and claude-sonnet-5-5 (thinking adaptive); agent step limit 15; one company per execution |
| Run | each method/model pair once per company |
| Decision rule | `docs/DESIGN.md` section 7: fewer wrong figures first, then accuracy, then cost, same model |

Report hashes: BAC `f9ef8e91ee6404145488b6b21839264448790adf409af04bcad2b69dd5111757`, VZ `e33fc69d5adab2345d7ee2c73f8a40b6fe9455ff4afe736b00e5cb75905c93e3`, CAT `80441fcb25e60a20842388fae6ab7ca1ea94557b32fbf4fbe5e03eb4cc54e1fc`, KO `845d255e739b40c9fe6f6aaf1414c274f5110593505d8ed669cca6d3ec34e854`.

## Key conventions decided before running (with the ambiguities)
- **Banks (BAC):** same treatment as JPMorgan: operating income, capex, cash, operating margin, free cash flow and net debt are not applicable; revenue is "Total revenue, net of interest expense"; debt is short-term borrowings plus long-term debt.
- **Equity:** the parent's share when the report prints it (KO: 32,169; CAT has no noncontrolling interest at year end: 21,318). Verizon's balance sheet prints only "Total equity" 105,741 (it includes 1,281 of noncontrolling interests), so that is the key value; an answer of 104,460 would be marked wrong, which is a known weakness of the key.
- **Net income and EPS:** attributable to the parent (VZ 17,174; KO 13,107; CAT 8,884).
- **Debt:** the sum of the balance-sheet debt captions, finance leases left as the caption has them. CAT: short-term borrowings 5,514 plus long-term debt due within one year 35 and 7,085 plus long-term debt after one year 10,678 and 20,018 (Machinery, Power & Energy and Financial Products), 43,330. Verizon 158,150. KO 45,492. BAC 365,904.
- **CAT capex:** "Capital expenditures – excluding equipment leased to others" 2,821. A second line, "Expenditures for equipment leased to others" 1,465, could also be counted by an analyst; only 2,821 is accepted.
- **CAT guidance:** Caterpillar publishes its 2026 expectations (sales growth around the top end of 5 to 7 percent, capex around 3.5 billion), so the guidance question is not an absent item for it. `score.py` drops that question from the absent count for CAT only (no credit, no penalty). For the other three it stays an absent item, as for JPMorgan before.
- Segments are not scored for these four.

## Run plan and budget
Balance before the holdout: 3.81 USD. Order, cheapest first: agent Haiku, agent Sonnet, single prompt Haiku, single prompt Sonnet. Expected cost: agent Haiku about 0.05, agent Sonnet about 0.5, single prompt Haiku about 0.7, single prompt Sonnet about 2.7 (the four reports are 3.7 MB, against 3.1 MB for the validation set at 2.30 USD). The last run is only launched after the owner confirms the balance.

## What can still change
Nothing in the prompts, tools or key. Any error found afterwards is logged and reported, not fixed in this round.
