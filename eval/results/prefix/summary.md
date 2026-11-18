# Run: prefix

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=True
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 93.2% of units, 48.2% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 14:53

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.528 | 0.246 | 0.750 | 0.841 | 0.540 [0.44, 0.63] | 0.417 [0.33, 0.50] | 0.734 [0.64, 0.82] | 0.423 [0.29, 0.58] | 0.520 [0.30, 0.73] | 0.452 [0.36, 0.55] |
| non_outdated | 101 | 0.619 | 0.287 | 0.807 | 0.861 | 0.584 [0.49, 0.68] | 0.468 [0.37, 0.55] | 0.787 [0.69, 0.87] |  |  |  |
| lookup | 42 | 0.738 | 0.238 | 0.833 | 0.881 | 0.619 [0.47, 0.76] | 0.390 [0.28, 0.51] | 0.881 [0.78, 0.97] |  |  |  |
| paraphrase | 30 | 0.533 | 0.300 | 0.700 | 0.800 | 0.467 [0.27, 0.66] | 0.395 [0.24, 0.56] | 0.667 [0.47, 0.86] |  |  |  |
| exact_term | 7 | 0.714 | 0.571 | 0.857 | 0.857 | 0.857 [0.57, 1.00] | 0.679 [0.36, 0.93] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.467 | 0.267 | 0.900 | 0.900 | 0.600 [0.32, 0.82] | 0.637 [0.40, 0.86] | 0.767 [0.50, 0.95] |  |  |  |
| compound | 7 | 0.500 | 0.286 | 0.857 | 0.929 | 0.571 [0.33, 0.79] | 0.677 [0.38, 0.93] | 0.714 [0.58, 0.83] |  |  |  |
| outdated_version | 25 | 0.160 | 0.080 | 0.520 | 0.760 | 0.360 [0.16, 0.57] | 0.213 [0.10, 0.35] | 0.520 [0.32, 0.72] | 0.423 [0.29, 0.58] | 0.520 [0.30, 0.73] | 0.452 [0.36, 0.55] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.053 [0.05, 0.05] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.200 | 0.200 | 0.800 | 1.000 | 0.500 [0.20, 0.80] | 0.328 [0.12, 0.56] | 0.700 [0.40, 0.90] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.528 | 0.730 | 0.734 | 0.696 | 0.246 | 0.448 | 0.540 | 0.417 | 0.452 | 0.429 | 0.423 | 0.450 | 0.520 | 0.524 | 0.462 | 0.750 | 0.841 |
| non_outdated | 101.000 | 61.000 | 0.619 | 0.782 | 0.787 | 0.779 | 0.287 | 0.490 | 0.584 | 0.468 |  |  |  |  |  |  |  | 0.807 | 0.861 |
| lookup | 42.000 | 34.000 | 0.738 | 0.881 | 0.881 | 0.807 | 0.238 | 0.476 | 0.619 | 0.390 |  |  |  |  |  |  |  | 0.833 | 0.881 |
| paraphrase | 30.000 | 28.000 | 0.533 | 0.667 | 0.667 | 0.606 | 0.300 | 0.433 | 0.467 | 0.395 |  |  |  |  |  |  |  | 0.700 | 0.800 |
| exact_term | 7.000 | 7.000 | 0.714 | 0.857 | 0.857 | 0.792 | 0.571 | 0.714 | 0.857 | 0.679 |  |  |  |  |  |  |  | 0.857 | 0.857 |
| multi_doc | 15.000 | 8.000 | 0.467 | 0.767 | 0.767 | 0.936 | 0.267 | 0.567 | 0.600 | 0.637 |  |  |  |  |  |  |  | 0.900 | 0.900 |
| compound | 7.000 | 5.000 | 0.500 | 0.643 | 0.714 | 1.000 | 0.286 | 0.429 | 0.571 | 0.677 |  |  |  |  |  |  |  | 0.857 | 0.929 |
| outdated_version | 25.000 | 22.000 | 0.160 | 0.520 | 0.520 | 0.364 | 0.080 | 0.280 | 0.360 | 0.213 | 0.452 | 0.429 | 0.423 | 0.450 | 0.520 | 0.524 | 0.462 | 0.520 | 0.760 |
| real_pair | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.500 | 0.000 | 0.000 | 0.000 | 0.053 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.200 | 0.600 | 0.700 | 0.449 | 0.200 | 0.300 | 0.500 | 0.328 |  |  |  |  |  |  |  | 0.800 | 1.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/legacy/legacy-subscription-agreement-v4 | How long does GitLab retain security incident communications sent to customers? |
| lk-11 | lookup | 22 | hb:people-policies/france-sas/remote-work-charter | Over what reference period are average weekly working hours calculated for the 48-hour limit in GitLab's people policies? |
| pp-03 | paraphrase | 30 | hb:support/support-engineer-responsibilities | As a GitLab Support engineer, when should I rethink the dates I want to take off? |
| pp-04 | paraphrase | not found | hb:legal/legacy/legacy-subscription-agreement-v7 | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| pp-14 | paraphrase | not found | hb:legal/legacy/legacy-psa-v3 | Can I buy second-hand work equipment from an individual and claim it back from GitLab? |
| ex-08 | exact_term | 24 | hb:legal/legacy/legacy-subscription-agreement-v3 | What is LevelUp at GitLab? |
| md-06 | multi_doc | 27 | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-06 | outdated_version | not found | hb:finance/procurement/vendor-guidelines/po-terms | How long after the purchase date can I submit a GitLab expense claim and still be reimbursed without manager approval? |
| ov-11 | outdated_version | 11 | syn:ltd-benefits-uk-2023 | How long is parental leave for GitLab team members in the US? |
| ov-16 | outdated_version | 21 | syn:support-on-call-2023 | How far in advance should GitLab team members book international flights? |
| ov-26 | outdated_version | 7 | syn:inc-benefits-us-2023 | How long can a business trip last and still be covered by GitLab's travel insurance? |
| ov-27 | outdated_version | 8 | hb:legal/legacy/legacy-subscription-agreement-v6 | What is the maximum baggage protection under GitLab's business travel insurance? |
| ov-30 | outdated_version | 6 | hb:total-rewards/benefits/general-and-entity-benefits/gitlab-ireland-ltd | How much of base salary does GitLab's US short- and long-term disability insurance replace? |
| ov-32 | outdated_version | 9 | hb:hiring/referral-process | How long does GitLab's recruiting team take to review a referral submission? |
| ov-33 | outdated_version | not found | hb:legal/record-retention-policy | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | syn:ltd-benefits-uk-2023 | How long does GitLab keep risk treatment plans? |
| ov-36 | outdated_version | 12 | hb:hiring/interviewing/infrastructure-interview | If someone I referred to GitLab reached team interviews but wasn't hired, how long should I wait before referring them again? |
| ov-38 | outdated_version | not found | hb:people-policies/france-sas/remote-work-charter | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/subscription-agreement/index | What discount on legal fees does GitLab's US legal services benefit provide? |
| lk-30 | lookup | 14 | hb:security/product-security/vulnerability-management | My request for an exception to a GitLab security policy was turned down. Where do I send an appeal? |
| lk-32 | lookup | not found | syn:travel-safety-2022 | What happens when an emergency ticket comes in to GitLab Support? |
| lk-41 | lookup | 10 | hb:total-rewards/incentives | How often is the bonus paid for GitLab directors and above? |
| pp-24 | paraphrase | not found | hb:total-rewards/incentives | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 12 | hb:hiring/interviewing/customer-support-interviewing | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-30 | paraphrase | not found | syn:expenses-2023 | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:legal/legacy/privacy-statement | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-32 | paraphrase | 10 | hb:legal/esg/earth-month | Does GitLab give staff in Belgium anything each year towards environmentally friendly purchases? |
| pp-33 | paraphrase | 11 | hb:security/security-and-technology-policies/security-and-technology-policies-management | Where must the sign-off for a GitLab security policy exception be recorded? |
| pp-34 | paraphrase | 28 | hb:legal/subscription-agreement/index | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |

## Outdated-version questions

stale / fact_stale: 1 = old version first, 0.5 = exact score tie, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | - | - |  |  |
| ov-07 | 1 | 2 | 0.500 |  |
| ov-08 | 2 | 3 | 0.500 |  |
| ov-11 | 11 | 12 | 0.500 |  |
| ov-12 | 3 | 2 | 0.500 |  |
| ov-13 | 2 | 1 | 0.500 | 0.000 |
| ov-14 | 1 | 2 | 0.000 | 0.500 |
| ov-16 | 21 | 20 | 0.500 |  |
| ov-17 | 1 | 2 | 0.000 | 0.000 |
| ov-21 | 2 | 1 | 0.500 | 0.500 |
| ov-22 | 2 | 1 | 0.500 | 1.000 |
| ov-25 | 2 | 1 | 0.500 | 0.500 |
| ov-26 | 7 | 6 | 0.500 | 0.500 |
| ov-27 | 8 | 7 | 0.500 | 0.500 |
| ov-28 | 1 | 2 | 0.500 | 0.500 |
| ov-29 | 2 | 3 | 0.000 | 0.000 |
| ov-30 | 6 | 5 | 0.500 | 0.500 |
| ov-31 | 2 | 1 | 0.500 | 0.500 |
| ov-32 | 9 | 8 | 0.500 | 0.500 |
| ov-33 | - | - |  |  |
| ov-34 | - | - |  |  |
| ov-36 | 12 | 11 | 0.500 |  |
| ov-38 | - | - |  |  |
| ov-40 | 2 | 1 | 0.500 |  |
| ov-44 | - | 30 | 1.000 |  |
