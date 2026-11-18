# Run: test_final

- split: **test** (39 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: BAAI/bge-small-en-v1.5
- retrieval: mode=hybrid top_k=30 version_filter=none date_aware=True reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 0.0% of units, 0.0% of tokens never embedded
- gold quotes reachable in this chunking: 39/39
- run at: 2026-11-18 17:40

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 33 | 0.803 | 0.364 | 0.924 | 1.000 | 0.697 [0.52, 0.84] | 0.549 [0.40, 0.70] | 0.970 [0.89, 1.00] | 0.143 [0.00, 0.33] | 1.000 [1.00, 1.00] | 0.071 [0.00, 0.27] |
| non_outdated | 19 | 0.711 | 0.368 | 0.921 | 1.000 | 0.632 [0.39, 0.81] | 0.566 [0.38, 0.74] | 0.947 [0.81, 1.00] |  |  |  |
| lookup | 8 | 0.625 | 0.250 | 0.875 | 1.000 | 0.625 [0.25, 0.88] | 0.432 [0.19, 0.71] | 0.875 [0.62, 1.00] |  |  |  |
| paraphrase | 5 | 0.800 | 0.400 | 1.000 | 1.000 | 0.600 [0.00, 1.00] | 0.545 [0.06, 1.00] | 1.000 [1.00, 1.00] |  |  |  |
| exact_term | 3 | 1.000 | 0.667 | 1.000 | 1.000 | 0.667 [0.00, 1.00] | 0.692 [0.08, 1.00] | 1.000 [1.00, 1.00] |  |  |  |
| multi_doc | 3 | 0.500 | 0.333 | 0.833 | 1.000 | 0.667 [0.50, 1.00] | 0.833 [0.75, 1.00] | 1.000 [1.00, 1.00] |  |  |  |
| outdated_version | 14 | 0.929 | 0.357 | 0.929 | 1.000 | 0.786 [0.53, 1.00] | 0.526 [0.31, 0.79] | 1.000 [1.00, 1.00] | 0.143 [0.00, 0.33] | 1.000 [1.00, 1.00] | 0.071 [0.00, 0.27] |
| real_pair | 1 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 [1.00, 1.00] | 0.250 [0.25, 0.25] | 1.000 [1.00, 1.00] |  |  | 0.000 [0.00, 0.00] |
| history | 2 | 0.500 | 0.000 | 1.000 | 1.000 | 0.500 [0.00, 1.00] | 0.288 [0.08, 0.50] | 1.000 [1.00, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 33.000 | 21.000 | 0.803 | 0.955 | 0.970 | 0.904 | 0.364 | 0.606 | 0.697 | 0.549 | 0.071 | 0.071 | 0.143 | 0.182 | 1.000 |  |  |  |  |  |  | 0.924 | 1.000 |
| non_outdated | 19.000 | 14.000 | 0.711 | 0.921 | 0.947 | 0.860 | 0.368 | 0.579 | 0.632 | 0.566 |  |  |  |  |  |  |  |  |  |  |  | 0.921 | 1.000 |
| lookup | 8.000 | 8.000 | 0.625 | 0.875 | 0.875 | 0.750 | 0.250 | 0.500 | 0.625 | 0.432 |  |  |  |  |  |  |  |  |  |  |  | 0.875 | 1.000 |
| paraphrase | 5.000 | 3.000 | 0.800 | 1.000 | 1.000 | 0.867 | 0.400 | 0.600 | 0.600 | 0.545 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |
| exact_term | 3.000 | 3.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.667 | 0.667 | 0.667 | 0.692 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |
| multi_doc | 3.000 | 2.000 | 0.500 | 0.833 | 1.000 | 1.000 | 0.333 | 0.667 | 0.667 | 0.833 |  |  |  |  |  |  |  |  |  |  |  | 0.833 | 1.000 |
| outdated_version | 14.000 | 9.000 | 0.929 | 1.000 | 1.000 | 0.964 | 0.357 | 0.643 | 0.786 | 0.526 | 0.071 | 0.071 | 0.143 | 0.182 | 1.000 |  |  |  |  |  |  | 0.929 | 1.000 |
| real_pair | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.250 | 0.000 | 0.000 |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |
| history | 2.000 | 2.000 | 0.500 | 1.000 | 1.000 | 0.750 | 0.000 | 0.500 | 0.500 | 0.288 |  |  |  |  |  |  |  |  |  |  |  | 1.000 | 1.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-08 | lookup | not found | hb:security/security-assurance/security-risk/storm-program | How long does GitLab retain its annual risk assessment report? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-09 | 1 | 2 | 0.000 | 0.000 |
| ov-10 | 1 | 2 | 0.000 | 0.000 |
| ov-15 | 1 | 3 | 0.000 | 0.000 |
| ov-18 | 1 | 3 | 0.000 | 0.000 |
| ov-19 | 1 | 2 | 0.000 | 0.000 |
| ov-20 | 1 | 2 | 0.000 | 0.000 |
| ov-23 | 2 | 1 | 1.000 | 0.000 |
| ov-24 | 1 | 3 | 0.000 | 0.000 |
| ov-35 | 1 | 2 | 0.000 | 0.000 |
| ov-37 | 1 | 2 | 0.000 | 1.000 |
| ov-39 | 1 | 2 | 0.000 | 0.000 |
| ov-41 | 1 | 2 | 0.000 | 1.000 |
| ov-42 | 1 | 3 | 0.000 | 0.000 |
| ov-43 | 1 | 2 | 0.000 | 0.000 |
