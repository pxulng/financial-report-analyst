# McDonald's (MCD) test: freeze

Added after the second holdout. One company, FY2025 10-K (ended 2025-12-31), run once with agent v3 (prompt v5, Sonnet 5.5), no change to the prompt or tools before the run.

- File: `data/10k/MCD_10-K_FY2025.md` (converted from the HTML 10-K `mcd-20251231.htm`), sha256 `ec6db5f6994fe8528622d6462a528ab9d74e2c6bea05cd709469c04b96803641`.
- Why this company: negative shareholders' equity (deficit of 1,791), which tests the `not_applicable` rule for debt_to_equity.
- Key decisions made before the run: debt = Long-term debt 39,973 (no short-term debt line is printed; lease liabilities not counted, as for the other companies); interest_expense = 1,582 (line "Interest expense-net of capitalized interest"); debt_to_equity = not_applicable (equity < 0); cfo_to_debt = 0.264; interest_coverage = 7.83 (12,393 / 1,582).
- Key entries added to `evaluation/build_key.py` and `build_key_credit.py`; the 17 earlier entries are unchanged.
