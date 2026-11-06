function runTool(p, txt) {
const lines = txt.replace(/\t/g, " ").split("\n");
function heading(i) {
  for (let j = i; j >= Math.max(0, i - 600); j--) {
    const l = lines[j].trim();
    if (/^#+ /.test(l) || /^item\s+\d+[ab]?[.:]/i.test(l) || /^note\s+\d+/i.test(l)) return l.slice(0, 120);
  }
  return "";
}
let out = "";
if (p.tool === "search") {
  const terms = String(p.query || "").toLowerCase().split(/[^a-z0-9']+/).filter(w => w.length > 2);
  const scored = [];
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i].toLowerCase();
    let s = 0;
    for (const t of terms) if (l.includes(t)) s++;
    if (s > 0 && /\d{2}/.test(l)) s += 0.5;
    if (s >= Math.max(1, terms.length * 0.5)) scored.push({ i, s });
  }
  scored.sort((a, b) => b.s - a.s || a.i - b.i);
  const picked = [];
  for (const c of scored) {
    if (picked.every(x => Math.abs(x.i - c.i) > 4)) picked.push(c);
    if (picked.length >= 8) break;
  }
  picked.sort((a, b) => a.i - b.i);
  for (const c of picked) {
    const chunk = lines.slice(Math.max(0, c.i - 1), c.i + 4).map(x => x.trim()).filter(Boolean).join(" | ").slice(0, 700);
    out += "[line " + (c.i + 1) + " | section: " + heading(c.i) + "]\n" + chunk + "\n\n";
  }
  if (!out) out = "No passage matched. Try other words.";
} else if (p.tool === "statement") {
  const S = {
    income: { h: /^(?:.*subsidiaries )?(?:consolidated )?(?:statements? of (?:consolidated )?(?:operations|income|earnings)|income statements?)$/i, m: [/net (income|earnings|\(loss\))/i, /(revenues?|sales)/i, /per (common )?share|diluted/i] },
    balance: { h: /^(?:.*subsidiaries )?(?:consolidated )?(?:balance sheets?|statements? of financial position)$/i, m: [/total assets/i, /total liabilities|liabilities and (share|stock)holders/i, /total (share|stock)holders|total equity/i] },
    cashflow: { h: /^(?:.*subsidiaries )?(?:consolidated )?(?:statements? of cash flows?|cash flows? statements?)$/i, m: [/operating activities|operations/i, /investing/i, /financing/i] }
  }[String(p.statement || "").toLowerCase()];
  if (!S) { out = "Unknown statement. Use one of: income, balance, cashflow."; }
  else {
    let best = -1, bs = -1, firstConsol = -1;
    for (let i = 0; i < lines.length; i++) {
      const hl = lines[i].replace(/^[#*\s]+/, "").replace(/[*\s]+$/, "");
      if (hl.length < 110 && S.h.test(hl)) {
        if (firstConsol < 0 && /consolidated/i.test(hl)) firstConsol = i;
        const w = lines.slice(i + 1, i + 130);
        let n = 0;
        for (const x of w) if (/\d{1,3},\d{3}|\d+\.\d{2}/.test(x)) n++;
        const wt = w.join("\n");
        if (n >= 12 && S.m.every(r => r.test(wt)) && n > bs) { bs = n; best = i; }
      }
    }
    if (best < 0) best = firstConsol;
    if (best < 0) out = "Statement not found in this report. Use search_report instead.";
    else out = "[statement starts at line " + (best + 1) + "]\n" + lines.slice(best, best + 110).map(x => x.trim()).filter(Boolean).join("\n").slice(0, 9000);
  }
} else { out = "Unknown tool."; }
return out.slice(0, 9500);
}
module.exports = { runTool };
