# Run: s2b_bge

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 7189); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:09

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.444 | 0.226 | 0.750 | 0.869 | 0.528 [0.43, 0.62] | 0.391 [0.31, 0.47] | 0.754 [0.66, 0.84] | 0.733 [0.47, 1.00] | 0.600 [0.42, 0.78] | 0.652 [0.48, 0.83] |
| non_outdated | 101 | 0.525 | 0.272 | 0.787 | 0.876 | 0.579 [0.47, 0.68] | 0.446 [0.36, 0.53] | 0.792 [0.70, 0.87] |  |  |  |
| lookup | 42 | 0.690 | 0.357 | 0.881 | 0.929 | 0.714 [0.56, 0.86] | 0.501 [0.37, 0.64] | 0.881 [0.78, 0.97] |  |  |  |
| paraphrase | 30 | 0.400 | 0.167 | 0.633 | 0.767 | 0.367 [0.19, 0.55] | 0.280 [0.16, 0.42] | 0.633 [0.45, 0.80] |  |  |  |
| exact_term | 7 | 0.571 | 0.429 | 0.857 | 1.000 | 0.857 [0.57, 1.00] | 0.595 [0.31, 0.86] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.400 | 0.233 | 0.867 | 0.967 | 0.600 [0.36, 0.74] | 0.604 [0.42, 0.72] | 0.867 [0.65, 1.00] |  |  |  |
| compound | 7 | 0.286 | 0.143 | 0.643 | 0.714 | 0.357 [0.00, 0.75] | 0.341 [0.03, 0.75] | 0.714 [0.50, 0.89] |  |  |  |
| outdated_version | 25 | 0.120 | 0.040 | 0.600 | 0.840 | 0.320 [0.15, 0.52] | 0.168 [0.08, 0.28] | 0.600 [0.41, 0.82] | 0.733 [0.47, 1.00] | 0.600 [0.42, 0.78] | 0.652 [0.48, 0.83] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.167 [0.17, 0.17] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.300 | 0.200 | 0.600 | 0.900 | 0.500 [0.20, 0.80] | 0.289 [0.08, 0.53] | 0.700 [0.40, 0.90] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.444 | 0.702 | 0.754 | 0.638 | 0.226 | 0.429 | 0.528 | 0.391 | 0.652 | 0.750 | 0.733 | 0.900 | 0.600 | 0.674 | 0.667 | 0.587 | 0.600 | 0.587 | 0.600 | 0.750 | 0.869 |
| non_outdated | 101.000 | 61.000 | 0.525 | 0.738 | 0.792 | 0.704 | 0.272 | 0.485 | 0.579 | 0.446 |  |  |  |  |  |  |  |  |  |  |  | 0.787 | 0.876 |
| lookup | 42.000 | 34.000 | 0.690 | 0.833 | 0.881 | 0.769 | 0.357 | 0.571 | 0.714 | 0.501 |  |  |  |  |  |  |  |  |  |  |  | 0.881 | 0.929 |
| paraphrase | 30.000 | 28.000 | 0.400 | 0.633 | 0.633 | 0.532 | 0.167 | 0.333 | 0.367 | 0.280 |  |  |  |  |  |  |  |  |  |  |  | 0.633 | 0.767 |
| exact_term | 7.000 | 7.000 | 0.571 | 0.857 | 0.857 | 0.714 | 0.429 | 0.857 | 0.857 | 0.595 |  |  |  |  |  |  |  |  |  |  |  | 0.857 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.400 | 0.733 | 0.867 | 0.867 | 0.233 | 0.467 | 0.600 | 0.604 |  |  |  |  |  |  |  |  |  |  |  | 0.867 | 0.967 |
| compound | 7.000 | 5.000 | 0.286 | 0.500 | 0.714 | 0.690 | 0.143 | 0.286 | 0.357 | 0.341 |  |  |  |  |  |  |  |  |  |  |  | 0.643 | 0.714 |
| outdated_version | 25.000 | 22.000 | 0.120 | 0.560 | 0.600 | 0.372 | 0.040 | 0.200 | 0.320 | 0.168 | 0.652 | 0.750 | 0.733 | 0.900 | 0.600 | 0.674 | 0.667 | 0.587 | 0.600 | 0.587 | 0.600 | 0.600 | 0.840 |
| real_pair | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.200 | 0.000 | 0.000 | 0.000 | 0.167 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.300 | 0.600 | 0.700 | 0.477 | 0.200 | 0.300 | 0.500 | 0.289 |  |  |  |  |  |  |  |  |  |  |  | 0.600 | 0.900 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:finance/procurement/vendor-guidelines/vendor-security-addendum | How long does GitLab retain security incident communications sent to customers? |
| pp-03 | paraphrase | 6 | hb:legal/subscription-agreement/index | As a GitLab Support engineer, when should I rethink the dates I want to take off? |
| pp-04 | paraphrase | 6 | hb:legal/subscription-agreement/index | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| pp-08 | paraphrase | 6 | hb:total-rewards/incentives | Can I get a bonus for recommending a friend for an internship at GitLab? |
| ex-08 | exact_term | not found | hb:security/security-assurance/security-compliance/sec-controls | What is LevelUp at GitLab? |
| md-06 | multi_doc | not found | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| lk-22 | lookup | 8 | hb:legal/testing-agreement-v3 | How can either party terminate the GitLab Testing Agreement for convenience? |
| ov-11 | outdated_version | 16 | hb:total-rewards/benefits/general-and-entity-benefits/singapore-pte-ltd | How long is parental leave for GitLab team members in the US? |
| ov-12 | outdated_version | 14 | hb:legal/esg | For how long does someone I refer to GitLab count as my referral? |
| ov-26 | outdated_version | 30 | hb:finance/expenses | How long can a business trip last and still be covered by GitLab's travel insurance? |
| ov-27 | outdated_version | 7 | syn:expenses-2023 | What is the maximum baggage protection under GitLab's business travel insurance? |
| ov-29 | outdated_version | 6 | hb:people-policies/leave-of-absence/us | Up to what age are team members' children eligible for Modern Health? |
| ov-33 | outdated_version | 28 | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | hb:security/product-security/vulnerability-management/sla-exceptions | How long does GitLab keep risk treatment plans? |
| ov-36 | outdated_version | 13 | hb:hiring/candidate-faq | If someone I referred to GitLab reached team interviews but wasn't hired, how long should I wait before referring them again? |
| ov-38 | outdated_version | not found | hb:legal/subscription-agreement/index | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/legacy/legacy-psa-v1 | What discount on legal fees does GitLab's US legal services benefit provide? |
| lk-30 | lookup | 6 | hb:security/security-assurance/security-risk/third-party-risk-management | My request for an exception to a GitLab security policy was turned down. Where do I send an appeal? |
| lk-32 | lookup | 26 | hb:legal/subscription-agreement/index | What happens when an emergency ticket comes in to GitLab Support? |
| lk-34 | lookup | not found | hb:total-rewards/benefits/general-and-entity-benefits/ltd-benefits-uk | How much does GitLab match on the Group RRSP for team members in Canada? |
| pp-19 | paraphrase | not found | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-22 | paraphrase | 8 | hb:total-rewards/benefits/general-and-entity-benefits/pty-benefits-australia | Will GitLab top up my retirement savings in Singapore beyond the government scheme? |
| pp-24 | paraphrase | not found | hb:hiring/talent-acquisition-framework/coordinator | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-27 | paraphrase | not found | hb:support/gratis-support | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:people-policies | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | 23 | hb:security/security-assurance/field-security/trust_center_guide | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-33 | paraphrase | 15 | hb:legal/api-terms | Where must the sign-off for a GitLab security policy exception be recorded? |
| pp-34 | paraphrase | 18 | hb:finance/procurement/vendor-guidelines/vendor-agreement | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 2 | 1 | 1.000 | 1.000 |
| ov-07 | 2 | 1 | 1.000 |  |
| ov-08 | 2 | 1 | 1.000 |  |
| ov-11 | 16 | 17 | 0.000 |  |
| ov-12 | 14 | 15 | 0.000 | 0.000 |
| ov-13 | 2 | 1 | 1.000 | 1.000 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 2 | 1 | 1.000 |  |
| ov-17 | 2 | 1 | 1.000 | 1.000 |
| ov-21 | 1 | 2 | 0.000 | 0.000 |
| ov-22 | 1 | 2 | 0.000 |  |
| ov-25 | 2 | 3 | 0.000 |  |
| ov-26 | 30 | 29 | 1.000 | 1.000 |
| ov-27 | 7 | 8 | 0.000 |  |
| ov-28 | 2 | 1 | 1.000 | 1.000 |
| ov-29 | 6 | 5 | 1.000 | 1.000 |
| ov-30 | 2 | 1 | 1.000 | 1.000 |
| ov-31 | 2 | 1 | 1.000 | 1.000 |
| ov-32 | 5 | 4 | 1.000 | 1.000 |
| ov-33 | 28 | 29 | 0.000 | 0.000 |
| ov-34 | - | - |  |  |
| ov-36 | 13 | 12 | 1.000 | 0.000 |
| ov-38 | - | 29 | 1.000 |  |
| ov-40 | 1 | 2 | 0.000 | 1.000 |
| ov-44 | - | - |  |  |
