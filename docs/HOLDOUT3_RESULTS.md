# Third holdout: results (prompt v6, statement finder fixed for NEE)

Reports never used to build any rule: Honeywell (HON), Home Depot (HD), Wells Fargo (WFC). Sonnet 5.5, one run each, key frozen first (`docs/HOLDOUT3_FREEZE.md`).

| Company | Original items read | Computed | Wrong or invented | Credit items right |
|---|---|---|---|---|
| HD | 9/9 | 4/4 | 0 | 4/4 |
| WFC (bank) | 8/8 | 3/3 | 0 | 4/4 (all correctly not_applicable) |
| HON | 8/9 | 3/4 | 2 | 2/2 scored (2 excluded) |

Total: 0 wrong for HD and WFC; 2 wrong for HON (operating income and the operating margin that depends on it). For comparison, the first holdout on prompt v4b had 3 wrong figures on 4 reports.

## What worked
- Bank rule (v6): WFC returned not_applicable for interest expense, coverage, debt/equity and CFO/debt, and still gave total debt, equity and revenue growth.
- HD: every figure and ratio matched, including interest expense 2,412 and coverage 8.66.

## What failed (HON)
1. Operating income: Honeywell prints no "Operating income" line on its income statement. The agent used 5,573 from an MD&A reconciliation table instead of reporting not_applicable. It said where the number came from, but the rule says to use the statement line only. Operating margin followed.
2. Cause behind it: the statement finder returned stock-option and cash-flow notes instead of Honeywell's income statement and cash-flow statement, so the agent worked from searches (24 tool calls instead of 11 to 14). The finder looks for a title line; Honeywell's statement title is singular ("Statement of Operations") and followed by a unit line in the middle of the table, which breaks the window checks.
3. Excluded by the key before the run: HON interest expense and coverage (the only candidate line is "Interest and other financial charges"). The agent used 1,344 and flagged the caption.

## Not fixed yet
- Statement finder for HON (not touched, to keep this test honest).
- Rule for operating income: "only the line printed on the income statement; a figure from MD&A is not_applicable".
- Risk factors: read_section did not find the risk factors for HON, WFC and MCD (the agent used search snippets and said so). Not scored.
- Any change now needs a fourth untouched set to be validated.

## Cost
Balance to be noted.
