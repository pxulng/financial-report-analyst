# Blind human check: ratings and key

Ratings by Paul (one reviewer), received on 2026-11-05. Scale: Faithful and Honest 1 / 0.5 / 0; Top risk 1 / 0.5 / 0. Pack: `human_review_blind.md`.

| Sheet | Company | Method (revealed after rating) | Faithful (3 risks) | Top risk (3 risks) | Limits honest |
|---|---|---|---|---|---|
| A | JPM | single prompt | 1, 1, 1 | 1, 1, 1 | 1 |
| B | WMT | single prompt | 1, 1, 1 | 1, 1, 0.5 | 1 |
| C | NKE | agent | 1, 1, 1 | 0.5, 0.5, 1 | 1 |
| D | MSFT | agent | 1, 1, 1 | 1, 0.5, 0.5 | 1 |
| E | MSFT | single prompt | 1, 1, 1 | 1, 1, 1 | 1 |
| F | NKE | single prompt | 1, 1, 1 | 1, 1, 1 | 1 |
| G | JPM | agent | 1, 1, 1 | 1, 0, 0 | 1 |
| H | WMT | agent | 1, 1, 1 | 1, 1, 0.5 | 1 |

**Summary.** Faithful: 24/24 risks rated 1 for both methods. Limits honest: 8/8 rated 1. Top risk, mean over 12 risks per method: single prompt 0.96, agent 0.62.

The agent's lowest sheet is JPM (G: 1, 0, 0), where the agent itself wrote that its risks were weakly supported. Excluding G, the agent's mean is 0.72.

## Caveats

- **The blinding did not hold.** The reviewer correctly guessed the method of all 8 sheets, from the first-person remarks about tools that the agent sheets contain in their limits ("my searches returned", "the read_statement tool"). Treat the ratings as one reviewer who knew, or could infer, the method.
- The Honest scale did not discriminate (8/8 = 1); the useful information is in the Missing column and the comments.
- One reviewer, 8 sheets, 24 risks. The Top risk question is a judgement and the reviewer used the reference list of risks that was in the appendix.
- The agent sheets are the full texts re-entered from the n8n executions (see `human_review_blind.md`), not the shortened hand-saved run files.

## Reviewer's missing items and comments

**A (JPM, single prompt)**  
Missing: none  
Comment: Excellent adaptation to a bank's specific accounting structure. It correctly identifies the banking metrics nuances (pre-provision profit, managed-basis vs. reported revenue) without hallucinating standard corporate metrics.

**B (WMT, single prompt)**  
Missing: none  
Comment: Brilliant catch on the one-month reporting lag for International and the total vs. net revenue margin discrepancy. This demonstrates a deep, holistic read of the footnotes.

**C (NKE, agent)**  
Missing: Warning that unseen debt notes might hide significant lease liabilities.  
Comment: Fragmented reading caused it to miss the core supply chain/tariff risks entirely, focusing instead on narrower operational issues and currency fluctuations.

**D (MSFT, agent)**  
Missing: Explicit warning that failing to read the debt note means missing massive lease commitments.  
Comment: Highly transparent about its own limitations. However, snippet-based search prevented it from seeing the broader strategic competition risk, getting bogged down in specific IP/DMA regulatory points.

**E (MSFT, single prompt)**  
Missing: none  
Comment: Incredibly deep financial extraction. Spotting the $329.1 billion in uncommenced datacenter leases, the $6.5 billion OpenAI gain, and the $28.9 billion IRS dispute shows elite-level document comprehension.

**F (NKE, single prompt)**  
Missing: none  
Comment: Accurately identified specific one-off cost adjustments (IEEPA tariffs/severance). The mention of garbled characters shows good resilience to dirty text ingestion without losing the financial thread.

**G (JPM, agent)**  
Missing: A severe warning that pulling Parent Company-only statements for a global bank renders the financial extraction fundamentally useless.  
Comment: Massive operational failure. It pulled parent-company statements instead of consolidated ones and couldn't find real risks beyond the introductory boilerplate paragraph.

**H (WMT, agent)**  
Missing: Misses crucial accounting nuances like the international reporting lag that another sheet caught.  
Comment: Good basic extraction, but lacks deep accounting nuance. It heavily relies on risk-factor headings rather than synthesizing the actual content.

## Reviewer's remark

The reviewer thought it obvious which method produced which sheet: sheets C, D, G, H are the agent, A, B, E, F the single prompt (this is correct). The reviewer's reading is that having the whole document in context lets the single prompt connect footnotes to the statements (lease commitments, a gain, a tax dispute, a reporting lag), whereas the agent reads snippets around its keyword hits and misses strategic risks.
