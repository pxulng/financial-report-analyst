# Financial report analyst: agent or single prompt?

Project 4 of an AI portfolio (n8n + Claude). An assistant that reads a US company's annual report (10-K) and produces a sourced fact sheet: key figures, ratios, segments, risks, and what the report does not say. The study measures whether an **agent with tools** beats a **single prompt containing the whole report**, on real public filings.

> **Status: study complete, agent improved over several rounds.** The question was whether an **agent with tools** beats a **single prompt containing the whole report** on 10-Ks. Round 1 (prompts frozen in advance): the single prompt won on the pre-written decision rule. After better tools and prompts, a clean holdout (Bank of America, Verizon, Caterpillar, Coca-Cola) gave the Sonnet agent 3 wrong figures against 4 for the Sonnet single prompt, at about a quarter of the cost; on Haiku the single prompt wins ([holdout results](docs/HOLDOUT_RESULTS.md)). Later rounds added credit ratios, 13 more reports (McDonald's, Honeywell, Home Depot, Wells Fargo, GE, Lockheed Martin and others; 23 reports in total), fixes to the tools and a fact sheet for analysts. Latest state: prompt **v9** on 7 reports with finance leases: 62 of 63 figures read, 2 wrong, both on Boeing because of an inconsistency in my own key ([v9 results](docs/V9_RESULTS.md)). A try of prompt v8 made things worse (13 wrong) and was rejected ([v8 validation](docs/V8_VALIDATION.md)). Samples are small (one run per company, and the 7 reports were also used to find the problem), so these numbers are indicative, not a guarantee. Read the [case study](docs/CASE_STUDY.md) and the [design](docs/DESIGN.md) (frozen before any model was run); every round has its freeze and results file in `docs/`.

> **What this is not.** It is not investment advice. The tool makes no buy or sell recommendation and no valuation estimate. Reports are public SEC filings; no confidential data is used.

## Why this study

[Project 3](https://github.com/pxulng/agent-avant-vente) compared an agent and a single prompt on 15 pages of documentation: the single prompt was enough, and whether an agent pays off on a much larger corpus was left untested. A 10-K runs to hundreds of pages, so this project tests that hypothesis with the same method: thresholds fixed in advance, a test set to improve the prompts, a validation set run once, and an error log.

## Design

- First study: 10 companies: 6 test (Apple, Johnson & Johnson, Exxon Mobil, Boeing, Starbucks, Tesla) and 4 validation (Microsoft, Walmart, Nike, JPMorgan Chase), drawn at random with a seed fixed in advance. Later rounds added holdout companies (Bank of America, Verizon, Caterpillar, Coca-Cola, Goldman Sachs, Pfizer, NextEra, McDonald's, Honeywell, Home Depot, Wells Fargo, GE, Lockheed Martin), each with its key and freeze record.
- About 15 items per company, scored against a key built from the financial statements.
- Blocking measure: a wrong figure presented as certain.
- Two models (Haiku 5.5, Sonnet 5.5); three methods (keyword search, single prompt, agent).

## Repository

| Folder | Content |
|---|---|
| `data/10k/` | The annual reports used, as supplied (public SEC filings) |
| `docs/` | Case study, design document, freeze records, validation results |
| `prompts/` | The prompts, one file per version (single prompt; agent v1 to v9; v9 is the current one) |
| `workflow/` | The n8n workflows (single prompt, report tools, agent for one company, comparison of several companies), without credentials; see `workflow/README.md` |
| `baseline/` | Keyword-search floor, no AI |
| `evaluation/` | Key, scoring script, every run, scores, error log, human review |
| `tools/` | `to_excel.py` (fact sheet to Excel with live formulas and a list of items to verify) and `compare_excel.py` (two companies side by side) |
| `examples/` | Real outputs: Lockheed Martin and GE fact sheets and their Excel comparison |

## For the analyst

The agent returns one JSON fact sheet per company. `tools/to_excel.py` turns it into an Excel file with three sheets: the fact sheet (ratios as live formulas, missing figures highlighted), a ranked "To verify" list and the risks. To compare two companies, run the agent once per company (the `compare_companies` workflow does this) and use `tools/compare_excel.py`: it flags what is not comparable (for example a company that prints no operating income line). See [ANALYST_SHEET.md](docs/ANALYST_SHEET.md). It is a prototype that prepares the analyst's work; the analyst still verifies the figures.
