# Run: chunk250

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=250 overlap=25 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 4774 (embedded units: 4774); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 14:53

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.496 | 0.206 | 0.675 | 0.786 | 0.444 [0.37, 0.53] | 0.344 [0.28, 0.42] | 0.798 [0.72, 0.87] | 0.538 [0.38, 0.71] | 0.520 [0.33, 0.72] | 0.455 [0.35, 0.57] |
| non_outdated | 101 | 0.550 | 0.238 | 0.723 | 0.812 | 0.495 [0.41, 0.60] | 0.389 [0.31, 0.48] | 0.817 [0.73, 0.89] |  |  |  |
| lookup | 42 | 0.643 | 0.310 | 0.786 | 0.881 | 0.548 [0.40, 0.72] | 0.416 [0.29, 0.57] | 0.905 [0.79, 1.00] |  |  |  |
| paraphrase | 30 | 0.533 | 0.167 | 0.633 | 0.700 | 0.400 [0.22, 0.59] | 0.265 [0.14, 0.41] | 0.767 [0.60, 0.93] |  |  |  |
| exact_term | 7 | 0.571 | 0.286 | 0.857 | 0.857 | 0.857 [0.57, 1.00] | 0.476 [0.23, 0.75] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.400 | 0.200 | 0.733 | 0.867 | 0.467 [0.27, 0.60] | 0.523 [0.37, 0.69] | 0.733 [0.50, 0.89] |  |  |  |
| compound | 7 | 0.357 | 0.143 | 0.571 | 0.714 | 0.286 [0.00, 0.57] | 0.386 [0.04, 0.72] | 0.643 [0.20, 0.94] |  |  |  |
| outdated_version | 25 | 0.280 | 0.080 | 0.480 | 0.680 | 0.240 [0.09, 0.40] | 0.158 [0.06, 0.27] | 0.720 [0.54, 0.88] | 0.538 [0.38, 0.71] | 0.520 [0.33, 0.72] | 0.455 [0.35, 0.57] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.200 [0.20, 0.20] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.100 | 0.000 | 0.600 | 0.800 | 0.200 [0.00, 0.50] | 0.120 [0.02, 0.26] | 0.900 [0.70, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.496 | 0.710 | 0.798 | 0.677 | 0.206 | 0.333 | 0.444 | 0.344 | 0.455 | 0.474 | 0.538 | 0.571 | 0.520 | 0.545 | 0.692 | 0.675 | 0.786 |
| non_outdated | 101.000 | 61.000 | 0.550 | 0.757 | 0.817 | 0.730 | 0.238 | 0.366 | 0.495 | 0.389 |  |  |  |  |  |  |  | 0.723 | 0.812 |
| lookup | 42.000 | 34.000 | 0.643 | 0.881 | 0.905 | 0.753 | 0.310 | 0.429 | 0.548 | 0.416 |  |  |  |  |  |  |  | 0.786 | 0.881 |
| paraphrase | 30.000 | 28.000 | 0.533 | 0.667 | 0.767 | 0.636 | 0.167 | 0.267 | 0.400 | 0.265 |  |  |  |  |  |  |  | 0.633 | 0.700 |
| exact_term | 7.000 | 7.000 | 0.571 | 0.857 | 0.857 | 0.714 | 0.286 | 0.571 | 0.857 | 0.476 |  |  |  |  |  |  |  | 0.857 | 0.857 |
| multi_doc | 15.000 | 8.000 | 0.400 | 0.633 | 0.733 | 0.856 | 0.200 | 0.333 | 0.467 | 0.523 |  |  |  |  |  |  |  | 0.733 | 0.867 |
| compound | 7.000 | 5.000 | 0.357 | 0.571 | 0.643 | 0.744 | 0.143 | 0.286 | 0.286 | 0.386 |  |  |  |  |  |  |  | 0.571 | 0.714 |
| outdated_version | 25.000 | 22.000 | 0.280 | 0.520 | 0.720 | 0.465 | 0.080 | 0.200 | 0.240 | 0.158 | 0.455 | 0.474 | 0.538 | 0.571 | 0.520 | 0.545 | 0.692 | 0.480 | 0.680 |
| real_pair | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.200 | 0.000 | 0.000 | 1.000 | 0.200 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.100 | 0.900 | 0.900 | 0.471 | 0.000 | 0.200 | 0.200 | 0.120 |  |  |  |  |  |  |  | 0.600 | 0.800 |

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
| lk-30 | lookup | 14 | hb:legal/employment-law | My request for an exception to a GitLab security policy was turned down. Where do I send an appeal? |
| lk-32 | lookup | not found | hb:legal/privacy/law-enforcement-guidelines | What happens when an emergency ticket comes in to GitLab Support? |
| lk-33 | lookup | 8 | hb:support/support-time-off-buddies | I've been on an emergency customer ticket for over an hour and two colleagues have joined in. What should I set up? |
| pp-24 | paraphrase | 12 | hb:total-rewards/compensation | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-27 | paraphrase | 7 | hb:total-rewards/benefits/general-and-entity-benefits | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | 23 | syn:expenses-2023 | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:finance/travel | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-33 | paraphrase | 27 | hb:security/security-assurance/security-risk/third-party-risk-management | Where must the sign-off for a GitLab security policy exception be recorded? |
| pp-34 | paraphrase | 17 | hb:legal/legacy/legacy-reseller-agreement-v1 | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |
| md-13 | compound | 8 | hb:support/support-engineer-responsibilities | How far ahead is GitLab Support's on-call schedule available, and when should an engineer hold a catch-up session with their time-off buddy after returning? |
| md-21 | compound | 12 | pdf:salford-whistleblowing | How long does the University of Roehampton aim to take over an external whistleblowing investigation, and within what time must pay-discrimination complaints be filed under GitLab Inc's US notices? |

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
