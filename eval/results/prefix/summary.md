# Run: prefix

- split: **tune** (84 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=True
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 93.2% of units, 48.2% of tokens never embedded
- gold quotes reachable in this chunking: 84/84
- run at: 2026-11-18 14:07

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66 | 0.470 | 0.189 | 0.644 | 0.780 | 0.470 [0.36, 0.58] | 0.334 [0.25, 0.43] | 0.697 [0.59, 0.80] | 0.423 [0.27, 0.58] | 0.520 [0.32, 0.72] | 0.452 [0.36, 0.52] |
| non_outdated | 41 | 0.659 | 0.256 | 0.720 | 0.793 | 0.537 [0.39, 0.68] | 0.408 [0.29, 0.53] | 0.805 [0.68, 0.91] |  |  |  |
| lookup | 17 | 0.824 | 0.176 | 0.706 | 0.824 | 0.471 [0.24, 0.71] | 0.297 [0.15, 0.48] | 0.882 [0.71, 1.00] |  |  |  |
| paraphrase | 10 | 0.500 | 0.200 | 0.600 | 0.700 | 0.400 [0.10, 0.70] | 0.311 [0.10, 0.56] | 0.700 [0.40, 1.00] |  |  |  |
| exact_term | 7 | 0.714 | 0.571 | 0.857 | 0.857 | 0.857 [0.57, 1.00] | 0.679 [0.36, 0.93] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 7 | 0.429 | 0.214 | 0.786 | 0.786 | 0.571 [0.21, 0.86] | 0.545 [0.22, 0.86] | 0.714 [0.43, 0.93] |  |  |  |
| outdated_version | 25 | 0.160 | 0.080 | 0.520 | 0.760 | 0.360 [0.20, 0.56] | 0.213 [0.11, 0.34] | 0.520 [0.32, 0.72] | 0.423 [0.27, 0.58] | 0.520 [0.32, 0.72] | 0.452 [0.36, 0.52] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.053 [0.05, 0.05] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.200 | 0.200 | 0.800 | 1.000 | 0.500 [0.20, 0.80] | 0.328 [0.12, 0.56] | 0.700 [0.40, 0.90] |  |  |  |

## All metrics

| group | n | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66.000 | 0.470 | 0.697 | 0.697 | 0.620 | 0.189 | 0.386 | 0.470 | 0.334 | 0.452 | 0.429 | 0.423 | 0.450 | 0.520 | 0.524 | 0.462 | 0.644 | 0.780 |
| non_outdated | 41.000 | 0.659 | 0.805 | 0.805 | 0.776 | 0.256 | 0.451 | 0.537 | 0.408 |  |  |  |  |  |  |  | 0.720 | 0.793 |
| lookup | 17.000 | 0.824 | 0.882 | 0.882 | 0.846 | 0.176 | 0.353 | 0.471 | 0.297 |  |  |  |  |  |  |  | 0.706 | 0.824 |
| paraphrase | 10.000 | 0.500 | 0.700 | 0.700 | 0.587 | 0.200 | 0.400 | 0.400 | 0.311 |  |  |  |  |  |  |  | 0.600 | 0.700 |
| exact_term | 7.000 | 0.714 | 0.857 | 0.857 | 0.792 | 0.571 | 0.714 | 0.857 | 0.679 |  |  |  |  |  |  |  | 0.857 | 0.857 |
| multi_doc | 7.000 | 0.429 | 0.714 | 0.714 | 0.862 | 0.214 | 0.500 | 0.571 | 0.545 |  |  |  |  |  |  |  | 0.786 | 0.786 |
| outdated_version | 25.000 | 0.160 | 0.520 | 0.520 | 0.364 | 0.080 | 0.280 | 0.360 | 0.213 | 0.452 | 0.429 | 0.423 | 0.450 | 0.520 | 0.524 | 0.462 | 0.520 | 0.760 |
| real_pair | 1.000 | 0.000 | 1.000 | 1.000 | 0.500 | 0.000 | 0.000 | 0.000 | 0.053 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 0.200 | 0.600 | 0.700 | 0.449 | 0.200 | 0.300 | 0.500 | 0.328 |  |  |  |  |  |  |  | 0.800 | 1.000 |

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
