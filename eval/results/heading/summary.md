# Run: heading

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: heading size=500 overlap=50 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 4704 (embedded units: 4704); truncated by the embedding model: 35.0% of units, 25.2% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 14:53

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.508 | 0.230 | 0.679 | 0.774 | 0.456 [0.36, 0.55] | 0.377 [0.30, 0.46] | 0.770 [0.69, 0.85] | 0.500 [0.38, 0.64] | 0.760 [0.58, 0.92] | 0.523 [0.45, 0.61] |
| non_outdated | 101 | 0.594 | 0.257 | 0.658 | 0.777 | 0.460 [0.36, 0.56] | 0.400 [0.31, 0.48] | 0.782 [0.70, 0.87] |  |  |  |
| lookup | 42 | 0.690 | 0.286 | 0.643 | 0.738 | 0.476 [0.33, 0.63] | 0.387 [0.25, 0.52] | 0.833 [0.70, 0.95] |  |  |  |
| paraphrase | 30 | 0.533 | 0.167 | 0.567 | 0.800 | 0.367 [0.19, 0.55] | 0.245 [0.13, 0.38] | 0.733 [0.54, 0.90] |  |  |  |
| exact_term | 7 | 0.857 | 0.714 | 1.000 | 1.000 | 0.857 [0.57, 1.00] | 0.800 [0.54, 1.00] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.400 | 0.200 | 0.833 | 0.867 | 0.500 [0.33, 0.61] | 0.567 [0.33, 0.79] | 0.767 [0.50, 0.93] |  |  |  |
| compound | 7 | 0.429 | 0.143 | 0.429 | 0.500 | 0.286 [0.08, 0.44] | 0.377 [0.06, 0.68] | 0.643 [0.30, 0.88] |  |  |  |
| outdated_version | 25 | 0.160 | 0.120 | 0.760 | 0.760 | 0.440 [0.22, 0.64] | 0.285 [0.14, 0.43] | 0.720 [0.52, 0.88] | 0.500 [0.38, 0.64] | 0.760 [0.58, 0.92] | 0.523 [0.45, 0.61] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.500 [0.50, 0.50] | 1.000 [1.00, 1.00] | 0.500 [0.50, 0.50] | 1.000 [1.00, 1.00] | 0.500 [0.50, 0.50] |
| history | 10 | 0.400 | 0.300 | 0.900 | 0.900 | 0.700 [0.40, 1.00] | 0.447 [0.22, 0.69] | 0.900 [0.70, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.508 | 0.722 | 0.770 | 0.687 | 0.230 | 0.397 | 0.456 | 0.377 | 0.523 | 0.500 | 0.500 | 0.409 | 0.760 | 0.568 | 0.500 | 0.679 | 0.774 |
| non_outdated | 101.000 | 61.000 | 0.594 | 0.743 | 0.782 | 0.753 | 0.257 | 0.406 | 0.460 | 0.400 |  |  |  |  |  |  |  | 0.658 | 0.777 |
| lookup | 42.000 | 34.000 | 0.690 | 0.833 | 0.833 | 0.767 | 0.286 | 0.476 | 0.476 | 0.387 |  |  |  |  |  |  |  | 0.643 | 0.738 |
| paraphrase | 30.000 | 28.000 | 0.533 | 0.667 | 0.733 | 0.625 | 0.167 | 0.267 | 0.367 | 0.245 |  |  |  |  |  |  |  | 0.567 | 0.800 |
| exact_term | 7.000 | 7.000 | 0.857 | 0.857 | 0.857 | 0.871 | 0.714 | 0.857 | 0.857 | 0.800 |  |  |  |  |  |  |  | 1.000 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.400 | 0.633 | 0.767 | 0.856 | 0.200 | 0.367 | 0.500 | 0.567 |  |  |  |  |  |  |  | 0.833 | 0.867 |
| compound | 7.000 | 5.000 | 0.429 | 0.643 | 0.643 | 0.873 | 0.143 | 0.214 | 0.286 | 0.377 |  |  |  |  |  |  |  | 0.429 | 0.500 |
| outdated_version | 25.000 | 22.000 | 0.160 | 0.640 | 0.720 | 0.423 | 0.120 | 0.360 | 0.440 | 0.285 | 0.523 | 0.500 | 0.500 | 0.409 | 0.760 | 0.568 | 0.500 | 0.760 | 0.760 |
| real_pair | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.500 | 0.000 | 1.000 | 1.000 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.400 | 0.900 | 0.900 | 0.637 | 0.300 | 0.500 | 0.700 | 0.447 |  |  |  |  |  |  |  | 0.900 | 0.900 |

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
| lk-30 | lookup | not found | hb:legal/privacy/transparency-reports | My request for an exception to a GitLab security policy was turned down. Where do I send an appeal? |
| lk-32 | lookup | not found | hb:legal/privacy/law-enforcement-guidelines | What happens when an emergency ticket comes in to GitLab Support? |
| lk-33 | lookup | 14 | hb:support/support-engineer-responsibilities | I've been on an emergency customer ticket for over an hour and two colleagues have joined in. What should I set up? |
| lk-39 | lookup | 6 | syn:inc-benefits-us-2023 | I just got married and I work for GitLab Korea. How long do I have to add my spouse to my insurance? |
| lk-41 | lookup | 6 | hb:total-rewards/incentives | How often is the bonus paid for GitLab directors and above? |
| pp-24 | paraphrase | not found | hb:total-rewards/incentives | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 20 | hb:legal/readmes/emilyplotkin | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-27 | paraphrase | 29 | hb:support/support-time-off | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | 9 | hb:finance/expenses | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:legal/privacy/employee-privacy-policy | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-32 | paraphrase | 9 | hb:legal/esg/esg-training | Does GitLab give staff in Belgium anything each year towards environmentally friendly purchases? |
| pp-33 | paraphrase | not found | hb:legal/anti-corruption-policy | Where must the sign-off for a GitLab security policy exception be recorded? |
| pp-34 | paraphrase | not found | hb:legal/legacy/legacy-reseller-agreement-v1 | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |
| md-21 | compound | 9 | pdf:salford-whistleblowing | How long does the University of Roehampton aim to take over an external whistleblowing investigation, and within what time must pay-discrimination complaints be filed under GitLab Inc's US notices? |

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
