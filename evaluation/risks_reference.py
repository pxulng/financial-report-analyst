"""Reference list of 3 major risks per company, written before the panel was run (Apple: see note).
Each risk = a short label + keywords. A risk is 'grounded' if at least one keyword appears 3+ times in the 10-K file.
A model risk is counted as found if it matches the label's topic (human or keyword match at scoring time)."""
import json,re
R={
"AAPL":[("Supply chain concentration: outsourced manufacturing in Asia, single or limited-source components",["outsourcing partners","single or limited"]),
        ("Legal and regulatory pressure on the business model: antitrust, App Store rules, Digital Markets Act",["antitrust","Digital Markets Act"]),
        ("Tariffs, trade restrictions and geopolitical tension affecting costs and operations",["tariff","geopolitical"])],
"MSFT":[("Intense competition across all markets, including platform ecosystems",["intense competition","competitors"]),
        ("Risks from AI development and deployment: costs, regulation, reputational harm",["artificial intelligence","AI"]),
        ("Cybersecurity incidents and data protection",["cyberattack","cybersecurity","security breach"])],
"WMT":[("Execution of the omnichannel and eCommerce strategy and cost of the investments",["omnichannel","eCommerce"]),
       ("Economic conditions, inflation and consumer spending",["inflation","consumer spending"]),
       ("Tariffs, trade policy and supply chain disruption",["tariff","supply chain"])],
"NKE":[("Global economic conditions and consumer discretionary spending",["global economic conditions","discretionary spending"]),
       ("Intense competition and the ability to innovate and keep brand strength",["intense competition","brand"]),
       ("Dependence on contract manufacturers in Asia, supply chain and tariffs",["contract manufacturers","tariff"])],
"JNJ":[("Competition and loss of patent exclusivity (Innovative Medicine)",["loss of patent exclusivity","patent"]),
       ("Product liability and litigation, including talc",["talc","product liability"]),
       ("Pricing pressure, reimbursement and healthcare regulation",["pricing pressure","reimbursement"])],
"XOM":[("Volatility of oil, gas and chemical prices and margins",["commodity price","prices"]),
       ("Climate change policies and the energy transition",["climate change","energy transition"]),
       ("Geopolitical and operational risks, including project execution and operating in unstable regions",["geopolitical","project"])],
"BA":[("Dependence on commercial airlines and cyclical aircraft demand",["commercial airlines","airline"]),
      ("Aircraft safety, quality and regulatory oversight (FAA, 737 MAX)",["FAA","737"]),
      ("Supplier and supply chain disruption, labor disruption and production rate",["supplier","supply chain"])],
"SBUX":[("Economic conditions and consumer spending",["economic conditions","consumer"]),
        ("Intense competition and brand strength",["competition","brand"]),
        ("Commodity costs (coffee) and supply chain",["coffee","supply chain"])],
"TSLA":[("Production ramp-up, new products and manufacturing execution",["production","new products"]),
        ("Government incentives, regulatory credits, tariffs and trade policy",["regulatory credits","tariff"]),
        ("Attracting and retaining key employees and qualified personnel",["key employees","qualified personnel"])],
"JPM":[("Credit risk and economic conditions",["credit risk","credit losses"]),
       ("Regulation, capital and liquidity requirements",["capital","liquidity"]),
       ("Cybersecurity and operational risk",["cyber","operational risk"])],
}
key=json.load(open("key.json")); out={}; bad=[]
for t,lst in R.items():
    txt=re.sub(r"\s+"," ",open("../data/10k/"+key[t]["file"],encoding="utf-8",errors="ignore").read())
    out[t]=[]
    for lab,kws in lst:
        counts={k:len(re.findall(re.escape(k),txt,re.I)) for k in kws}
        ok=any(v>=3 for v in counts.values())
        if not ok: bad.append((t,lab))
        out[t].append({"risk":lab,"keywords":kws,"keyword_counts":counts,"grounded":ok})
json.dump(out,open("risks_reference.json","w"),indent=1)
print("not grounded:",bad)
