# Validation of prompt v8 on 7 reports with finance leases: v8 is NOT adopted

Test: v8 (always check the debt note) run on Boeing, Honeywell, Verizon, Exxon, Home Depot, Walmart and Caterpillar, one agent run per company, through the comparison workflow. Cost about 1 USD. Scored against the frozen key (`evaluation/key.json`, `key_credit.json`), nothing changed in the key.

Result: read 56/63 (88.9%), computed 22/28 (78.6%), absent 20/20, 13 wrong figures. Walmart and Caterpillar: 0 wrong.

Where the errors come from:
- **New with v8 (debt):** Home Depot (52,809 vs key 55,772), Honeywell (34,516 vs 34,580), Boeing (53,737 vs 53,848) and the net_debt, debt_to_equity and cfo_to_debt computed from them. The wider v8 sentence ("if the balance-sheet debt captions include finance leases, take the borrowings alone") makes the agent subtract finance leases that sit inside captions which do not name them. The key follows the balance-sheet captions as printed (only a caption that names finance leases, such as "Debt and finance leases", is adjusted). Home Depot had 0 wrong with v6, so this is a regression.
- **Already present before v8 (not caused by it):** Verizon debt 155,639 vs 158,150 and equity 104,460 vs 105,741 (same three errors with v5; the agent uses equity attributable to the company, the key uses "Total equity"); Exxon revenue 323,905 (Sales and other operating revenue) vs key 332,238 (Total revenues and other income). These are definition mismatches between agent and key that were never resolved.

Decision (rule in docs/DESIGN.md section 7: fewer wrong figures first): v8 is rejected, the workflow goes back to v7. The key was not changed to fit the result.

Open points:
1. The written definition ("without lease liabilities") and the key convention (printed captions) disagree for companies whose debt captions contain finance leases. One of the two has to be chosen and documented before a new test; changing the key after seeing results would not be a fair test.
2. A possible v8b keeps the v7 rule but asks the agent to read the debt note, report the finance-lease amount in the note and not subtract it unless the caption names finance leases. Not tested.
3. Verizon equity and Exxon revenue need a decision on the key or on the definition.

Run files: `evaluation/runs/*_agent_v8_sonnet-5-5_validation7.json`.
