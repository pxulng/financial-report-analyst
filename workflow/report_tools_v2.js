// Report tools v2. Same code runs inside the n8n sub-workflow (node "Run tool") and in the local test.
// runTool(p, txt): p = {tool: "search"|"statement"|"section", query, statement, section, offset}, txt = report text.
function runTool(p, txt) {
  const lines = String(txt || "").replace(/\t/g, " ").split("\n");
  const numCount = (ls) => { let n = 0; for (const x of ls) if (/\d{1,3},\d{3}|\d+\.\d{2}/.test(x)) n++; return n; };
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
      income: { a: [/net (income|earnings)/i, /diluted/i, /(income tax|provision for income taxes|taxes on income)/i], h: /^(?:.*subsidiaries )?(?:consolidated )?(?:statements? of (?:consolidated )?(?:operations|income|earnings)|income statements?)$/i, m: [/net (income|earnings|\(loss\))/i, /(revenues?|sales)/i, /per (common )?share|diluted/i], title: /consolidated\s+(statements?\s+of\s+(operations|income|earnings)|income statements?)|statements?\s+of\s+(consolidated\s+)?(operations|income|earnings)/i },
      balance: { a: [/total assets/i, /total liabilities/i, /total (stock|share)holders.{0,3} equity|total equity/i], h: /^(?:.*subsidiaries )?(?:consolidated )?(?:balance sheets?|statements? of financial position)$/i, m: [/total assets/i, /total liabilities|liabilities and (share|stock)holders/i, /total (share|stock)holders|total equity/i], title: /consolidated\s+balance sheets?|balance sheets?|statements?\s+of\s+financial position/i },
      cashflow: { a: [/operating activities|from operations/i, /investing/i, /financing/i], h: /^(?:.*subsidiaries )?(?:consolidated )?(?:statements? of cash flows?|cash flows? statements?)$/i, m: [/operating activities|operations/i, /investing/i, /financing/i], title: /consolidated\s+statements?\s+of\s+cash\s+flows?|statements?\s+of\s+cash\s+flows?|cash\s+flows?\s+statements?/i }
    }[String(p.statement || "").toLowerCase()];
    if (!S) out = "Unknown statement. Use one of: income, balance, cashflow.";
    else {
      const bad = /parent company|condensed|quarterly|unaudited|pro forma/i;
      const nearParent = (i) => { for (let j = Math.max(0, i - 400); j <= Math.min(lines.length - 1, i + 10); j++) { const l = lines[j].trim(); if (l.length < 120 && /parent company|parent-only|registrant/i.test(l)) return true; } return false; };
      // Method 1: find the statement by its title line, then check the window.
      let best = -1, bs = -1, firstConsol = -1;
      for (let i = 0; i < lines.length; i++) {
        const hl = lines[i].replace(/^[#*\s]+/, "").replace(/[*\s]+$/, "");
        if (hl.length < 110 && S.h.test(hl)) {
          if (firstConsol < 0 && /consolidated/i.test(hl)) firstConsol = i;
          const w = lines.slice(i + 1, i + 130);
          let n = numCount(w);
          const wt = w.join("\n");
          if (n >= 12 && S.m.every(r => r.test(wt)) && n > bs) { bs = n; best = i; }
        }
      }
      if (best < 0) best = firstConsol;
      let valid = false;
      if (best >= 0) {
        const w = lines.slice(best, best + 115);
        valid = S.a.every(r => r.test(w.join("\n"))) && numCount(w) >= 18 && !bad.test(lines.slice(Math.max(0, best - 8), best + 9).join("\n")) && !nearParent(best);
      }
      if (!valid) {
        // Method 2: find the statement by its table header and row labels (titles may come after the table).
        const hdr = /(in millions|in thousands|in billions|\(millions|\(in )|(years?|fiscal years?) ended|^\s*(december|september|june|may|january|february|march|april|july|august|october|november) \d{1,2}[, ]|^\s*(as of|at) /i;
        let b2 = -1, sc = -1;
        for (let i = 0; i < lines.length; i++) {
          if (lines[i].length > 160 || !hdr.test(lines[i])) continue;
          const w = lines.slice(i, i + 120);
          if (!S.a.every(r => r.test(w.join("\n")))) continue;
          const n = numCount(w);
          if (n < 18) continue;
          const ctx = lines.slice(Math.max(0, i - 8), i + 9).join("\n");
          if (bad.test(ctx) || nearParent(i)) continue;
          const titled = S.title.test(lines.slice(Math.max(0, i - 8), i + 125).join("\n"));
          const score = n + (titled ? 40 : 0) + (/consolidated/i.test(ctx + w.join("\n").slice(0, 6000)) ? 15 : 0);
          if (score > sc) { sc = score; b2 = i; }
        }
        if (b2 >= 0) best = b2; else if (!valid && best < 0) best = -1;
      }
      if (best < 0) out = "Statement not found in this report. Use search_report or read_section instead.";
      else out = "[statement starts at line " + (best + 1) + "]\n" + lines.slice(best, best + 110).map(x => x.trim()).filter(Boolean).join("\n").slice(0, 9500);
    }
  } else if (p.tool === "section") {
    const sec = String(p.section || "").trim().toLowerCase();
    const off = Math.max(0, parseInt(p.offset, 10) || 0);
    let start = -1, end = -1;
    if (sec === "risk_factors" || sec === "risk factors") {
      const A = [], B = [];
      for (let i = 0; i < lines.length; i++) {
        const l = lines[i].replace(/^[#*\s]+/, "");
        if (/^item\s*1a\b/i.test(l)) A.push(i);
        if (/^item\s*(1b|1c|2)\b/i.test(l)) B.push(i);
      }
      let bestLen = 0, prevB = -1;
      for (const b of B) {
        const a = A.find(x => x > prevB && x < b - 5);
        prevB = b;
        if (a === undefined) continue;
        if (b - a > bestLen) { bestLen = b - a; start = a; end = b; }
      }
    } else if (sec) {
      let bestLen = 0;
      for (let i = 0; i < lines.length; i++) {
        const l = lines[i].replace(/^[#*\s]+/, "").trim();
        if (l.length < 100 && l.toLowerCase().includes(sec) && !/\d{3},\d{3}/.test(l) && (/^(note\s+\d+|item\s+\d)/i.test(l) || /^#+ /.test(lines[i]) || l.length < 70)) {
          let e = i + 1;
          while (e < lines.length && e - i < 4000 && !(e > i + 15 && (/^#+ /.test(lines[e]) && /^(note\s+\d+|item\s+\d)/i.test(lines[e].replace(/^#+\s*/, ""))))) e++;
          const len = lines.slice(i, e).join("\n").length;
          if (len > bestLen) { bestLen = len; start = i; end = e; }
        }
      }
    }
    if (start < 0) out = "Section not found. Try risk_factors, or a heading word such as 'long-term debt', 'segment', 'debt'.";
    else {
      const body = lines.slice(start, end).map(x => x.trim()).filter(Boolean).join("\n");
      out = "[section starts at line " + (start + 1) + " | characters " + off + "-" + Math.min(body.length, off + 9000) + " of " + body.length + (off + 9000 < body.length ? " | next page: offset " + (off + 9000) : " | end of section") + "]\n" + body.slice(off, off + 9000);
    }
  } else out = "Unknown tool.";
  return out.slice(0, 9900);
}
if (typeof module !== "undefined") module.exports = { runTool };
