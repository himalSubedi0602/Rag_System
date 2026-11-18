# Run: bge_prefix

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=True
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 57.8% of units, 1.1% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:10

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.583 | 0.306 | 0.837 | 0.897 | 0.603 [0.51, 0.69] | 0.488 [0.40, 0.58] | 0.786 [0.71, 0.86] | 0.611 [0.39, 0.81] | 0.720 [0.52, 0.88] | 0.652 [0.43, 0.86] |
| non_outdated | 101 | 0.668 | 0.342 | 0.866 | 0.901 | 0.624 [0.52, 0.71] | 0.528 [0.42, 0.62] | 0.792 [0.70, 0.87] |  |  |  |
| lookup | 42 | 0.833 | 0.452 | 0.952 | 0.952 | 0.762 [0.61, 0.89] | 0.597 [0.46, 0.73] | 0.905 [0.78, 1.00] |  |  |  |
| paraphrase | 30 | 0.567 | 0.233 | 0.767 | 0.800 | 0.400 [0.22, 0.59] | 0.330 [0.19, 0.47] | 0.667 [0.47, 0.83] |  |  |  |
| exact_term | 7 | 0.714 | 0.429 | 0.857 | 1.000 | 0.857 [0.57, 1.00] | 0.619 [0.33, 0.86] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.467 | 0.200 | 0.933 | 0.967 | 0.667 [0.42, 0.82] | 0.602 [0.39, 0.79] | 0.800 [0.64, 0.92] |  |  |  |
| compound | 7 | 0.500 | 0.357 | 0.643 | 0.786 | 0.429 [0.20, 0.64] | 0.714 [0.38, 1.00] | 0.571 [0.50, 0.69] |  |  |  |
| outdated_version | 25 | 0.240 | 0.160 | 0.720 | 0.880 | 0.520 [0.31, 0.72] | 0.329 [0.20, 0.47] | 0.760 [0.60, 0.91] | 0.611 [0.39, 0.81] | 0.720 [0.52, 0.88] | 0.652 [0.43, 0.86] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.200 [0.20, 0.20] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.600 | 0.500 | 0.600 | 1.000 | 0.600 [0.30, 0.90] | 0.525 [0.23, 0.80] | 0.800 [0.50, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.583 | 0.738 | 0.786 | 0.740 | 0.306 | 0.536 | 0.603 | 0.488 | 0.652 | 0.700 | 0.611 | 0.714 | 0.720 | 0.630 | 0.556 | 0.543 | 0.472 | 0.522 | 0.500 | 0.837 | 0.897 |
| non_outdated | 101.000 | 61.000 | 0.668 | 0.752 | 0.792 | 0.802 | 0.342 | 0.569 | 0.624 | 0.528 |  |  |  |  |  |  |  |  |  |  |  | 0.866 | 0.901 |
| lookup | 42.000 | 34.000 | 0.833 | 0.881 | 0.905 | 0.865 | 0.452 | 0.738 | 0.762 | 0.597 |  |  |  |  |  |  |  |  |  |  |  | 0.952 | 0.952 |
| paraphrase | 30.000 | 28.000 | 0.567 | 0.600 | 0.667 | 0.612 | 0.233 | 0.333 | 0.400 | 0.330 |  |  |  |  |  |  |  |  |  |  |  | 0.767 | 0.800 |
| exact_term | 7.000 | 7.000 | 0.714 | 0.857 | 0.857 | 0.762 | 0.429 | 0.857 | 0.857 | 0.619 |  |  |  |  |  |  |  |  |  |  |  | 0.857 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.467 | 0.733 | 0.800 | 0.933 | 0.200 | 0.500 | 0.667 | 0.602 |  |  |  |  |  |  |  |  |  |  |  | 0.933 | 0.967 |
| compound | 7.000 | 5.000 | 0.500 | 0.571 | 0.571 | 1.000 | 0.357 | 0.429 | 0.429 | 0.714 |  |  |  |  |  |  |  |  |  |  |  | 0.643 | 0.786 |
| outdated_version | 25.000 | 22.000 | 0.240 | 0.680 | 0.760 | 0.487 | 0.160 | 0.400 | 0.520 | 0.329 | 0.652 | 0.700 | 0.611 | 0.714 | 0.720 | 0.630 | 0.556 | 0.543 | 0.472 | 0.522 | 0.500 | 0.720 | 0.880 |
| real_pair | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.500 | 0.000 | 0.000 | 1.000 | 0.200 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.600 | 0.800 | 0.800 | 0.689 | 0.500 | 0.500 | 0.600 | 0.525 |  |  |  |  |  |  |  |  |  |  |  | 0.600 | 1.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/legacy/legacy-subscription-agreement-v2 | How long does GitLab retain security incident communications sent to customers? |
| pp-04 | paraphrase | not found | hb:legal/legacy/privacy-statement | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| ex-08 | exact_term | not found | hb:security/security-assurance/security-compliance/sec-controls | What is LevelUp at GitLab? |
| md-06 | multi_doc | not found | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-11 | outdated_version | 17 | hb:total-rewards/benefits/general-and-entity-benefits/canada-corp-benefits | How long is parental leave for GitLab team members in the US? |
| ov-26 | outdated_version | 28 | hb:total-rewards/benefits/general-and-entity-benefits/inc-benefits-us | How long can a business trip last and still be covered by GitLab's travel insurance? |
| ov-33 | outdated_version | 6 | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | hb:legal/legacy/privacy-statement | How long does GitLab keep risk treatment plans? |
| ov-36 | outdated_version | 7 | hb:hiring/candidate-faq | If someone I referred to GitLab reached team interviews but wasn't hired, how long should I wait before referring them again? |
| ov-38 | outdated_version | not found | hb:legal/subscription-agreement/index | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| lk-26 | lookup | 11 | hb:support/license-and-renewals/workflows/self-managed/troubleshoot_cloud_licensing | Which TLS version must be enabled and preferred in new GitLab deployments? |
| lk-32 | lookup | 15 | hb:legal/subscription-agreement/index | What happens when an emergency ticket comes in to GitLab Support? |
| lk-33 | lookup | 11 | hb:support/providing_excellent_customer_service | I've been on an emergency customer ticket for over an hour and two colleagues have joined in. What should I set up? |
| pp-19 | paraphrase | 6 | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-22 | paraphrase | 13 | syn:ltd-benefits-uk-2023 | Will GitLab top up my retirement savings in Singapore beyond the government scheme? |
| pp-24 | paraphrase | not found | hb:hiring/talent-acquisition-framework/coordinator | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | not found | hb:hiring/conducting-a-gitlab-interview | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-27 | paraphrase | 13 | hb:total-rewards/benefits/general-and-entity-benefits/canada-corp-benefits | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:support/license-and-renewals/workflows/self-managed/troubleshoot_cloud_licensing | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | 29 | hb:legal/legacy/privacy-statement | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-32 | paraphrase | 10 | hb:legal/esg/fy23-esg-report | Does GitLab give staff in Belgium anything each year towards environmentally friendly purchases? |
| pp-34 | paraphrase | 6 | hb:finance/procurement | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 3 | 2 | 1.000 | 1.000 |
| ov-07 | 2 | 1 | 1.000 |  |
| ov-08 | 1 | 4 | 0.000 |  |
| ov-11 | 17 | 18 | 0.000 |  |
| ov-12 | 2 | 1 | 1.000 | 1.000 |
| ov-13 | 2 | 1 | 1.000 | 0.000 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 1 | 3 | 0.000 | 0.000 |
| ov-17 | 1 | 2 | 0.000 | 0.000 |
| ov-21 | 1 | 2 | 0.000 | 0.000 |
| ov-22 | 2 | 1 | 1.000 | 1.000 |
| ov-25 | 2 | 1 | 1.000 | 1.000 |
| ov-26 | 28 | 29 | 0.000 | 0.000 |
| ov-27 | 1 | 2 | 0.000 | 1.000 |
| ov-28 | 2 | 1 | 1.000 | 1.000 |
| ov-29 | 5 | 4 | 1.000 | 1.000 |
| ov-30 | 1 | 2 | 0.000 | 0.000 |
| ov-31 | 2 | 1 | 1.000 | 1.000 |
| ov-32 | 4 | 3 | 1.000 | 1.000 |
| ov-33 | 6 | 5 | 1.000 | 1.000 |
| ov-34 | - | - |  |  |
| ov-36 | 7 | 6 | 1.000 | 0.000 |
| ov-38 | - | - |  |  |
| ov-40 | 2 | 1 | 1.000 |  |
| ov-44 | 2 | 1 | 1.000 |  |
