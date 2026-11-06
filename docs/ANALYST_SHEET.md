# Analyst-ready Excel output

`tools/to_excel.py` turns the agent's JSON fact sheet into a workbook (`python3 tools/to_excel.py fact_sheet.json out.xlsx`). Example: `examples/LMT_fact_sheet.json` and `examples/LMT_fact_sheet.xlsx` (Lockheed Martin, real agent output from the fourth holdout).

- **Fact sheet**: the 10 figures with source and the agent's note; the 7 ratios as live Excel formulas on those cells (the analyst can change an input and see the ratio move); rows that are not "found" are highlighted.
- **To verify**: a review list built by fixed rules, not by a model: every status other than found (High), notes that signal a judgement such as restricted cash, discontinued operations, debt note not read, MD&A source (Medium), every limit the agent wrote (Medium), and absent-from-report answers that rest on a search only (Low). A "Checked" column lets the analyst tick items off.
- **Risks and context**: segments, the three risks the company names, and the three questions a report does not answer.

Checked: formulas recalculated in LibreOffice give the same values as the agent's calculator (7 of 7 ratios).

Not done: the n8n workflow still returns JSON; connecting this converter to the workflow output is the next step.

## Comparison of two companies
`tools/compare_excel.py a.json b.json out.xlsx` puts two fact sheets side by side (example: `examples/LMT_vs_GE_comparison.xlsx`, Lockheed Martin vs GE Aerospace, real agent outputs). No extra model call: the agent runs once per company, so a comparison costs two runs.
- **Comparison**: every figure and ratio for both companies (ratios are live formulas), the gap, and an automatic "comparability" column: red when a number exists for one company only (here: GE prints no operating income, so operating margin and interest coverage cannot be compared), yellow when the agent made a definition choice for one company (restricted cash in GE's cash, discontinued operations in its net income and cash flow, internal-use software in its capex). A warning appears at the top if the fiscal year ends, currency or unit differ.
- **Sources and notes** and **To verify** carry both companies' sources, notes and review items.
- Checked: formulas recalculated in LibreOffice; the rules do not know if two companies use the same accounting definitions beyond what the agent wrote in its notes.

## Comparison inside the n8n workflow (status)

- `workflow/compare_node.js` holds the comparison logic. It is installed as a Code node named "Compare" after "Reading" in the agent workflow (same rules as `tools/compare_excel.py`, no model call).
- Offline test on the real LMT and GE fact sheets: correct side-by-side table, operating income flagged NOT COMPARABLE (GE prints no operating income line).
- Workflow test 1 (three executions in ONE workflow, about 0.4 USD): the AI Agent node (v3.1, Sonnet 5.5, adaptive thinking) fails with "Bad request" on the SECOND item of a run, in either order, with 0 tool calls, also with batch size 1. Cause not identified.
- Fix that works: a parent workflow "Annual-report analyst: compare companies" (id 2VRBWVjdmDJAy1G3) takes a list of tickers, calls the single-company agent workflow once per ticker through "Execute Workflow" (mode "each", so each company is a separate execution), then the "Compare" Code node builds the side-by-side table. The agent workflow got an "When called" trigger and no longer contains Compare. Test with LMT and GE: both sheets valid, 17 comparison rows, operating income / margin / interest coverage flagged NOT COMPARABLE (GE prints no operating income line), about 0.3 USD, about 55 s.
- The analyst changes the ticker list in the "Tickers" node of the parent workflow. The Excel export of the comparison is still done by `tools/compare_excel.py` from the two sheets.
