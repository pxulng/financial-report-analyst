"""Turns the agent's JSON fact sheet into an Excel workbook an analyst can review.
Usage: python3 to_excel.py fact_sheet.json out.xlsx
Sheets: "Fact sheet" (figures, ratios with live formulas), "To verify" (automatic review list), "Risks and context".
The "To verify" list is built by rules, not by a model: statuses other than found, notes that signal a judgement
(restricted cash, discontinued operations, debt note not read, MD&A, ...), every item the agent put in "limits",
and the risks when the agent could not read the risk section."""
import json, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FLAGS = [
 (re.compile(r"did not (check|read|find|see)|not read|not checked|was not read|could not", re.I), "Not checked by the agent"),
 (re.compile(r"restricted cash|includes? (discontinued|internal-use|finance lease)|discontinued operations|continuing operations", re.I), "Definition choice"),
 (re.compile(r"MD&A|snippet|search (result|passage)|fragment", re.I), "Taken from a secondary source"),
 (re.compile(r"may |might |could |unclear|ambiguous|approximately|revised|restated", re.I), "Uncertain or revised"),
]
LABEL = {"revenue":"Revenue","operating_income":"Operating income","net_income":"Net income (group share)","diluted_eps":"Diluted EPS (USD)",
 "operating_cash_flow":"Operating cash flow","capex":"Capex","cash":"Cash and equivalents","total_financial_debt":"Total financial debt",
 "shareholders_equity":"Shareholders' equity","interest_expense":"Interest expense","revenue_growth":"Revenue growth","operating_margin":"Operating margin",
 "free_cash_flow":"Free cash flow","net_debt":"Net debt","interest_coverage":"Interest coverage (x)","debt_to_equity":"Debt / equity (x)","cfo_to_debt":"CFO / debt (x)"}
PCT = {"revenue_growth","operating_margin"}; TIMES = {"interest_coverage","debt_to_equity","cfo_to_debt"}

def review_items(d):
    out = []
    for kind in ("figures", "computed"):
        for r in d.get(kind, []):
            name = LABEL.get(r["item"], r["item"]); note = r.get("note") or ""
            if r["status"] != "found":
                out.append(("High", name, "Status: " + r["status"].replace("_", " "), note))
            for rx, why in FLAGS:
                if note and rx.search(note):
                    out.append(("Medium", name, why, note)); break
    for l in d.get("limits", []):
        out.append(("Medium", "Agent's own limit", "Stated by the agent", l))
    for q in d.get("not_in_report", []):
        if "search" in (q.get("answer", "") + q.get("source", "")).lower() and "not" in q.get("answer", "").lower():
            out.append(("Low", q["question"], "Answered by search only", q["answer"]))
    seen, uniq = set(), []
    for o in out:
        if (o[1], o[3]) not in seen: seen.add((o[1], o[3])); uniq.append(o)
    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(uniq, key=lambda o: order[o[0]])

def build(d, path):
    wb = Workbook(); ws = wb.active; ws.title = "Fact sheet"
    hdr = PatternFill("solid", fgColor="1F3A5F"); white = Font(color="FFFFFF", bold=True)
    thin = Side(style="thin", color="D0D0D0"); box = Border(top=thin, bottom=thin, left=thin, right=thin)
    ws["A1"] = d.get("company", ""); ws["A1"].font = Font(size=14, bold=True)
    ws["A2"] = "Fiscal year end: %s | %s %s | Prepared by an AI agent from the 10-K; to be reviewed by an analyst" % (d.get("fiscal_year_end",""), d.get("reporting_currency",""), d.get("unit",""))
    ws["A2"].font = Font(italic=True, color="555555")
    r = 4
    for c, t in enumerate(["Figure", "Value", "Status", "Source in the report", "Agent's note"], 1):
        x = ws.cell(r, c, t); x.fill = hdr; x.font = white
    rows = {}
    for f in d.get("figures", []):
        r += 1; rows[f["item"]] = r
        ws.cell(r, 1, LABEL.get(f["item"], f["item"])); v = ws.cell(r, 2, f.get("value")); v.number_format = '#,##0.00' if f["item"] == "diluted_eps" else '#,##0;(#,##0)'
        ws.cell(r, 3, f["status"].replace("_", " ")); ws.cell(r, 4, f.get("source", "")); ws.cell(r, 5, f.get("note", ""))
        if f["status"] != "found":
            for c in range(1, 6): ws.cell(r, c).fill = PatternFill("solid", fgColor="FFF2CC")
    r += 2
    for c, t in enumerate(["Ratio", "Value", "Status", "Formula (live)", "Inputs and note"], 1):
        x = ws.cell(r, c, t); x.fill = hdr; x.font = white
    def ref(k): return "B%d" % rows[k] if k in rows else None
    F = {"revenue_growth": None, "operating_margin": "{operating_income}/{revenue}", "free_cash_flow": "{operating_cash_flow}-{capex}", "net_debt": "{total_financial_debt}-{cash}",
         "interest_coverage": "{operating_income}/{interest_expense}", "debt_to_equity": "{total_financial_debt}/{shareholders_equity}", "cfo_to_debt": "{operating_cash_flow}/{total_financial_debt}"}
    for cptd in d.get("computed", []):
        r += 1; k = cptd["item"]; ws.cell(r, 1, LABEL.get(k, k)); cell = ws.cell(r, 2)
        tpl = F.get(k); formula = None
        if cptd["status"] == "found" and tpl:
            names = re.findall(r"{(\w+)}", tpl)
            if all(ref(n) and isinstance(d["figures"][[x["item"] for x in d["figures"]].index(n)].get("value"), (int, float)) for n in names):
                formula = "=" + tpl.format(**{n: ref(n) for n in names})
        cell.value = formula if formula else cptd.get("value")
        cell.number_format = '0.0%' if k in PCT else ('0.00"x"' if k in TIMES else '#,##0;(#,##0)')
        ws.cell(r, 3, cptd["status"].replace("_", " ")); ws.cell(r, 4, cptd.get("formula", ""))
        ws.cell(r, 5, (cptd.get("inputs", "") + (" | " if cptd.get("note") else "") + cptd.get("note", "")).strip())
        if cptd["status"] != "found":
            for c in range(1, 6): ws.cell(r, c).fill = PatternFill("solid", fgColor="FFF2CC")
    for col, w in zip("ABCDE", (28, 16, 14, 52, 80)): ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=4, max_row=r):
        for x in row: x.alignment = Alignment(wrap_text=True, vertical="top"); x.border = box

    wv = wb.create_sheet("To verify")
    wv["A1"] = "Review list built automatically from the agent's notes and limits (not a model opinion)"; wv["A1"].font = Font(bold=True)
    for c, t in enumerate(["Priority", "Item", "Why it is listed", "Detail", "Checked (Y/N)"], 1):
        x = wv.cell(3, c, t); x.fill = hdr; x.font = white
    colr = {"High": "F8CBAD", "Medium": "FFE699", "Low": "E2EFDA"}
    for i, (p, it, why, det) in enumerate(review_items(d), 4):
        for c, t in enumerate([p, it, why, det, ""], 1):
            x = wv.cell(i, c, t); x.alignment = Alignment(wrap_text=True, vertical="top"); x.border = box
        wv.cell(i, 1).fill = PatternFill("solid", fgColor=colr[p])
    for col, w in zip("ABCDE", (10, 30, 30, 95, 14)): wv.column_dimensions[col].width = w

    wr = wb.create_sheet("Risks and context")
    wr["A1"] = "Segments"; wr["A1"].font = Font(bold=True)
    s = d.get("segments") or {}
    wr["A2"] = "%s reportable segment(s): %s" % (s.get("count", ""), "; ".join(s.get("names", []))); wr["A3"] = "Source: " + s.get("source", "")
    wr["A5"] = "Main risks named by the company"; wr["A5"].font = Font(bold=True)
    r = 6
    for k in d.get("major_risks", []):
        wr.cell(r, 1, k["risk"]); wr.cell(r, 2, k["source"]); r += 1
    r += 1; wr.cell(r, 1, "Questions an annual report usually does not answer").font = Font(bold=True); r += 1
    for q in d.get("not_in_report", []):
        wr.cell(r, 1, q["question"]); wr.cell(r, 2, q["status"].replace("_", " ")); wr.cell(r, 3, q["answer"]); r += 1
    for col, w in zip("ABC", (90, 55, 90)): wr.column_dimensions[col].width = w
    for row in wr.iter_rows():
        for x in row: x.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)

if __name__ == "__main__":
    build(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
