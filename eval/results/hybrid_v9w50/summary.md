# Run: hybrid_v9w50

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=hybrid top_k=30 version_filter=none date_aware=True reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:35

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.540 | 0.313 | 0.889 | 0.944 | 0.694 [0.62, 0.77] | 0.509 [0.43, 0.59] | 0.893 [0.83, 0.95] | 0.000 [0.00, 0.00] | 0.920 [0.80, 1.00] | 0.000 [0.00, 0.00] |
| non_outdated | 101 | 0.515 | 0.302 | 0.871 | 0.931 | 0.678 [0.59, 0.76] | 0.500 [0.41, 0.59] | 0.886 [0.82, 0.94] |  |  |  |
| lookup | 42 | 0.643 | 0.452 | 0.976 | 0.976 | 0.857 [0.74, 0.95] | 0.617 [0.51, 0.73] | 0.976 [0.92, 1.00] |  |  |  |
| paraphrase | 30 | 0.467 | 0.133 | 0.700 | 0.800 | 0.433 [0.24, 0.60] | 0.278 [0.17, 0.39] | 0.800 [0.62, 0.94] |  |  |  |
| exact_term | 7 | 0.429 | 0.429 | 1.000 | 1.000 | 0.857 [0.57, 1.00] | 0.602 [0.34, 0.86] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.367 | 0.233 | 0.967 | 1.000 | 0.700 [0.56, 0.84] | 0.613 [0.37, 0.85] | 0.900 [0.81, 0.97] |  |  |  |
| compound | 7 | 0.357 | 0.143 | 0.643 | 1.000 | 0.429 [0.00, 0.86] | 0.407 [0.08, 0.78] | 0.714 [0.50, 0.93] |  |  |  |
| outdated_version | 25 | 0.640 | 0.360 | 0.960 | 1.000 | 0.760 [0.58, 0.92] | 0.545 [0.41, 0.70] | 0.920 [0.80, 1.00] | 0.000 [0.00, 0.00] | 0.920 [0.80, 1.00] | 0.000 [0.00, 0.00] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.500 [0.50, 0.50] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.000 | 0.000 | 0.200 | 1.000 | 0.000 [0.00, 0.00] | 0.090 [0.07, 0.11] | 0.000 [0.00, 0.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.540 | 0.821 | 0.893 | 0.741 | 0.313 | 0.583 | 0.694 | 0.509 | 0.000 | 0.000 | 0.000 | 0.000 | 0.920 |  |  |  |  |  |  | 0.889 | 0.944 |
| non_outdated | 101.000 | 61.000 | 0.515 | 0.807 | 0.886 | 0.732 | 0.302 | 0.559 | 0.678 | 0.500 |  |  |  |  |  |  |  |  |  |  |  | 0.871 | 0.931 |
| lookup | 42.000 | 34.000 | 0.643 | 0.905 | 0.976 | 0.779 | 0.452 | 0.714 | 0.857 | 0.617 |  |  |  |  |  |  |  |  |  |  |  | 0.976 | 0.976 |
| paraphrase | 30.000 | 28.000 | 0.467 | 0.733 | 0.800 | 0.621 | 0.133 | 0.333 | 0.433 | 0.278 |  |  |  |  |  |  |  |  |  |  |  | 0.700 | 0.800 |
| exact_term | 7.000 | 7.000 | 0.429 | 0.857 | 0.857 | 0.626 | 0.429 | 0.857 | 0.857 | 0.602 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.367 | 0.767 | 0.900 | 0.830 | 0.233 | 0.533 | 0.700 | 0.613 |  |  |  |  |  |  |  |  |  |  |  | 0.967 | 1.000 |
| compound | 7.000 | 5.000 | 0.357 | 0.571 | 0.714 | 0.821 | 0.143 | 0.357 | 0.429 | 0.407 |  |  |  |  |  |  |  |  |  |  |  | 0.643 | 1.000 |
| outdated_version | 25.000 | 22.000 | 0.640 | 0.880 | 0.920 | 0.776 | 0.360 | 0.680 | 0.760 | 0.545 | 0.000 | 0.000 | 0.000 | 0.000 | 0.920 |  |  |  |  |  |  | 0.960 | 1.000 |
| real_pair | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.500 | 0.000 | 1.000 | 1.000 | 0.500 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |  |  |  |  |  |  | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.000 | 0.000 | 0.000 | 0.108 | 0.000 | 0.000 | 0.000 | 0.090 |  |  |  |  |  |  |  |  |  |  |  | 0.200 | 1.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/subscription-agreement/index | How long does GitLab retain security incident communications sent to customers? |
| pp-05 | paraphrase | 10 | hb:security/security-assurance/governance/security-training | Do people joining GitLab have to complete a security course when they start? |
| pp-08 | paraphrase | 8 | hb:total-rewards/incentives | Can I get a bonus for recommending a friend for an internship at GitLab? |
| ex-08 | exact_term | 21 | hb:hiring/conducting-a-gitlab-interview | What is LevelUp at GitLab? |
| ov-11 | outdated_version | 7 | hb:total-rewards/benefits/general-and-entity-benefits/remote-com | How long is parental leave for GitLab team members in the US? |
| ov-34 | outdated_version | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab keep risk treatment plans? |
| pp-19 | paraphrase | 8 | hb:support/on-call | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-27 | paraphrase | not found | hb:total-rewards/benefits/parental-leave-toolkit | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:people-policies | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:legal/legacy/privacy-statement-v2 | Do I need a PIN on my own phone if I use it for GitLab work? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 1 | 9 | 0.000 | 0.000 |
| ov-07 | 1 | 8 | 0.000 | 0.000 |
| ov-08 | 1 | 8 | 0.000 | 0.000 |
| ov-11 | 7 | 19 | 0.000 |  |
| ov-12 | 2 | 11 | 0.000 | 0.000 |
| ov-13 | 1 | 9 | 0.000 | 0.000 |
| ov-14 | 1 | 8 | 0.000 | 0.000 |
| ov-16 | 1 | 9 | 0.000 | 0.000 |
| ov-17 | 1 | 6 | 0.000 | 0.000 |
| ov-21 | 1 | 10 | 0.000 | 0.000 |
| ov-22 | 1 | 8 | 0.000 | 0.000 |
| ov-25 | 1 | 9 | 0.000 | 0.000 |
| ov-26 | 2 | 9 | 0.000 | 0.000 |
| ov-27 | 2 | 8 | 0.000 | 0.000 |
| ov-28 | 1 | 8 | 0.000 | 0.000 |
| ov-29 | 2 | 11 | 0.000 | 0.000 |
| ov-30 | 1 | 11 | 0.000 | 0.000 |
| ov-31 | 1 | 10 | 0.000 | 0.000 |
| ov-32 | 1 | 5 | 0.000 | 0.000 |
| ov-33 | 2 | 8 | 0.000 | 0.000 |
| ov-34 | - | - |  |  |
| ov-36 | 2 | 12 | 0.000 | 0.000 |
| ov-38 | 1 | 7 | 0.000 | 0.000 |
| ov-40 | 1 | 11 | 0.000 | 0.000 |
| ov-44 | 4 | 17 | 0.000 | 0.000 |
