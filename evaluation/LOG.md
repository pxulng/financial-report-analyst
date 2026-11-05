# Evaluation log

Dated entries, in order. Nothing is edited after the fact; corrections are new entries.

## 2026-11-05: cost measurement, Apple, reference 2 (single prompt), prompt v1

Workflow: `workflow/` (n8n, reference 2). Prompt: `prompts/reference2_system_prompt.txt` v1 (sha256 `7a7d5b55…a8971d`). Report: `data/10k/AAPL_10-K_FY2026.md`.

| Model | Input tokens | Output tokens | Stop | JSON | Cost (account balance) |
|---|---|---|---|---|---|
| Haiku 5.5 | 151,734 | 4,324 | end_turn | valid | about 0.09 USD (2.07 to 1.98) |
| Sonnet 5.5 | 151,734 | 3,728 | end_turn | valid | about 0.34 USD (6.98 to 6.64) |

Outputs: `evaluation/runs/`. These two runs count as the first pass of prompt v1 on the test set (Apple). They are not scored yet: the key was built after the runs, from the report only (see below).

Declared limit: the author saw the Haiku output before the Apple key and the Apple risk reference list were written. The Apple figures key is taken from the statements by script, independently of the model output; the Apple risk list will be flagged as written after seeing one output.

## 2026-11-05: figures key built

`evaluation/build_key.py` locates each figure in the financial statements of the report (label and printed value must appear together) and computes the derived items with the frozen formulas. Result: `evaluation/key.json`. No model had been run on the nine other companies when the key was built.

Choices made while applying the frozen definitions (to confirm or overrule before the validation run):

- **Not applicable operating income:** Nike, Johnson & Johnson, ExxonMobil and JPMorgan do not publish an "operating income" line, so the item and the operating margin are not applicable for them. Boeing publishes "Earnings from operations" and Tesla "Income from operations": read as operating income.
- **JPMorgan:** operating income, capex and cash are not applicable (no "cash and cash equivalents" line; the balance sheet shows "cash and due from banks" and "deposits with banks"). Free cash flow, net debt and operating margin follow. Total financial debt is read as short-term borrowings plus long-term debt.
- **ExxonMobil revenue:** "Total revenues and other income" (332,238), the only total line. Equity is "ExxonMobil share of equity".
- **Walmart revenue:** "Total revenues" (713,163), which includes membership income; net sales are 706,413.
- **Tesla debt:** the balance sheet line combines debt and finance leases; the debt note gives "Total debt" (1,569 current and 6,584 long-term), finance leases excluded as defined.
- **Starbucks equity:** negative (shareholders' deficit, -8,096.6). **Boeing equity:** 5,454 (Boeing shareholders), total equity 5,457.
- **Johnson & Johnson debt:** "Loans and notes payable" plus long-term debt.

Check sample for the author (20 %): `evaluation/KEY_CHECK_SAMPLE.md`.
