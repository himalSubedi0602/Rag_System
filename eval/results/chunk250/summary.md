# Run: chunk250

- split: **tune** (84 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=250 overlap=25 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 4774 (embedded units: 4774); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 84/84
- run at: 2026-11-18 14:07

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66 | 0.462 | 0.167 | 0.598 | 0.742 | 0.417 [0.30, 0.53] | 0.288 [0.20, 0.38] | 0.811 [0.71, 0.89] | 0.538 [0.38, 0.69] | 0.520 [0.32, 0.72] | 0.455 [0.34, 0.57] |
| non_outdated | 41 | 0.573 | 0.220 | 0.671 | 0.780 | 0.524 [0.37, 0.67] | 0.367 [0.25, 0.49] | 0.866 [0.77, 0.95] |  |  |  |
| lookup | 17 | 0.647 | 0.235 | 0.706 | 0.882 | 0.529 [0.29, 0.76] | 0.342 [0.18, 0.54] | 0.941 [0.82, 1.00] |  |  |  |
| paraphrase | 10 | 0.600 | 0.200 | 0.500 | 0.600 | 0.300 [0.00, 0.60] | 0.258 [0.02, 0.51] | 0.900 [0.70, 1.00] |  |  |  |
| exact_term | 7 | 0.571 | 0.286 | 0.857 | 0.857 | 0.857 [0.57, 1.00] | 0.476 [0.23, 0.74] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 7 | 0.357 | 0.143 | 0.643 | 0.714 | 0.500 [0.21, 0.79] | 0.472 [0.19, 0.75] | 0.643 [0.36, 0.86] |  |  |  |
| outdated_version | 25 | 0.280 | 0.080 | 0.480 | 0.680 | 0.240 [0.08, 0.40] | 0.158 [0.06, 0.28] | 0.720 [0.56, 0.88] | 0.538 [0.38, 0.69] | 0.520 [0.32, 0.72] | 0.455 [0.34, 0.57] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.200 [0.20, 0.20] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.100 | 0.000 | 0.600 | 0.800 | 0.200 [0.00, 0.50] | 0.120 [0.02, 0.26] | 0.900 [0.70, 1.00] |  |  |  |

## All metrics

| group | n | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66.000 | 0.462 | 0.705 | 0.811 | 0.644 | 0.167 | 0.303 | 0.417 | 0.288 | 0.455 | 0.474 | 0.538 | 0.571 | 0.520 | 0.545 | 0.692 | 0.598 | 0.742 |
| non_outdated | 41.000 | 0.573 | 0.817 | 0.866 | 0.754 | 0.220 | 0.366 | 0.524 | 0.367 |  |  |  |  |  |  |  | 0.671 | 0.780 |
| lookup | 17.000 | 0.647 | 0.941 | 0.941 | 0.775 | 0.235 | 0.353 | 0.529 | 0.342 |  |  |  |  |  |  |  | 0.706 | 0.882 |
| paraphrase | 10.000 | 0.600 | 0.800 | 0.900 | 0.725 | 0.200 | 0.300 | 0.300 | 0.258 |  |  |  |  |  |  |  | 0.500 | 0.600 |
| exact_term | 7.000 | 0.571 | 0.857 | 0.857 | 0.714 | 0.286 | 0.571 | 0.857 | 0.476 |  |  |  |  |  |  |  | 0.857 | 0.857 |
| multi_doc | 7.000 | 0.357 | 0.500 | 0.643 | 0.786 | 0.143 | 0.286 | 0.500 | 0.472 |  |  |  |  |  |  |  | 0.643 | 0.714 |
| outdated_version | 25.000 | 0.280 | 0.520 | 0.720 | 0.465 | 0.080 | 0.200 | 0.240 | 0.158 | 0.455 | 0.474 | 0.538 | 0.571 | 0.520 | 0.545 | 0.692 | 0.480 | 0.680 |
| real_pair | 1.000 | 0.000 | 0.000 | 1.000 | 0.200 | 0.000 | 0.000 | 1.000 | 0.200 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 0.100 | 0.900 | 0.900 | 0.471 | 0.000 | 0.200 | 0.200 | 0.120 |  |  |  |  |  |  |  | 0.600 | 0.800 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/subscription-agreement/index | How long does GitLab retain security incident communications sent to customers? |
| pp-14 | paraphrase | not found | hb:finance/procurement/vendor-guidelines/legacy-vendor-agreement-v1 | Can I buy second-hand work equipment from an individual and claim it back from GitLab? |
| ex-08 | exact_term | not found | hb:security/security-assurance/security-compliance/sec-controls | What is LevelUp at GitLab? |
| md-06 | multi_doc | not found | hb:finance/procurement/vendor-guidelines/vendor-security-addendum | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-11 | outdated_version | 12 | hb:total-rewards/benefits/general-and-entity-benefits/ltd-benefits-uk | How long is parental leave for GitLab team members in the US? |
| ov-29 | outdated_version | 6 | syn:us-leave-of-absence-2022 | Up to what age are team members' children eligible for Modern Health? |
| ov-32 | outdated_version | 6 | hb:hiring/interviewing/customer-support-interviewing | How long does GitLab's recruiting team take to review a referral submission? |
| ov-33 | outdated_version | not found | hb:legal/record-retention-policy | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab keep risk treatment plans? |
| ov-38 | outdated_version | 19 | hb:support | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/subscription-agreement/index | What discount on legal fees does GitLab's US legal services benefit provide? |

## Outdated-version questions

stale / fact_stale: 1 = old version first, 0.5 = exact score tie, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 1 | 2 | 0.500 |  |
| ov-07 | 1 | 2 | 0.000 |  |
| ov-08 | 2 | 1 | 1.000 |  |
| ov-11 | 12 | 11 | 0.500 |  |
| ov-12 | 5 | 4 | 0.500 |  |
| ov-13 | 2 | 1 | 0.500 | 0.500 |
| ov-14 | 1 | 2 | 0.000 | 0.000 |
| ov-16 | 4 | 3 | 0.500 |  |
| ov-17 | 2 | 1 | 1.000 | 1.000 |
| ov-21 | 1 | 2 | 0.500 | 0.500 |
| ov-22 | 1 | 2 | 0.500 |  |
| ov-25 | 1 | 2 | 0.500 | 0.500 |
| ov-26 | 2 | 1 | 0.500 |  |
| ov-27 | 4 | 3 | 0.500 |  |
| ov-28 | 2 | 1 | 0.500 | 0.500 |
| ov-29 | 6 | 9 | 0.000 | 0.000 |
| ov-30 | 5 | 6 | 0.500 | 0.500 |
| ov-31 | 2 | 3 | 0.500 | 0.500 |
| ov-32 | 6 | 5 | 0.500 | 0.500 |
| ov-33 | - | - |  |  |
| ov-34 | - | - |  |  |
| ov-36 | 4 | 3 | 0.500 | 0.500 |
| ov-38 | 19 | 18 | 0.500 | 1.000 |
| ov-40 | 1 | 2 | 0.000 | 1.000 |
| ov-44 | - | - |  |  |
