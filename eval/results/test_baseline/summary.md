# Run: test_baseline

- split: **test** (39 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- chunks: 2468 (embedded units: 2468); truncated by the embedding model: 92.7% of units, 46.7% of tokens never embedded
- gold quotes reachable in this chunking: 39/39
- run at: 2026-11-18 17:40

## Headline metrics (95% bootstrap intervals in brackets)

Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; doc-level stale is secondary.

`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.

| group | n | doc_R@1 | chunk_R@1 | chunk_R@30 | chunk_R@100 | chunk_recall@5 | chunk_mrr | doc_recall@5 | fact_stale | fact_found | stale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 33 | 0.364 | 0.152 | 0.576 | 0.818 | 0.364 [0.18, 0.55] | 0.288 [0.15, 0.43] | 0.848 [0.72, 0.95] | 1.000 [1.00, 1.00] | 0.429 [0.13, 0.82] | 0.769 [0.45, 1.00] |
| non_outdated | 19 | 0.526 | 0.263 | 0.684 | 0.789 | 0.368 [0.17, 0.59] | 0.376 [0.18, 0.57] | 0.842 [0.67, 1.00] |  |  |  |
| lookup | 8 | 0.625 | 0.250 | 0.625 | 0.750 | 0.375 [0.12, 0.75] | 0.321 [0.07, 0.62] | 0.875 [0.62, 1.00] |  |  |  |
| paraphrase | 5 | 0.600 | 0.200 | 0.800 | 1.000 | 0.200 [0.00, 0.33] | 0.261 [0.00, 0.42] | 1.000 [1.00, 1.00] |  |  |  |
| exact_term | 3 | 0.333 | 0.333 | 0.667 | 0.667 | 0.333 [0.00, 1.00] | 0.354 [0.00, 1.00] | 0.667 [0.00, 1.00] |  |  |  |
| multi_doc | 3 | 0.333 | 0.333 | 0.667 | 0.667 | 0.667 [0.50, 1.00] | 0.733 [0.60, 1.00] | 0.667 [0.50, 1.00] |  |  |  |
| outdated_version | 14 | 0.143 | 0.000 | 0.429 | 0.857 | 0.357 [0.07, 0.71] | 0.170 [0.04, 0.34] | 0.857 [0.69, 1.00] | 1.000 [1.00, 1.00] | 0.429 [0.13, 0.82] | 0.769 [0.45, 1.00] |
| real_pair | 1 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 [0.00, 0.00] | 0.143 [0.14, 0.14] | 1.000 [1.00, 1.00] |  |  | 1.000 [1.00, 1.00] |
| history | 2 | 0.500 | 0.000 | 0.500 | 1.000 | 0.500 [0.00, 1.00] | 0.125 [0.00, 0.25] | 1.000 [1.00, 1.00] |  |  |  |

## All metrics

| group | n | clusters | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 | fact_stale | fact_stale@5 | fact_found | stale_t001 | fact_stale_t001 | stale_t005 | fact_stale_t005 | stale_t01 | fact_stale_t01 | chunk_recall@30 | chunk_recall@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 33.000 | 21.000 | 0.364 | 0.758 | 0.848 | 0.591 | 0.152 | 0.348 | 0.364 | 0.288 | 0.769 | 0.833 | 1.000 | 1.000 | 0.429 | 0.692 | 0.833 | 0.577 | 0.583 | 0.500 | 0.500 | 0.576 | 0.818 |
| non_outdated | 19.000 | 14.000 | 0.526 | 0.737 | 0.842 | 0.701 | 0.263 | 0.342 | 0.368 | 0.376 |  |  |  |  |  |  |  |  |  |  |  | 0.684 | 0.789 |
| lookup | 8.000 | 8.000 | 0.625 | 0.750 | 0.875 | 0.698 | 0.250 | 0.375 | 0.375 | 0.321 |  |  |  |  |  |  |  |  |  |  |  | 0.625 | 0.750 |
| paraphrase | 5.000 | 3.000 | 0.600 | 0.800 | 1.000 | 0.750 | 0.200 | 0.200 | 0.200 | 0.261 |  |  |  |  |  |  |  |  |  |  |  | 0.800 | 1.000 |
| exact_term | 3.000 | 3.000 | 0.333 | 0.667 | 0.667 | 0.548 | 0.333 | 0.333 | 0.333 | 0.354 |  |  |  |  |  |  |  |  |  |  |  | 0.667 | 0.667 |
| multi_doc | 3.000 | 2.000 | 0.333 | 0.667 | 0.667 | 0.778 | 0.333 | 0.500 | 0.667 | 0.733 |  |  |  |  |  |  |  |  |  |  |  | 0.667 | 0.667 |
| outdated_version | 14.000 | 9.000 | 0.143 | 0.786 | 0.857 | 0.442 | 0.000 | 0.357 | 0.357 | 0.170 | 0.769 | 0.833 | 1.000 | 1.000 | 0.429 | 0.692 | 0.833 | 0.577 | 0.583 | 0.500 | 0.500 | 0.429 | 0.857 |
| real_pair | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.500 | 0.000 | 0.000 | 0.000 | 0.143 | 1.000 | 1.000 |  |  |  | 1.000 |  | 1.000 |  | 0.500 |  | 1.000 | 1.000 |
| history | 2.000 | 2.000 | 0.500 | 1.000 | 1.000 | 0.667 | 0.000 | 0.000 | 0.500 | 0.125 |  |  |  |  |  |  |  |  |  |  |  | 0.500 | 1.000 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-08 | lookup | not found | hb:legal/eu-data-act-terms | How long does GitLab retain its annual risk assessment report? |
| ex-05 | exact_term | 7 | hb:security/security-assurance/security-compliance/pci-charter | How often are PCI in-scope applications reviewed in GitLab's access review procedure? |
| ov-18 | outdated_version | 9 | hb:finance/accounts-payable/corp-credit-cards | What is GitLab's yearly reimbursement limit for business cards? |
| ov-20 | outdated_version | not found | hb:legal/technology-partner-agreement-v1 | For applications where a password is the only authentication, how often must GitLab passwords expire? |

## Outdated-version questions

stale / fact_stale (by rank): 1 = old version first, 0 = current first, blank = neither version retrieved.

| id | first current doc rank | first old doc rank | stale | fact_stale |
|---|---|---|---|---|
| ov-09 | 1 | 2 | 0.000 |  |
| ov-10 | 3 | 2 | 1.000 | 1.000 |
| ov-15 | 3 | 2 | 1.000 | 1.000 |
| ov-18 | 9 | 10 | 0.000 |  |
| ov-19 | 3 | 2 | 1.000 |  |
| ov-20 | - | - |  |  |
| ov-23 | 2 | 1 | 1.000 | 1.000 |
| ov-24 | 2 | 1 | 1.000 | 1.000 |
| ov-35 | 2 | 1 | 1.000 | 1.000 |
| ov-37 | 3 | 2 | 1.000 |  |
| ov-39 | 2 | 1 | 1.000 |  |
| ov-41 | 4 | 3 | 1.000 |  |
| ov-42 | 1 | 2 | 0.000 |  |
| ov-43 | 2 | 1 | 1.000 | 1.000 |
