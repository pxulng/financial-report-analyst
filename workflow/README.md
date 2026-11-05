# n8n workflows

Three workflows, exported without credentials or instance ids. Import in n8n (Workflows, Import from file), attach your own Anthropic credential.

- `single_prompt_reference2.json`: reference 2. Fetches the frozen prompt and one 10-K from this repository, sends both in one model call, then checks the JSON. Lists the 10 companies; edit the `Reports` node to run a subset. Model used in the study: Haiku 5.5 or Sonnet 5.5 (change the model in `Message a model`).
- `agent_with_tools.json`: the agent. AI Agent node (step limit 15) with three tools: `search_report`, `read_statement` and a calculator. The two report tools call the sub-workflow `report_tools_subworkflow.json` (import it first, then set its id in the `search_report` and `read_statement` nodes; the id is a placeholder in the export). It fetches the report from `data/10k/` and either searches it by keywords or returns a statement as printed. Run one company per execution: running several companies in one execution made every run hit the step limit in this study. Agent settings used: Haiku 5.5 with thinking disabled, Sonnet 5.5 with thinking adaptive.

The node `Reading` in both workflows parses the answer and reports strict JSON validity. In the agent it also tries a lenient extraction (first `{` to last `}`) and reports it separately.
