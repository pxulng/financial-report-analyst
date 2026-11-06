// n8n Code node "Compare": runs after "Reading". With two or more valid fact sheets it builds a side-by-side comparison
// (same rules as tools/compare_excel.py). No model call: the agent never sees the other company, so it cannot invent differences.
function buildComparison(results) {
  const ok = results.filter(r => r.sheet && r.sheet.figures && r.sheet.computed);
  if (ok.length < 2) return { comparison: null, note: "Need at least two valid fact sheets to compare (got " + ok.length + ")." };
  const F = ["revenue","operating_income","net_income","diluted_eps","operating_cash_flow","capex","cash","total_financial_debt","shareholders_equity","interest_expense"];
  const C = ["revenue_growth","operating_margin","free_cash_flow","net_debt","interest_coverage","debt_to_equity","cfo_to_debt"];
  const choice = /restricted cash|includes? (discontinued|internal-use|finance lease)|discontinued operations|continuing operations/i;
  const maps = ok.map(r => { const m = {}; for (const x of r.sheet.figures.concat(r.sheet.computed)) m[x.item] = x; return m; });
  const names = ok.map(r => r.sheet.company || r.id);
  const warnings = [];
  const ends = new Set(ok.map(r => r.sheet.fiscal_year_end)); if (ends.size > 1) warnings.push("Fiscal years end on different dates: " + [...ends].join(", ") + ".");
  const units = new Set(ok.map(r => (r.sheet.reporting_currency || "") + " " + (r.sheet.unit || ""))); if (units.size > 1) warnings.push("Currency or unit differs: the amounts are NOT in the same unit.");
  const rows = F.concat(C).map(k => {
    const vals = maps.map(m => m[k] || { status: "not_in_report", value: null });
    const statuses = new Set(vals.map(v => v.status));
    let comparability;
    if (statuses.size > 1) comparability = "NOT COMPARABLE: " + vals.map((v, i) => names[i] + " = " + v.status.replace(/_/g, " ")).join("; ");
    else if (!statuses.has("found")) comparability = "Not available for any company";
    else {
      const flagged = vals.map((v, i) => (choice.test(v.note || "") ? names[i] : null)).filter(Boolean);
      comparability = flagged.length ? "Check definitions (" + flagged.join(", ") + ")" : "Comparable on the agents' definitions";
    }
    return { item: k, values: vals.map(v => v.status === "found" ? v.value : v.status), comparability };
  });
  const md = ["| Item | " + names.join(" | ") + " | Comparability |", "|---|" + names.map(() => "---|").join("") + "---|"]
    .concat(rows.map(r => "| " + r.item + " | " + r.values.join(" | ") + " | " + r.comparability + " |")).join("\n");
  return { comparison: { companies: names, warnings, rows }, markdown: md };
}
if (typeof module !== "undefined") module.exports = { buildComparison };
else {
  const results = JSON.parse($input.first().json.results);
  return [{ json: Object.assign({ n: results.length }, buildComparison(results)) }];
}
