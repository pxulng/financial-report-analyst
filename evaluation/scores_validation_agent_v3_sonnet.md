# Validation set, agent v3, Sonnet 5.5 (thinking adaptive), one execution per company

Scored with `score.py`, one file per company.

| Company | Strict JSON | Read | Computed | Absent | Wrong/invented | Notes |
|---|---|---|---|---|---|---|
| MSFT | ok | 9/9 | 4/4 | 3/3 | 0 | 11 tool calls |
| WMT | ok | 9/9 | 4/4 | 3/3 | 0 | debt 44,762 correct |
| NKE | ok | 9/9 | 4/4 | 3/3 | 0 | operating income and margin correctly not_applicable |
| JPM | ok | 8/9 | 3/4 | 2/3 | 2 | cash 21,742 and net_debt 478,240 presented as found (key: not applicable); guidance answered "found" with NII outlook; 14 tool calls, risks weakly supported |

Totals: read 35/36, computed 15/16, absent 11/12, wrong or invented 2. Strict JSON 4/4.
Cost: not measured yet.
