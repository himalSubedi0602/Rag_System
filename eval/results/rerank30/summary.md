# Run: rerank30

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=True
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:12

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.599 | 0.433 | 0.786 | 0.873 | 0.671 [0.58, 0.76] | 0.580 [0.49, 0.67] | 0.841 [0.76, 0.91] | 0.647 [0.44, 0.87] | 0.680 [0.48, 0.85] | 0.522 [0.33, 0.71] |
| non_outdated | 101 | 0.649 | 0.480 | 0.812 | 0.881 | 0.688 [0.60, 0.77] | 0.618 [0.52, 0.71] | 0.832 [0.75, 0.90] |  |  |  |
| lookup | 42 | 0.786 | 0.595 | 0.905 | 0.952 | 0.881 [0.78, 0.97] | 0.690 [0.57, 0.80] | 0.952 [0.88, 1.00] |  |  |  |
| paraphrase | 30 | 0.567 | 0.400 | 0.667 | 0.767 | 0.467 [0.28, 0.66] | 0.429 [0.26, 0.61] | 0.700 [0.52, 0.89] |  |  |  |
| exact_term | 7 | 0.714 | 0.571 | 0.857 | 1.000 | 0.714 [0.43, 1.00] | 0.667 [0.38, 0.93] | 0.714 [0.43, 1.00] |  |  |  |
| multi_doc | 15 | 0.500 | 0.400 | 0.967 | 1.000 | 0.767 [0.64, 0.88] | 0.855 [0.69, 0.97] | 0.900 [0.75, 0.98] |  |  |  |
| compound | 7 | 0.429 | 0.214 | 0.500 | 0.571 | 0.286 [0.00, 0.57] | 0.439 [0.01, 0.86] | 0.643 [0.50, 0.72] |  |  |  |
| outdated_version | 25 | 0.400 | 0.240 | 0.680 | 0.840 | 0.600 [0.39, 0.80] | 0.424 [0.27, 0.57] | 0.880 [0.74, 1.00] | 0.647 [0.44, 0.87] | 0.680 [0.48, 0.85] | 0.522 [0.33, 0.71] |
| real_pair | 1 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.100 [0.10, 0.10] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 0.000 [0.00, 0.00] |
| history | 10 | 0.400 | 0.300 | 0.700 | 0.900 | 0.700 [0.40, 1.00] | 0.433 [0.20, 0.68] | 0.900 [0.70, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.599 | 0.829 | 0.841 | 0.775 | 0.433 | 0.611 | 0.671 | 0.580 | 0.522 | 0.545 | 0.647 | 0.625 | 0.680 |  |  |  |  |  |  | 0.786 | 0.873 |
| non_outdated | 101.000 | 61.000 | 0.649 | 0.817 | 0.832 | 0.810 | 0.480 | 0.614 | 0.688 | 0.618 |  |  |  |  |  |  |  |  |  |  |  | 0.812 | 0.881 |
| lookup | 42.000 | 34.000 | 0.786 | 0.952 | 0.952 | 0.865 | 0.595 | 0.786 | 0.881 | 0.690 |  |  |  |  |  |  |  |  |  |  |  | 0.905 | 0.952 |
| paraphrase | 30.000 | 28.000 | 0.567 | 0.700 | 0.700 | 0.628 | 0.400 | 0.400 | 0.467 | 0.429 |  |  |  |  |  |  |  |  |  |  |  | 0.667 | 0.767 |
| exact_term | 7.000 | 7.000 | 0.714 | 0.714 | 0.714 | 0.738 | 0.571 | 0.714 | 0.714 | 0.667 |  |  |  |  |  |  |  |  |  |  |  | 0.857 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.500 | 0.800 | 0.900 | 1.000 | 0.400 | 0.667 | 0.767 | 0.855 |  |  |  |  |  |  |  |  |  |  |  | 0.967 | 1.000 |
| compound | 7.000 | 5.000 | 0.429 | 0.643 | 0.643 | 0.929 | 0.214 | 0.286 | 0.286 | 0.439 |  |  |  |  |  |  |  |  |  |  |  | 0.500 | 0.571 |
| outdated_version | 25.000 | 22.000 | 0.400 | 0.880 | 0.880 | 0.632 | 0.240 | 0.600 | 0.600 | 0.424 | 0.522 | 0.545 | 0.647 | 0.625 | 0.680 |  |  |  |  |  |  | 0.680 | 0.840 |
| real_pair | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.100 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |  |  |  |  |  |  | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.400 | 0.800 | 0.900 | 0.633 | 0.300 | 0.500 | 0.700 | 0.433 |  |  |  |  |  |  |  |  |  |  |  | 0.700 | 0.900 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/legacy/privacy-statement-v2 | How long does GitLab retain security incident communications sent to customers? |
| pp-04 | paraphrase | not found | hb:legal/legacy/legacy-subscription-agreement-v3 | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| pp-05 | paraphrase | 7 | hb:security/security-assurance/governance/sec-awareness-training | Do people joining GitLab have to complete a security course when they start? |
| ex-08 | exact_term | not found | hb:legal/customer-negotiations | What is LevelUp at GitLab? |
| ex-09 | exact_term | 6 | hb:security/security-assurance/governance/security-training | Which organisation's guidelines does GitLab's Secure Coding Training use? |
| ov-11 | outdated_version | 7 | hb:total-rewards/benefits/general-and-entity-benefits/singapore-pte-ltd | How long is parental leave for GitLab team members in the US? |
| ov-34 | outdated_version | not found | syn:stock-options-2021 | How long does GitLab keep risk treatment plans? |
| ov-44 | outdated_version | not found | hb:legal/legacy/legacy-subscription-agreement-v3 | What discount on legal fees does GitLab's US legal services benefit provide? |
| lk-45 | lookup | 6 | hb:finance/accounting/finance-ops/billing-ops | Our supplier only accepts paper cheques. Can GitLab Accounts Payable send one? |
| pp-19 | paraphrase | not found | hb:total-rewards/benefits/general-and-entity-benefits/remote-com | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-21 | paraphrase | 12 | hb:total-rewards/benefits/general-and-entity-benefits/gitlab-ireland-ltd | I'm joining GitLab in Canada. Will I pay anything for my health insurance? |
| pp-24 | paraphrase | 30 | hb:hiring/candidate-faq | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 29 | hb:hiring/candidate-faq | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-27 | paraphrase | not found | hb:support/support-time-off | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:people-policies | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | 19 | hb:legal/legacy/privacy-statement-v2 | Do I need a PIN on my own phone if I use it for GitLab work? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 1 | 2 | 0.000 | 0.000 |
| ov-07 | 3 | 1 | 1.000 |  |
| ov-08 | 1 | 2 | 0.000 |  |
| ov-11 | 7 | 8 | 0.000 |  |
| ov-12 | 2 | 1 | 1.000 | 1.000 |
| ov-13 | 2 | 1 | 1.000 | 1.000 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 2 | 1 | 1.000 | 1.000 |
| ov-17 | 2 | 1 | 1.000 | 1.000 |
| ov-21 | 1 | 2 | 0.000 | 0.000 |
| ov-22 | 2 | 1 | 1.000 | 1.000 |
| ov-25 | 1 | 2 | 0.000 |  |
| ov-26 | 2 | 1 | 1.000 | 1.000 |
| ov-27 | 3 | 2 | 1.000 | 1.000 |
| ov-28 | 1 | 2 | 0.000 | 0.000 |
| ov-29 | 2 | 1 | 1.000 | 1.000 |
| ov-30 | 1 | 2 | 0.000 | 0.000 |
| ov-31 | 1 | 2 | 0.000 | 0.000 |
| ov-32 | 2 | 1 | 1.000 | 1.000 |
| ov-33 | 2 | 1 | 1.000 | 1.000 |
| ov-34 | - | - |  |  |
| ov-36 | 1 | 2 | 0.000 | 0.000 |
| ov-38 | 1 | 2 | 0.000 |  |
| ov-40 | 1 | 2 | 0.000 |  |
| ov-44 | - | - |  |  |
