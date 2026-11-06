"""Side-by-side comparison of two companies from two agent fact sheets.
Usage: python3 compare_excel.py a.json b.json out.xlsx
Sheets: "Comparison" (figures and ratios of both companies, live formulas, a comparability column built by rules),
"Sources and notes" (source and agent's note for every number), "To verify" (both companies' review lists).
No model call: the agent is run once per company, this script only puts the two results side by side."""
import json, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from to_excel import LABEL, PCT, TIMES, FLAGS, review_items

ORDER_F = ["revenue","operating_income","net_income","diluted_eps","operating_cash_flow","capex","cash","total_financial_debt","shareholders_equity","interest_expense"]
ORDER_C = ["revenue_growth","operating_margin","free_cash_flow","net_debt","interest_coverage","debt_to_equity","cfo_to_debt"]
TPL = {"operating_margin":"{operating_income}/{revenue}","free_cash_flow":"{operating_cash_flow}-{capex}","net_debt":"{total_financial_debt}-{cash}",
       "interest_coverage":"{operating_income}/{interest_expense}","debt_to_equity":"{total_financial_debt}/{shareholders_equity}","cfo_to_debt":"{operating_cash_flow}/{total_financial_debt}"}

def short(name): return re.sub(r"\s*\(.*\)|,? (Inc|Corporation|Company|Corp)\.?$", "", name).strip()[:22]

def comparability(item, A, B, na="A", nb="B"):
    a, b = A[item], B[item]
    if a["status"] != b["status"]:
        return "NOT COMPARABLE: %s for one company, %s for the other" % (a["status"].replace("_"," "), b["status"].replace("_"," "))
    if a["status"] != "found": return "Not available for either"
    out = []
    for r, tag in ((a,na),(b,nb)):
        n = r.get("note") or ""
        for rx, why in FLAGS[1:3]:
            if rx.search(n): out.append("%s: %s" % (tag, why.lower())); break
    return "Check definitions (" + "; ".join(out) + ")" if out else "Comparable on the agent's definitions"

def build(da, db, path):
    fa = {r["item"]: r for r in da["figures"] + da["computed"]}; fb = {r["item"]: r for r in db["figures"] + db["computed"]}
    na, nb = short(da["company"]), short(db["company"])
    wb = Workbook(); ws = wb.active; ws.title = "Comparison"
    hdr = PatternFill("solid", fgColor="1F3A5F"); white = Font(color="FFFFFF", bold=True)
    thin = Side(style="thin", color="D0D0D0"); box = Border(top=thin, bottom=thin, left=thin, right=thin)
    ws["A1"] = "%s vs %s" % (da["company"], db["company"]); ws["A1"].font = Font(size=14, bold=True)
    warn = []
    if da.get("fiscal_year_end") != db.get("fiscal_year_end"): warn.append("Fiscal years end on different dates (%s vs %s)." % (da.get("fiscal_year_end"), db.get("fiscal_year_end")))
    if da.get("reporting_currency") != db.get("reporting_currency") or da.get("unit") != db.get("unit"): warn.append("Currency or unit differs: the amounts are NOT in the same unit.")
    ws["A2"] = " ".join(warn) or "Same currency, unit and fiscal year end (%s, %s)." % (da.get("reporting_currency"), da.get("unit"))
    ws["A2"].font = Font(italic=True, color="C00000" if warn else "555555")
    r = 4
    for c, t in enumerate(["Item", na, nb, "Gap (A - B)", "Comparability (automatic)"], 1):
        x = ws.cell(r, c, t); x.fill = hdr; x.font = white
    rowof = {}
    def val(rec): return rec["value"] if rec["status"] == "found" else None
    for k in ORDER_F + ORDER_C:
        r += 1; rowof[k] = r
        ws.cell(r, 1, LABEL.get(k, k))
    def put(col, rec_map, k, other):
        rr = rowof[k]; rec = rec_map[k]; cell = ws.cell(rr, col); L = "B" if col == 2 else "C"
        if k in TPL and rec["status"] == "found":
            names = re.findall(r"{(\w+)}", TPL[k])
            if all(fmap[col][n]["status"] == "found" for n in names):
                cell.value = "=" + TPL[k].format(**{n: "%s%d" % (L, rowof[n]) for n in names})
            else: cell.value = rec["value"]
        elif rec["status"] == "found": cell.value = rec["value"]
        else: cell.value = rec["status"].replace("_", " ")
        cell.number_format = '0.0%' if k in PCT else ('0.00"x"' if k in TIMES else ('0.00' if k == "diluted_eps" else '#,##0;(#,##0)'))
        if rec["status"] != "found": cell.fill = PatternFill("solid", fgColor="FFF2CC")
    fmap = {2: fa, 3: fb}
    for k in ORDER_F + ORDER_C:
        put(2, fa, k, fb); put(3, fb, k, fa); rr = rowof[k]
        if fa[k]["status"] == "found" and fb[k]["status"] == "found":
            g = ws.cell(rr, 4, "=B%d-C%d" % (rr, rr)); g.number_format = '0.0%' if k in PCT else ('0.00"x"' if k in TIMES else '#,##0;(#,##0)')
        else: ws.cell(rr, 4, "n/a")
        t = comparability(k, fa, fb, na, nb); ws.cell(rr, 5, t)
        if t.startswith("NOT"): ws.cell(rr, 5).fill = PatternFill("solid", fgColor="F8CBAD")
        elif t.startswith("Check"): ws.cell(rr, 5).fill = PatternFill("solid", fgColor="FFE699")
    for col, w in zip("ABCDE", (28, 20, 20, 16, 80)): ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=4, max_row=r):
        for x in row: x.alignment = Alignment(wrap_text=True, vertical="top"); x.border = box
    r += 2; ws.cell(r, 1, "Segments").font = Font(bold=True)
    for d, n in ((da, na), (db, nb)):
        r += 1; s = d.get("segments") or {}; ws.cell(r, 1, n); ws.cell(r, 2, "%s: %s" % (s.get("count",""), "; ".join(s.get("names", []))))
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5); ws.cell(r, 2).alignment = Alignment(wrap_text=True)

    wn = wb.create_sheet("Sources and notes")
    for c, t in enumerate(["Item", "Company", "Source in the report", "Agent's note"], 1):
        x = wn.cell(1, c, t); x.fill = hdr; x.font = white
    i = 1
    for k in ORDER_F:
        for d, n, m in ((da, na, fa), (db, nb, fb)):
            i += 1; rec = m[k]
            for c, t in enumerate([LABEL.get(k, k), n, rec.get("source", ""), rec.get("note", "")], 1):
                x = wn.cell(i, c, t); x.alignment = Alignment(wrap_text=True, vertical="top")
    for col, w in zip("ABCD", (26, 20, 50, 100)): wn.column_dimensions[col].width = w

    wv = wb.create_sheet("To verify")
    for c, t in enumerate(["Company", "Priority", "Item", "Why it is listed", "Detail", "Checked (Y/N)"], 1):
        x = wv.cell(1, c, t); x.fill = hdr; x.font = white
    colr = {"High": "F8CBAD", "Medium": "FFE699", "Low": "E2EFDA"}; i = 1
    for d, n in ((da, na), (db, nb)):
        for p, it, why, det in review_items(d):
            i += 1
            for c, t in enumerate([n, p, it, why, det, ""], 1):
                x = wv.cell(i, c, t); x.alignment = Alignment(wrap_text=True, vertical="top")
            wv.cell(i, 2).fill = PatternFill("solid", fgColor=colr[p])
    for col, w in zip("ABCDEF", (20, 10, 28, 28, 90, 14)): wv.column_dimensions[col].width = w
    wb.save(path)

if __name__ == "__main__":
    build(json.load(open(sys.argv[1], encoding="utf-8")), json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3])
