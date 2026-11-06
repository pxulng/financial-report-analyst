# Evaluation log

Dated entries, in order. Nothing is edited after the fact; corrections are new entries.

## 2026-11-05: cost measurement, Apple, reference 2 (single prompt), prompt v1

Workflow: `workflow/` (n8n, reference 2). Prompt: `prompts/reference2_system_prompt.txt` v1 (sha256 `7a7d5b55…a8971d`). Report: `data/10k/AAPL_10-K_FY2026.md`.

| Model | Input tokens | Output tokens | Stop | JSON | Cost (account balance) |
|---|---|---|---|---|---|
| Haiku 5.5 | 151,734 | 4,324 | end_turn | valid | about 0.09 USD (2.07 to 1.98) |
| Sonnet 5.5 | 151,734 | 3,728 | end_turn | valid | about 0.34 USD (6.98 to 6.64) |

Outputs: `evaluation/runs/`. These two runs count as the first pass of prompt v1 on the test set (Apple). They are not scored yet: the key was built after the runs, from the report only (see below).

Declared limit: the author saw the Haiku output before the Apple key and the Apple risk reference list were written. The Apple figures key is taken from the statements by script, independently of the model output; the Apple risk list will be flagged as written after seeing one output.

## 2026-11-05: figures key built

`evaluation/build_key.py` locates each figure in the financial statements of the report (label and printed value must appear together) and computes the derived items with the frozen formulas. Result: `evaluation/key.json`. No model had been run on the nine other companies when the key was built.

Choices made while applying the frozen definitions (to confirm or overrule before the validation run):

- **Not applicable operating income:** Nike, Johnson & Johnson, ExxonMobil and JPMorgan do not publish an "operating income" line, so the item and the operating margin are not applicable for them. Boeing publishes "Earnings from operations" and Tesla "Income from operations": read as operating income.
- **JPMorgan:** operating income, capex and cash are not applicable (no "cash and cash equivalents" line; the balance sheet shows "cash and due from banks" and "deposits with banks"). Free cash flow, net debt and operating margin follow. Total financial debt is read as short-term borrowings plus long-term debt.
- **ExxonMobil revenue:** "Total revenues and other income" (332,238), the only total line. Equity is "ExxonMobil share of equity".
- **Walmart revenue:** "Total revenues" (713,163), which includes membership income; net sales are 706,413.
- **Tesla debt:** the balance sheet line combines debt and finance leases; the debt note gives "Total debt" (1,569 current and 6,584 long-term), finance leases excluded as defined.
- **Starbucks equity:** negative (shareholders' deficit, -8,096.6). **Boeing equity:** 5,454 (Boeing shareholders), total equity 5,457.
- **Johnson & Johnson debt:** "Loans and notes payable" plus long-term debt.

Check sample for the author (20 %): `evaluation/KEY_CHECK_SAMPLE.md`.

## 2026-11-05: risk reference list

`evaluation/risks_reference.py` and `risks_reference.json`: three major risks per company, each with keywords. A risk is "grounded" when one of its keywords appears at least three times in the 10-K file (all 30 are). The list was written from the companies' risk-factor sections and general knowledge of their business, before the nine other companies were run.

Declared limit: the Apple list was written after the author and Claude had seen one Haiku output for Apple, whose three risks (supply constraints, concentrated manufacturing, antitrust litigation) overlap with the reference list. Apple's risk score therefore carries a bias in favour of the models and will be reported with that note. Scoring of a model's risk against the list is by topic, not by wording; it is done by a human reader for the test set and spot-checked on validation.

## 2026-11-05: test set, reference 2 (single prompt), prompt v1, Haiku 5.5, five companies

A first launch processed one company only (n8n executed the prompt-fetch step once for the whole list); the workflow was reordered and rerun. Johnson & Johnson was therefore run twice; the outputs kept are from the second run (execution 53).

| Company | Input tokens | Output tokens | Stop | JSON |
|---|---|---|---|---|
| JNJ | 171,226 | 5,101 | end_turn | valid |
| XOM | 178,223 | 7,019 | end_turn | valid |
| BA | 161,264 | 5,819 | end_turn | valid |
| SBUX | 120,445 | 4,758 | end_turn | valid |
| TSLA | 220,277 | 4,696 | end_turn | valid |

No report was too long for the window. Outputs: `evaluation/runs/`. Not scored yet. Cost from the account balance: to be added.

## 2026-11-05: key check by the author

13 of the 17 sampled figures confirmed, no error found. 4 could not be located by the author (three of them are sums of several debt lines or a line named differently) and were rechecked by Claude only. Deviation from the rule "the author checks the whole 20 % sample" is declared here.

## 2026-11-05: cost of the Haiku test pass

Balance 6.64 to 6.04 USD for six Haiku runs (five companies, Johnson & Johnson twice): about 0.10 USD per report. Consistent with Haiku 5.5 at about 0.50 USD per million input tokens and 2.50 per million output tokens; Sonnet 5.5 (0.34 USD for Apple) then comes out near 2 and 10 USD. Prices are inferred from balances, not read from a price list.

## 2026-11-05: scoring, test set pass 1, reference 2 (prompt v1), Haiku 5.5

Script: `evaluation/score.py`; table: `evaluation/scores_test_pass1_haiku.md`. Scoring rules as in `docs/DESIGN.md`. Risks are scored by a keyword proxy only for now; the human reading comes later. Measure 5 (source) is implemented in a weaker form than designed: the script checks that the value given appears somewhere in the report, not in the cited section.

Result: figures read 53/54 (98.1 %), computed 23/24 (95.8 %), absent items 18/18, JSON valid 6/6, wrong or invented figures: 2 (both Exxon revenue, one cause).

Findings:

1. **Key correction (Boeing debt), made after seeing the model output.** The first key took the balance-sheet debt (54,098), which includes finance lease obligations; the definition excludes them. Haiku read 53,848 and cited the company's own line "Debt, excluding finance lease obligations" (line 4282 of the file), which is exactly the frozen definition. The key now uses that line; Boeing net debt follows (42,927). This correction favours the model on this item and is declared as such. The scoring script showed 4 errors before the correction and 2 after it.
2. **Exxon revenue is a definition ambiguity, not corrected.** The key uses "Total revenues and other income" (332,238); Haiku used "Sales and other operating revenue" (323,905) and said so in its note. Both readings fit the wording "total sales or total revenues line". The key is left as it is and the error counts; the ambiguity is reported next to the score. Revenue growth inherits the difference.
3. **Exxon debt:** Haiku and the key agree (43,537) but both include finance lease obligations that Exxon does not break out; Haiku flagged it in its limits. The strict definition cannot be applied to this report.

## 2026-11-05: reference 1 (keyword search, no AI)

`baseline/reference1_keyword_search.py`: one fixed list of label patterns for all companies, first line that matches and carries a number. Written once and not tuned after seeing results (frozen as of this entry). It was run on all 10 companies at once, validation included, because it uses no model and no prompt that could be tuned on them.

Figures read correct: 48/90 (53 %); wrong numbers presented as found: 30 over 10 companies. It cannot say "not applicable" or "absent", and does no computation, so only the nine figures read are scored. Outputs: `evaluation/runs/*_reference1_keywords.json`. This is the floor of the study.

## 2026-11-05: agent v1, Apple, Haiku 5.5 (first test)

Agent: n8n AI Agent node, tools `search_report`, `read_statement` (a sub-workflow that fetches the report from GitHub and searches or extracts a statement) and a calculator; 15 iterations maximum; prompt `prompts/agent_system_prompt.txt` v1 (sha256 `650b0c75…811c9`).

First launch (execution 54): all tool calls failed because the sub-workflow was not published; the agent answered honestly that it could not read the report and filled nothing in. Not counted. Sub-workflow published, second launch (execution 55):

- 12 tool calls (3 statements, 5 searches, 4 calculator), well under the 15 limit.
- The final answer is **not valid JSON**: the model wrote a truncated item (`"net_debt", "value": 44...}`) and a confused note on total debt (it first put net debt in the debt field, then talked itself out of it in the note). Counts as an invalid JSON for measure 7.
- Tokens are not reported by the agent node; the cost is read from the account balance.
- Run kept in `evaluation/runs/AAPL_agent_v1_haiku-5-5.json`. It uses one of the two prompt versions allowed on the test set for the agent only if the prompt is changed; this is the first version.

## 2026-11-05: agent v1, five companies, Haiku 5.5: all reached the iteration limit

Execution 64 (JNJ, XOM, BA, SBUX, TSLA, prompt `agent_system_prompt.txt` v1): all five agents stopped on "Max iterations (15) reached" with no sheet. Measure 8 fails 5/5 and no figure can be scored. Cause not established: Apple (execution 55) and a diagnostic Exxon run needed only 5 model steps (13 tool calls batched), so the failure may come from running the five agents at once; this is checked on the next run.

Diagnostic (execution 223, Exxon alone, limit raised to 30, not scored, not kept as a result): the agent finished in 5 steps, but (a) its final message began with a paragraph of prose before the JSON, which breaks the format ("answer with one JSON object only"); (b) one calculator input was garbled (`(328? )`), another divided income before tax by total revenue, a figure that is not an operating margin; the model corrected itself in the final sheet; (c) the Apple run of execution 55 ended with a truncated item ("value": 44...).

Decision: agent prompt v2 (`prompts/agent_system_prompt_v2.txt`, sha256 `c24c3fb7…81a9c`; the first of the two versions allowed on the test set after v1): efficiency instructions (call independent tools in the same step, one search per topic, one calculation per computed item) and a strict last-message rule (starts with `{`, no prose, no abbreviation). The iteration limit stays at 15. Scoring: JSON validity is reported strictly (prose before or after the object counts as invalid, as in the frozen format) and the figures are also scored from the extracted object so that accuracy is not hidden by format; both are published.

## 2026-11-05 - Agent prompt v2, Haiku 5.5, 6 test companies (n8n execution 232)
- Result: 6/6 runs stopped at the 15-iteration limit (90 model calls = 15 per company). No fact sheet produced for any company (0/6 valid JSON, strict or lenient).
- The prompt v2 instructions (parallel calls, at most 15 steps) did not change the behaviour. The Reading node reports no tool-call count (agent node does not expose it), so tool usage is unknown for this run.
- Prompt v2 therefore failed; one more prompt version is allowed under the protocol. Cause not yet established: need the per-step trace of one run before changing anything.

### Diagnostic 2026-11-05 (n8n execution 419)
- Same agent (prompt v2, Haiku 5.5), XOM alone: finished in about 20 s, 4 model steps, 11 tool calls (3 read_statement, 4 search_report, 4 Calculator), strict-valid JSON.
- So the 6/6 iteration-limit failures of execution 232 (and of the v1 5-company run) come from running several companies in one execution, not from the prompt. Cause inside n8n not established. Protocol change: one execution per company. The prompt is unchanged, so this is not a new prompt version.
- XOM run file was saved by hand from the execution output: free-text fields (notes, risk sentences) are shortened; figures, statuses, segments and absent answers are as returned.

## 2026-11-05 - Agent prompt v2, Haiku 5.5, test set, one execution per company (executions 419/427/436/443/450/457)
Scores: scores_test_pass2_agent_v2_haiku.md. Each company took about 20 s, 3-4 model steps, 10-12 tool calls. No iteration-limit hit when run alone.
- JSON: strict 5/6 valid; JNJ had two prose paragraphs before a fenced JSON block (valid after extraction: 6/6).
- Read figures 50/54 (92.6%), computed 21/24 (87.5%), absent questions 18/18, wrong or invented figures: 7.
- Reference 2, Haiku, prompt v1 (for comparison): read 53/54, computed 23/24, absent 18/18, wrong 2.
- The 7 errors: AAPL total debt (agent wrote 43,806 = net debt in the value field and corrected it to 80,111 only in "limits": counts as wrong); BA total debt and net debt (54,098 vs key 53,848: finance leases included, 250 gap); TSLA total debt and net debt (8,376 vs key 8,153: the balance sheet merges debt and finance leases; the agent flagged it); XOM revenue and growth (323,905 "Sales and other operating revenue" vs key 332,238 "Total revenues and other income": the XOM ambiguity already logged).
- Reading: on this test set the agent is less accurate than the single prompt on Haiku with prompt v1, and also needs a harness workaround (one execution per company). Run files were saved by hand from the n8n output: long free-text fields were shortened, figures/statuses/segments/risks are unchanged.
- score.py: now tolerates run files without token counts (agent node exposes none).
- Not yet measured: cost of this pass (to be derived from the account balance).
- Cost of the single-company agent pass (diagnostic XOM + 6 runs = 7 executions): balance 5.54 -> 5.51 USD, about 0.03 USD in total, roughly 0.004 USD per company on Haiku 5.5 (balance rounded to 0.01, so +/- 0.01). The failed 6-company run (execution 232) cost about 0.14 USD (5.68 -> 5.54): the loop made it about 6 times dearer than a normal run.

## 2026-11-05 - Agent prompt v3 (last allowed version on the test set)
- File prompts/agent_system_prompt_v3.txt, sha256 103573f4dbd359cdd38ae681750df95e056303d81a30cb8b6b944eca0fa23365. Two additions to v2: (1) every value field must hold the final correct number, computed items consistent with reported figures, no provisional value corrected later in notes; (2) if the balance sheet merges debt and finance leases, search the debt note once to find the borrowings alone; (3) the last message must have no sentence, heading or code fence around the JSON.
- Definitions are unchanged on purpose (same as reference 2), so the XOM revenue ambiguity is not addressed.
- Runs: one execution per company, same 6 test companies, Haiku 5.5.

## 2026-11-05 - Agent prompt v3, Haiku 5.5, test set (executions 464/471/480/488/496/503) - scores_test_pass3_agent_v3_haiku.md
- Read 52/54 (96.3%), computed 23/24 (95.8%), absent 18/18, wrong or invented 3. JSON strict 4/6 (JNJ and BA had a prose paragraph before the JSON despite the v3 instruction), 6/6 after extraction.
- Versus v2: read 50 -> 52, computed 21 -> 23, wrong 7 -> 3. Versus reference 2 Haiku v1: read 53/54, computed 23/24, wrong 2.
- Remaining wrong: AAPL total debt 43,806 (key 80,111; the note text even says the sum of the three lines; v3 did not fix it, the agent did not run the extra debt-note search either); BA total debt and net debt (54,098/43,177 vs key 53,848/42,927: finance leases, the agent says it did not search the debt note).
- Fixed by v3: TSLA debt (searched Note 9, removed finance leases: 8,153 = key; 18 tool calls, the only run above 13). XOM revenue now matches the key, but it flipped back and forth between v2 and v3 with an unchanged definition, so it is run-to-run variation, not a v3 effect.
- Tool use: 10-13 calls per company, TSLA 18. No iteration-limit hit.
- Caveat: one run per company, so differences of 1-2 figures between versions are within run-to-run noise (XOM revenue shows it). The test set is now closed for the agent (v1, v2, v3 used). The frozen design allows at most 2 prompt versions per method, so v3 is a third version: the miscount (I told Paul one version remained after v2) is declared here. v1 never produced a usable full test run, but it still counts. The v3 result is therefore reported as exploratory; the validation run will use v3 and the 3-version count will be stated in the case study..
- Cost of v3 pass (6 runs): balance 5.51 -> 5.46 USD, about 0.05 USD, roughly 0.008 USD per company on Haiku 5.5 (rounded to 0.01).

## 2026-11-05 - Reference 2 (single prompt v1), Sonnet 5.5, test set (JNJ XOM BA SBUX TSLA in execution 513; AAPL from the earlier cost run) - scores_test_pass1_sonnet.md
- Read 53/54 (98.1%), computed 23/24 (95.8%), absent 18/18, wrong or invented 2, JSON valid 6/6. Same totals as Haiku with the same prompt.
- The only errors are XOM revenue and revenue_growth (323,905 "Sales and other operating revenue" vs key 332,238): the XOM definition ambiguity already logged, not a reading error.
- Tokens (5 companies): about 851k input and 19.6k output; at the inferred Sonnet price (2 / 10 USD per million) about 1.9 USD, i.e. about 0.38 USD per company, versus about 0.09 for Haiku. To be checked against the balance.
- Measured cost: balance 5.46 -> 3.56 USD = 1.90 USD for the 5 companies of execution 513, i.e. 0.38 USD per company with Sonnet 5.5 (the 2.24 USD token estimate above included the AAPL run done earlier). Cumulative spend stays below 10 USD.

## 2026-11-05 - Agent prompt v3, Sonnet 5.5, test set (executions 515/524/534/541/549/556) - scores_test_pass3_agent_v3_sonnet.md
- Setting change versus Haiku: Sonnet 5.5 refuses "thinking disabled" (first attempt, execution 514, failed at once with an API error); the model node uses thinking mode "adaptive". Haiku runs had thinking disabled. The single-prompt Sonnet runs used the Anthropic node default.
- Read 54/54, computed 24/24, absent 18/18, wrong or invented 0, JSON strict valid 6/6, no iteration-limit hit; 10-13 tool calls per company; BA and TSLA both ran the debt-note search and removed finance leases (53,848 and 8,153 = key). XOM took "Total revenues and other income" (key) and flagged the ambiguity in its notes.
- Versus Sonnet single prompt (v1): read 53/54, computed 23/24, wrong 2 (XOM revenue). Versus Haiku agent v3: read 52/54, wrong 3.
- Caveat: one run per company; XOM revenue has flipped between runs of the same prompt, so a 0 vs 2 difference on one ambiguous line is not conclusive.
- Cost of this pass: to be derived from the balance (before: 3.56).
- Cost of agent v3 Sonnet test pass: balance 3.56 -> 2.78 USD = 0.78 USD for 6 companies, about 0.13 per company (Sonnet agent is about 16 times dearer than Haiku agent).

## Validation pass 1: agent v3, Haiku 5.5 (executions 565, 572, 580, 589)
Frozen prompt v3, one execution per company, no change between runs.
- MSFT: 9/9, 4/4, 0 wrong. WMT: 8/9, 4/4, 1 wrong (value field 45,162 against 44,762 in the agent's own note and in net_debt). NKE: 8/9, 3/4, 2 wrong (derived operating income presented as found; the key says not applicable); strict JSON invalid because two sentences precede the fenced block, valid after extraction.
- JPM: the agent hit the 15-step limit and returned no sheet. Counted as a failure, not retried (frozen protocol).
- Hand-saved files: free text shortened, figures as returned. Scores in `scores_validation_agent_v3_haiku.md`.

## Validation pass 2: single prompt (reference 2 v1), Haiku 5.5 (executions 612, 613)
Frozen prompt, no change. MSFT, WMT, NKE in one batch (612); JPM alone (613, measure 9).
- MSFT 9/9, 4/4, 0 wrong. NKE 9/9, 4/4, 0 wrong. WMT 8/9, 3/4, 2 wrong (total_financial_debt 44,304 against 44,762, and the net_debt that follows).
- JPM: the 1.59 MB report did go through in a single call (552,576 input tokens, answer valid JSON), so the window assumption was wrong: measure 9 outcome is "accepted". The sheet is poor, though: cash 21,742 and net_debt 477,251 presented as found (key: not applicable), total_financial_debt 500 (key 499,982), capex and free cash flow not_in_report where the key says not applicable. 3 wrong figures, read 6/9.
- Totals over the 4 companies: read 32/36, computed 13/16, absent 11/12, wrong or invented 5. Strict JSON 4/4.
- Tokens: 1,059,267 in, 17,063 out, about 0.57 USD at Haiku prices. Scores in `scores_validation_reference2_haiku.md`.

## Validation pass 3: agent v3, Sonnet 5.5, thinking adaptive (executions 614, 621, 630, 638)
Frozen prompt v3, one execution per company.
- MSFT 9/9, 4/4, 0 wrong. WMT 9/9, 4/4, 0 wrong. NKE 9/9, 4/4, 0 wrong (operating income and margin not_applicable, as the key says).
- JPM: finished in 14 tool calls with valid JSON (Haiku failed at the step limit on the same company). 8/9, 3/4, 2 wrong: cash and net_debt given as found where the key says not applicable. Risks were weakly supported by the agent's own admission.
- Totals: read 35/36, computed 15/16, absent 11/12, wrong 2, strict JSON 4/4. Scores in `scores_validation_agent_v3_sonnet.md`.

## Validation pass 4: single prompt (reference 2 v1), Sonnet 5.5 (executions 650, 651)
Frozen prompt. MSFT, WMT, NKE in one batch (650); JPM alone (651).
- MSFT, WMT, NKE: 27/27 read, 12/12 computed, 0 wrong.
- JPM: accepted in a single call (552,576 input tokens), valid JSON. 7/9, 4/4, 1 wrong (cash 21,742 presented as found; key: not applicable); total_financial_debt marked not_applicable (key 499,982), absent 2/3.
- Totals: read 34/36, computed 16/16, absent 11/12, wrong 1, strict JSON 4/4. Tokens 1,059,267 in / 18,086 out, about 2.30 USD at Sonnet prices. Scores in `scores_validation_reference2_sonnet.md`.

## Validation summary
Paul's balance after the Sonnet single-prompt passes: 4.36 USD (6.66 after top-up), so the single-prompt Sonnet pass cost 2.30 USD, equal to the token-based estimate. The agent Sonnet validation cost cannot be read from the balance (top-up in between); estimated from the test set. Decision and caveats in `docs/VALIDATION_RESULTS.md`.

## Blind human check (8 sheets, Sonnet, validation set)
Ratings received; results and key in `human_review_ratings.md`. Faithful 24/24 both methods; top-risk mean single prompt 0.96, agent 0.62. The reviewer identified the method of all 8 sheets, so the blinding failed (agent limits speak in the first person about tools).

## 2026-11-06: agent v2 (project 4b), tools and prompt v4
Design written first: `docs/V2_DESIGN.md` (SHA-256 925c8ec9b26ac5cdb618ad45700b728975d20b0e13837c15315b7d4d583102bf).
- Free tool test (`workflow/tools_test/tool_test.js`, 59 checks: does the statement the tool returns contain the key's printed values, 10 reports x 3 statements): tools v1 (project 4) 56/59 (failures: JPMorgan income statement and cash flow); tools v2 first version 49/59; v2 after three code iterations on these same checks 59/59. Declared: the tool code was tuned on the 10 reports it is tested on, and one pick (JPMorgan balance sheet) first returned the parent-company statement while still passing the check, found by reading the output and fixed with a nearby-heading rule.
- `read_section` checked by hand on the 10 reports: the risk-factors span (Item 1A to Item 1B) is found correctly for all 10 (88,100 to 112,271 characters for the large ones).
- Prompt v4 = v3 plus the `read_section` tool, "read the first page of the risk factors", "use consolidated statements, never parent-company", and the bank rule. File `prompts/agent_system_prompt_v4.txt`, SHA-256 e4e8d8ac97cbeaa37b5ed38c6364b2091c23e2ead620e8c73485cb36362be1b6.

## Agent v2 (prompt v4, tools v2), test set, Haiku 5.5 (thinking disabled), 2026-11-06
Six runs, one company per execution (AAPL 652, JNJ 661, XOM 669, BA 676, SBUX 684, TSLA 691). Scores in `scores_test_agent_v4_haiku.md`.
- v4: read 51/54, computed 21/24, absent 18/18, 6 wrong. v3 on the same set: read 52/54, computed 23/24, 3 wrong.
- Wrong values: AAPL debt (net debt written in the debt field), BA and TSLA debt (finance leases included or excluded differently from the key, gaps of 250 and 24), XOM revenue growth (computed on the sales line, not the total revenue line).
- Strict JSON failed on JNJ and XOM (reasoning text before the fence); lenient extraction valid.
- Result: v4 is not better than v3 on the test set. Decision on a v4b is pending (maximum one more prompt version, per docs/V2_DESIGN.md).
