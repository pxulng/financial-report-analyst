# Financial report analyst: agent or single prompt?

Project 4 of an AI portfolio (n8n + Claude). An assistant that reads a US company's annual report (10-K) and produces a sourced fact sheet: key figures, ratios, segments, risks, and what the report does not say. The study measures whether an **agent with tools** beats a **single prompt containing the whole report**, on real public filings.

> **Status: in progress.** The design and its thresholds were frozen on 5 November 2026, before any model was run. No results yet. See [`docs/DESIGN.md`](docs/DESIGN.md) and [`docs/FREEZE_DESIGN.md`](docs/FREEZE_DESIGN.md).

> **What this is not.** It is not investment advice. The tool makes no buy or sell recommendation and no valuation estimate. Reports are public SEC filings; no confidential data is used.

## Why this study

[Project 3](https://github.com/pxulng/agent-avant-vente) compared an agent and a single prompt on 15 pages of documentation: the single prompt was enough, and whether an agent pays off on a much larger corpus was left untested. A 10-K runs to hundreds of pages, so this project tests that hypothesis with the same method: thresholds fixed in advance, a test set to improve the prompts, a validation set run once, and an error log.

## Plan

- 10 companies: 6 test (Apple, Johnson & Johnson, Exxon Mobil, Boeing, Starbucks, Tesla) and 4 validation (Microsoft, Walmart, Nike, JPMorgan Chase), drawn at random with a seed fixed in advance.
- About 15 items per company, scored against a key built from the financial statements.
- Blocking measure: a wrong figure presented as certain.
- Two models (Haiku 5.5, Sonnet 5.5); three methods (keyword search, single prompt, agent).

## Repository

| Folder | Content |
|---|---|
| `data/10k/` | The annual reports used, as supplied (public SEC filings) |
| `docs/` | Design document, freeze record |
| `prompts/`, `workflow/`, `evaluation/` | To be filled as the study proceeds |
