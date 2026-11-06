# Fixes after the third holdout (prompt v7, statement finder v2.1)

Causes found on Honeywell (see `docs/HOLDOUT3_RESULTS.md`):
1. Statement finder, three checks too strict, all fixed in `workflow/report_tools_v2.js`: (a) the income-statement check wanted "income tax" but Honeywell prints "Tax expense" (now accepted); (b) the "quarterly/unaudited" warning looked 8 lines above the title and caught the table of contents ("Unaudited Quarterly Financial Information"), now only 2 lines above to 6 below; (c) the "registrant" check looked 400 lines back and caught the cover page text, now 120 lines.
2. Prompt v7: operating_income is only the line printed on the income statement; if there is none it is not_applicable, and an MD&A, segment or non-GAAP figure is never used.

Check without any model call on all 21 reports x 3 statements: only 4 outputs changed. HON income and cash flow now open the real statements. BAC income and balance sheet also changed and are now the real consolidated statements (before: a "selected data" table and a different table). Every other output is identical.

Not validated yet: a run with v7 on reports never used so far.
