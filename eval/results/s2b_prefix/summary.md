# Run: s2b_prefix

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=True
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 7189); truncated by the embedding model: 58.0% of units, 3.6% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:10

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.512 | 0.313 | 0.782 | 0.845 | 0.587 [0.49, 0.68] | 0.482 [0.38, 0.57] | 0.770 [0.67, 0.86] | 0.562 [0.29, 0.85] | 0.640 [0.43, 0.81] | 0.591 [0.36, 0.84] |
| non_outdated | 101 | 0.609 | 0.371 | 0.817 | 0.866 | 0.624 [0.52, 0.72] | 0.542 [0.44, 0.64] | 0.792 [0.70, 0.88] |  |  |  |
| lookup | 42 | 0.738 | 0.452 | 0.881 | 0.929 | 0.643 [0.49, 0.79] | 0.546 [0.41, 0.68] | 0.905 [0.81, 0.98] |  |  |  |
| paraphrase | 30 | 0.533 | 0.333 | 0.667 | 0.767 | 0.567 [0.38, 0.76] | 0.437 [0.27, 0.61] | 0.667 [0.47, 0.86] |  |  |  |
| exact_term | 7 | 0.571 | 0.286 | 0.857 | 0.857 | 0.714 [0.43, 1.00] | 0.464 [0.21, 0.79] | 0.714 [0.43, 1.00] |  |  |  |
| multi_doc | 15 | 0.467 | 0.267 | 0.900 | 0.900 | 0.700 [0.45, 0.88] | 0.689 [0.50, 0.85] | 0.800 [0.55, 0.96] |  |  |  |
| compound | 7 | 0.500 | 0.357 | 0.857 | 0.857 | 0.500 [0.21, 0.79] | 0.734 [0.42, 1.00] | 0.714 [0.58, 0.83] |  |  |  |
| outdated_version | 25 | 0.120 | 0.080 | 0.640 | 0.760 | 0.440 [0.23, 0.65] | 0.241 [0.13, 0.35] | 0.680 [0.48, 0.88] | 0.562 [0.29, 0.85] | 0.640 [0.43, 0.81] | 0.591 [0.36, 0.84] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.250 [0.25, 0.25] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.300 | 0.300 | 0.900 | 1.000 | 0.500 [0.20, 0.80] | 0.440 [0.21, 0.69] | 0.700 [0.40, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.512 | 0.702 | 0.770 | 0.685 | 0.313 | 0.520 | 0.587 | 0.482 | 0.591 | 0.588 | 0.562 | 0.462 | 0.640 | 0.455 | 0.438 | 0.477 | 0.469 | 0.500 | 0.438 | 0.782 | 0.845 |
| non_outdated | 101.000 | 61.000 | 0.609 | 0.738 | 0.792 | 0.765 | 0.371 | 0.550 | 0.624 | 0.542 |  |  |  |  |  |  |  |  |  |  |  | 0.817 | 0.866 |
| lookup | 42.000 | 34.000 | 0.738 | 0.833 | 0.905 | 0.808 | 0.452 | 0.571 | 0.643 | 0.546 |  |  |  |  |  |  |  |  |  |  |  | 0.881 | 0.929 |
| paraphrase | 30.000 | 28.000 | 0.533 | 0.633 | 0.667 | 0.601 | 0.333 | 0.500 | 0.567 | 0.437 |  |  |  |  |  |  |  |  |  |  |  | 0.667 | 0.767 |
| exact_term | 7.000 | 7.000 | 0.571 | 0.571 | 0.714 | 0.613 | 0.286 | 0.571 | 0.714 | 0.464 |  |  |  |  |  |  |  |  |  |  |  | 0.857 | 0.857 |
| multi_doc | 15.000 | 8.000 | 0.467 | 0.767 | 0.800 | 0.933 | 0.267 | 0.600 | 0.700 | 0.689 |  |  |  |  |  |  |  |  |  |  |  | 0.900 | 0.900 |
| compound | 7.000 | 5.000 | 0.500 | 0.714 | 0.714 | 1.000 | 0.357 | 0.500 | 0.500 | 0.734 |  |  |  |  |  |  |  |  |  |  |  | 0.857 | 0.857 |
| outdated_version | 25.000 | 22.000 | 0.120 | 0.560 | 0.680 | 0.362 | 0.080 | 0.400 | 0.440 | 0.241 | 0.591 | 0.588 | 0.562 | 0.462 | 0.640 | 0.455 | 0.438 | 0.477 | 0.469 | 0.500 | 0.438 | 0.640 | 0.760 |
| real_pair | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.250 | 0.000 | 0.000 | 1.000 | 0.250 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.300 | 0.600 | 0.700 | 0.495 | 0.300 | 0.500 | 0.500 | 0.440 |  |  |  |  |  |  |  |  |  |  |  | 0.900 | 1.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/subscription-agreement/index | How long does GitLab retain security incident communications sent to customers? |
| pp-04 | paraphrase | not found | hb:legal/subscription-agreement/index | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| pp-08 | paraphrase | 8 | hb:total-rewards/incentives | Can I get a bonus for recommending a friend for an internship at GitLab? |
| pp-14 | paraphrase | not found | hb:legal/legacy/legacy-psa-v2 | Can I buy second-hand work equipment from an individual and claim it back from GitLab? |
| ex-07 | exact_term | not found | hb:legal/patent-program | What is Āku Mahi at the University of Waikato? |
| ex-08 | exact_term | 25 | hb:total-rewards/compensation | What is LevelUp at GitLab? |
| md-06 | multi_doc | not found | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-11 | outdated_version | 28 | hb:total-rewards/benefits/general-and-entity-benefits/ltd-benefits-uk | How long is parental leave for GitLab team members in the US? |
| ov-26 | outdated_version | 14 | hb:total-rewards/benefits/general-and-entity-benefits/inc-benefits-us | How long can a business trip last and still be covered by GitLab's travel insurance? |
| ov-27 | outdated_version | 22 | hb:legal/legacy/legacy-subscription-agreement-v6 | What is the maximum baggage protection under GitLab's business travel insurance? |
| ov-32 | outdated_version | 14 | hb:hiring/referral-process | How long does GitLab's recruiting team take to review a referral submission? |
| ov-33 | outdated_version | not found | hb:legal/record-retention-policy | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | syn:inc-benefits-us-2023 | How long does GitLab keep risk treatment plans? |
| ov-38 | outdated_version | not found | hb:people-policies/france-sas/remote-work-charter | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | 6 | hb:legal/subscription-agreement/index | What discount on legal fees does GitLab's US legal services benefit provide? |
| lk-30 | lookup | 18 | hb:legal/ethics-compliance-program | My request for an exception to a GitLab security policy was turned down. Where do I send an appeal? |
| lk-33 | lookup | 6 | hb:support/providing_excellent_customer_service | I've been on an emergency customer ticket for over an hour and two colleagues have joined in. What should I set up? |
| lk-41 | lookup | 6 | hb:total-rewards/incentives | How often is the bonus paid for GitLab directors and above? |
| pp-24 | paraphrase | not found | hb:hiring/conducting-a-gitlab-interview | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 23 | hb:hiring/conducting-a-gitlab-interview | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-27 | paraphrase | 9 | hb:total-rewards/benefits/general-and-entity-benefits/canada-corp-benefits | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:finance/expenses | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:finance/travel | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-33 | paraphrase | not found | hb:security/security-assurance/field-security/customer-security-assessment-process | Where must the sign-off for a GitLab security policy exception be recorded? |
| pp-34 | paraphrase | 19 | hb:legal/reseller-agreement | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 4 | 3 | 1.000 |  |
| ov-07 | 2 | 1 | 1.000 |  |
| ov-08 | 5 | 6 | 0.000 |  |
| ov-11 | 28 | 29 | 0.000 |  |
| ov-12 | 2 | 3 | 0.000 | 0.000 |
| ov-13 | 2 | 1 | 1.000 | 1.000 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 3 | 2 | 1.000 |  |
| ov-17 | 1 | 2 | 0.000 | 0.000 |
| ov-21 | 2 | 1 | 1.000 | 1.000 |
| ov-22 | 2 | 1 | 1.000 | 1.000 |
| ov-25 | 2 | 1 | 1.000 | 1.000 |
| ov-26 | 14 | 13 | 1.000 | 1.000 |
| ov-27 | 22 | 21 | 1.000 | 1.000 |
| ov-28 | 1 | 2 | 0.000 | 0.000 |
| ov-29 | 5 | 6 | 0.000 | 0.000 |
| ov-30 | 2 | 1 | 1.000 | 0.000 |
| ov-31 | 3 | 2 | 1.000 | 1.000 |
| ov-32 | 14 | 13 | 1.000 | 1.000 |
| ov-33 | - | - |  |  |
| ov-34 | - | - |  |  |
| ov-36 | 3 | 4 | 0.000 | 0.000 |
| ov-38 | - | - |  |  |
| ov-40 | 1 | 2 | 0.000 | 0.000 |
| ov-44 | 6 | 7 | 0.000 |  |
