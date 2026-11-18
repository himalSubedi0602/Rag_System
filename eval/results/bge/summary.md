# Run: bge

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:09

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.480 | 0.210 | 0.786 | 0.873 | 0.548 [0.46, 0.64] | 0.398 [0.33, 0.47] | 0.798 [0.72, 0.88] | 0.765 [0.58, 0.94] | 0.680 [0.48, 0.85] | 0.696 [0.50, 0.88] |
| non_outdated | 101 | 0.569 | 0.262 | 0.812 | 0.881 | 0.574 [0.47, 0.66] | 0.442 [0.36, 0.51] | 0.817 [0.73, 0.89] |  |  |  |
| lookup | 42 | 0.690 | 0.310 | 0.905 | 0.952 | 0.714 [0.56, 0.86] | 0.481 [0.37, 0.60] | 0.905 [0.78, 1.00] |  |  |  |
| paraphrase | 30 | 0.467 | 0.167 | 0.667 | 0.767 | 0.300 [0.13, 0.47] | 0.253 [0.13, 0.39] | 0.667 [0.47, 0.83] |  |  |  |
| exact_term | 7 | 0.714 | 0.571 | 0.857 | 1.000 | 0.857 [0.57, 1.00] | 0.667 [0.38, 0.90] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.433 | 0.200 | 0.967 | 1.000 | 0.700 [0.50, 0.83] | 0.606 [0.47, 0.69] | 0.867 [0.73, 1.00] |  |  |  |
| compound | 7 | 0.429 | 0.214 | 0.500 | 0.571 | 0.357 [0.00, 0.71] | 0.437 [0.01, 0.86] | 0.786 [0.58, 0.94] |  |  |  |
| outdated_version | 25 | 0.120 | 0.000 | 0.680 | 0.840 | 0.440 [0.27, 0.64] | 0.222 [0.15, 0.31] | 0.720 [0.52, 0.91] | 0.765 [0.58, 0.94] | 0.680 [0.48, 0.85] | 0.696 [0.50, 0.88] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.100 [0.10, 0.10] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.300 | 0.300 | 0.700 | 0.900 | 0.600 [0.30, 0.90] | 0.429 [0.20, 0.70] | 0.800 [0.50, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.480 | 0.726 | 0.798 | 0.676 | 0.210 | 0.464 | 0.548 | 0.398 | 0.696 | 0.789 | 0.765 | 0.917 | 0.680 | 0.674 | 0.676 | 0.543 | 0.529 | 0.543 | 0.529 | 0.786 | 0.873 |
| non_outdated | 101.000 | 61.000 | 0.569 | 0.757 | 0.817 | 0.742 | 0.262 | 0.490 | 0.574 | 0.442 |  |  |  |  |  |  |  |  |  |  |  | 0.812 | 0.881 |
| lookup | 42.000 | 34.000 | 0.690 | 0.881 | 0.905 | 0.791 | 0.310 | 0.619 | 0.714 | 0.481 |  |  |  |  |  |  |  |  |  |  |  | 0.905 | 0.952 |
| paraphrase | 30.000 | 28.000 | 0.467 | 0.633 | 0.667 | 0.559 | 0.167 | 0.300 | 0.300 | 0.253 |  |  |  |  |  |  |  |  |  |  |  | 0.667 | 0.767 |
| exact_term | 7.000 | 7.000 | 0.714 | 0.857 | 0.857 | 0.762 | 0.571 | 0.857 | 0.857 | 0.667 |  |  |  |  |  |  |  |  |  |  |  | 0.857 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.433 | 0.667 | 0.867 | 0.890 | 0.200 | 0.433 | 0.700 | 0.606 |  |  |  |  |  |  |  |  |  |  |  | 0.967 | 1.000 |
| compound | 7.000 | 5.000 | 0.429 | 0.643 | 0.786 | 0.893 | 0.214 | 0.286 | 0.357 | 0.437 |  |  |  |  |  |  |  |  |  |  |  | 0.500 | 0.571 |
| outdated_version | 25.000 | 22.000 | 0.120 | 0.600 | 0.720 | 0.410 | 0.000 | 0.360 | 0.440 | 0.222 | 0.696 | 0.789 | 0.765 | 0.917 | 0.680 | 0.674 | 0.676 | 0.543 | 0.529 | 0.543 | 0.529 | 0.680 | 0.840 |
| real_pair | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.333 | 0.000 | 0.000 | 0.000 | 0.100 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.300 | 0.800 | 0.800 | 0.561 | 0.300 | 0.500 | 0.600 | 0.429 |  |  |  |  |  |  |  |  |  |  |  | 0.700 | 0.900 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:finance/procurement/vendor-guidelines/vendor-security-addendum | How long does GitLab retain security incident communications sent to customers? |
| pp-04 | paraphrase | not found | hb:legal/api-terms | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| ex-08 | exact_term | not found | hb:security/security-assurance/security-compliance/sec-controls | What is LevelUp at GitLab? |
| md-06 | multi_doc | 10 | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-11 | outdated_version | 10 | hb:total-rewards/benefits/general-and-entity-benefits/remote-com | How long is parental leave for GitLab team members in the US? |
| ov-26 | outdated_version | 9 | syn:expenses-2023 | How long can a business trip last and still be covered by GitLab's travel insurance? |
| ov-27 | outdated_version | 6 | syn:expenses-2023 | What is the maximum baggage protection under GitLab's business travel insurance? |
| ov-33 | outdated_version | 6 | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab keep risk treatment plans? |
| ov-38 | outdated_version | 22 | hb:legal/subscription-agreement/index | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/legacy/legacy-subscription-agreement-v7 | What discount on legal fees does GitLab's US legal services benefit provide? |
| lk-26 | lookup | 15 | hb:support/license-and-renewals/workflows/self-managed/troubleshoot_cloud_licensing | Which TLS version must be enabled and preferred in new GitLab deployments? |
| lk-32 | lookup | 9 | hb:legal/subscription-agreement/index | What happens when an emergency ticket comes in to GitLab Support? |
| lk-33 | lookup | 8 | hb:support/support-engineer-responsibilities | I've been on an emergency customer ticket for over an hour and two colleagues have joined in. What should I set up? |
| pp-19 | paraphrase | not found | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-22 | paraphrase | 6 | syn:ltd-benefits-uk-2023 | Will GitLab top up my retirement savings in Singapore beyond the government scheme? |
| pp-24 | paraphrase | 20 | hb:total-rewards/compensation | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 13 | hb:hiring/interviewing/infrastructure-interview | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-27 | paraphrase | not found | hb:support/support-time-off | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:people-policies | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | 25 | hb:legal/legacy/privacy-statement-v2 | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-32 | paraphrase | 8 | hb:legal/esg/fy23-esg-report | Does GitLab give staff in Belgium anything each year towards environmentally friendly purchases? |
| pp-34 | paraphrase | 9 | hb:finance/procurement/vendor-guidelines/vendor-agreement | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 2 | 1 | 1.000 | 1.000 |
| ov-07 | 2 | 1 | 1.000 |  |
| ov-08 | 2 | 1 | 1.000 |  |
| ov-11 | 10 | 9 | 1.000 |  |
| ov-12 | 2 | 1 | 1.000 | 1.000 |
| ov-13 | 2 | 1 | 1.000 | 0.000 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 1 | 2 | 0.000 | 0.000 |
| ov-17 | 2 | 1 | 1.000 | 1.000 |
| ov-21 | 2 | 1 | 1.000 | 1.000 |
| ov-22 | 2 | 1 | 1.000 | 1.000 |
| ov-25 | 1 | 2 | 0.000 |  |
| ov-26 | 9 | 10 | 0.000 | 0.000 |
| ov-27 | 6 | 7 | 0.000 | 1.000 |
| ov-28 | 2 | 1 | 1.000 | 1.000 |
| ov-29 | 5 | 6 | 0.000 | 1.000 |
| ov-30 | 2 | 1 | 1.000 | 1.000 |
| ov-31 | 2 | 1 | 1.000 | 1.000 |
| ov-32 | 4 | 3 | 1.000 | 1.000 |
| ov-33 | 6 | 3 | 1.000 | 1.000 |
| ov-34 | - | - |  |  |
| ov-36 | 5 | 4 | 1.000 | 0.000 |
| ov-38 | 22 | 23 | 0.000 |  |
| ov-40 | 1 | 2 | 0.000 |  |
| ov-44 | - | - |  |  |
