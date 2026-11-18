# Run: small2big

- split: **tune** (84 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 7189); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 84/84
- run at: 2026-11-18 14:07

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66 | 0.439 | 0.205 | 0.758 | 0.864 | 0.523 [0.40, 0.64] | 0.371 [0.28, 0.47] | 0.758 [0.64, 0.85] | 0.500 [0.36, 0.64] | 0.720 [0.52, 0.88] | 0.545 [0.43, 0.66] |
| non_outdated | 41 | 0.585 | 0.280 | 0.780 | 0.829 | 0.622 [0.48, 0.76] | 0.465 [0.34, 0.59] | 0.854 [0.76, 0.94] |  |  |  |
| lookup | 17 | 0.588 | 0.294 | 0.882 | 0.941 | 0.647 [0.41, 0.82] | 0.422 [0.25, 0.62] | 0.882 [0.71, 1.00] |  |  |  |
| paraphrase | 10 | 0.600 | 0.200 | 0.600 | 0.700 | 0.500 [0.20, 0.80] | 0.308 [0.09, 0.55] | 0.900 [0.70, 1.00] |  |  |  |
| exact_term | 7 | 0.714 | 0.286 | 0.857 | 0.857 | 0.857 [0.57, 1.00] | 0.529 [0.27, 0.79] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 7 | 0.429 | 0.357 | 0.714 | 0.714 | 0.500 [0.21, 0.79] | 0.732 [0.36, 1.00] | 0.714 [0.43, 0.93] |  |  |  |
| outdated_version | 25 | 0.200 | 0.080 | 0.720 | 0.920 | 0.360 [0.16, 0.56] | 0.217 [0.12, 0.34] | 0.600 [0.40, 0.80] | 0.500 [0.36, 0.64] | 0.720 [0.52, 0.88] | 0.545 [0.43, 0.66] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.200 [0.20, 0.20] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.200 | 0.200 | 0.800 | 1.000 | 0.600 [0.30, 0.90] | 0.329 [0.14, 0.56] | 0.900 [0.70, 1.00] |  |  |  |

## All metrics

| group | n | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66.000 | 0.439 | 0.697 | 0.758 | 0.619 | 0.205 | 0.394 | 0.523 | 0.371 | 0.545 | 0.618 | 0.500 | 0.545 | 0.720 | 0.591 | 0.583 | 0.758 | 0.864 |
| non_outdated | 41.000 | 0.585 | 0.780 | 0.854 | 0.748 | 0.280 | 0.488 | 0.622 | 0.465 |  |  |  |  |  |  |  | 0.780 | 0.829 |
| lookup | 17.000 | 0.588 | 0.882 | 0.882 | 0.724 | 0.294 | 0.529 | 0.647 | 0.422 |  |  |  |  |  |  |  | 0.882 | 0.941 |
| paraphrase | 10.000 | 0.600 | 0.800 | 0.900 | 0.712 | 0.200 | 0.300 | 0.500 | 0.308 |  |  |  |  |  |  |  | 0.600 | 0.700 |
| exact_term | 7.000 | 0.714 | 0.714 | 0.857 | 0.750 | 0.286 | 0.714 | 0.857 | 0.529 |  |  |  |  |  |  |  | 0.857 | 0.857 |
| multi_doc | 7.000 | 0.429 | 0.571 | 0.714 | 0.857 | 0.357 | 0.429 | 0.500 | 0.732 |  |  |  |  |  |  |  | 0.714 | 0.714 |
| outdated_version | 25.000 | 0.200 | 0.560 | 0.600 | 0.406 | 0.080 | 0.240 | 0.360 | 0.217 | 0.545 | 0.618 | 0.500 | 0.545 | 0.720 | 0.591 | 0.583 | 0.720 | 0.920 |
| real_pair | 1.000 | 0.000 | 0.000 | 1.000 | 0.200 | 0.000 | 0.000 | 1.000 | 0.200 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 0.200 | 0.800 | 0.900 | 0.496 | 0.200 | 0.300 | 0.600 | 0.329 |  |  |  |  |  |  |  | 0.800 | 1.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/subscription-agreement/index | How long does GitLab retain security incident communications sent to customers? |
| lk-07 | lookup | 7 | hb:finance/procurement/vendor-guidelines/vendor-security-addendum | How often are user access reviews performed for SOX in-scope applications at GitLab? |
| pp-14 | paraphrase | 30 | hb:finance/procurement/vendor-guidelines/legacy-vendor-agreement-v1 | Can I buy second-hand work equipment from an individual and claim it back from GitLab? |
| ex-08 | exact_term | not found | hb:total-rewards/compensation | What is LevelUp at GitLab? |
| md-06 | multi_doc | not found | hb:finance/procurement/vendor-guidelines/vendor-security-addendum | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-11 | outdated_version | 12 | hb:total-rewards/benefits/general-and-entity-benefits/singapore-pte-ltd | How long is parental leave for GitLab team members in the US? |
| ov-16 | outdated_version | 6 | hb:hiring/candidate-faq | How far in advance should GitLab team members book international flights? |
| ov-27 | outdated_version | 7 | hb:legal/testing-agreement-v5 | What is the maximum baggage protection under GitLab's business travel insurance? |
| ov-29 | outdated_version | 14 | syn:ltd-benefits-uk-2023 | Up to what age are team members' children eligible for Modern Health? |
| ov-32 | outdated_version | 8 | hb:hiring/interviewing/customer-support-interviewing | How long does GitLab's recruiting team take to review a referral submission? |
| ov-33 | outdated_version | not found | hb:legal/record-retention-policy | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab keep risk treatment plans? |
| ov-36 | outdated_version | 6 | hb:hiring/talent-acquisition-framework/coordinator | If someone I referred to GitLab reached team interviews but wasn't hired, how long should I wait before referring them again? |
| ov-38 | outdated_version | 27 | hb:hiring/talent-acquisition-framework/coordinator | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/legacy/legacy-reseller-agreement-v1 | What discount on legal fees does GitLab's US legal services benefit provide? |

## Outdated-version questions

stale / fact_stale: 1 = old version first, 0.5 = exact score tie, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 2 | 3 | 0.500 | 0.500 |
| ov-07 | 2 | 1 | 1.000 |  |
| ov-08 | 3 | 2 | 1.000 | 0.000 |
| ov-11 | 12 | 13 | 0.500 |  |
| ov-12 | 5 | 4 | 0.500 | 0.500 |
| ov-13 | 2 | 1 | 0.500 | 0.500 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 6 | 5 | 0.500 |  |
| ov-17 | 1 | 2 | 0.000 | 0.000 |
| ov-21 | 1 | 2 | 0.500 | 0.500 |
| ov-22 | 1 | 2 | 0.500 |  |
| ov-25 | 1 | 2 | 0.500 | 0.500 |
| ov-26 | 2 | 1 | 0.500 | 0.500 |
| ov-27 | 7 | 6 | 0.500 | 0.500 |
| ov-28 | 2 | 1 | 0.500 | 0.500 |
| ov-29 | 14 | 19 | 0.000 | 0.000 |
| ov-30 | 2 | 1 | 0.500 | 0.500 |
| ov-31 | 3 | 2 | 0.500 | 0.500 |
| ov-32 | 8 | 7 | 0.500 | 0.500 |
| ov-33 | - | - |  |  |
| ov-34 | - | - |  |  |
| ov-36 | 6 | 4 | 0.500 | 0.500 |
| ov-38 | 27 | 20 | 1.000 | 1.000 |
| ov-40 | 1 | 2 | 0.500 | 1.000 |
| ov-44 | - | - |  |  |
