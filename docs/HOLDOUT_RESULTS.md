# Holdout results (BAC, VZ, CAT, KO), frozen in docs/HOLDOUT_FREEZE.md

Each method ran once per company. Scores: `evaluation/scores_holdout_*.md`. Runs: `evaluation/runs/*_holdout.json`.

| Method | Read | Computed | Absent flagged | Wrong or invented | Strict JSON | Cost, 4 reports |
|---|---|---|---|---|---|---|
| Agent v2 (prompt v4b), Haiku 5.5 | 26/36 (BAC: step limit, no sheet) | 12/16 | 8/8 | 1 | 2/3 | a few cents |
| Single prompt, Haiku 5.5 | 33/36 | 14/16 | 10/11 | 5 | 4/4 | 0.66 USD (tokens x price) |
| Agent v2 (prompt v4b), Sonnet 5.5 | 34/36 | 15/16 | 11/11 | 3 | 4/4 | about 0.8 USD for all 8 agent runs (balance 3.81 to 2.93), Sonnet share about 0.7 |
| Single prompt, Sonnet 5.5 | 33/36 | 15/16 | 11/11 | 4 | 4/4 | 2.65 USD (tokens x price) |

Absent counts exclude the CAT guidance question (the report has 2026 expectations; see the freeze).

## Errors
- **Verizon, all four methods that returned a sheet:** equity 104,460 against the key's 105,741. The balance sheet prints only "Total equity" (including 1,281 of noncontrolling interests); the models subtract them, as the prompt asks. On Sonnet both methods also subtract Verizon's finance leases (2,511) from the debt, which the prompts' definitions ask for ("do not include lease liabilities"), giving 155,639 against the key's 158,150, and a net debt that follows. The key was frozen before the runs and sums the printed captions, so these count as wrong. Both are ambiguities of the key, not clear model errors.
- **BAC, single prompt:** invents a cash figure (231,845, Sonnet and Haiku) and a net debt (Haiku) for a bank, where the key says not applicable. The agent on Sonnet marked them not applicable, with the right reference note.
- **KO, single prompt Haiku:** debt 46,492 against 45,492 and the net debt that follows (a one-million slip).
- **BAC, agent Haiku:** step limit reached, no sheet (one report out of four; the same failure as JPMorgan with agent v3).

## Decision rule (docs/DESIGN.md section 7), same model
- **Sonnet:** the agent has fewer wrong figures (3 against 4), reads at least as many (34 against 33), and costs about a quarter of the price (about 0.7 against 2.65 USD). The agent wins. Without Verizon's key ambiguities, it has 0 wrong figures against 1.
- **Haiku:** the agent has fewer wrong figures (1 against 5) but reads fewer (26/36 against 33/36), because of the missing BAC sheet, so it is not at least as good on accuracy. The single prompt wins, as in round 1.

## Reading it honestly
- Four companies and one run each: the Sonnet gap (3 against 4) is one figure, driven by a bank cash item. Do not read more into it than "the agent is at least as accurate and costs several times less".
- The holdout was chosen on purpose to be hard, with a second bank and heavy leases; it was fixed before the runs, with the key conventions and their known weaknesses.
- The agent prompt has had five versions against the single prompt's one; the holdout was not used to change any prompt or tool.
- Hand-saved agent run files have shortened free text; figures, statuses, segments, risks and absent answers are as returned.
- Not done: a blind human check of risks on the holdout sheets (the keyword proxy in the scores is 0/3 for all, because no risk reference was written for these four).
