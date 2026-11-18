# Run: twostage

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:17

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.563 | 0.397 | 0.750 | 0.758 | 0.615 [0.53, 0.70] | 0.538 [0.45, 0.62] | 0.746 [0.66, 0.83] | 0.611 [0.39, 0.82] | 0.720 [0.54, 0.91] | 0.500 [0.28, 0.71] |
| non_outdated | 101 | 0.614 | 0.436 | 0.777 | 0.787 | 0.668 [0.57, 0.76] | 0.584 [0.49, 0.67] | 0.772 [0.67, 0.86] |  |  |  |
| lookup | 42 | 0.714 | 0.548 | 0.905 | 0.905 | 0.881 [0.76, 0.98] | 0.658 [0.53, 0.78] | 0.905 [0.78, 1.00] |  |  |  |
| paraphrase | 30 | 0.567 | 0.333 | 0.600 | 0.633 | 0.400 [0.22, 0.59] | 0.369 [0.21, 0.53] | 0.600 [0.41, 0.79] |  |  |  |
| exact_term | 7 | 0.714 | 0.571 | 0.857 | 0.857 | 0.857 [0.57, 1.00] | 0.679 [0.39, 0.93] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.467 | 0.367 | 0.800 | 0.800 | 0.633 [0.44, 0.75] | 0.787 [0.61, 0.93] | 0.767 [0.54, 0.92] |  |  |  |
| compound | 7 | 0.429 | 0.214 | 0.643 | 0.643 | 0.429 [0.10, 0.62] | 0.533 [0.13, 0.86] | 0.643 [0.30, 0.88] |  |  |  |
| outdated_version | 25 | 0.360 | 0.240 | 0.640 | 0.640 | 0.400 [0.21, 0.60] | 0.352 [0.21, 0.51] | 0.640 [0.46, 0.83] | 0.611 [0.39, 0.82] | 0.720 [0.54, 0.91] | 0.500 [0.28, 0.71] |
| real_pair | 1 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.100 [0.10, 0.10] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 0.000 [0.00, 0.00] |
| history | 10 | 0.300 | 0.200 | 0.800 | 0.800 | 0.700 [0.40, 0.90] | 0.382 [0.17, 0.61] | 0.800 [0.50, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.563 | 0.734 | 0.746 | 0.707 | 0.397 | 0.532 | 0.615 | 0.538 | 0.500 | 0.500 | 0.611 | 0.571 | 0.720 |  |  |  |  |  |  | 0.750 | 0.758 |
| non_outdated | 101.000 | 61.000 | 0.614 | 0.757 | 0.772 | 0.758 | 0.436 | 0.564 | 0.668 | 0.584 |  |  |  |  |  |  |  |  |  |  |  | 0.777 | 0.787 |
| lookup | 42.000 | 34.000 | 0.714 | 0.905 | 0.905 | 0.802 | 0.548 | 0.738 | 0.881 | 0.658 |  |  |  |  |  |  |  |  |  |  |  | 0.905 | 0.905 |
| paraphrase | 30.000 | 28.000 | 0.567 | 0.600 | 0.600 | 0.589 | 0.333 | 0.333 | 0.400 | 0.369 |  |  |  |  |  |  |  |  |  |  |  | 0.600 | 0.633 |
| exact_term | 7.000 | 7.000 | 0.714 | 0.714 | 0.857 | 0.750 | 0.571 | 0.714 | 0.857 | 0.679 |  |  |  |  |  |  |  |  |  |  |  | 0.857 | 0.857 |
| multi_doc | 15.000 | 8.000 | 0.467 | 0.733 | 0.767 | 0.933 | 0.367 | 0.567 | 0.633 | 0.787 |  |  |  |  |  |  |  |  |  |  |  | 0.800 | 0.800 |
| compound | 7.000 | 5.000 | 0.429 | 0.643 | 0.643 | 0.857 | 0.214 | 0.357 | 0.429 | 0.533 |  |  |  |  |  |  |  |  |  |  |  | 0.643 | 0.643 |
| outdated_version | 25.000 | 22.000 | 0.360 | 0.640 | 0.640 | 0.500 | 0.240 | 0.400 | 0.400 | 0.352 | 0.500 | 0.500 | 0.611 | 0.571 | 0.720 |  |  |  |  |  |  | 0.640 | 0.640 |
| real_pair | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.100 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |  |  |  |  |  |  | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.300 | 0.800 | 0.800 | 0.550 | 0.200 | 0.500 | 0.700 | 0.382 |  |  |  |  |  |  |  |  |  |  |  | 0.800 | 0.800 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:finance/procurement/vendor-guidelines/vendor-security-addendum | How long does GitLab retain security incident communications sent to customers? |
| pp-04 | paraphrase | not found | hb:legal/legacy/legacy-subscription-agreement-v6 | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| pp-05 | paraphrase | 6 | hb:security/security-assurance/governance/sec-awareness-training | Do people joining GitLab have to complete a security course when they start? |
| pp-14 | paraphrase | not found | hb:finance/procurement/tips-for-submitting-a-zip-request | Can I buy second-hand work equipment from an individual and claim it back from GitLab? |
| ex-08 | exact_term | not found | hb:legal/privacy/customer-product-usage-information | What is LevelUp at GitLab? |
| md-06 | multi_doc | not found | syn:token-management-standard-2023 | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-11 | outdated_version | not found | hb:total-rewards/benefits/general-and-entity-benefits/singapore-pte-ltd | How long is parental leave for GitLab team members in the US? |
| ov-26 | outdated_version | not found | hb:total-rewards/benefits/general-and-entity-benefits | How long can a business trip last and still be covered by GitLab's travel insurance? |
| ov-27 | outdated_version | not found | hb:legal/legacy/legacy-psa-v2 | What is the maximum baggage protection under GitLab's business travel insurance? |
| ov-29 | outdated_version | not found | hb:total-rewards/benefits/general-and-entity-benefits | Up to what age are team members' children eligible for Modern Health? |
| ov-32 | outdated_version | not found | syn:referral-operations-2023 | How long does GitLab's recruiting team take to review a referral submission? |
| ov-33 | outdated_version | not found | syn:records-retention-2023 | How long does GitLab retain production backup test records? |
| ov-34 | outdated_version | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab keep risk treatment plans? |
| ov-38 | outdated_version | not found | hb:legal/subscription-agreement/index | Whose approval is needed if a GitLab team member books more than 5 co-working days in a month? |
| ov-44 | outdated_version | not found | hb:legal/legacy/legacy-subscription-agreement-v5 | What discount on legal fees does GitLab's US legal services benefit provide? |
| lk-26 | lookup | not found | hb:support/license-and-renewals/workflows/self-managed/troubleshoot_cloud_licensing | Which TLS version must be enabled and preferred in new GitLab deployments? |
| lk-32 | lookup | not found | hb:legal/subscription-agreement/index | What happens when an emergency ticket comes in to GitLab Support? |
| lk-33 | lookup | not found | hb:support/support-engineer-responsibilities | I've been on an emergency customer ticket for over an hour and two colleagues have joined in. What should I set up? |
| pp-19 | paraphrase | not found | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-22 | paraphrase | not found | syn:ltd-benefits-uk-2023 | Will GitLab top up my retirement savings in Singapore beyond the government scheme? |
| pp-24 | paraphrase | not found | hb:hiring/candidate-faq | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | not found | hb:hiring/candidate-faq | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-27 | paraphrase | not found | hb:support/support-time-off | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:people-policies | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:legal/legacy/privacy-statement-v2 | Do I need a PIN on my own phone if I use it for GitLab work? |
| pp-32 | paraphrase | not found | hb:legal/esg | Does GitLab give staff in Belgium anything each year towards environmentally friendly purchases? |
| pp-34 | paraphrase | not found | hb:finance/procurement/vendor-guidelines/vendor-agreement | A supplier is chasing an overdue invoice and I flagged it as urgent. When will GitLab actually pay it? |
| md-21 | compound | not found | hb:legal/ethics-compliance-program | How long does the University of Roehampton aim to take over an external whistleblowing investigation, and within what time must pay-discrimination complaints be filed under GitLab Inc's US notices? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 1 | 2 | 0.000 | 0.000 |
| ov-07 | 2 | 1 | 1.000 | 0.000 |
| ov-08 | 1 | 2 | 0.000 | 1.000 |
| ov-11 | - | - |  |  |
| ov-12 | 2 | 1 | 1.000 | 1.000 |
| ov-13 | 2 | 1 | 1.000 | 1.000 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 2 | 1 | 1.000 | 1.000 |
| ov-17 | 2 | 1 | 1.000 | 1.000 |
| ov-21 | 1 | 2 | 0.000 | 0.000 |
| ov-22 | 2 | 1 | 1.000 | 1.000 |
| ov-25 | 1 | 2 | 0.000 | 1.000 |
| ov-26 | - | - |  |  |
| ov-27 | - | - |  |  |
| ov-28 | 1 | 2 | 0.000 | 0.000 |
| ov-29 | - | - |  |  |
| ov-30 | 1 | 2 | 0.000 | 0.000 |
| ov-31 | 1 | 2 | 0.000 | 0.000 |
| ov-32 | - | 1 | 1.000 | 1.000 |
| ov-33 | - | 1 | 1.000 | 1.000 |
| ov-34 | - | - |  |  |
| ov-36 | 1 | 2 | 0.000 | 0.000 |
| ov-38 | - | - |  |  |
| ov-40 | 1 | 2 | 0.000 | 1.000 |
| ov-44 | - | - |  |  |
