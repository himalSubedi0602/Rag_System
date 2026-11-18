# Run: chunk1000

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=1000 overlap=100 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 1330 (embedded units: 1330); truncated by the embedding model: 93.5% of units, 70.8% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 14:53

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.444 | 0.262 | 0.758 | 0.853 | 0.563 [0.46, 0.66] | 0.433 [0.33, 0.52] | 0.702 [0.60, 0.79] | 0.536 [0.43, 0.65] | 0.560 [0.36, 0.76] | 0.525 [0.45, 0.61] |
| non_outdated | 101 | 0.515 | 0.307 | 0.817 | 0.856 | 0.624 [0.52, 0.72] | 0.491 [0.38, 0.58] | 0.757 [0.66, 0.84] |  |  |  |
| lookup | 42 | 0.643 | 0.381 | 0.881 | 0.881 | 0.738 [0.59, 0.86] | 0.519 [0.39, 0.65] | 0.857 [0.74, 0.95] |  |  |  |
| paraphrase | 30 | 0.433 | 0.233 | 0.800 | 0.833 | 0.467 [0.29, 0.66] | 0.355 [0.22, 0.51] | 0.633 [0.45, 0.82] |  |  |  |
| exact_term | 7 | 0.571 | 0.286 | 0.714 | 0.857 | 0.714 [0.29, 1.00] | 0.433 [0.15, 0.74] | 0.714 [0.29, 1.00] |  |  |  |
| multi_doc | 15 | 0.400 | 0.300 | 0.833 | 0.933 | 0.667 [0.31, 0.88] | 0.696 [0.37, 0.90] | 0.800 [0.50, 0.98] |  |  |  |
| compound | 7 | 0.286 | 0.214 | 0.571 | 0.643 | 0.429 [0.08, 0.78] | 0.514 [0.12, 0.87] | 0.643 [0.50, 0.88] |  |  |  |
| outdated_version | 25 | 0.160 | 0.080 | 0.520 | 0.840 | 0.320 [0.12, 0.54] | 0.199 [0.08, 0.34] | 0.480 [0.28, 0.68] | 0.536 [0.43, 0.65] | 0.560 [0.36, 0.76] | 0.525 [0.45, 0.61] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.067 [0.07, 0.07] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.100 | 0.000 | 0.400 | 0.600 | 0.200 [0.00, 0.50] | 0.117 [0.01, 0.26] | 0.600 [0.30, 0.90] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_exact | fact_stale_exact | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.444 | 0.655 | 0.702 | 0.610 | 0.262 | 0.480 | 0.563 | 0.433 | 0.525 | 0.571 | 0.536 | 0.500 | 0.560 | 0.550 | 0.536 | 0.758 | 0.853 |
| non_outdated | 101.000 | 61.000 | 0.515 | 0.698 | 0.757 | 0.675 | 0.307 | 0.530 | 0.624 | 0.491 |  |  |  |  |  |  |  | 0.817 | 0.856 |
| lookup | 42.000 | 34.000 | 0.643 | 0.786 | 0.857 | 0.730 | 0.381 | 0.571 | 0.738 | 0.519 |  |  |  |  |  |  |  | 0.881 | 0.881 |
| paraphrase | 30.000 | 28.000 | 0.433 | 0.600 | 0.633 | 0.531 | 0.233 | 0.467 | 0.467 | 0.355 |  |  |  |  |  |  |  | 0.800 | 0.833 |
| exact_term | 7.000 | 7.000 | 0.571 | 0.714 | 0.714 | 0.637 | 0.286 | 0.571 | 0.714 | 0.433 |  |  |  |  |  |  |  | 0.714 | 0.857 |
| multi_doc | 15.000 | 8.000 | 0.400 | 0.733 | 0.800 | 0.842 | 0.300 | 0.567 | 0.667 | 0.696 |  |  |  |  |  |  |  | 0.833 | 0.933 |
| compound | 7.000 | 5.000 | 0.286 | 0.500 | 0.643 | 0.636 | 0.214 | 0.429 | 0.429 | 0.514 |  |  |  |  |  |  |  | 0.571 | 0.643 |
| outdated_version | 25.000 | 22.000 | 0.160 | 0.480 | 0.480 | 0.350 | 0.080 | 0.280 | 0.320 | 0.199 | 0.525 | 0.571 | 0.536 | 0.500 | 0.560 | 0.550 | 0.536 | 0.520 | 0.840 |
| real_pair | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.250 | 0.000 | 0.000 | 0.000 | 0.067 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.100 | 0.500 | 0.600 | 0.333 | 0.000 | 0.200 | 0.200 | 0.117 |  |  |  |  |  |  |  | 0.400 | 0.600 |

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
| lk-30 | lookup | 11 | hb:legal/privacy/transparency-reports | My request for an exception to a GitLab security policy was turned down. Where do I send an appeal? |
| lk-32 | lookup | not found | hb:legal/legacy/legacy-subscription-agreement-v6 | What happens when an emergency ticket comes in to GitLab Support? |
| lk-37 | lookup | 6 | hb:total-rewards/benefits/general-and-entity-benefits/ltd-benefits-uk | What is the pension contribution rate for GitLab BV team members in the Netherlands? |
| lk-46 | lookup | not found | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | What monthly occupational allowance do GitLab France team members receive for remote work? |
| pp-19 | paraphrase | not found | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-24 | paraphrase | 15 | hb:total-rewards/compensation | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 24 | hb:hiring/interviewing/infrastructure-interview | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-30 | paraphrase | not found | hb:finance/expenses | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:legal/privacy/employee-privacy-policy | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-33 | paraphrase | 17 | hb:security/security-and-technology-policies/security-and-technology-policies-management | Where must the sign-off for a GitLab security policy exception be recorded? |
| pp-34 | paraphrase | 12 | hb:legal/legacy/legacy-psa-v2 | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |
| md-14 | compound | not found | hb:total-rewards/benefits/general-and-entity-benefits/bv-benefits-belgium | How much notice does GitLab Support aim to give for on-call shift changes, and how quickly should St Mary's University respond to an annual leave request? |

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
