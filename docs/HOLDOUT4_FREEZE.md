# Fourth holdout (General Electric, Lockheed Martin): freeze

Validation of the fixes in `docs/V5_FIXES.md`: prompt v7 (commit 0263cee) and the statement finder v2.1. Reports never used to build any rule. Sonnet 5.5, one run each, nothing changed between this freeze and the runs.

| Company | File | sha256 |
|---|---|---|
| GE | data/10k/GE_10-K_FY2025.md | `fe1d82827c6c1df84d81984884a7427de80e610c7bf6ca014d60076fd8c657ec` |
| LMT | data/10k/LMT_10-K_FY2025.md | `05b1a5b93a0007939c3fe9bc4525ef876e9c0b1191ba540aaee2748cd6605df1` |

## Key decisions made before the runs
- GE (GE Aerospace): the income statement prints no "Operating income" line, so operating_income and operating_margin = not_applicable (this tests rule v7). Revenue = Total revenue 45,855 (prev 38,702). Net income = attributable to the Company 8,704. Diluted EPS = net earnings per share 8.14 (continuing operations alone is 8.05). Operating cash flow = 8,537 (total; continuing is 8,543). Debt = short-term borrowings 1,686 + long-term borrowings 18,808 = 20,494. Equity = Total shareholders' equity 18,677.
- GE excluded (ambiguous): capex (the only line is "Additions to property, plant and equipment and internal-use software" 1,273), cash (the balance sheet line includes restricted cash), free cash flow, net debt, interest expense and coverage ("Interest and other financial charges" 843, as for Honeywell). Scored: debt/equity 1.0973, CFO/debt 0.4166.
- LMT: revenue = Total sales 75,048 (prev 71,043). Operating income = "Operating profit" 7,731 (printed on the statement; margin 0.103). Net income 5,017. Diluted EPS 21.49. Operating cash flow 8,557. Capex 1,649. Cash 4,121. Debt = current maturities 1,168 + long-term debt 20,532 = 21,700. Equity 6,721. Interest expense 1,118 (printed line); coverage 6.92; debt/equity 3.2287; CFO/debt 0.3943.
