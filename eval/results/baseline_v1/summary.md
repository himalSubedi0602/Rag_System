# Run: baseline_v1 (BEFORE the measurement + test-data fixes; kept for comparison)

- split: **tune** (55 questions; no_answer excluded from retrieval metrics)
- chunking: fixed size=500 overlap=50 prefix=False
- embedding: sentence-transformers/all-MiniLM-L6-v2
- retrieval: mode=vector top_k=30 version_filter=none date_aware=False reranker=False
- run at: 2026-11-17 21:17

## Metrics

| group | n | doc_recall@1 | doc_recall@3 | doc_recall@5 | doc_mrr | chunk_recall@1 | chunk_recall@3 | chunk_recall@5 | chunk_mrr | stale | stale@5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| overall | 48.000 | 0.573 | 0.708 | 0.781 | 0.708 | 0.198 | 0.417 | 0.458 | 0.356 | 0.400 | 0.300 |
| lookup | 14.000 | 0.786 | 0.857 | 0.857 | 0.821 | 0.143 | 0.357 | 0.357 | 0.275 |  |  |
| paraphrase | 10.000 | 0.700 | 0.700 | 0.700 | 0.706 | 0.300 | 0.400 | 0.400 | 0.363 |  |  |
| exact_term | 7.000 | 0.714 | 0.857 | 0.857 | 0.786 | 0.429 | 0.857 | 0.857 | 0.619 |  |  |
| multi_doc | 7.000 | 0.357 | 0.429 | 0.643 | 0.750 | 0.214 | 0.286 | 0.429 | 0.542 |  |  |
| outdated_version | 10.000 | 0.200 | 0.600 | 0.800 | 0.470 | 0.000 | 0.300 | 0.400 | 0.147 | 0.400 | 0.300 |

## Answerable questions with no gold document in the top 5

| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |
|---|---|---|---|---|
| lk-06 | lookup | not found | hb:legal/legacy/legacy-subscription-agreement-v4 | How long does GitLab retain security incident communications sent to customers? |
| lk-11 | lookup | not found | hb:total-rewards/benefits/general-and-entity-benefits/france-sas | Over what reference period are average weekly working hours calculated for the 48-hour limit in GitLab's people policies? |
| pp-03 | paraphrase | 18 | hb:legal/legacy/legacy-subscription-agreement-v4 | As a GitLab Support engineer, when should I rethink the dates I want to take off? |
| pp-04 | paraphrase | not found | hb:legal/legacy/legacy-subscription-agreement-v5 | If I signed away the 48-hour weekly limit at GitLab, how much warning must I give to take that back? |
| pp-14 | paraphrase | not found | hb:finance/procurement/vendor-guidelines/legacy-vendor-agreement-v1 | Can I buy second-hand work equipment from an individual and claim it back from GitLab? |
| ex-08 | exact_term | not found | hb:total-rewards/compensation | What is LevelUp at GitLab? |
| md-06 | multi_doc | not found | hb:security/policies_and_standards/software-development-lifecycle-standard | How long does GitLab keep records of production changes, and how often are external certification systems access-reviewed? |
| ov-06 | outdated_version | 18 | hb:finance/accounting | How long after the purchase date can I submit a GitLab expense claim and still be reimbursed without manager approval? |
| ov-11 | outdated_version | 7 | hb:total-rewards/benefits/general-and-entity-benefits/korea-ltd-benefits | How long is parental leave for GitLab team members in the US? |

## Stale cases (outdated version ranked above the current one)

| id | first current rank | first outdated rank | outdated doc |
|---|---|---|---|
| ov-02 | 4 | 1 | hb:legal/testing-agreement-v3 |
| ov-06 | 18 | 11 | syn:expenses-2023 |
| ov-12 | 4 | 2 | syn:referral-process-2022 |
| ov-14 | 2 | 1 | syn:phishing-program-2022 |
