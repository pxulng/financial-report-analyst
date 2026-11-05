# Validation freeze (5 November 2026)

Everything below is fixed before any validation company (MSFT, WMT, NKE, JPM) is run. Each method/model pair runs once on the validation set; nothing is changed after seeing a result.

| Item | Frozen value |
|---|---|
| Single prompt (reference 2) | `prompts/reference2_system_prompt.txt`, sha256 `7a7d5b55b2e176876161343dfb1b540c1a7c637be708c8e41f8554b280a8971d` |
| Agent prompt | `prompts/agent_system_prompt_v3.txt`, sha256 `103573f4dbd359cdd38ae681750df95e056303d81a30cb8b6b944eca0fa23365` |
| Models | claude-haiku-5-5 and claude-sonnet-5-5 |
| Agent settings | step limit 15; Haiku with thinking disabled; Sonnet with thinking "adaptive" (the model refuses "disabled") |
| Agent run mode | one execution per company (several companies in one execution made every agent hit the step limit) |
| Scoring | `evaluation/score.py` and `evaluation/key.json` as committed; thresholds from `docs/design_frozen_original_fr.md` |

Declared deviations from the design, kept visible: the agent prompt went through three versions on the test set (the design allows two); the agent run mode changed to one company per execution; the Sonnet thinking setting differs from Haiku.

Validation order (cheapest first, to stay inside the budget): agent Haiku, single prompt Haiku, agent Sonnet, single prompt Sonnet. JPM (1.59 MB, longer than the context window) is sent to the single prompt once, and its failure or success is recorded as measure 9.
