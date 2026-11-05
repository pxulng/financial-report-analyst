| Company | JSON | Read | Computed | Absent | Wrong/invented | Value found in report | Risks (keyword proxy) |
|---|---|---|---|---|---|---|---|
| JPM | ok | 6/9 | 2/4 | 2/3 | 3 | 7/7 | 2/3 |
| MSFT | ok | 9/9 | 4/4 | 3/3 | 0 | 9/9 | 2/3 |
| NKE | ok | 9/9 | 4/4 | 3/3 | 0 | 8/8 | 1/3 |
| WMT | ok | 8/9 | 3/4 | 3/3 | 2 | 8/9 | 2/3 |

Totals: read 32/36 = 88.9%; computed 13/16 = 81.2%; absent 11/12; wrong or invented 5; value-in-report 32/33

Errors:
- JPM: capex: should be not_applicable, got status not_in_report
- JPM: cash: invented number 21742 (key: not applicable)
- JPM: total_financial_debt: WRONG 500, key 499982
- JPM: free_cash_flow: should be not_applicable, got status not_in_report
- JPM: net_debt: invented number 477251 (key: not applicable)
- WMT: total_financial_debt: WRONG 44304, key 44762
- WMT: net_debt: WRONG 33577, key 34035
