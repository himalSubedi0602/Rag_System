# Run: bge_v9w50

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=vector top_k=30 version_filter=none date_aware=True reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:36

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.496 | 0.230 | 0.778 | 0.873 | 0.563 [0.48, 0.65] | 0.400 [0.33, 0.47] | 0.782 [0.71, 0.86] | 0.000 [0.00, 0.00] | 0.680 [0.48, 0.85] | 0.000 [0.00, 0.00] |
| non_outdated | 101 | 0.480 | 0.208 | 0.802 | 0.881 | 0.574 [0.48, 0.66] | 0.402 [0.33, 0.47] | 0.787 [0.70, 0.87] |  |  |  |
| lookup | 42 | 0.524 | 0.238 | 0.905 | 0.952 | 0.690 [0.54, 0.83] | 0.437 [0.34, 0.55] | 0.881 [0.76, 0.98] |  |  |  |
| paraphrase | 30 | 0.467 | 0.133 | 0.667 | 0.767 | 0.433 [0.24, 0.62] | 0.245 [0.13, 0.37] | 0.700 [0.50, 0.87] |  |  |  |
| exact_term | 7 | 0.571 | 0.429 | 0.857 | 1.000 | 0.857 [0.57, 1.00] | 0.560 [0.27, 0.81] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.367 | 0.167 | 0.900 | 1.000 | 0.533 [0.32, 0.68] | 0.527 [0.39, 0.64] | 0.733 [0.54, 0.86] |  |  |  |
| compound | 7 | 0.429 | 0.214 | 0.500 | 0.571 | 0.286 [0.00, 0.57] | 0.438 [0.01, 0.86] | 0.643 [0.50, 0.88] |  |  |  |
| outdated_version | 25 | 0.560 | 0.320 | 0.680 | 0.840 | 0.520 [0.33, 0.71] | 0.393 [0.24, 0.56] | 0.760 [0.60, 0.91] | 0.000 [0.00, 0.00] | 0.680 [0.48, 0.85] | 0.000 [0.00, 0.00] |
| real_pair | 1 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.125 [0.12, 0.12] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 0.000 [0.00, 0.00] |
| history | 10 | 0.000 | 0.000 | 0.200 | 0.900 | 0.000 [0.00, 0.00] | 0.069 [0.04, 0.10] | 0.000 [0.00, 0.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.496 | 0.679 | 0.782 | 0.668 | 0.230 | 0.440 | 0.563 | 0.400 | 0.000 | 0.000 | 0.000 | 0.000 | 0.680 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.778 | 0.873 |
| non_outdated | 101.000 | 61.000 | 0.480 | 0.688 | 0.787 | 0.676 | 0.208 | 0.450 | 0.574 | 0.402 |  |  |  |  |  |  |  |  |  |  |  | 0.802 | 0.881 |
| lookup | 42.000 | 34.000 | 0.524 | 0.810 | 0.881 | 0.683 | 0.238 | 0.595 | 0.690 | 0.437 |  |  |  |  |  |  |  |  |  |  |  | 0.905 | 0.952 |
| paraphrase | 30.000 | 28.000 | 0.467 | 0.600 | 0.700 | 0.556 | 0.133 | 0.267 | 0.433 | 0.245 |  |  |  |  |  |  |  |  |  |  |  | 0.667 | 0.767 |
| exact_term | 7.000 | 7.000 | 0.571 | 0.714 | 0.857 | 0.655 | 0.429 | 0.714 | 0.857 | 0.560 |  |  |  |  |  |  |  |  |  |  |  | 0.857 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.367 | 0.567 | 0.733 | 0.807 | 0.167 | 0.367 | 0.533 | 0.527 |  |  |  |  |  |  |  |  |  |  |  | 0.900 | 1.000 |
| compound | 7.000 | 5.000 | 0.429 | 0.571 | 0.643 | 0.893 | 0.214 | 0.286 | 0.286 | 0.438 |  |  |  |  |  |  |  |  |  |  |  | 0.500 | 0.571 |
| outdated_version | 25.000 | 22.000 | 0.560 | 0.640 | 0.760 | 0.635 | 0.320 | 0.400 | 0.520 | 0.393 | 0.000 | 0.000 | 0.000 | 0.000 | 0.680 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.680 | 0.840 |
| real_pair | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.125 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.000 | 0.000 | 0.000 | 0.099 | 0.000 | 0.000 | 0.000 | 0.069 |  |  |  |  |  |  |  |  |  |  |  | 0.200 | 0.900 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:finance/procurement/vendor-guidelines/vendor-security-addendum | How long does GitLab retain security incident communications sent to customers? |
| pp-04 | paraphrase | not found | hb:legal/api-terms | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| pp-08 | paraphrase | 6 | hb:total-rewards/incentives | Can I get a bonus for recommending a friend for an internship at GitLab? |
| ex-08 | exact_term | not found | hb:security/security-assurance/security-compliance/sec-controls | What is LevelUp at GitLab? |
| md-03 | multi_doc | 6 | hb:finance/accounting | Compare Brunel University London's deadline for staff expense claims with GitLab's deadline for vendors to submit invoices. |
| md-06 | multi_doc | 9 | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| lk-23 | lookup | 6 | pdf:qmul-hybrid-working | When will the University of Cambridge's Hybrid Working Policy be reviewed? |
| ov-11 | outdated_version | 9 | hb:total-rewards/benefits/general-and-entity-benefits/remote-com | How long is parental leave for GitLab team members in the US? |
| ov-26 | outdated_version | 6 | hb:finance/expenses | How long can a business trip last and still be covered by GitLab's travel insurance? |
| ov-34 | outdated_version | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab keep risk treatment plans? |
| ov-36 | outdated_version | 7 | hb:hiring/candidate-faq | If someone I referred to GitLab reached team interviews but wasn't hired, how long should I wait before referring them again? |
| ov-38 | outdated_version | 20 | hb:legal/subscription-agreement/index | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/legacy/legacy-subscription-agreement-v7 | What discount on legal fees does GitLab's US legal services benefit provide? |
| lk-26 | lookup | 15 | hb:support/license-and-renewals/workflows/self-managed/troubleshoot_cloud_licensing | Which TLS version must be enabled and preferred in new GitLab deployments? |
| lk-32 | lookup | 9 | hb:legal/subscription-agreement/index | What happens when an emergency ticket comes in to GitLab Support? |
| lk-33 | lookup | 7 | hb:support/support-engineer-responsibilities | I've been on an emergency customer ticket for over an hour and two colleagues have joined in. What should I set up? |
| pp-19 | paraphrase | not found | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-24 | paraphrase | 14 | hb:total-rewards/compensation | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 12 | hb:hiring/interviewing/infrastructure-interview | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-27 | paraphrase | not found | hb:support/support-time-off | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:people-policies | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | 25 | hb:legal/legacy/privacy-statement-v2 | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-32 | paraphrase | 8 | hb:legal/esg/fy23-esg-report | Does GitLab give staff in Belgium anything each year towards environmentally friendly purchases? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 1 | 9 | 0.000 | 0.000 |
| ov-07 | 1 | 8 | 0.000 |  |
| ov-08 | 1 | 9 | 0.000 |  |
| ov-11 | 9 | 21 | 0.000 |  |
| ov-12 | 4 | 13 | 0.000 | 0.000 |
| ov-13 | 1 | 9 | 0.000 | 0.000 |
| ov-14 | 1 | 7 | 0.000 | 0.000 |
| ov-16 | 1 | 9 | 0.000 | 0.000 |
| ov-17 | 1 | 8 | 0.000 | 0.000 |
| ov-21 | 1 | 9 | 0.000 | 0.000 |
| ov-22 | 1 | 9 | 0.000 | 0.000 |
| ov-25 | 1 | 5 | 0.000 |  |
| ov-26 | 6 | 19 | 0.000 | 0.000 |
| ov-27 | 3 | 13 | 0.000 | 0.000 |
| ov-28 | 1 | 9 | 0.000 | 0.000 |
| ov-29 | 4 | 13 | 0.000 | 0.000 |
| ov-30 | 1 | 10 | 0.000 | 0.000 |
| ov-31 | 1 | 10 | 0.000 | 0.000 |
| ov-32 | 3 | 8 | 0.000 | 0.000 |
| ov-33 | 4 | 10 | 0.000 | 0.000 |
| ov-34 | - | - |  |  |
| ov-36 | 7 | 12 | 0.000 | 0.000 |
| ov-38 | 20 | 28 | 0.000 |  |
| ov-40 | 1 | 11 | 0.000 |  |
| ov-44 | - | - |  |  |
