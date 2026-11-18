# Run: bge

- split: **tune** (84 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 84/84
- run at: 2026-11-18 14:08

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66 | 0.447 | 0.174 | 0.780 | 0.864 | 0.553 [0.44, 0.67] | 0.377 [0.29, 0.47] | 0.833 [0.74, 0.92] | 0.529 [0.50, 0.59] | 0.680 [0.48, 0.84] | 0.543 [0.50, 0.61] |
| non_outdated | 41 | 0.646 | 0.280 | 0.841 | 0.878 | 0.622 [0.48, 0.76] | 0.470 [0.35, 0.59] | 0.902 [0.80, 0.98] |  |  |  |
| lookup | 17 | 0.824 | 0.235 | 0.882 | 0.882 | 0.706 [0.47, 0.88] | 0.465 [0.31, 0.63] | 0.941 [0.82, 1.00] |  |  |  |
| paraphrase | 10 | 0.500 | 0.200 | 0.700 | 0.700 | 0.300 [0.00, 0.60] | 0.267 [0.06, 0.53] | 0.900 [0.70, 1.00] |  |  |  |
| exact_term | 7 | 0.714 | 0.571 | 0.857 | 1.000 | 0.857 [0.57, 1.00] | 0.667 [0.33, 0.90] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 7 | 0.357 | 0.214 | 0.929 | 1.000 | 0.643 [0.36, 0.86] | 0.579 [0.29, 0.82] | 0.857 [0.57, 1.00] |  |  |  |
| outdated_version | 25 | 0.120 | 0.000 | 0.680 | 0.840 | 0.440 [0.24, 0.64] | 0.222 [0.14, 0.31] | 0.720 [0.56, 0.88] | 0.529 [0.50, 0.59] | 0.680 [0.48, 0.84] | 0.543 [0.50, 0.61] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.100 [0.10, 0.10] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.300 | 0.300 | 0.700 | 0.900 | 0.600 [0.30, 0.90] | 0.429 [0.20, 0.70] | 0.800 [0.50, 1.00] |  |  |  |

## All metrics

| group | n | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66.000 | 0.447 | 0.742 | 0.833 | 0.641 | 0.174 | 0.477 | 0.553 | 0.377 | 0.543 | 0.553 | 0.529 | 0.542 | 0.680 | 0.761 | 0.765 | 0.780 | 0.864 |
| non_outdated | 41.000 | 0.646 | 0.829 | 0.902 | 0.782 | 0.280 | 0.549 | 0.622 | 0.470 |  |  |  |  |  |  |  | 0.841 | 0.878 |
| lookup | 17.000 | 0.824 | 0.941 | 0.941 | 0.882 | 0.235 | 0.647 | 0.706 | 0.465 |  |  |  |  |  |  |  | 0.882 | 0.882 |
| paraphrase | 10.000 | 0.500 | 0.800 | 0.900 | 0.637 | 0.200 | 0.300 | 0.300 | 0.267 |  |  |  |  |  |  |  | 0.700 | 0.700 |
| exact_term | 7.000 | 0.714 | 0.857 | 0.857 | 0.762 | 0.571 | 0.857 | 0.857 | 0.667 |  |  |  |  |  |  |  | 0.857 | 1.000 |
| multi_doc | 7.000 | 0.357 | 0.571 | 0.857 | 0.764 | 0.214 | 0.357 | 0.643 | 0.579 |  |  |  |  |  |  |  | 0.929 | 1.000 |
| outdated_version | 25.000 | 0.120 | 0.600 | 0.720 | 0.410 | 0.000 | 0.360 | 0.440 | 0.222 | 0.543 | 0.553 | 0.529 | 0.542 | 0.680 | 0.761 | 0.765 | 0.680 | 0.840 |
| real_pair | 1.000 | 0.000 | 1.000 | 1.000 | 0.333 | 0.000 | 0.000 | 0.000 | 0.100 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 0.300 | 0.800 | 0.800 | 0.561 | 0.300 | 0.500 | 0.600 | 0.429 |  |  |  |  |  |  |  | 0.700 | 0.900 |

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

## Outdated-version questions

stale / fact_stale: 1 = old version first, 0.5 = exact score tie, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 2 | 1 | 0.500 | 0.500 |
| ov-07 | 2 | 1 | 1.000 |  |
| ov-08 | 2 | 1 | 0.500 |  |
| ov-11 | 10 | 9 | 0.500 |  |
| ov-12 | 2 | 1 | 0.500 | 0.500 |
| ov-13 | 2 | 1 | 0.500 | 0.500 |
| ov-14 | 2 | 1 | 0.500 | 0.500 |
| ov-16 | 1 | 2 | 0.500 | 0.500 |
| ov-17 | 2 | 1 | 1.000 | 1.000 |
| ov-21 | 2 | 1 | 0.500 | 0.500 |
| ov-22 | 2 | 1 | 0.500 | 0.500 |
| ov-25 | 1 | 2 | 0.500 |  |
| ov-26 | 9 | 10 | 0.500 | 0.500 |
| ov-27 | 6 | 7 | 0.500 | 0.500 |
| ov-28 | 2 | 1 | 0.500 | 0.500 |
| ov-29 | 5 | 6 | 0.500 | 0.500 |
| ov-30 | 2 | 1 | 0.500 | 0.500 |
| ov-31 | 2 | 1 | 0.500 | 0.500 |
| ov-32 | 4 | 3 | 0.500 | 0.500 |
| ov-33 | 6 | 3 | 0.500 | 0.500 |
| ov-34 | - | - |  |  |
| ov-36 | 5 | 4 | 0.500 | 0.500 |
| ov-38 | 22 | 23 | 0.500 |  |
| ov-40 | 1 | 2 | 0.500 |  |
| ov-44 | - | - |  |  |
