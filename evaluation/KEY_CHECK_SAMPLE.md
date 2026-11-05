# Figures key: 20 % check sample

Rule fixed before any model ran on the full panel: the figures key is extracted from the financial statements of each 10-K by script (`build_key.py`), then the author checks a random 20 % of the figures read (computed figures follow from them).

- Population: 84 figures read that exist in the key (items marked not applicable are excluded).
- Draw: `random.Random(20261105).shuffle` over the list of (company, item), first 17 kept.
- To check: open the file at the given line and compare the value in the key with the report. Write OK, or the correct value, in the last column.
- Decision rule: if one figure is wrong, the whole key of that company is rechecked before any scoring.

| Company | Item | Key value (USD millions; EPS in USD) | File | Where | OK? |
|---|---|---|---|---|---|
| AAPL | capex | 9,041 | `data/10k/AAPL_10-K_FY2026.md` | line 1910: Payments for acquisition of property, plant and equipment | |
| AAPL | revenue | 478,834 | `data/10k/AAPL_10-K_FY2026.md` | line 1449: Total net sales | |
| BA | cash | 10,921 | `data/10k/BA_10-K_FY2025.md` | line 2071: Cash and cash equivalents | |
| BA | debt | 54,098 | `data/10k/BA_10-K_FY2025.md` | line 2091: Short-term debt and current portion of long-term debt 8,461; line 2097: Long-term debt 45,637 | |
| JPM | equity | 362,438 | `data/10k/JPM_10-K_FY2025.md` | line 4549: Total stockholders’ equity | |
| JPM | net_income | 57,048 | `data/10k/JPM_10-K_FY2025.md` | line 4492: Net income | |
| MSFT | operating_cash_flow | 182,935 | `data/10k/MSFT_10-K_FY2026.md` | line 3054: Net cash from operations | |
| NKE | diluted_eps | 2.10 | `data/10k/NKE_10-K_FY2026.md` | line 1721: Diluted | |
| SBUX | debt | 16,074.8 | `data/10k/SBUX_10-K_FY2025.md` | line 1954: Current portion of long-term debt 1,498.9; line 1954: Long-term debt 14,575.9 | |
| SBUX | revenue | 37,184.4 | `data/10k/SBUX_10-K_FY2025.md` | line 1250: Total net revenues | |
| TSLA | cash | 16,513 | `data/10k/TSLA_10-K_FY2025.md` | line 1995: Cash and cash equivalents | |
| TSLA | operating_income | 4,355 | `data/10k/TSLA_10-K_FY2025.md` | line 2070: Income from operations | |
| WMT | debt | 44,762 | `data/10k/WMT_10-K_FY2026.md` | line 2331: Short-term borrowings 6,596; line 2588: Long-term debt due within one year 3,542; line 2193: Long-term debt 34,624 | |
| WMT | equity | 99,617 | `data/10k/WMT_10-K_FY2026.md` | line 2605: Total Walmart shareholders' equity | |
| WMT | net_income | 21,893 | `data/10k/WMT_10-K_FY2026.md` | line 2526: Consolidated net income attributable to Walmart | |
| WMT | revenue | 713,163 | `data/10k/WMT_10-K_FY2026.md` | line 1910: Total revenues | |
| XOM | debt | 43,537 | `data/10k/XOM_10-K_FY2025.md` | line 1654: Notes and loans payable 9,296; line 1564: Long-term debt 34,241 | |
