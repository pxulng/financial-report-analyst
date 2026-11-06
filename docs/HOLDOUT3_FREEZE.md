# Third holdout (Honeywell, Home Depot): freeze

First test of prompt v6 and the fixed statement finder on 10-Ks never used to build any rule. Sonnet 5.5, one run each, no change to prompt or tools between this freeze and the runs. Wells Fargo was also sent but the file is only the 10-K wrapper: its financial statements are in the Annual Report (Exhibit 13), which is not in the file. It is not used.

| Company | File | sha256 |
|---|---|---|
| HON | data/10k/HON_10-K_FY2025.md | `7d7ef814df8d52c24a34a6a798b7e8ec1a94086c983c26393cac3d3be375286e` |
| HD | data/10k/HD_10-K_FY2025.md | `e685f52447cee81ce49f08a04d71c0c12763d39bee6adc62449b6d934260c554` |

## Key decisions made before the runs
- HON operating_income = not_applicable: the income statement prints no "Operating income" line (an MD&A table shows a defined "operating income" of 5,573, which is not the statement line). operating_margin follows.
- HON diluted_eps = 7.36 (total EPS assuming dilution; continuing operations alone is 6.94). operating_cash_flow = 6,408 (the printed total, including discontinued operations; continuing is 6,075). net_income = 4,729 (attributable to Honeywell).
- HON debt = 5,893 + 1,546 + 27,141 = 34,580; equity = Total Honeywell shareowners' equity 13,904 (not the 15,030 with noncontrolling interest). cash = 12,487 (short-term investments excluded).
- HON interest_expense and interest_coverage = excluded: the only candidate line, "Interest and other financial charges" (1,344), is not clearly a gross interest expense line.
- HD fiscal 2025 ended 2026-02-01; revenue growth uses 159,514 (a 53-week year). debt = 4,464 + 4,967 + 46,341 = 55,772 (lease liabilities not counted); equity 12,813; interest_expense = 2,412 (printed line); coverage 8.66.
- Known before the run: the statement finder does not locate the HON income statement and cash-flow statement (it returns notes). The runs are done without fixing it, to see whether the agent recovers with its other tools. The fix comes after.
