# Run: baseline

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 92.7% of units, 46.7% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 14:52

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.433 | 0.179 | 0.698 | 0.806 | 0.496 [0.40, 0.59] | 0.356 [0.28, 0.43] | 0.734 [0.65, 0.81] | 0.458 [0.33, 0.60] | 0.480 [0.27, 0.69] | 0.477 [0.38, 0.57] |
| non_outdated | 101 | 0.520 | 0.213 | 0.752 | 0.827 | 0.530 [0.43, 0.63] | 0.398 [0.32, 0.48] | 0.757 [0.67, 0.84] |  |  |  |
| lookup | 42 | 0.595 | 0.190 | 0.810 | 0.857 | 0.524 [0.37, 0.67] | 0.356 [0.24, 0.47] | 0.833 [0.71, 0.93] |  |  |  |
| paraphrase | 30 | 0.467 | 0.200 | 0.667 | 0.800 | 0.467 [0.28, 0.66] | 0.308 [0.17, 0.45] | 0.667 [0.47, 0.86] |  |  |  |
| exact_term | 7 | 0.714 | 0.429 | 0.857 | 0.857 | 0.857 [0.57, 1.00] | 0.619 [0.33, 0.86] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.400 | 0.200 | 0.800 | 0.867 | 0.567 [0.29, 0.79] | 0.558 [0.33, 0.73] | 0.767 [0.50, 0.93] |  |  |  |
| compound | 7 | 0.357 | 0.214 | 0.571 | 0.643 | 0.429 [0.08, 0.78] | 0.473 [0.06, 0.87] | 0.571 [0.10, 0.83] |  |  |  |
| outdated_version | 25 | 0.080 | 0.040 | 0.480 | 0.720 | 0.360 [0.14, 0.58] | 0.185 [0.08, 0.30] | 0.640 [0.43, 0.83] | 0.458 [0.33, 0.60] | 0.480 [0.27, 0.69] | 0.477 [0.38, 0.57] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.043 [0.04, 0.04] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.200 | 0.100 | 0.800 | 1.000 | 0.500 [0.20, 0.80] | 0.272 [0.12, 0.47] | 0.800 [0.50, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.433 | 0.683 | 0.734 | 0.626 | 0.179 | 0.429 | 0.496 | 0.356 | 0.477 | 0.438 | 0.458 | 0.333 | 0.480 | 0.545 | 0.500 | 0.698 | 0.806 |
| non_outdated | 101.000 | 61.000 | 0.520 | 0.713 | 0.757 | 0.695 | 0.213 | 0.455 | 0.530 | 0.398 |  |  |  |  |  |  |  | 0.752 | 0.827 |
| lookup | 42.000 | 34.000 | 0.595 | 0.833 | 0.833 | 0.716 | 0.190 | 0.452 | 0.524 | 0.356 |  |  |  |  |  |  |  | 0.810 | 0.857 |
| paraphrase | 30.000 | 28.000 | 0.467 | 0.600 | 0.667 | 0.559 | 0.200 | 0.400 | 0.467 | 0.308 |  |  |  |  |  |  |  | 0.667 | 0.800 |
| exact_term | 7.000 | 7.000 | 0.714 | 0.857 | 0.857 | 0.786 | 0.429 | 0.857 | 0.857 | 0.619 |  |  |  |  |  |  |  | 0.857 | 0.857 |
| multi_doc | 15.000 | 8.000 | 0.400 | 0.633 | 0.767 | 0.839 | 0.200 | 0.467 | 0.567 | 0.558 |  |  |  |  |  |  |  | 0.800 | 0.867 |
| compound | 7.000 | 5.000 | 0.357 | 0.500 | 0.571 | 0.752 | 0.214 | 0.286 | 0.429 | 0.473 |  |  |  |  |  |  |  | 0.571 | 0.643 |
| outdated_version | 25.000 | 22.000 | 0.080 | 0.560 | 0.640 | 0.349 | 0.040 | 0.320 | 0.360 | 0.185 | 0.477 | 0.438 | 0.458 | 0.333 | 0.480 | 0.545 | 0.500 | 0.480 | 0.720 |
| real_pair | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.500 | 0.000 | 0.000 | 0.000 | 0.043 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.200 | 0.800 | 0.800 | 0.503 | 0.100 | 0.300 | 0.500 | 0.272 |  |  |  |  |  |  |  | 0.800 | 1.000 |

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
| lk-30 | lookup | 16 | hb:legal/privacy/transparency-reports | My request for an exception to a GitLab security policy was turned down. Where do I send an appeal? |
| lk-32 | lookup | not found | hb:legal/privacy/law-enforcement-guidelines | What happens when an emergency ticket comes in to GitLab Support? |
| lk-34 | lookup | 6 | hb:total-rewards/compensation | How much does GitLab match on the Group RRSP for team members in Canada? |
| lk-37 | lookup | 6 | hb:total-rewards/benefits/general-and-entity-benefits/remote-com | What is the pension contribution rate for GitLab BV team members in the Netherlands? |
| lk-41 | lookup | 6 | hb:total-rewards/incentives | How often is the bonus paid for GitLab directors and above? |
| pp-24 | paraphrase | 18 | hb:total-rewards/compensation | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 8 | hb:hiring/candidate-faq | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-30 | paraphrase | not found | syn:expenses-2023 | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:legal/api-terms | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-32 | paraphrase | 9 | hb:legal/esg/fy23-esg-report | Does GitLab give staff in Belgium anything each year towards environmentally friendly purchases? |
| pp-33 | paraphrase | 19 | hb:security/security-assurance/security-risk/third-party-risk-management | Where must the sign-off for a GitLab security policy exception be recorded? |
| pp-34 | paraphrase | 21 | hb:legal/subscription-agreement/index | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |
| md-13 | compound | 10 | hb:support/support-engineer-responsibilities | How far ahead is GitLab Support's on-call schedule available, and when should an engineer hold a catch-up session with their time-off buddy after returning? |
| md-21 | compound | 6 | pdf:salford-whistleblowing | How long does the University of Roehampton aim to take over an external whistleblowing investigation, and within what time must pay-discrimination complaints be filed under GitLab Inc's US notices? |

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
