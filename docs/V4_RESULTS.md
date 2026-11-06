# Agent v4 candidate (prompt v6 + statement finder fix): first check

Changes, all aimed at the causes of the errors in the second holdout (`docs/HOLDOUT2_RESULTS.md`):
1. Statement finder: the income-statement check now accepts "dilution" as well as "diluted" (NEE prints "Assuming dilution"). Checked on all 18 reports x 3 statements: only NEE income changed (now line 3330, the real statement).
2. Prompt v6, rule 2: a figure that is not printed as a line is never built by adding or subtracting other lines (only exception: the finance-lease adjustment of total_financial_debt); it is `not_in_report`.
3. Prompt v6, bank rule: for banks, broker-dealers and insurers, interest_expense, interest_coverage, debt_to_equity and cfo_to_debt are all `not_applicable`, like operating income, capex and net debt.

## Regression on NEE (the company that failed before; not an untouched test)
Execution 1019, Sonnet 5.5: read 9/9 of the original items right (capex excluded as in the key), computed items right, credit items 4/4 right (interest expense 4,572 and coverage 1.81, both wrong before). The agent did not add up the capex lines and said why.

## Not yet done
- GS (bank rule) not rerun.
- v6 is not validated: it must be run on reports it has never seen, with the key frozen first. The 18 reports so far have all been used while building the rules.
