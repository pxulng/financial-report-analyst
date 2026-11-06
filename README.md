# Financial report analyst: agent or single prompt?

Project 4 of an AI portfolio (n8n + Claude). An assistant that reads a US company's annual report (10-K) and produces a sourced fact sheet: key figures, ratios, segments, risks, and what the report does not say. The study measures whether an **agent with tools** beats a **single prompt containing the whole report**, on real public filings.

> **Status: study complete, with a second round.** Round 1 (agent v3, prompts frozen in advance): the single prompt (whole report in one call) beat the agent on the pre-written decision rule (wrong figures on four validation companies: Sonnet single prompt 1, Sonnet agent 2, Haiku agent 3, Haiku single prompt 5). Round 2 (agent v2: better tools and prompt v4b, tuned after seeing round-1 errors, so exploratory, not a clean holdout): the Sonnet agent made 0 wrong figures on the same four companies for about 0.43 USD, against 2.30 USD for the Sonnet single prompt. A clean holdout (Bank of America, Verizon, Caterpillar, Coca-Cola, fixed before running) then gave the Sonnet agent 3 wrong figures against 4 for the Sonnet single prompt, at about a quarter of the cost; on Haiku the single prompt wins. See the [holdout results](docs/HOLDOUT_RESULTS.md). Round 4 (agent v3, prompt v5) adds interest expense and three credit ratios: 26 of 28 new items right and 1 wrong on eight companies, with no regression on the original items; see [V3 results](docs/V3_RESULTS.md). Read the [case study](docs/CASE_STUDY.md), the [validation results](docs/VALIDATION_RESULTS.md) and the [design](docs/DESIGN.md) (frozen before any model was run).

> **What this is not.** It is not investment advice. The tool makes no buy or sell recommendation and no valuation estimate. Reports are public SEC filings; no confidential data is used.

## Why this study

[Project 3](https://github.com/pxulng/agent-avant-vente) compared an agent and a single prompt on 15 pages of documentation: the single prompt was enough, and whether an agent pays off on a much larger corpus was left untested. A 10-K runs to hundreds of pages, so this project tests that hypothesis with the same method: thresholds fixed in advance, a test set to improve the prompts, a validation set run once, and an error log.

## Design

- 10 companies: 6 test (Apple, Johnson & Johnson, Exxon Mobil, Boeing, Starbucks, Tesla) and 4 validation (Microsoft, Walmart, Nike, JPMorgan Chase), drawn at random with a seed fixed in advance.
- About 15 items per company, scored against a key built from the financial statements.
- Blocking measure: a wrong figure presented as certain.
- Two models (Haiku 5.5, Sonnet 5.5); three methods (keyword search, single prompt, agent).

## Repository

| Folder | Content |
|---|---|
| `data/10k/` | The annual reports used, as supplied (public SEC filings) |
| `docs/` | Case study, design document, freeze records, validation results |
| `prompts/` | The frozen prompts (single prompt, agent v2, v3, v4 and v4b) |
| `workflow/` | The three n8n workflows (agent v2 with three report tools, report-tools sub-workflow v2, single prompt), without credentials |
| `baseline/` | Keyword-search floor, no AI |
| `evaluation/` | Key, scoring script, every run, scores, error log, human review |
