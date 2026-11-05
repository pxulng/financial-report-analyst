# Validation results (MSFT, WMT, NKE, JPM), prompts frozen before the run

Each method was run once per company. Scores: `evaluation/scores_validation_*.md`. Runs: `evaluation/runs/*`.

| Method | Figures read | Computed | Absent flagged | Wrong or invented (measure 1) | Strict JSON | Cost, 4 companies |
|---|---|---|---|---|---|---|
| Agent v3, Haiku 5.5 | 25/36 (JPM: no sheet, counted as 0 of 9) | 11/16 | 9/12 | 3 | 2/4 (3/4 after extraction) | about 0.05 USD (balance) |
| Single prompt, Haiku 5.5 | 32/36 | 13/16 | 11/12 | 5 | 4/4 | about 0.57 USD (tokens x price) |
| Agent v3, Sonnet 5.5 | 35/36 | 15/16 | 11/12 | 2 | 4/4 | not measured (see below) |
| Single prompt, Sonnet 5.5 | 34/36 | 16/16 | 11/12 | 1 | 4/4 | 2.30 USD (tokens x price, matches the balance drop 6.66 to 4.36) |

Agent Haiku on JPM stopped at the 15-step limit (measure 8: one report, which is the acceptable maximum). Counting JPM's missing sheet as 9 figures not read, its read rate is 25/36.

## Decision rule (docs/DESIGN.md, section 7), same model

- **Haiku:** the agent has fewer wrong figures (3 against 5) but reads fewer figures (25/36 against 32/36), so it is not "at least as good" on rule 2. The single prompt wins.
- **Sonnet:** the agent has more wrong figures (2 against 1), so it fails rule 1. The single prompt wins.
- **Recommended model:** no method reaches measure 1's validation target of 0 wrong figures. The design says: systematic human review. The best method on this validation is the single prompt on Sonnet 5.5 (1 wrong figure, JPM cash).

## Reading the result honestly

- Every error of the two Sonnet methods is on JPM, a bank where the key marks several items not applicable. On MSFT, WMT and NKE both Sonnet methods have 0 wrong figures, and the agent costs about four to five times less. That observation was made after seeing the results; it does not change the decision above.
- Single prompt on JPM (measure 9): the 1.59 MB report fits in one call (552,576 input tokens), so no report was too long. The earlier assumption was wrong.
- The agent prompt went through three versions against two allowed (declared in LOG.md); the single prompt stayed at version 1. This favours the agent, and it still does not win.
- Agent Sonnet cost: not measured on validation, because the account was topped up in between. Test-set measure for reference: about 0.13 USD per company, so roughly 0.5 USD for the four.
- Hand-saved agent runs have shortened free text; figures, statuses, segments, risks and absent answers are as returned.
- Still to do: blind human check of risks and limits on 8 sheets, measure 5 (cited figure appears in cited section), export of the n8n workflows.
