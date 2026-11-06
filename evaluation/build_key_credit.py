"""Builds evaluation/key_credit.json: the credit-ratio items of agent v3 (prompt v5), from key.json plus the interest expense lines.
Rules (docs/V3_DESIGN.md): interest_expense = the gross interest expense line printed on the consolidated income statement; a statement
that prints only a net interest line or none gives not_in_report. debt_to_equity = total_financial_debt / shareholders_equity (not_applicable if
equity <= 0). cfo_to_debt = operating_cash_flow / total_financial_debt. interest_coverage = operating_income / interest_expense.
Banks: all four not_applicable. 'excluded' items are not scored (definition too ambiguous, declared in the design)."""
import json
key=json.load(open("key.json"))
NA={"status":"not_applicable"}; NIR={"status":"not_in_report"}; EXC={"status":"excluded"}
IE={"AAPL":NIR,"MSFT":NIR,"NKE":NIR,"WMT":EXC,"CAT":EXC,"JPM":NA,"BAC":NA,
    "JNJ":971,"XOM":603,"BA":2771,"SBUX":542.6,"TSLA":338,"VZ":6694,"KO":1654}
out={}
for t,k in key.items():
    it=k["items"]; bank=t in("JPM","BAC"); c={}
    f=lambda v:{"status":"found","value":v}
    ie=IE[t]; c["interest_expense"]=ie if isinstance(ie,dict) else f(ie)
    if bank:
        for n in("debt_to_equity","cfo_to_debt","interest_coverage"): c[n]=NA
    else:
        debt=it["debt"]["value"]; eq=it["equity"]["value"]; ocf=it["operating_cash_flow"]["value"]; oi=it["operating_income"]
        c["debt_to_equity"]=f(round(debt/eq,4)) if eq>0 else NA
        c["cfo_to_debt"]=f(round(ocf/debt,4))
        if isinstance(ie,dict): c["interest_coverage"]=ie if ie["status"]!="not_applicable" else NA
        elif oi["status"]=="not_applicable": c["interest_coverage"]=NA
        else: c["interest_coverage"]=f(round(oi["value"]/ie,2))
    out[t]=c
json.dump(out,open("key_credit.json","w"),indent=1)
for t,c in out.items(): print(t,{n:v.get("value",v["status"]) for n,v in c.items()})
