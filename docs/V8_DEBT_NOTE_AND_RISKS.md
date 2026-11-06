# Improvements after the comparison work: risk factors finder and debt note check

## 1. Risk factors finder (tool code, no model cost)

Problem: `read_section("risk_factors")` returned "Section not found" on four of the 23 reports (Honeywell, McDonald's, GE, Wells Fargo). These reports print a plain heading "Risk Factors" and no "Item 1A" heading, so the agent had to rely on search snippets.

Fix (`workflow/report_tools_v2.js`, also in the n8n sub-workflow): a fallback is used only when the "Item 1A" method finds nothing. It looks for a heading "Risk Factors" on its own line and ends the section at the next standard heading (cybersecurity, properties, legal proceedings, controls and procedures).

Check, offline on all 23 reports: the four reports now return a section of 47,000 to 105,000 characters (GE 62,000, HON 105,000, MCD 47,000, WFC 100,000); the 19 other reports use the old method and are unchanged. The content of the four sections was not read line by line, and the agent was not re-run on them.

## 2. Prompt v8: always check the debt note (REJECTED after validation, see docs/V8_VALIDATION.md)

Problem: on Lockheed Martin the v7 agent wrote in its limits that it had not read the debt note, so finance leases inside the debt captions could have gone unnoticed.

Change (`prompts/agent_system_prompt_v8.txt`): before reporting `total_financial_debt`, the agent must check the debt note once (search or read_section "debt"), take borrowings alone if finance leases are included, and say in the note which numbers it used and that the note was checked.

Test (one run, Lockheed Martin, about 0.15 USD, 16 tool calls, inside the 15-step budget of the model loop): 9/9 figures and 4/4 ratios correct, 0 wrong, and total financial debt 21,700 as in the key. The agent now states that the debt note was checked and that the report mentions no significant finance leases.

Limits of this test:
- One company only. Lockheed Martin has no finance leases in its debt, so the test shows the agent still reports the right figure and says it checked; it does not show that it subtracts finance leases correctly when they exist.
- The agent still wrote in its limits that "no separate debt-note table was read in full": it checked the note through search snippets, not by reading the whole note. A stricter rule (read_section on the debt note) would cost one more step.
- v8 is not yet validated on a company with finance leases inside the debt captions.

Run file: `evaluation/runs/LMT_agent_v8_sonnet-5-5_debtnote.json`.
