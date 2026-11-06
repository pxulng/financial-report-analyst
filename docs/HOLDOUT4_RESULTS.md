# Fourth holdout: results (prompt v7 + statement finder v2.1)

Reports never used to build any rule: GE Aerospace (GE) and Lockheed Martin (LMT). Sonnet 5.5, one run each, key frozen first (`docs/HOLDOUT4_FREEZE.md`).

| Company | Original items read | Computed | Wrong or invented | Credit items right |
|---|---|---|---|---|
| GE | 7/7 | 2/2 | 0 | 2/2 (2 excluded) |
| LMT | 9/9 | 4/4 | 0 | 4/4 |

**0 wrong figures on both reports.**

- Rule v7 confirmed on GE: the income statement prints no "Operating income" line, and the agent returned not_applicable for operating income, operating margin and coverage, saying so in the note. On Honeywell (v6) the same situation produced a wrong figure from the MD&A.
- Statement finder: both reports opened their real income statement, balance sheet and cash-flow statement on the first call (13 and 15 tool calls; Honeywell needed 24 before the fix).
- LMT: operating profit 7,731 read from the statement line, interest coverage 6.92, debt/equity 3.23, all as in the key.

## Still not solved
- read_section does not find the risk factors on GE (and before on HON, WFC, MCD): the agent used search snippets and said so in its limits. The risks are not scored.
- The agent does not always check the debt note for finance leases (it says so in the note).
- Two reports per round is a small sample: this shows the two fixes work, it is not a measure of overall accuracy.

## Cost
Balance 1.58 -> 1.29 USD for two runs (GE, LMT): 0.29 USD, about 0.15 per report.
