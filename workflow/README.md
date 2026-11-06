# n8n workflows

Four workflows, exported without credentials or instance ids. Import in n8n (Workflows, Import from file), attach your own Anthropic credential, then replace the placeholder ids (`<ID of ...>`) with the ids n8n gives the imported workflows. Import order: report-tools sub-workflow, agent, compare.

- `single_prompt_reference2.json`: reference 2. Fetches the frozen prompt and one 10-K from this repository, sends both in one model call, then checks the JSON. Edit the `Reports` node to run a subset. Model used in the study: Haiku 5.5 or Sonnet 5.5 (change the model in `Message a model`).
- `report_tools_subworkflow.json`: the three report tools (keyword search, a statement as printed, a section in pages of 9,000 characters). It fetches the report from `data/10k/` on GitHub. The code is also in `report_tools_v2.js`. 23 reports are supported.
- `agent_with_tools.json`: the agent for ONE company. AI Agent node (step limit 15) with four tools: `search_report`, `read_statement`, `read_section` (these three call the sub-workflow; set its id in the three tool nodes) and a calculator. It fetches prompt v9 from `prompts/` on GitHub. It can be run by hand (`Run`, edit the `Reports` node) or called by another workflow (`When called`, with one item `{ "id": "LMT" }`). Settings used: Sonnet 5.5 with adaptive thinking.
- `compare_companies.json`: the parent workflow for comparing companies. It takes a list of tickers (node `Tickers`), calls the agent workflow once per ticker (`Execute Workflow`, mode "each"), then the `Compare` node builds a side-by-side table with a comparability flag per row. `compare_node.js` holds the same code. The Excel version of the comparison is produced by `tools/compare_excel.py`.

Why one agent run per company: with several companies in ONE execution, the AI Agent node answered "Bad request" on the second item (cause not found), in this study and with this node version. Calling the agent once per company from a parent workflow avoids it.

The node `Reading` parses the answer and reports strict JSON validity (and a lenient extraction, reported separately).
