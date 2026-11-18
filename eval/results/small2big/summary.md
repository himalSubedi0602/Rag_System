# Run: small2big

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 7189); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 14:53

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.468 | 0.242 | 0.790 | 0.881 | 0.536 [0.45, 0.62] | 0.415 [0.34, 0.49] | 0.750 [0.66, 0.84] | 0.500 [0.37, 0.65] | 0.720 [0.52, 0.88] | 0.545 [0.44, 0.67] |
| non_outdated | 101 | 0.535 | 0.282 | 0.807 | 0.871 | 0.579 [0.48, 0.68] | 0.464 [0.38, 0.55] | 0.787 [0.69, 0.87] |  |  |  |
| lookup | 42 | 0.571 | 0.333 | 0.905 | 0.929 | 0.667 [0.51, 0.81] | 0.474 [0.35, 0.60] | 0.857 [0.73, 0.97] |  |  |  |
| paraphrase | 30 | 0.533 | 0.200 | 0.667 | 0.833 | 0.433 [0.25, 0.62] | 0.309 [0.18, 0.45] | 0.700 [0.52, 0.89] |  |  |  |
| exact_term | 7 | 0.714 | 0.286 | 0.857 | 0.857 | 0.857 [0.57, 1.00] | 0.529 [0.29, 0.79] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.433 | 0.333 | 0.833 | 0.867 | 0.567 [0.33, 0.76] | 0.718 [0.52, 0.88] | 0.800 [0.60, 0.95] |  |  |  |
| compound | 7 | 0.357 | 0.214 | 0.714 | 0.714 | 0.429 [0.00, 0.86] | 0.462 [0.05, 0.87] | 0.643 [0.20, 0.94] |  |  |  |
| outdated_version | 25 | 0.200 | 0.080 | 0.720 | 0.920 | 0.360 [0.20, 0.54] | 0.217 [0.12, 0.33] | 0.600 [0.44, 0.77] | 0.500 [0.37, 0.65] | 0.720 [0.52, 0.88] | 0.545 [0.44, 0.67] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.200 [0.20, 0.20] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.200 | 0.200 | 0.800 | 1.000 | 0.600 [0.30, 0.90] | 0.329 [0.14, 0.56] | 0.900 [0.70, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.468 | 0.698 | 0.750 | 0.651 | 0.242 | 0.425 | 0.536 | 0.415 | 0.545 | 0.618 | 0.500 | 0.545 | 0.720 | 0.591 | 0.583 | 0.790 | 0.881 |
| non_outdated | 101.000 | 61.000 | 0.535 | 0.733 | 0.787 | 0.711 | 0.282 | 0.470 | 0.579 | 0.464 |  |  |  |  |  |  |  | 0.807 | 0.871 |
| lookup | 42.000 | 34.000 | 0.571 | 0.833 | 0.857 | 0.704 | 0.333 | 0.571 | 0.667 | 0.474 |  |  |  |  |  |  |  | 0.905 | 0.929 |
| paraphrase | 30.000 | 28.000 | 0.533 | 0.667 | 0.700 | 0.619 | 0.200 | 0.300 | 0.433 | 0.309 |  |  |  |  |  |  |  | 0.667 | 0.833 |
| exact_term | 7.000 | 7.000 | 0.714 | 0.714 | 0.857 | 0.750 | 0.286 | 0.714 | 0.857 | 0.529 |  |  |  |  |  |  |  | 0.857 | 0.857 |
| multi_doc | 15.000 | 8.000 | 0.433 | 0.667 | 0.800 | 0.889 | 0.333 | 0.467 | 0.567 | 0.718 |  |  |  |  |  |  |  | 0.833 | 0.867 |
| compound | 7.000 | 5.000 | 0.357 | 0.571 | 0.643 | 0.737 | 0.214 | 0.357 | 0.429 | 0.462 |  |  |  |  |  |  |  | 0.714 | 0.714 |
| outdated_version | 25.000 | 22.000 | 0.200 | 0.560 | 0.600 | 0.406 | 0.080 | 0.240 | 0.360 | 0.217 | 0.545 | 0.618 | 0.500 | 0.545 | 0.720 | 0.591 | 0.583 | 0.720 | 0.920 |
| real_pair | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.200 | 0.000 | 0.000 | 1.000 | 0.200 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.200 | 0.800 | 0.900 | 0.496 | 0.200 | 0.300 | 0.600 | 0.329 |  |  |  |  |  |  |  | 0.800 | 1.000 |

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
| lk-30 | lookup | 18 | hb:legal/public-policy | My request for an exception to a GitLab security policy was turned down. Where do I send an appeal? |
| lk-32 | lookup | not found | hb:legal/subscription-agreement/index | What happens when an emergency ticket comes in to GitLab Support? |
| lk-33 | lookup | 8 | hb:support/support-time-off-buddies | I've been on an emergency customer ticket for over an hour and two colleagues have joined in. What should I set up? |
| lk-34 | lookup | 7 | hb:total-rewards/compensation | How much does GitLab match on the Group RRSP for team members in Canada? |
| pp-19 | paraphrase | 7 | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-24 | paraphrase | not found | hb:total-rewards/compensation | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 12 | hb:hiring/conducting-a-gitlab-interview | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-27 | paraphrase | 8 | hb:legal/product | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | 28 | hb:finance/expenses | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:finance/travel | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-33 | paraphrase | not found | hb:security/security-assurance/security-risk/third-party-risk-management | Where must the sign-off for a GitLab security policy exception be recorded? |
| pp-34 | paraphrase | 18 | hb:legal/legacy/legacy-reseller-agreement-v1 | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |
| md-13 | compound | 15 | hb:legal/subscription-agreement/index | How far ahead is GitLab Support's on-call schedule available, and when should an engineer hold a catch-up session with their time-off buddy after returning? |
| md-21 | compound | 11 | pdf:salford-whistleblowing | How long does the University of Roehampton aim to take over an external whistleblowing investigation, and within what time must pay-discrimination complaints be filed under GitLab Inc's US notices? |

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
