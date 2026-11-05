# Blind human check: risks and limits (8 fact sheets)
Purpose (docs/DESIGN.md, section 6): judge the quality of the risks and of the limits on 8 fact sheets, without knowing which method produced them.
Sheets: validation set (MSFT, WMT, NKE, JPM), the two Sonnet 5.5 methods, 4 x 2 = 8 sheets, shuffled and labelled A to H. The method behind each label is kept out of the repository until you have rated all 8. Texts are the full texts returned by the models (nothing shortened).
## How to rate
For each risk, write one number after each question mark:
- **Faithful**: does the sentence say what the report says (1 = yes, 0.5 = partly, 0 = no or invented)? Check against the cited section of the 10-K in `data/10k/`.
- **Top risk**: would you call it one of the three most important risks the company itself identifies (1 = yes, 0.5 = reasonable but not top 3, 0 = no, minor or generic)?
For the limits of each sheet:
- **Honest**: do the limits tell an analyst what to double-check (1 = yes, 0.5 = partly, 0 = they are empty, vague or hide a real weakness)?
- **Missing**: write in a few words any weakness the sheet does not warn about (or "none").
Then fill the 3-line comment if something struck you. Do not try to guess the method; if you think you can tell, note it at the end.
Suggested time: 5 to 8 minutes per sheet. For the "Top risk" question, the reference risks of each company (written before any model was run) are in the appendix.

---

## Sheet A: JPM

**Risk 1.** The Firm is highly regulated, and changes in law, supervisory expectations, capital and liquidity rules, or executive-branch actions, or a compliance failure, could raise costs, cut revenue or force it to change its business.
  Source cited: Item 1A Risk Factors, Legal and Regulatory, p. 10
  - Faithful ? 
  - Top risk ? 

**Risk 2.** Adverse economic and market conditions (interest rates, credit spreads, volatility, inflation, recession and political developments) could hurt results, market-making and investment positions, and capital and liquidity.
  Source cited: Item 1A Risk Factors, Market (and Political), pp. 14-17
  - Faithful ? 
  - Top risk ? 

**Risk 3.** Operational failures and cyber attacks, which the Firm says have occurred and are inevitable, could disrupt services, expose client data, cause losses and damage its reputation.
  Source cited: Item 1A Risk Factors, Operational, pp. 20-23
  - Faithful ? 
  - Top risk ? 

**Limits stated by the sheet**
- Operating income, operating margin, capex, free cash flow, total financial debt and net debt are marked not_applicable because JPMorgan is a bank holding company and the report does not publish these items. The analyst may want alternative bank metrics such as pre-provision profit (86,807, non-GAAP) or income before tax (72,595).
- Revenue is total net revenue on a reported basis (182,447). The report also gives a managed-basis figure of 185,581 (non-GAAP) that adds a taxable-equivalent adjustment.
- Operating cash flow is published as a large outflow (-147,782) driven by trading and securities-financing balances, so it should not be read as weak cash generation.
- The cash figure is 'Cash and due from banks' only. If the analyst prefers a broader definition, deposits with banks (321,596) are a separate balance-sheet line.
- The three major risks were selected by me from Item 1A because the report does not rank its risks. Credit, liquidity, capital and country risks are also listed as principal risks on pp. 9-10.
- The report includes extensive exhibits (e.g. Exhibits 4.6, 10.x, 19, 21, 22.2, 97) that contain no financial data used here.

  - Honest ? 
  - Missing : 
  - Comment : 

---

## Sheet B: WMT

**Risk 1.** Failure to execute the omnichannel strategy and the cost of heavy investments in eCommerce, technology, AI and automation could hurt market position, net sales and financial performance, and could lead to impairment charges.
  Source cited: Item 1A, Strategic Risks, p. 13
  - Faithful ? 
  - Top risk ? 

**Risk 2.** Changes in tax and trade policy, including tariffs, could raise merchandise costs and affect margins, and the company expects the dynamic tariff environment to continue in fiscal 2027 with an unpredictable and possibly material impact.
  Source cited: Item 1A, Legal, Tax, Regulatory, Compliance, Reputational and Other Risks, p. 23
  - Faithful ? 
  - Top risk ? 

**Risk 3.** Cyberattacks, system failures or loss of customer, member, associate or payment data could cause fines, litigation, reputational damage and lost sales, and AI is intensifying these threats.
  Source cited: Item 1A, Operational Risks, pp. 17-20; Item 1C, p. 28
  - Faithful ? 
  - Top risk ? 

**Limits stated by the sheet**
- The three major risks are my selection from many risk factors. The company does not rank them, so the analyst may want to choose differently.
- Total financial debt is the sum of three balance sheet lines. The 38,166 of long-term debt includes deferred loan costs, discounts and fair value hedge adjustments (Note 5, p. 67).
- Walmart International figures are consolidated with a one-month lag (calendar year basis), so they are not strictly aligned to January 31 (Note 1, p. 57).
- Net income used is the group share (21,893). Consolidated net income including non-controlling interest is 22,270. The latter was used for return on assets in Item 7.
- Operating margin is computed on total revenues (4.18 %). The company reports 4.2 % on net sales, so the two bases differ slightly.
- The filing text includes exhibits (e.g. securities description, plans, separation agreement) that carry no financial data. They were not used.

  - Honest ? 
  - Missing : 
  - Comment : 

---

## Sheet C: NKE

**Risk 1.** Product, marketplace and brand management actions across the portfolio, including declining store traffic, heavy promotions and high inventory in Greater China and a strategic reset of Converse, have hurt and may continue to hurt revenues and profitability, with negative impacts expected to continue through fiscal 2027.
  Source cited: Item 1A. Risk Factors
  - Faithful ? 
  - Top risk ? 

**Risk 2.** Foreign currency fluctuations have adversely affected and could continue to affect results, and hedging only lessens and delays the effects.
  Source cited: Item 1A. Risk Factors (foreign currency)
  - Faithful ? 
  - Top risk ? 

**Risk 3.** A slowing or changing economy in key markets, including a recession, could hurt customers' financial health and reduce orders and sales.
  Source cited: Item 1A. Risk Factors (economic conditions)
  - Faithful ? 
  - Top risk ? 

**Limits stated by the sheet**
- Operating income is not a published line, so operating_income and operating_margin are not_applicable. The analyst may want to derive an EBIT-type measure from Note 15 (the segment note says the CODM uses EBIT), but I did not.
- The three risks are my selection from the passages the search tool returned. I did not read the whole Item 1A, and the report does not rank its risks.
- The page numbers I could see are 56 (income statement), 58 (balance sheet) and 59 (cash flow). The long-term debt note page was not visible.
- Net debt uses only cash and equivalents. Short-term investments of 1,464 are excluded, per the definitions.
- The fiscal 2027 search showed only qualitative outlook language, and I did not search the report further for forward-looking guidance.

  - Honest ? 
  - Missing : 
  - Comment : 

---

## Sheet D: MSFT

**Risk 1.** Cybersecurity threats and security incidents, including AI-enhanced attacks, supply-chain compromises and insider or third-party access problems, could compromise the company's systems and data.
  Source cited: Item 1A. Risk Factors (cybersecurity discussion)
  - Faithful ? 
  - Top risk ? 

**Risk 2.** Third parties may claim the company infringes their intellectual property, including copyright claims arising from AI training, inference and output. Resolving these claims could require less favorable royalty or licensing agreements, or stopping the sale of affected products.
  Source cited: Item 1A. Risk Factors, Intellectual Property Risks
  - Faithful ? 
  - Top risk ? 

**Risk 3.** The company is subject to regulatory oversight, including the EU Digital Markets Act and Digital Services Act, and this creates compliance risk.
  Source cited: Item 1, Government Regulation, which refers to Item 1A. Risk Factors
  - Faithful ? 
  - Top risk ? 

**Limits stated by the sheet**
- The three risks were chosen from the passages my searches returned, not from a full read of Item 1A. The analyst should confirm they are the company's most important risks. The regulatory risk is cited from the Item 1 cross-reference, not from the text of Item 1A.
- Page numbers are given only where they were visible in the tool output (51, 53 and 54). The cash flow statement page number is read from the footer after the statement.
- The earnings guidance search was a single search, and it was not exhaustive.
- Total financial debt is the sum of the two debt lines on the balance sheet. I did not read the debt note to check for finance leases or other items inside long-term debt.
- The cash flow statement also shows 'Other, net' investing outflows of 19,861, which are not part of capex.

  - Honest ? 
  - Missing : 
  - Comment : 

---

## Sheet E: MSFT

**Risk 1.** The company's cloud and AI strategy requires very large, accelerated capital and operating investments ahead of fully developed revenue, and may not earn expected returns if customer demand, pricing, costs or access to capital differ from expectations. This could also cause underutilized infrastructure or asset impairments.
  Source cited: Item 1A, Strategic and Competitive Risks, pp. 15-16
  - Faithful ? 
  - Top risk ? 

**Risk 2.** The company faces intense competition across all its markets (platform ecosystems, AI and cloud providers, open-source, free ad-funded offerings), which may cause price reductions, lower volumes and higher costs.
  Source cited: Item 1A, Strategic and Competitive Risks, pp. 14-15
  - Faithful ? 
  - Top risk ? 

**Risk 3.** Cyberattacks and security vulnerabilities, including nation-state attacks and AI-enabled threats, could reduce revenue, increase costs, create liability and harm the company's reputation.
  Source cited: Item 1A, Cybersecurity, Data Privacy, and Platform Abuse Risks, pp. 17-20
  - Faithful ? 
  - Top risk ? 

**Limits stated by the sheet**
- Page numbers come from the page headers in the document text and match the 10-K index.
- Capex is the cash-flow line 'Additions to property and equipment' (115,948). Large infrastructure spending also flows through finance leases (24,608 of right-of-use assets obtained in FY2026), unpaid PP&E purchases (26.7 billion in accounts payable) and 329.1 billion of datacenter leases not yet commenced (Note 13). Free cash flow and net debt therefore understate total capital commitments.
- Net debt excludes lease liabilities (operating 21,925; finance 66,594) and short-term investments (55,908), per the definitions. Cash, cash equivalents and short-term investments total 76,843.
- Net income and diluted EPS include OpenAI-related net gains of about $6.5 billion pre-tax ($5.0 billion after tax, $0.67 per share), mainly a dilution gain from the OpenAI recapitalization. The company's non-GAAP diluted EPS excluding this is $17.28. GAAP figures are reported here.
- Fiscal year 2026 revenue growth is 17.8% and the report states 18%. Revenue and operating income included a favorable foreign-currency impact of 2% (Item 7, p. 37).
- The three major risks are my selection from the company's Item 1A list; the report does not rank its risks.
- The IRS has proposed an additional $28.9 billion in tax, plus penalties and interest, for 2004-2013 (Note 11, p. 76). The company disputes it. This is not reflected in any figure above.

  - Honest ? 
  - Missing : 
  - Comment : 

---

## Sheet F: NKE

**Risk 1.** Changes in U.S. or other countries' trade policies, tariffs and import/export rules have already raised costs and could materially harm the company's business, financial condition and results.
  Source cited: Item 1A, 'Changes to U.S. or other countries' trade policies and tariff and import/export regulations...', p. 19; also Item 1, International Operations and Trade, p. 4
  - Faithful ? 
  - Top risk ? 

**Risk 2.** The athletic footwear, apparel and equipment industry is highly competitive, with new entrants and AI-driven technological change, and failure to respond could reduce demand and force price cuts.
  Source cited: Item 1A, 'Our products, services and experiences face intense competition', p. 10
  - Faithful ? 
  - Top risk ? 

**Risk 3.** Weak global economic conditions, including inflation, interest rates, currency volatility and lower consumer discretionary spending, could reduce demand and margins and hurt customers' financial health.
  Source cited: Item 1A, 'Global economic conditions...' and 'Economic factors beyond our control...', pp. 10-11
  - Faithful ? 
  - Top risk ? 

**Limits stated by the sheet**
- Operating income is not published, so operating_income and operating_margin are not_applicable. The analyst may want to consider the non-GAAP EBIT of 3,850 (8.3% margin), but it is not the requested line.
- Page numbers were taken from the report's page markers and the Item 15 index. Some extracted text has garbled characters, for example in the Greater China table and Notes 1, 12 and 13. The figures used were checked against the clean statements.
- Fiscal 2026 results include a 986 benefit in cost of sales from expected IEEPA tariff recoveries and 385 of severance charges (Item 7, p. 31). Both affect comparability.
- Total financial debt uses book value net of swap fair-value adjustments (7,942). Face value is 8,000.
- Global Brand Divisions and Corporate are presented in the segment note as reconciling or non-reportable items and are not counted as reportable segments. The count of 5 follows the report's wording.
- The CFO is due to leave on August 17, 2026 (Item 1, executive officers footnote, p. 8). This is not a financial figure but may be relevant to the analyst.

  - Honest ? 
  - Missing : 
  - Comment : 

---

## Sheet G: JPM

**Risk 1.** Legal and regulatory risks, including the impact of extensive supervision and regulation and changes to or in the application or interpretation of laws and regulations, could adversely affect the Firm.
  Source cited: Item 1A. Risk Factors, Summary (pp. 9-31)
  - Faithful ? 
  - Top risk ? 

**Risk 2.** The Firm warns that any of its principal risk factors could by itself, or combined with others, materially and adversely affect its financial condition, results of operations and capital position. The passages I retrieved gave only the first listed category, legal and regulatory risk. This item is a general statement and not a second specific risk.
  Source cited: Item 1A. Risk Factors, introduction (pp. 9-31)
  - Faithful ? 
  - Top risk ? 

**Risk 3.** The report refers to the financial consequences for holders of the Firm's debt and equity securities in a resolution scenario. I did not read the full risk text, so this is not a confirmed top-three risk.
  Source cited: Item 7, Liquidity Risk Management, Parent Company, referring to Item 1A
  - Faithful ? 
  - Top risk ? 

**Limits stated by the sheet**
- The read_statement tool for the income statement returned the comprehensive income statement and balance sheet text. Revenue and diluted EPS come from MD&A tables and the income statement's EPS line, and I did not see the full income statement itself. The analyst should check these against the income statement.
- The tool's 'balance' and 'cashflow' outputs returned the Parent Company-only statements. The consolidated balance sheet came from the first call. The consolidated operating cash flow came from a search of the consolidated cash-flow statement.
- I did not find a capex line in the consolidated cash-flow statement, so capex and free cash flow are not_applicable. The analyst may want to check whether the report shows purchases of premises and equipment elsewhere.
- Total financial debt excludes beneficial interests issued by consolidated VIEs (27,951). Including them would raise debt to 527,933.
- The risk section was read only through search snippets. The three risks are therefore weakly supported, and the analyst should read Item 1A (pp. 9-31) to confirm the top three.
- The 2026 adjusted expense guidance figure was not retrieved. The analyst should read the Outlook section for it.

  - Honest ? 
  - Missing : 
  - Comment : 

---

## Sheet H: WMT

**Risk 1.** Failure to execute the omnichannel strategy, and the cost of investments in eCommerce and technology, could materially hurt Walmart's market position, net sales and financial performance.
  Source cited: Item 1A Risk Factors, Strategic Risks
  - Faithful ? 
  - Top risk ? 

**Risk 2.** Changes in tax and trade laws and policies, including tariffs, could materially hurt financial performance. The Walmart U.S. and Sam's Club U.S. segments generated about 82% of fiscal 2026 net sales, and a significant portion of their general merchandise is made in other countries.
  Source cited: Item 1A Risk Factors, Legal, Tax, Regulatory, Compliance, Reputational and Other Risks
  - Faithful ? 
  - Top risk ? 

**Risk 3.** Strong competition from other retailers, wholesale club operators, omnichannel retailers and other businesses could materially hurt financial performance.
  Source cited: Item 1A Risk Factors, Strategic Risks
  - Faithful ? 
  - Top risk ? 

**Limits stated by the sheet**
- Page numbers are those printed in the report where visible: income statement p. 52, balance sheet p. 54, cash flow p. 56. The page for the Item 1A risk factors was not confirmed, other than Item 1A starting around p. 13.
- I chose the three risks from the risk-factor headings that the searches returned. I did not read all of Item 1A, so the analyst may rank the risks differently.
- The absence of earnings guidance rests on keyword searches, not a full read of the MD&A.
- Interest on finance leases and lease obligations is excluded from total_financial_debt as defined. Including lease obligations would change net debt.

  - Honest ? 
  - Missing : 
  - Comment : 

---

## Appendix: reference risks per company (written before any model was run)

**MSFT**
- Intense competition across all markets, including platform ecosystems
- Risks from AI development and deployment: costs, regulation, reputational harm
- Cybersecurity incidents and data protection

**WMT**
- Execution of the omnichannel and eCommerce strategy and cost of the investments
- Economic conditions, inflation and consumer spending
- Tariffs, trade policy and supply chain disruption

**NKE**
- Global economic conditions and consumer discretionary spending
- Intense competition and the ability to innovate and keep brand strength
- Dependence on contract manufacturers in Asia, supply chain and tariffs

**JPM**
- Credit risk and economic conditions
- Regulation, capital and liquidity requirements
- Cybersecurity and operational risk

## End
Any remark on the exercise (for example "I think sheets C and F come from the same method because..."):
