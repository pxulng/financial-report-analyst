# Case study: reading 10-K annual reports with an agent or a single prompt

## Question
Project 3 compared an agent with tools and a single prompt on 15 pages of documentation, and the single prompt was enough. It left one hypothesis open: on a much larger document, does an agent that searches the text with tools pay off? A 10-K runs to hundreds of pages (about 110,000 to 130,000 tokens for Apple, more for a bank), so this project tests that hypothesis with the same discipline: thresholds fixed before any model was run (`DESIGN.md`), a test set to tune the prompts, a validation set run once with the prompts frozen (`VALIDATION_FREEZE.md`), and an error log (`../evaluation/LOG.md`).

The deliverable is a sourced fact sheet per company: nine figures read, four computed ratios, segments, three risks, three questions the report does not answer, and the limits of the analysis. The blocking measure is a wrong figure presented as certain.

## Setup
- 10 US companies. Test: Apple, Johnson & Johnson, Exxon Mobil, Boeing, Starbucks, Tesla. Validation: Microsoft, Walmart, Nike, JPMorgan Chase (a bank, deliberately kept for validation so that no prompt was tuned on it).
- A key built from each report's financial statements, with the "not applicable" cases (for example operating income or net debt for a bank) fixed before any run.
- Methods: a keyword search with no AI (the floor), the whole report in one prompt, and an n8n agent with `search_report`, `read_statement` and a calculator (15 steps maximum). Models: Haiku 5.5 and Sonnet 5.5.
- Scoring by script (`evaluation/score.py`): figures read, figures computed, absent items flagged, wrong or invented figures, JSON validity.

## What happened on the test set (6 companies)
| Method | Read | Computed | Wrong figures | Strict JSON |
|---|---|---|---|---|
| Keyword search, no AI | 48/90 over the 10 companies | not computed | 30 over the 10 companies | n/a |
| Single prompt, Haiku | 53/54 | 23/24 | 2 | 6/6 |
| Single prompt, Sonnet | 53/54 | 23/24 | 2 | 6/6 |
| Agent v2, Haiku | 50/54 | 21/24 | 7 | |
| Agent v3, Haiku | 52/54 | 23/24 | 3 | 4/6 (6/6 after extraction) |
| Agent v3, Sonnet | 54/54 | 24/24 | 0 | 6/6 |

The agent needed three prompt versions to get here. The design allowed two per method, so this is declared as a deviation that favours the agent. The first agent batch also hit the 15-step limit on every company; running one company per execution fixed it, and I did not establish why.

## Validation (4 companies, prompts frozen, one run per method)
| Method | Read | Computed | Absent flagged | Wrong figures | Strict JSON | Cost, 4 companies |
|---|---|---|---|---|---|---|
| Agent v3, Haiku | 25/36 | 11/16 | 9/12 | 3 | 2/4 | about 0.05 USD |
| Single prompt, Haiku | 32/36 | 13/16 | 11/12 | 5 | 4/4 | about 0.57 USD |
| Agent v3, Sonnet | 35/36 | 15/16 | 11/12 | 2 | 4/4 | not measured (about 0.5 estimated) |
| Single prompt, Sonnet | 34/36 | 16/16 | 11/12 | 1 | 4/4 | 2.30 USD |

(The agent on Haiku hit the step limit on JPMorgan and returned no sheet; its missing nine figures count as not read. Keyword search on the same four: 17/36 read, 13 wrong.)

Applying the decision rule written beforehand (fewer wrong figures first, then accuracy, then cost, same model): the single prompt wins on both models. On Haiku the agent has fewer wrong figures but reads fewer figures; on Sonnet it has more wrong figures. No method reaches the target of zero wrong figures on validation, so the design's recommendation is systematic human review, and the best method is the single prompt on Sonnet 5.5, with one wrong figure (JPMorgan's cash, where the key says not applicable).

## Round 2: agent v2 (better tools, prompt v4b)
After round 1, I gave the agent a `read_section` tool (long sections such as the risk factors or the debt note, read in pages), a statement finder that avoids parent-company-only tables, and prompt v4b (net debt must not go in the debt field, finance leases are subtracted, revenue growth uses the same line in both years). Prompt v4 was worse than v3 on the test set (6 wrong figures against 3); v4b matched v3 (3 wrong) and was then run on the validation set.

| Agent v2 | Read | Computed | Absent flagged | Wrong figures | Strict JSON | Cost |
|---|---|---|---|---|---|---|
| Haiku 5.5 | 35/36 | 16/16 | 12/12 | 1 | 2/4 | about 0.12 USD for 16 runs (test sets included) |
| Sonnet 5.5 | 36/36 | 16/16 | 11/12 | 0 | 4/4 | about 0.43 USD for 4 companies |

On the same four companies, the Sonnet agent now beats the Sonnet single prompt (0 wrong figures against 1, for about a fifth of the cost), and the Haiku agent beats the Haiku single prompt (1 against 5). By the pre-written rule the agent v2 wins. I do not claim it as a clean result: the changes responded to errors seen on these companies, and the agent has had five prompt versions against one. On the test set, Haiku still puts net debt in the debt field for Apple and misses Boeing's finance leases. The next step is a clean holdout of new reports including a bank.

## What the numbers do not say on their own
- **The errors are concentrated on the bank.** On Microsoft, Walmart and Nike both Sonnet methods make no wrong figure, and the agent costs about four to five times less. That reading came after seeing the results and does not change the decision.
- **A long report fits.** JPMorgan's 1.59 MB report went through in a single call (about 552,000 input tokens). My assumption that it would exceed the window was wrong, so the "too long" measure counted zero reports.
- **The agent's weaknesses are about reading, not arithmetic.** It reached the right statements often but on the bank it pulled parent-company-only statements, found a revenue figure only in the management discussion, and picked risks from search snippets, which it said itself. The single prompt connects footnotes to statements because it sees the whole text.
- **Human check of risks (8 sheets, one reviewer).** Both methods' risks were rated faithful to the report (24 of 24). On "is this a top risk", the single prompt averaged 0.96 and the agent 0.63 (0.78 without the JPMorgan sheet). The reviewer correctly guessed the method of all 8 sheets, so the blind check was not blind: the agent's limits speak in the first person about its tools. See `evaluation/human_review_ratings.md`.

## Cost
Per company on the test set: single prompt about 0.09 USD (Haiku) and 0.38 USD (Sonnet); agent about 0.004 to 0.008 USD (Haiku) and 0.13 USD (Sonnet). Costs were derived from the account balance, and on validation from token counts at the model's price. The agent exposes no token usage in n8n, which is why its cost is read from the balance.

## Limits
10 companies and about 150 items; one reviewer; a key built from the same reports that are analysed; the agent had three prompt versions against the single prompt's one; the human check was not blind; the agent's round-1 cost on the validation set was not measured (round 2 was measured from the balance); some agent run files were saved by hand with shortened free text (figures, statuses and segments as returned); the keyword search was written once and never tuned. Hand-saved files are marked in each run file.

## Conclusion (round 1)
With the whole report affordable in one call, the single prompt remained at least as good as the agent: it made fewer wrong figures on validation and its risks were judged better. This confirms project 3's conclusion at the scale of a 10-K. The agent's advantage is cost, strongest when the report is a standard corporate one. Neither method removes the need for human review of a bank's sheet, and a wrong figure on a bank's cash is exactly what a reviewer must catch.

## Conclusion (round 2)
Round 1 favoured the single prompt; round 2 shows that part of the agent's gap came from its tools and prompt, not from the approach: with a section reader and tighter definitions the Sonnet agent reached 0 wrong figures at a fifth of the cost. Because the tuning used the same companies, the claim is limited to: the agent is competitive and much cheaper, and a clean holdout would settle it.

## Reproducing
Prompts in `prompts/`, the three n8n workflows in `workflow/`, reports in `data/10k/`, runs and scores in `evaluation/`. Prompt hashes and settings are in `VALIDATION_FREEZE.md`; results and the decision in `VALIDATION_RESULTS.md`.
