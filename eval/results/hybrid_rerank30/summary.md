# Run: hybrid_rerank30

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=hybrid top_k=30 version_filter=none date_aware=False reranker=True
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:33

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.619 | 0.437 | 0.901 | 0.944 | 0.710 [0.62, 0.79] | 0.600 [0.51, 0.68] | 0.857 [0.78, 0.92] | 0.652 [0.48, 0.83] | 0.920 [0.80, 1.00] | 0.542 [0.36, 0.72] |
| non_outdated | 101 | 0.673 | 0.485 | 0.896 | 0.931 | 0.718 [0.63, 0.79] | 0.634 [0.54, 0.72] | 0.842 [0.76, 0.91] |  |  |  |
| lookup | 42 | 0.786 | 0.619 | 0.976 | 0.976 | 0.929 [0.85, 1.00] | 0.713 [0.60, 0.82] | 0.952 [0.88, 1.00] |  |  |  |
| paraphrase | 30 | 0.667 | 0.400 | 0.733 | 0.800 | 0.467 [0.28, 0.66] | 0.434 [0.27, 0.61] | 0.733 [0.55, 0.90] |  |  |  |
| exact_term | 7 | 0.714 | 0.571 | 1.000 | 1.000 | 0.714 [0.43, 1.00] | 0.680 [0.39, 0.93] | 0.714 [0.43, 1.00] |  |  |  |
| multi_doc | 15 | 0.467 | 0.367 | 1.000 | 1.000 | 0.767 [0.64, 0.88] | 0.821 [0.64, 0.95] | 0.900 [0.75, 0.98] |  |  |  |
| compound | 7 | 0.429 | 0.214 | 0.786 | 1.000 | 0.429 [0.20, 0.64] | 0.564 [0.21, 0.89] | 0.643 [0.50, 0.72] |  |  |  |
| outdated_version | 25 | 0.400 | 0.240 | 0.920 | 1.000 | 0.680 [0.48, 0.85] | 0.463 [0.33, 0.60] | 0.920 [0.80, 1.00] | 0.652 [0.48, 0.83] | 0.920 [0.80, 1.00] | 0.542 [0.36, 0.72] |
| real_pair | 1 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.100 [0.10, 0.10] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 0.000 [0.00, 0.00] |
| history | 10 | 0.400 | 0.300 | 1.000 | 1.000 | 0.700 [0.40, 1.00] | 0.451 [0.23, 0.69] | 0.900 [0.70, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.619 | 0.841 | 0.857 | 0.795 | 0.437 | 0.611 | 0.710 | 0.600 | 0.542 | 0.565 | 0.652 | 0.632 | 0.920 |  |  |  |  |  |  | 0.901 | 0.944 |
| non_outdated | 101.000 | 61.000 | 0.673 | 0.822 | 0.842 | 0.829 | 0.485 | 0.614 | 0.718 | 0.634 |  |  |  |  |  |  |  |  |  |  |  | 0.896 | 0.931 |
| lookup | 42.000 | 34.000 | 0.786 | 0.952 | 0.952 | 0.861 | 0.619 | 0.786 | 0.929 | 0.713 |  |  |  |  |  |  |  |  |  |  |  | 0.976 | 0.976 |
| paraphrase | 30.000 | 28.000 | 0.667 | 0.733 | 0.733 | 0.710 | 0.400 | 0.400 | 0.467 | 0.434 |  |  |  |  |  |  |  |  |  |  |  | 0.733 | 0.800 |
| exact_term | 7.000 | 7.000 | 0.714 | 0.714 | 0.714 | 0.751 | 0.571 | 0.714 | 0.714 | 0.680 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.467 | 0.767 | 0.900 | 0.967 | 0.367 | 0.633 | 0.767 | 0.821 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |
| compound | 7.000 | 5.000 | 0.429 | 0.643 | 0.643 | 0.929 | 0.214 | 0.357 | 0.429 | 0.564 |  |  |  |  |  |  |  |  |  |  |  | 0.786 | 1.000 |
| outdated_version | 25.000 | 22.000 | 0.400 | 0.920 | 0.920 | 0.658 | 0.240 | 0.600 | 0.680 | 0.463 | 0.542 | 0.565 | 0.652 | 0.632 | 0.920 |  |  |  |  |  |  | 0.920 | 1.000 |
| real_pair | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.100 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |  |  |  |  |  |  | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.400 | 0.800 | 0.900 | 0.632 | 0.300 | 0.500 | 0.700 | 0.451 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/legacy/privacy-statement-v2 | How long does GitLab retain security incident communications sent to customers? |
| pp-03 | paraphrase | 6 | hb:support/on-call | As a GitLab Support engineer, when should I rethink the dates I want to take off? |
| pp-05 | paraphrase | 7 | hb:security/security-assurance/governance/sec-awareness-training | Do people joining GitLab have to complete a security course when they start? |
| ex-08 | exact_term | 11 | hb:legal/ethics-compliance-program | What is LevelUp at GitLab? |
| ex-09 | exact_term | 6 | hb:security/security-assurance/governance/security-training | Which organisation's guidelines does GitLab's Secure Coding Training use? |
| ov-11 | outdated_version | 9 | hb:total-rewards/benefits/general-and-entity-benefits/singapore-pte-ltd | How long is parental leave for GitLab team members in the US? |
| ov-34 | outdated_version | not found | syn:stock-options-2021 | How long does GitLab keep risk treatment plans? |
| lk-45 | lookup | 6 | hb:finance/accounting/finance-ops/billing-ops | Our supplier only accepts paper cheques. Can GitLab Accounts Payable send one? |
| pp-21 | paraphrase | 13 | hb:total-rewards/benefits/general-and-entity-benefits/gitlab-ireland-ltd | I'm joining GitLab in Canada. Will I pay anything for my health insurance? |
| pp-24 | paraphrase | 25 | hb:hiring/candidate-faq | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-25 | paraphrase | 28 | hb:hiring/candidate-faq | Before putting in for a role on another team at GitLab, who should I talk to first? |
| pp-27 | paraphrase | not found | hb:total-rewards/benefits/parental-leave-toolkit | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:people-policies | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:legal/legacy/privacy-statement-v2 | Do I need a PIN on my own phone if I use it for GitLab work? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 1 | 2 | 0.000 | 0.000 |
| ov-07 | 2 | 1 | 1.000 | 0.000 |
| ov-08 | 1 | 2 | 0.000 | 1.000 |
| ov-11 | 9 | 10 | 0.000 |  |
| ov-12 | 2 | 1 | 1.000 | 1.000 |
| ov-13 | 2 | 1 | 1.000 | 1.000 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 2 | 1 | 1.000 | 1.000 |
| ov-17 | 2 | 1 | 1.000 | 1.000 |
| ov-21 | 1 | 2 | 0.000 | 0.000 |
| ov-22 | 2 | 1 | 1.000 | 1.000 |
| ov-25 | 1 | 2 | 0.000 | 1.000 |
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
| ov-38 | 1 | 2 | 0.000 | 0.000 |
| ov-40 | 1 | 2 | 0.000 | 1.000 |
| ov-44 | 2 | 1 | 1.000 | 1.000 |
