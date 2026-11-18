# Run: hybrid_v8

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=hybrid top_k=30 version_filter=exclude_superseded date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:37

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.659 | 0.397 | 0.913 | 0.968 | 0.690 [0.60, 0.77] | 0.578 [0.50, 0.65] | 0.897 [0.83, 0.95] | 0.000 [0.00, 0.00] | 0.920 [0.80, 1.00] | 0.000 [0.00, 0.00] |
| non_outdated | 101 | 0.644 | 0.396 | 0.901 | 0.960 | 0.683 [0.59, 0.77] | 0.584 [0.49, 0.66] | 0.901 [0.83, 0.95] |  |  |  |
| lookup | 42 | 0.857 | 0.595 | 0.976 | 0.976 | 0.881 [0.77, 0.98] | 0.717 [0.61, 0.81] | 0.976 [0.92, 1.00] |  |  |  |
| paraphrase | 30 | 0.467 | 0.167 | 0.733 | 0.900 | 0.433 [0.26, 0.61] | 0.302 [0.18, 0.43] | 0.800 [0.62, 0.96] |  |  |  |
| exact_term | 7 | 0.714 | 0.571 | 1.000 | 1.000 | 0.857 [0.57, 1.00] | 0.721 [0.45, 0.93] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.467 | 0.300 | 1.000 | 1.000 | 0.667 [0.46, 0.82] | 0.743 [0.55, 0.92] | 0.933 [0.82, 1.00] |  |  |  |
| compound | 7 | 0.429 | 0.214 | 0.857 | 1.000 | 0.429 [0.00, 0.86] | 0.507 [0.13, 0.88] | 0.857 [0.69, 1.00] |  |  |  |
| outdated_version | 25 | 0.720 | 0.400 | 0.960 | 1.000 | 0.720 [0.52, 0.89] | 0.556 [0.41, 0.71] | 0.880 [0.74, 1.00] | 0.000 [0.00, 0.00] | 0.920 [0.80, 1.00] | 0.000 [0.00, 0.00] |
| real_pair | 1 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.250 [0.25, 0.25] | 1.000 [1.00, 1.00] | 0.000 [0.00, 0.00] | 1.000 [1.00, 1.00] | 0.000 [0.00, 0.00] |
| history | 10 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 [0.00, 0.00] | 0.000 [0.00, 0.00] | 0.000 [0.00, 0.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.659 | 0.877 | 0.897 | 0.824 | 0.397 | 0.639 | 0.690 | 0.578 | 0.000 | 0.000 | 0.000 | 0.000 | 0.920 |  |  |  |  |  |  | 0.913 | 0.968 |
| non_outdated | 101.000 | 61.000 | 0.644 | 0.876 | 0.901 | 0.827 | 0.396 | 0.629 | 0.683 | 0.584 |  |  |  |  |  |  |  |  |  |  |  | 0.901 | 0.960 |
| lookup | 42.000 | 34.000 | 0.857 | 0.976 | 0.976 | 0.913 | 0.595 | 0.810 | 0.881 | 0.717 |  |  |  |  |  |  |  |  |  |  |  | 0.976 | 0.976 |
| paraphrase | 30.000 | 28.000 | 0.467 | 0.767 | 0.800 | 0.634 | 0.167 | 0.367 | 0.433 | 0.302 |  |  |  |  |  |  |  |  |  |  |  | 0.733 | 0.900 |
| exact_term | 7.000 | 7.000 | 0.714 | 0.857 | 0.857 | 0.792 | 0.571 | 0.857 | 0.857 | 0.721 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.467 | 0.900 | 0.933 | 0.956 | 0.300 | 0.667 | 0.667 | 0.743 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |
| compound | 7.000 | 5.000 | 0.429 | 0.714 | 0.857 | 0.905 | 0.214 | 0.357 | 0.429 | 0.507 |  |  |  |  |  |  |  |  |  |  |  | 0.857 | 1.000 |
| outdated_version | 25.000 | 22.000 | 0.720 | 0.880 | 0.880 | 0.810 | 0.400 | 0.680 | 0.720 | 0.556 | 0.000 | 0.000 | 0.000 | 0.000 | 0.920 |  |  |  |  |  |  | 0.960 | 1.000 |
| real_pair | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.250 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |  |  |  |  |  |  | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |  |  |  |  |  |  |  |  |  |  |  | 0.000 | 0.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/subscription-agreement/index | How long does GitLab retain security incident communications sent to customers? |
| pp-05 | paraphrase | 10 | hb:security/security-assurance/governance/security-training | Do people joining GitLab have to complete a security course when they start? |
| ex-08 | exact_term | 22 | hb:hiring/conducting-a-gitlab-interview | What is LevelUp at GitLab? |
| ov-11 | outdated_version | 8 | hb:total-rewards/benefits/general-and-entity-benefits/remote-com | How long is parental leave for GitLab team members in the US? |
| ov-34 | outdated_version | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab keep risk treatment plans? |
| ov-44 | outdated_version | 8 | hb:legal/subscription-agreement/index | What discount on legal fees does GitLab's US legal services benefit provide? |
| pp-19 | paraphrase | 6 | hb:support/on-call | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-20 | paraphrase | 6 | hb:security/product-security/vulnerability-management/what-does-fixed-mean | Is it acceptable for a fresh GitLab deployment to support only the previous encryption-protocol version? |
| pp-27 | paraphrase | not found | hb:total-rewards/benefits/parental-leave-toolkit | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:finance/expenses | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:legal/legacy/privacy-statement-v2 | Do I need a PIN on my own phone if I use it for GitLab work? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 1 | - | 0.000 | 0.000 |
| ov-07 | 1 | - | 0.000 | 0.000 |
| ov-08 | 1 | - | 0.000 | 0.000 |
| ov-11 | 8 | - | 0.000 |  |
| ov-12 | 1 | - | 0.000 | 0.000 |
| ov-13 | 1 | - | 0.000 | 0.000 |
| ov-14 | 1 | - | 0.000 | 0.000 |
| ov-16 | 1 | - | 0.000 | 0.000 |
| ov-17 | 1 | - | 0.000 | 0.000 |
| ov-21 | 1 | - | 0.000 | 0.000 |
| ov-22 | 1 | - | 0.000 | 0.000 |
| ov-25 | 1 | - | 0.000 | 0.000 |
| ov-26 | 2 | - | 0.000 | 0.000 |
| ov-27 | 2 | - | 0.000 | 0.000 |
| ov-28 | 1 | - | 0.000 | 0.000 |
| ov-29 | 2 | - | 0.000 | 0.000 |
| ov-30 | 1 | - | 0.000 | 0.000 |
| ov-31 | 1 | - | 0.000 | 0.000 |
| ov-32 | 1 | - | 0.000 | 0.000 |
| ov-33 | 2 | - | 0.000 | 0.000 |
| ov-34 | - | - |  |  |
| ov-36 | 1 | - | 0.000 | 0.000 |
| ov-38 | 1 | - | 0.000 | 0.000 |
| ov-40 | 1 | - | 0.000 | 0.000 |
| ov-44 | 8 | - | 0.000 | 0.000 |
