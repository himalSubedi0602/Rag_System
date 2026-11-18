# Run: hybrid_k10

- split: **tune** (144 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=hybrid top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 159/159
- run at: 2026-11-18 17:10

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126 | 0.579 | 0.310 | 0.889 | 0.944 | 0.679 [0.59, 0.76] | 0.517 [0.44, 0.59] | 0.905 [0.84, 0.96] | 0.739 [0.55, 0.91] | 0.920 [0.80, 1.00] | 0.667 [0.45, 0.86] |
| non_outdated | 101 | 0.663 | 0.376 | 0.881 | 0.931 | 0.678 [0.58, 0.76] | 0.566 [0.48, 0.64] | 0.901 [0.83, 0.95] |  |  |  |
| lookup | 42 | 0.833 | 0.548 | 0.952 | 0.976 | 0.857 [0.74, 0.95] | 0.687 [0.58, 0.78] | 0.976 [0.92, 1.00] |  |  |  |
| paraphrase | 30 | 0.567 | 0.167 | 0.700 | 0.800 | 0.433 [0.26, 0.61] | 0.287 [0.17, 0.41] | 0.800 [0.63, 0.96] |  |  |  |
| exact_term | 7 | 0.714 | 0.571 | 1.000 | 1.000 | 0.857 [0.57, 1.00] | 0.721 [0.45, 0.93] | 0.857 [0.57, 1.00] |  |  |  |
| multi_doc | 15 | 0.467 | 0.300 | 0.967 | 1.000 | 0.667 [0.46, 0.82] | 0.743 [0.55, 0.92] | 0.933 [0.82, 1.00] |  |  |  |
| compound | 7 | 0.429 | 0.214 | 0.929 | 1.000 | 0.500 [0.07, 0.93] | 0.507 [0.13, 0.89] | 0.857 [0.60, 1.00] |  |  |  |
| outdated_version | 25 | 0.240 | 0.040 | 0.920 | 1.000 | 0.680 [0.50, 0.85] | 0.318 [0.24, 0.41] | 0.920 [0.80, 1.00] | 0.739 [0.55, 0.91] | 0.920 [0.80, 1.00] | 0.667 [0.45, 0.86] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.200 [0.20, 0.20] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] | 1.000 [1.00, 1.00] |
| history | 10 | 0.200 | 0.200 | 1.000 | 1.000 | 0.700 [0.40, 1.00] | 0.444 [0.25, 0.65] | 0.900 [0.70, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 126.000 | 75.000 | 0.579 | 0.885 | 0.905 | 0.773 | 0.310 | 0.631 | 0.679 | 0.517 | 0.667 | 0.696 | 0.739 | 0.778 | 0.920 |  |  |  |  |  |  | 0.889 | 0.944 |
| non_outdated | 101.000 | 61.000 | 0.663 | 0.876 | 0.901 | 0.833 | 0.376 | 0.639 | 0.678 | 0.566 |  |  |  |  |  |  |  |  |  |  |  | 0.881 | 0.931 |
| lookup | 42.000 | 34.000 | 0.833 | 0.976 | 0.976 | 0.897 | 0.548 | 0.833 | 0.857 | 0.687 |  |  |  |  |  |  |  |  |  |  |  | 0.952 | 0.976 |
| paraphrase | 30.000 | 28.000 | 0.567 | 0.767 | 0.800 | 0.675 | 0.167 | 0.367 | 0.433 | 0.287 |  |  |  |  |  |  |  |  |  |  |  | 0.700 | 0.800 |
| exact_term | 7.000 | 7.000 | 0.714 | 0.857 | 0.857 | 0.792 | 0.571 | 0.857 | 0.857 | 0.721 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |
| multi_doc | 15.000 | 8.000 | 0.467 | 0.900 | 0.933 | 0.956 | 0.300 | 0.667 | 0.667 | 0.743 |  |  |  |  |  |  |  |  |  |  |  | 0.967 | 1.000 |
| compound | 7.000 | 5.000 | 0.429 | 0.714 | 0.857 | 0.905 | 0.214 | 0.357 | 0.500 | 0.507 |  |  |  |  |  |  |  |  |  |  |  | 0.929 | 1.000 |
| outdated_version | 25.000 | 22.000 | 0.240 | 0.920 | 0.920 | 0.532 | 0.040 | 0.600 | 0.680 | 0.318 | 0.667 | 0.696 | 0.739 | 0.778 | 0.920 |  |  |  |  |  |  | 0.920 | 1.000 |
| real_pair | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.200 | 0.000 | 0.000 | 1.000 | 0.200 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |  |  |  |  |  |  | 1.000 | 1.000 |
| history | 10.000 | 10.000 | 0.200 | 0.900 | 0.900 | 0.546 | 0.200 | 0.700 | 0.700 | 0.444 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/subscription-agreement/index | How long does GitLab retain security incident communications sent to customers? |
| pp-05 | paraphrase | 9 | hb:security/security-assurance/governance/security-training | Do people joining GitLab have to complete a security course when they start? |
| ex-08 | exact_term | 22 | hb:hiring/conducting-a-gitlab-interview | What is LevelUp at GitLab? |
| ov-11 | outdated_version | 7 | hb:total-rewards/benefits/general-and-entity-benefits/remote-com | How long is parental leave for GitLab team members in the US? |
| ov-34 | outdated_version | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab keep risk treatment plans? |
| pp-19 | paraphrase | 10 | hb:support/on-call | Working remotely for GitLab France, what's the shortest break I must have between finishing one day and starting the next? |
| pp-24 | paraphrase | 8 | hb:hiring/candidate-faq | Which appraisal result lets me put myself forward for a different position within GitLab? |
| pp-27 | paraphrase | not found | hb:total-rewards/benefits/parental-leave-toolkit | Someone outside GitLab is funding my journey. Am I allowed to add some holiday time afterwards? |
| pp-30 | paraphrase | not found | hb:people-policies | I'm working from a café. How should I handle my GitLab laptop? |
| pp-31 | paraphrase | not found | hb:legal/legacy/privacy-statement-v2 | Do I need a PIN on my own phone if I use it for GitLab work? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-06 | 1 | 2 | 0.000 | 0.000 |
| ov-07 | 3 | 1 | 1.000 | 1.000 |
| ov-08 | 2 | 1 | 1.000 | 0.000 |
| ov-11 | 7 | 8 | 0.000 |  |
| ov-12 | 2 | 1 | 1.000 | 1.000 |
| ov-13 | 1 | 2 | 0.000 | 0.000 |
| ov-14 | 2 | 1 | 1.000 | 1.000 |
| ov-16 | 1 | 2 | 0.000 | 0.000 |
| ov-17 | 2 | 1 | 1.000 | 1.000 |
| ov-21 | 2 | 1 | 1.000 | 1.000 |
| ov-22 | 3 | 1 | 1.000 | 1.000 |
| ov-25 | 1 | 4 | 0.000 | 0.000 |
| ov-26 | 3 | 2 | 1.000 | 1.000 |
| ov-27 | 3 | 1 | 1.000 | 1.000 |
| ov-28 | 2 | 1 | 1.000 | 1.000 |
| ov-29 | 3 | 1 | 1.000 | 1.000 |
| ov-30 | 2 | 1 | 1.000 | 1.000 |
| ov-31 | 2 | 1 | 1.000 | 1.000 |
| ov-32 | 3 | 1 | 1.000 | 1.000 |
| ov-33 | 3 | 1 | 1.000 | 1.000 |
| ov-34 | - | - |  |  |
| ov-36 | 2 | 1 | 1.000 | 1.000 |
| ov-38 | 1 | 4 | 0.000 | 1.000 |
| ov-40 | 1 | 2 | 0.000 | 0.000 |
| ov-44 | 3 | 8 | 0.000 | 1.000 |
