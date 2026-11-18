# Run: baseline

- split: **tune** (84 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 92.7% of units, 46.7% of tokens never embedded
- gold quotes reachable in this chunking: 84/84
- run at: 2026-11-18 14:06

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66 | 0.432 | 0.159 | 0.614 | 0.758 | 0.455 [0.33, 0.58] | 0.320 [0.23, 0.41] | 0.735 [0.63, 0.83] | 0.458 [0.33, 0.58] | 0.480 [0.28, 0.68] | 0.477 [0.39, 0.57] |
| non_outdated | 41 | 0.646 | 0.232 | 0.695 | 0.780 | 0.512 [0.35, 0.66] | 0.403 [0.28, 0.53] | 0.793 [0.67, 0.90] |  |  |  |
| lookup | 17 | 0.706 | 0.118 | 0.706 | 0.824 | 0.471 [0.24, 0.71] | 0.290 [0.15, 0.45] | 0.882 [0.71, 1.00] |  |  |  |
| paraphrase | 10 | 0.700 | 0.300 | 0.600 | 0.700 | 0.400 [0.10, 0.70] | 0.346 [0.11, 0.63] | 0.700 [0.40, 1.00] |  |  |  |
| exact_term | 7 | 0.714 | 0.429 | 0.857 | 0.857 | 0.857 [0.57, 1.00] | 0.619 [0.33, 0.86] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 7 | 0.357 | 0.214 | 0.643 | 0.714 | 0.429 [0.14, 0.71] | 0.542 [0.22, 0.86] | 0.643 [0.36, 0.86] |  |  |  |
| outdated_version | 25 | 0.080 | 0.040 | 0.480 | 0.720 | 0.360 [0.20, 0.56] | 0.185 [0.09, 0.29] | 0.640 [0.44, 0.80] | 0.458 [0.33, 0.58] | 0.480 [0.28, 0.68] | 0.477 [0.39, 0.57] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.043 [0.04, 0.04] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.200 | 0.100 | 0.800 | 1.000 | 0.500 [0.20, 0.80] | 0.272 [0.12, 0.47] | 0.800 [0.50, 1.00] |  |  |  |

## All metrics

| group | n | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66.000 | 0.432 | 0.682 | 0.735 | 0.604 | 0.159 | 0.409 | 0.455 | 0.320 | 0.477 | 0.438 | 0.458 | 0.333 | 0.480 | 0.545 | 0.500 | 0.614 | 0.758 |
| non_outdated | 41.000 | 0.646 | 0.756 | 0.793 | 0.759 | 0.232 | 0.463 | 0.512 | 0.403 |  |  |  |  |  |  |  | 0.695 | 0.780 |
| lookup | 17.000 | 0.706 | 0.882 | 0.882 | 0.784 | 0.118 | 0.412 | 0.471 | 0.290 |  |  |  |  |  |  |  | 0.706 | 0.824 |
| paraphrase | 10.000 | 0.700 | 0.700 | 0.700 | 0.706 | 0.300 | 0.400 | 0.400 | 0.346 |  |  |  |  |  |  |  | 0.600 | 0.700 |
| exact_term | 7.000 | 0.714 | 0.857 | 0.857 | 0.786 | 0.429 | 0.857 | 0.857 | 0.619 |  |  |  |  |  |  |  | 0.857 | 0.857 |
| multi_doc | 7.000 | 0.357 | 0.429 | 0.643 | 0.750 | 0.214 | 0.286 | 0.429 | 0.542 |  |  |  |  |  |  |  | 0.643 | 0.714 |
| outdated_version | 25.000 | 0.080 | 0.560 | 0.640 | 0.349 | 0.040 | 0.320 | 0.360 | 0.185 | 0.477 | 0.438 | 0.458 | 0.333 | 0.480 | 0.545 | 0.500 | 0.480 | 0.720 |
| real_pair | 1.000 | 0.000 | 1.000 | 1.000 | 0.500 | 0.000 | 0.000 | 0.000 | 0.043 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 0.200 | 0.800 | 0.800 | 0.503 | 0.100 | 0.300 | 0.500 | 0.272 |  |  |  |  |  |  |  | 0.800 | 1.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/legacy/legacy-subscription-agreement-v4 | How long does GitLab retain security incident communications sent to customers? |
| lk-11 | lookup | not found | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | Over what reference period are average weekly working hours calculated for the 48-hour limit in GitLab's people policies? |
| pp-03 | paraphrase | 18 | hb:legal/legacy/legacy-subscription-agreement-v4 | As a GitLab Support engineer, when should I rethink the dates I want to take off? |
| pp-04 | paraphrase | not found | hb:legal/legacy/legacy-subscription-agreement-v5 | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| pp-14 | paraphrase | not found | hb:finance/procurement/vendor-guidelines/legacy-vendor-agreement-v1 | Can I buy second-hand work equipment from an individual and claim it back from GitLab? |
| ex-08 | exact_term | not found | hb:total-rewards/compensation | What is LevelUp at GitLab? |
| md-06 | multi_doc | not found | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-06 | outdated_version | 17 | hb:finance/accounting | How long after the purchase date can I submit a GitLab expense claim and still be reimbursed without manager approval? |
| ov-11 | outdated_version | 7 | hb:total-rewards/benefits/general-and-entity-benefits/korea-ltd-benefits | How long is parental leave for GitLab team members in the US? |
| ov-21 | outdated_version | 28 | hb:legal/privacy/transparency-reports | After how many failed login attempts must a GitLab system temporarily lock the account? |
| ov-32 | outdated_version | 13 | hb:hiring/referral-process | How long does GitLab's recruiting team take to review a referral submission? |
| ov-33 | outdated_version | not found | hb:legal/record-retention-policy | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | hb:legal/eu-data-act-terms | How long does GitLab keep risk treatment plans? |
| ov-36 | outdated_version | 7 | hb:hiring/interviewing/customer-support-interviewing | If someone I referred to GitLab reached team interviews but wasn't hired, how long should I wait before referring them again? |
| ov-38 | outdated_version | 10 | hb:support | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/legacy/legacy-subscription-agreement-v7 | What discount on legal fees does GitLab's US legal services benefit provide? |

## Outdated-version questions

stale / fact_stale: 1 = old version first, 0.5 = exact score tie, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 17 | 18 | 0.500 |  |
| ov-07 | 2 | 1 | 0.500 |  |
| ov-08 | 2 | 3 | 0.500 |  |
| ov-11 | 7 | 8 | 0.500 |  |
| ov-12 | 4 | 3 | 0.500 |  |
| ov-13 | 2 | 1 | 0.500 | 0.500 |
| ov-14 | 1 | 3 | 0.000 | 0.500 |
| ov-16 | 4 | 3 | 0.500 |  |
| ov-17 | 1 | 2 | 0.000 | 0.000 |
| ov-21 | 28 | 29 | 0.500 |  |
| ov-22 | 2 | 1 | 0.500 |  |
| ov-25 | 2 | 3 | 0.500 | 0.500 |
| ov-26 | 2 | 1 | 0.500 | 0.500 |
| ov-27 | 2 | 1 | 0.500 | 0.500 |
| ov-28 | 2 | 1 | 0.500 | 0.500 |
| ov-29 | 3 | 6 | 0.000 | 0.000 |
| ov-30 | 3 | 2 | 0.500 | 0.500 |
| ov-31 | 2 | 1 | 0.500 | 0.500 |
| ov-32 | 13 | 12 | 0.500 | 0.500 |
| ov-33 | - | - |  |  |
| ov-34 | - | - |  |  |
| ov-36 | 7 | 8 | 0.500 |  |
| ov-38 | 10 | 6 | 1.000 | 1.000 |
| ov-40 | 2 | 1 | 1.000 |  |
| ov-44 | - | - |  |  |
