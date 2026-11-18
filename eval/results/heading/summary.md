# Run: heading

- split: **tune** (84 questions; no_answer excluded from retrieval metrics)
- chunking: heading size=500 overlap=50 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 4704 (embedded units: 4704); truncated by the embedding model: 35.0% of units, 25.2% of tokens never embedded
- gold quotes reachable in this chunking: 84/84
- run at: 2026-11-18 14:07

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66 | 0.477 | 0.250 | 0.750 | 0.803 | 0.508 [0.39, 0.62] | 0.403 [0.30, 0.50] | 0.811 [0.72, 0.89] | 0.500 [0.37, 0.63] | 0.760 [0.60, 0.92] | 0.523 [0.45, 0.59] |
| non_outdated | 41 | 0.671 | 0.329 | 0.744 | 0.829 | 0.549 [0.39, 0.70] | 0.475 [0.34, 0.60] | 0.866 [0.77, 0.95] |  |  |  |
| lookup | 17 | 0.706 | 0.235 | 0.706 | 0.765 | 0.471 [0.24, 0.71] | 0.363 [0.19, 0.56] | 0.882 [0.71, 1.00] |  |  |  |
| paraphrase | 10 | 0.700 | 0.300 | 0.700 | 0.900 | 0.500 [0.20, 0.80] | 0.369 [0.14, 0.64] | 1.000 [1.00, 1.00] |  |  |  |
| exact_term | 7 | 0.857 | 0.714 | 1.000 | 1.000 | 0.857 [0.57, 1.00] | 0.800 [0.53, 1.00] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 7 | 0.357 | 0.214 | 0.643 | 0.714 | 0.500 [0.21, 0.79] | 0.571 [0.26, 0.86] | 0.643 [0.36, 0.86] |  |  |  |
| outdated_version | 25 | 0.160 | 0.120 | 0.760 | 0.760 | 0.440 [0.24, 0.64] | 0.285 [0.17, 0.42] | 0.720 [0.52, 0.88] | 0.500 [0.37, 0.63] | 0.760 [0.60, 0.92] | 0.523 [0.45, 0.59] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.500 [0.50, 0.50] | 1.000 [1.00, 1.00] | 0.500 [0.50, 0.50] | 1.000 [1.00, 1.00] | 0.500 [0.50, 0.50] |
| history | 10 | 0.400 | 0.300 | 0.900 | 0.900 | 0.700 [0.40, 1.00] | 0.447 [0.22, 0.69] | 0.900 [0.70, 1.00] |  |  |  |

## All metrics

| group | n | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66.000 | 0.477 | 0.750 | 0.811 | 0.664 | 0.250 | 0.447 | 0.508 | 0.403 | 0.523 | 0.500 | 0.500 | 0.409 | 0.760 | 0.568 | 0.500 | 0.750 | 0.803 |
| non_outdated | 41.000 | 0.671 | 0.817 | 0.866 | 0.812 | 0.329 | 0.500 | 0.549 | 0.475 |  |  |  |  |  |  |  | 0.744 | 0.829 |
| lookup | 17.000 | 0.706 | 0.882 | 0.882 | 0.793 | 0.235 | 0.471 | 0.471 | 0.363 |  |  |  |  |  |  |  | 0.706 | 0.765 |
| paraphrase | 10.000 | 0.700 | 0.900 | 1.000 | 0.820 | 0.300 | 0.400 | 0.500 | 0.369 |  |  |  |  |  |  |  | 0.700 | 0.900 |
| exact_term | 7.000 | 0.857 | 0.857 | 0.857 | 0.871 | 0.714 | 0.857 | 0.857 | 0.800 |  |  |  |  |  |  |  | 1.000 | 1.000 |
| multi_doc | 7.000 | 0.357 | 0.500 | 0.643 | 0.786 | 0.214 | 0.357 | 0.500 | 0.571 |  |  |  |  |  |  |  | 0.643 | 0.714 |
| outdated_version | 25.000 | 0.160 | 0.640 | 0.720 | 0.423 | 0.120 | 0.360 | 0.440 | 0.285 | 0.523 | 0.500 | 0.500 | 0.409 | 0.760 | 0.568 | 0.500 | 0.760 | 0.760 |
| real_pair | 1.000 | 0.000 | 1.000 | 1.000 | 0.500 | 0.000 | 1.000 | 1.000 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 0.400 | 0.900 | 0.900 | 0.637 | 0.300 | 0.500 | 0.700 | 0.447 |  |  |  |  |  |  |  | 0.900 | 0.900 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-02 | lookup | 7 | hb:support/license-and-renewals | What is the monthly limit for reimbursing a co-working space at GitLab? |
| lk-06 | lookup | not found | hb:legal/legacy/legacy-subscription-agreement-v5 | How long does GitLab retain security incident communications sent to customers? |
| ex-08 | exact_term | 10 | hb:legal/ethics-compliance-program/compliance-training | What is LevelUp at GitLab? |
| md-06 | multi_doc | not found | hb:finance/procurement/tips-for-submitting-a-zip-request | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-08 | outdated_version | 12 | hb:total-rewards/benefits/general-and-entity-benefits/ltd-benefits-uk | How much can I spend on meals per day while travelling for GitLab? |
| ov-11 | outdated_version | 19 | hb:total-rewards/benefits/general-and-entity-benefits/singapore-pte-ltd | How long is parental leave for GitLab team members in the US? |
| ov-32 | outdated_version | 16 | hb:hiring/referral-process | How long does GitLab's recruiting team take to review a referral submission? |
| ov-33 | outdated_version | not found | hb:legal/record-retention-policy | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab keep risk treatment plans? |
| ov-38 | outdated_version | 7 | hb:legal/anti-corruption-policy | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/subscription-agreement/index | What discount on legal fees does GitLab's US legal services benefit provide? |

## Outdated-version questions

stale / fact_stale: 1 = old version first, 0.5 = exact score tie, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 3 | 2 | 0.500 | 0.500 |
| ov-07 | 2 | 3 | 0.500 | 0.500 |
| ov-08 | 12 | 8 | 1.000 | 1.000 |
| ov-11 | 19 | 18 | 0.500 |  |
| ov-12 | 2 | 4 | 0.500 | 0.500 |
| ov-13 | 2 | 1 | 0.500 | 0.500 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 2 | 3 | 0.500 | 0.500 |
| ov-17 | 2 | 1 | 0.500 | 0.500 |
| ov-21 | 5 | 4 | 0.500 |  |
| ov-22 | 2 | 1 | 0.500 | 0.500 |
| ov-25 | 2 | 1 | 0.500 | 0.500 |
| ov-26 | 1 | 2 | 0.500 | 0.500 |
| ov-27 | 2 | 1 | 0.500 | 0.500 |
| ov-28 | 2 | 1 | 0.500 | 0.500 |
| ov-29 | 1 | 2 | 0.000 | 0.000 |
| ov-30 | 2 | 3 | 0.500 | 0.000 |
| ov-31 | 1 | 2 | 0.500 | 0.500 |
| ov-32 | 16 | 17 | 0.500 | 0.500 |
| ov-33 | - | - |  |  |
| ov-34 | - | - |  |  |
| ov-36 | 1 | 2 | 0.500 | 0.000 |
| ov-38 | 7 | 8 | 0.500 |  |
| ov-40 | 5 | 4 | 0.500 | 1.000 |
| ov-44 | - | - |  |  |
