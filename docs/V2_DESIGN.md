# Agent v2 (project 4b): design, written before any v2 run

Date: 6 November 2026. Written before the v2 tools were built and before any v2 model run. Hash of this file: recorded in `evaluation/LOG.md` at the first v2 run.

## Why a second round
Project 4 found that the agent (v3) did not beat the single prompt on the validation set. Its errors came from what the tools let it see, not from arithmetic: `read_statement` returned parent-company-only statements for the bank, risks were chosen from 700-character snippets, and nothing let the agent read a whole section. The author's goal is to show agents that help financial analysts study companies, so this round tests whether better tools close the gap.

## What changes
1. **`read_statement` v2**: finds a statement by its row labels and table header instead of its title (titles sit after the table in some filings, such as JPMorgan's), prefers consolidated statements and refuses parent-company, condensed and quarterly tables.
2. **New tool `read_section`**: returns a whole section of the report, in pages of 9,000 characters, for `risk_factors` (Item 1A), or any heading keyword (for example `long-term debt`, `segment`). Page number given by `offset`.
3. **Agent prompt v4** = v3 plus: the tool list; "read the consolidated statements, never parent-company-only statements"; "choose the three risks after reading the first page of `risk_factors`, not from search snippets"; and, for a bank or insurer, "operating income, capex, free cash flow, cash (as defined) and net debt are not_applicable".
4. Same model settings as v3 (Haiku 5.5 thinking disabled; Sonnet 5.5 adaptive), same step limit (15), one company per execution.

Not in this round: credit ratios (leverage, interest coverage). They need new items in the key and will be a separate step.

## Declared contamination
The validation set was already seen. The v4 changes (parent-company statements, snippet-based risks, the bank rule for cash) respond to errors observed on it, so **v4's validation score is exploratory, not a clean holdout.** In particular the bank rule is written with JPMorgan's key in mind. To obtain a clean result, 4 further companies (including one bank) can be added: their 10-Ks must be supplied by the author, the prompts frozen as they are after the test set, and each method run once. This document does not assume they will be added.

## Protocol
1. **Tool test (free, no model).** For each of the 10 reports and each of the three statements, the tool output must contain the key's printed value: income = revenue and net income and diluted EPS; balance = total equity (and cash when the key has it); cash flow = operating cash flow. 30 checks (fewer for not-applicable items). Report v1 and v2 results side by side.
2. **Test set (6 companies), agent v4 on Haiku**, at most 2 prompt versions of v4 (v4, then v4b if needed). The prompt is frozen after the test set.
3. **Validation (MSFT, WMT, NKE, JPM), v4 frozen**, Haiku then Sonnet, one run per company. Reported as exploratory.
4. **Comparison** with the v3 agent and the single prompt, same measures as project 4 (wrong figures first, then accuracy, then cost). Same scoring script and key.
5. **Success for v4**, written now: at most 1 wrong figure on the 4 validation companies on Sonnet (as good as the single prompt), JPMorgan sheet produced on both models, risks rated at least as good as the single prompt's in a new human check. If not reached, it is published as is.

## Budget
Haiku run on the test set about 0.05 USD; Sonnet runs about 0.15 USD per company. Estimated total under 2 USD. Balance at the start: 4.36 USD.

## Limits stated now
Same one-reviewer, small-sample limits as project 4; tools and prompt developed by the same person who knows the validation answers; the new human check cannot be blind to the agent's wording unless the first-person tool remarks are removed from the limits before the reviewer sees them.
