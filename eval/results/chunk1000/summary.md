# Run: chunk1000

- split: **tune** (84 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=1000 overlap=100 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 1330 (embedded units: 1330); truncated by the embedding model: 93.5% of units, 70.8% of tokens never embedded
- gold quotes reachable in this chunking: 84/84
- run at: 2026-11-18 14:07

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66 | 0.417 | 0.205 | 0.659 | 0.833 | 0.485 [0.36, 0.61] | 0.338 [0.25, 0.43] | 0.644 [0.52, 0.75] | 0.536 [0.43, 0.64] | 0.560 [0.36, 0.76] | 0.525 [0.45, 0.62] |
| non_outdated | 41 | 0.573 | 0.280 | 0.744 | 0.829 | 0.585 [0.44, 0.73] | 0.422 [0.30, 0.55] | 0.744 [0.61, 0.87] |  |  |  |
| lookup | 17 | 0.706 | 0.353 | 0.824 | 0.824 | 0.706 [0.47, 0.88] | 0.471 [0.28, 0.66] | 0.882 [0.71, 1.00] |  |  |  |
| paraphrase | 10 | 0.500 | 0.200 | 0.700 | 0.800 | 0.400 [0.10, 0.70] | 0.282 [0.07, 0.54] | 0.600 [0.30, 0.90] |  |  |  |
| exact_term | 7 | 0.571 | 0.286 | 0.714 | 0.857 | 0.714 [0.29, 1.00] | 0.433 [0.16, 0.71] | 0.714 [0.29, 1.00] |  |  |  |
| multi_doc | 7 | 0.357 | 0.214 | 0.643 | 0.857 | 0.429 [0.14, 0.71] | 0.492 [0.17, 0.79] | 0.643 [0.29, 0.93] |  |  |  |
| outdated_version | 25 | 0.160 | 0.080 | 0.520 | 0.840 | 0.320 [0.16, 0.52] | 0.199 [0.09, 0.32] | 0.480 [0.28, 0.68] | 0.536 [0.43, 0.64] | 0.560 [0.36, 0.76] | 0.525 [0.45, 0.62] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.067 [0.07, 0.07] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.100 | 0.000 | 0.400 | 0.600 | 0.200 [0.00, 0.50] | 0.117 [0.01, 0.26] | 0.600 [0.30, 0.90] |  |  |  |

## All metrics

| group | n | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 66.000 | 0.417 | 0.614 | 0.644 | 0.560 | 0.205 | 0.371 | 0.485 | 0.338 | 0.525 | 0.571 | 0.536 | 0.500 | 0.560 | 0.550 | 0.536 | 0.659 | 0.833 |
| non_outdated | 41.000 | 0.573 | 0.695 | 0.744 | 0.688 | 0.280 | 0.427 | 0.585 | 0.422 |  |  |  |  |  |  |  | 0.744 | 0.829 |
| lookup | 17.000 | 0.706 | 0.824 | 0.882 | 0.772 | 0.353 | 0.471 | 0.706 | 0.471 |  |  |  |  |  |  |  | 0.824 | 0.824 |
| paraphrase | 10.000 | 0.500 | 0.500 | 0.600 | 0.551 | 0.200 | 0.300 | 0.400 | 0.282 |  |  |  |  |  |  |  | 0.700 | 0.800 |
| exact_term | 7.000 | 0.571 | 0.714 | 0.714 | 0.637 | 0.286 | 0.571 | 0.714 | 0.433 |  |  |  |  |  |  |  | 0.714 | 0.857 |
| multi_doc | 7.000 | 0.357 | 0.643 | 0.643 | 0.733 | 0.214 | 0.357 | 0.429 | 0.492 |  |  |  |  |  |  |  | 0.643 | 0.857 |
| outdated_version | 25.000 | 0.160 | 0.480 | 0.480 | 0.350 | 0.080 | 0.280 | 0.320 | 0.199 | 0.525 | 0.571 | 0.536 | 0.500 | 0.560 | 0.550 | 0.536 | 0.520 | 0.840 |
| real_pair | 1.000 | 0.000 | 0.000 | 1.000 | 0.250 | 0.000 | 0.000 | 0.000 | 0.067 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 0.100 | 0.500 | 0.600 | 0.333 | 0.000 | 0.200 | 0.200 | 0.117 |  |  |  |  |  |  |  | 0.400 | 0.600 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/legacy/legacy-subscription-agreement-v4 | How long does GitLab retain security incident communications sent to customers? |
| lk-11 | lookup | 12 | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | Over what reference period are average weekly working hours calculated for the 48-hour limit in GitLab's people policies? |
| pp-03 | paraphrase | 8 | hb:legal/legacy/legacy-subscription-agreement-v4 | As a GitLab Support engineer, when should I rethink the dates I want to take off? |
| pp-04 | paraphrase | not found | hb:legal/subscription-agreement/index | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| pp-05 | paraphrase | 10 | hb:security/security-assurance/governance/sec-awareness-training | Do people joining GitLab have to complete a security course when they start? |
| pp-14 | paraphrase | 26 | hb:finance/procurement/vendor-guidelines/legacy-vendor-agreement-v1 | Can I buy second-hand work equipment from an individual and claim it back from GitLab? |
| ex-06 | exact_term | 8 | hb:legal/privacy/customer-product-usage-information | For which GitLab entities is the default mileage rate set at $.50/mile? |
| ex-08 | exact_term | not found | hb:total-rewards/compensation | What is LevelUp at GitLab? |
| md-06 | multi_doc | 21 | hb:legal/legacy/data-processing-addendum-and-standard-contractual-clauses | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| md-10 | multi_doc | 12 | hb:legal/privacy/transparency-reports | What is RED data at GitLab, and how often must access to Red Data systems be reviewed? |
| ov-06 | outdated_version | 7 | hb:finance/accounting | How long after the purchase date can I submit a GitLab expense claim and still be reimbursed without manager approval? |
| ov-08 | outdated_version | 6 | hb:finance/travel/sponsored | How much can I spend on meals per day while travelling for GitLab? |
| ov-11 | outdated_version | 8 | hb:total-rewards/benefits/general-and-entity-benefits/canada-corp-benefits | How long is parental leave for GitLab team members in the US? |
| ov-21 | outdated_version | 18 | hb:legal/privacy/transparency-reports | After how many failed login attempts must a GitLab system temporarily lock the account? |
| ov-22 | outdated_version | not found | hb:legal/technology-partner-agreement-v1 | What is the maximum lifetime of a GitLab group access token? |
| ov-26 | outdated_version | not found | hb:finance/expenses | How long can a business trip last and still be covered by GitLab's travel insurance? |
| ov-27 | outdated_version | 26 | hb:finance/expenses | What is the maximum baggage protection under GitLab's business travel insurance? |
| ov-32 | outdated_version | 7 | hb:hiring/interviewing/customer-support-interviewing | How long does GitLab's recruiting team take to review a referral submission? |
| ov-33 | outdated_version | not found | hb:legal/record-retention-policy | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | hb:total-rewards/benefits/general-and-entity-benefits/gitlab-gk | How long does GitLab keep risk treatment plans? |
| ov-36 | outdated_version | 14 | hb:hiring/interviewing/customer-support-interviewing | If someone I referred to GitLab reached team interviews but wasn't hired, how long should I wait before referring them again? |
| ov-38 | outdated_version | 6 | syn:expenses-2023 | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/subscription-agreement/index | What discount on legal fees does GitLab's US legal services benefit provide? |

## Outdated-version questions

stale / fact_stale: 1 = old version first, 0.5 = exact score tie, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 7 | 6 | 0.500 |  |
| ov-07 | 2 | 1 | 1.000 |  |
| ov-08 | 6 | 5 | 0.500 | 1.000 |
| ov-11 | 8 | 9 | 0.500 | 0.500 |
| ov-12 | 2 | 3 | 0.500 |  |
| ov-13 | 2 | 1 | 0.500 | 0.500 |
| ov-14 | 1 | 3 | 0.500 | 0.500 |
| ov-16 | 3 | 2 | 0.500 |  |
| ov-17 | 1 | 2 | 0.500 | 0.500 |
| ov-21 | 18 | 19 | 0.500 | 0.500 |
| ov-22 | - | - |  |  |
| ov-25 | 1 | 2 | 0.500 | 0.500 |
| ov-26 | - | - |  |  |
| ov-27 | 26 | 25 | 0.500 | 0.500 |
| ov-28 | 2 | 1 | 0.500 | 0.500 |
| ov-29 | 2 | 5 | 0.000 | 0.000 |
| ov-30 | 2 | 1 | 0.500 | 0.500 |
| ov-31 | 1 | 2 | 0.500 | 0.500 |
| ov-32 | 7 | 6 | 0.500 | 0.500 |
| ov-33 | - | - |  |  |
| ov-34 | - | - |  |  |
| ov-36 | 14 | 15 | 0.500 |  |
| ov-38 | 6 | 1 | 1.000 | 1.000 |
| ov-40 | 2 | 1 | 0.500 |  |
| ov-44 | - | - |  |  |
