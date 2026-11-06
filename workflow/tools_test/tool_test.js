// Free tool test: for each report and statement, does the tool output contain the key's printed values?
const fs = require("fs");
const { runTool } = require(process.argv[2] || "../report_tools_v2.js");
const key = JSON.parse(fs.readFileSync("../../evaluation/key.json", "utf8"));
const want = {
  income: ["revenue", "net_income", "diluted_eps"],
  balance: ["equity", "cash"],
  cashflow: ["operating_cash_flow"]
};
let ok = 0, tot = 0; const fails = [];
for (const [t, k] of Object.entries(key)) {
  const txt = fs.readFileSync("../../data/10k/" + k.file, "utf8");
  for (const [st, items] of Object.entries(want)) {
    const out = runTool({ tool: "statement", statement: st }, txt);
    for (const it of items) {
      const v = k.items[it];
      if (!v || v.status !== "found") continue;
      tot++;
      const pr = String(v.printed).replace(/[()]/g, "").replace(/^-/, "");
      if (out.includes(pr)) ok++; else fails.push(t + " " + st + " " + it + " (" + v.printed + ") first line: " + out.split("\n")[0]);
    }
  }
}
console.log("passed " + ok + "/" + tot); fails.forEach(f => console.log("FAIL", f));
