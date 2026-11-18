# Run: s2b_heading

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: heading size=500 overlap=50 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 4704 (embedded units: 7515); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:09

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.476 | 0.250 | 0.722 | 0.849 | 0.508 [0.42, 0.60] | 0.407 [0.33, 0.48] | 0.778 [0.70, 0.86] | 0.526 [0.33, 0.72] | 0.760 [0.57, 0.92] | 0.455 [0.29, 0.65] |
| non_outdated | 101 | 0.564 | 0.292 | 0.713 | 0.861 | 0.505 [0.40, 0.60] | 0.436 [0.34, 0.53] | 0.792 [0.71, 0.87] |  |  |  |
| lookup | 42 | 0.667 | 0.333 | 0.738 | 0.857 | 0.571 [0.42, 0.72] | 0.446 [0.32, 0.58] | 0.857 [0.73, 0.97] |  |  |  |
| paraphrase | 30 | 0.467 | 0.233 | 0.567 | 0.867 | 0.400 [0.22, 0.59] | 0.306 [0.16, 0.45] | 0.733 [0.54, 0.90] |  |  |  |
| exact_term | 7 | 0.857 | 0.571 | 1.000 | 1.000 | 0.857 [0.57, 1.00] | 0.720 [0.45, 0.93] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.400 | 0.233 | 0.867 | 0.867 | 0.500 [0.33, 0.61] | 0.571 [0.31, 0.78] | 0.767 [0.56, 0.91] |  |  |  |
| compound | 7 | 0.429 | 0.143 | 0.571 | 0.714 | 0.214 [0.00, 0.43] | 0.367 [0.05, 0.68] | 0.643 [0.30, 0.88] |  |  |  |
| outdated_version | 25 | 0.120 | 0.080 | 0.760 | 0.800 | 0.520 [0.30, 0.72] | 0.289 [0.17, 0.41] | 0.720 [0.52, 0.88] | 0.526 [0.33, 0.72] | 0.760 [0.57, 0.92] | 0.455 [0.29, 0.65] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.500 [0.50, 0.50] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.500 | 0.300 | 0.900 | 0.900 | 0.600 [0.30, 0.90] | 0.433 [0.20, 0.68] | 0.900 [0.70, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.476 | 0.742 | 0.778 | 0.670 | 0.250 | 0.456 | 0.508 | 0.407 | 0.455 | 0.500 | 0.526 | 0.571 | 0.760 | 0.545 | 0.526 | 0.523 | 0.500 | 0.500 | 0.500 | 0.722 | 0.849 |
| non_outdated | 101.000 | 61.000 | 0.564 | 0.748 | 0.792 | 0.737 | 0.292 | 0.450 | 0.505 | 0.436 |  |  |  |  |  |  |  |  |  |  |  | 0.713 | 0.861 |
| lookup | 42.000 | 34.000 | 0.667 | 0.857 | 0.857 | 0.768 | 0.333 | 0.571 | 0.571 | 0.446 |  |  |  |  |  |  |  |  |  |  |  | 0.738 | 0.857 |
| paraphrase | 30.000 | 28.000 | 0.467 | 0.667 | 0.733 | 0.583 | 0.233 | 0.300 | 0.400 | 0.306 |  |  |  |  |  |  |  |  |  |  |  | 0.567 | 0.867 |
| exact_term | 7.000 | 7.000 | 0.857 | 0.857 | 0.857 | 0.863 | 0.571 | 0.857 | 0.857 | 0.720 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.400 | 0.600 | 0.767 | 0.839 | 0.233 | 0.333 | 0.500 | 0.571 |  |  |  |  |  |  |  |  |  |  |  | 0.867 | 0.867 |
| compound | 7.000 | 5.000 | 0.429 | 0.643 | 0.643 | 0.870 | 0.143 | 0.214 | 0.214 | 0.367 |  |  |  |  |  |  |  |  |  |  |  | 0.571 | 0.714 |
| outdated_version | 25.000 | 22.000 | 0.120 | 0.720 | 0.720 | 0.400 | 0.080 | 0.480 | 0.520 | 0.289 | 0.455 | 0.500 | 0.526 | 0.571 | 0.760 | 0.545 | 0.526 | 0.523 | 0.500 | 0.500 | 0.500 | 0.760 | 0.800 |
| real_pair | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.500 | 0.000 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | 0.500 | 0.500 | 0.500 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.500 | 0.900 | 0.900 | 0.671 | 0.300 | 0.500 | 0.600 | 0.433 |  |  |  |  |  |  |  |  |  |  |  | 0.900 | 0.900 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-02 | lookup | 6 | hb:finance/procurement/tips-for-submitting-a-zip-request | What is the monthly limit for reimbursing a co-working space at GitLab? |
| lk-06 | lookup | not found | hb:legal/legacy/legacy-subscription-agreement-v5 | How long does GitLab retain security incident communications sent to customers? |
| ex-08 | exact_term | 24 | hb:legal/ethics-compliance-program/compliance-training | What is LevelUp at GitLab? |
| md-06 | multi_doc | not found | hb:legal/legacy/data-processing-addendum-and-standard-contractual-clauses | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-08 | outdated_version | 14 | hb:legal/esg/earth-month | How much can I spend on meals per day while travelling for GitLab? |
| ov-11 | outdated_version | 22 | hb:total-rewards/benefits/general-and-entity-benefits/singapore-pte-ltd | How long is parental leave for GitLab team members in the US? |
| ov-32 | outdated_version | 11 | syn:referral-process-2022 | How long does GitLab's recruiting team take to review a referral submission? |
| ov-33 | outdated_version | not found | hb:legal/record-retention-policy | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab keep risk treatment plans? |
| ov-38 | outdated_version | 8 | hb:legal/anti-corruption-policy | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/legacy/legacy-subscription-agreement-v7 | What discount on legal fees does GitLab's US legal services benefit provide? |
| lk-30 | lookup | 21 | hb:legal/privacy/transparency-reports | My request for an exception to a GitLab security policy was turned down. Where do I send an appeal? |
| lk-32 | lookup | not found | hb:legal/privacy/law-enforcement-guidelines | What happens when an emergency ticket comes in to GitLab Support? |
| lk-33 | lookup | 18 | hb:support/support-engineer-responsibilities | I've been on an emergency customer ticket for over an hour and two colleagues have joined in. What should I set up? |
| lk-41 | lookup | 6 | hb:total-rewards/incentives | How often is the bonus paid for GitLab directors and above? |
| pp-24 | paraphrase | not found | hb:total-rewards/incentives | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 9 | hb:legal/readmes/emilyplotkin | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-27 | paraphrase | not found | hb:support/support-time-off | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | 12 | hb:people-policies | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:legal/privacy/employee-privacy-policy | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-32 | paraphrase | 9 | hb:legal/esg/esg-training | Does GitLab give staff in Belgium anything each year towards environmentally friendly purchases? |
| pp-33 | paraphrase | not found | hb:security/security-assurance/security-risk/third-party-risk-management | Where must the sign-off for a GitLab security policy exception be recorded? |
| pp-34 | paraphrase | 16 | hb:finance/procurement/vendor-guidelines/vendor-agreement | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |
| md-21 | compound | 11 | pdf:salford-whistleblowing | How long does the University of Roehampton aim to take over an external whistleblowing investigation, and within what time must pay-discrimination complaints be filed under GitLab Inc's US notices? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 2 | 3 | 0.000 |  |
| ov-07 | 2 | 3 | 0.000 | 1.000 |
| ov-08 | 14 | 10 | 1.000 | 1.000 |
| ov-11 | 22 | 23 | 0.000 |  |
| ov-12 | 3 | 4 | 0.000 | 0.000 |
| ov-13 | 2 | 1 | 1.000 | 1.000 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 3 | 4 | 0.000 | 0.000 |
| ov-17 | 2 | 1 | 1.000 | 1.000 |
| ov-21 | 1 | 2 | 0.000 | 0.000 |
| ov-22 | 2 | 1 | 1.000 | 1.000 |
| ov-25 | 1 | 2 | 0.000 | 0.000 |
| ov-26 | 1 | 2 | 0.000 | 0.000 |
| ov-27 | 2 | 1 | 1.000 | 1.000 |
| ov-28 | 2 | 1 | 1.000 | 1.000 |
| ov-29 | 3 | 4 | 0.000 | 0.000 |
| ov-30 | 3 | 2 | 1.000 | 0.000 |
| ov-31 | 2 | 3 | 0.000 | 0.000 |
| ov-32 | 11 | 12 | 0.000 | 0.000 |
| ov-33 | - | - |  |  |
| ov-34 | - | - |  |  |
| ov-36 | 2 | 1 | 1.000 | 1.000 |
| ov-38 | 8 | 9 | 0.000 |  |
| ov-40 | 3 | 2 | 1.000 | 1.000 |
| ov-44 | - | - |  |  |
