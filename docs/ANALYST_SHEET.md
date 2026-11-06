# Analyst-ready Excel output

`tools/to_excel.py` turns the agent's JSON fact sheet into a workbook (`python3 tools/to_excel.py fact_sheet.json out.xlsx`). Example: `examples/LMT_fact_sheet.json` and `examples/LMT_fact_sheet.xlsx` (Lockheed Martin, real agent output from the fourth holdout).

- **Fact sheet**: the 10 figures with source and the agent's note; the 7 ratios as live Excel formulas on those cells (the analyst can change an input and see the ratio move); rows that are not "found" are highlighted.
- **To verify**: a review list built by fixed rules, not by a model: every status other than found (High), notes that signal a judgement such as restricted cash, discontinued operations, debt note not read, MD&A source (Medium), every limit the agent wrote (Medium), and absent-from-report answers that rest on a search only (Low). A "Checked" column lets the analyst tick items off.
- **Risks and context**: segments, the three risks the company names, and the three questions a report does not answer.

Checked: formulas recalculated in LibreOffice give the same values as the agent's calculator (7 of 7 ratios).

Not done: the n8n workflow still returns JSON; connecting this converter to the workflow output is the next step.
