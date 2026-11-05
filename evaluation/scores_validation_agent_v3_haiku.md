# Validation set, agent v3, Haiku 5.5 (thinking disabled), one execution per company

Scored with `score.py`, one file per company (JPM has no sheet, so score.py cannot total it).

| Company | Strict JSON | Read | Computed | Absent | Wrong/invented | Notes |
|---|---|---|---|---|---|---|
| MSFT | ok | 9/9 | 4/4 | 3/3 | 0 | 10 tool calls |
| WMT | ok | 8/9 | 4/4 | 3/3 | 1 | total_financial_debt value 45,162; the agent's own note and net_debt use 44,762 (key 44,762) |
| NKE | invalid (text before a fenced block; valid after extraction) | 8/9 | 3/4 | 3/3 | 2 | derived operating income 3,797 and margin 0.0818 where the key says not applicable (flagged as derived in the notes) |
| JPM | no output | - | - | - | - | stopped at the 15-step limit, no sheet (measure 9 case: statements longer than the window) |

Totals on the 3 companies with a sheet: read 25/27, computed 11/12, absent 9/9, wrong or invented 3.
Strict JSON: 2/4 (MSFT, WMT); valid after extraction: 3/4.
Cost: not measured yet (balance read after the pass).
