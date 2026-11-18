# Report: phase7c_combined (reference: hybrid, tune split)

- **hybrid**: Run 6: bge + BM25 hybrid merged with reciprocal rank fusion, k = 60 (pre-registered). Base = bge.
- **hybrid_rerank30**: Amendment 4b: bge + BM25 hybrid (RRF k = 60) + cross-encoder reranker over the top 30 fused candidates.
- **rerank30**: Run 7: bge + cross-encoder reranker over the top 30. Base = bge.
- **bge**: Run 5: bge-small instead of MiniLM. Reads 512 tokens, so 500-token chunks are not truncated.
- **baseline**: Run 1: baseline. Fixed 500-token chunks, 50 overlap, vector search only, MiniLM.

**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes zero; – = no detectable difference. Verdicts use the CLUSTER interval (first bracket); the plain per-question interval is shown for context only.

## Paired differences from hybrid

| run | Δ MAIN chunk R@5 (overall) | Δ chunk R@5 (non_outdated, guardrail) | Δ fact_stale (by rank, both found) | Δ stale doc-level (by rank) | Δ fact_found (outdated, guardrail) | Δ history chunk R@5 (guardrail) |
|---|---|---|---|---|---|---|
| hybrid |  |  |  |  |  |  |
| hybrid_rerank30 | +0.028 [-0.033, 0.085] – (plain [-0.028, 0.083]; 12/7, n=126, 75 clusters) | +0.035 [-0.029, 0.097] – (plain [-0.025, 0.099]; 10/5, n=101, 61 clusters) | -0.087 [-0.364, 0.227] – (plain [-0.391, 0.174]; 7/5, n=23, 20 clusters) | -0.125 [-0.346, 0.125] – (plain [-0.375, 0.125]; 6/3, n=24, 21 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=10, 10 clusters) |
| rerank30 | -0.012 [-0.065, 0.038] – (plain [-0.063, 0.040]; 7/8, n=126, 75 clusters) | +0.005 [-0.054, 0.065] – (plain [-0.054, 0.064]; 7/6, n=101, 61 clusters) | -0.176 [-0.438, 0.125] – (plain [-0.471, 0.118]; 5/2, n=17, 14 clusters) | -0.174 [-0.391, 0.048] – (plain [-0.391, 0.043]; 6/2, n=23, 20 clusters) | -0.240 [-0.435, -0.077] ❌ (plain [-0.400, -0.080]; 0/6, n=25, 22 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=10, 10 clusters) |
| bge | -0.135 [-0.221, -0.055] ❌ (plain [-0.202, -0.063]; 7/24, n=126, 75 clusters) | -0.109 [-0.202, -0.022] ❌ (plain [-0.188, -0.035]; 7/18, n=101, 61 clusters) | -0.059 [-0.222, 0.143] – (plain [-0.294, 0.118]; 2/1, n=17, 14 clusters) | +0.000 [-0.231, 0.238] – (plain [-0.217, 0.217]; 3/3, n=23, 20 clusters) | -0.240 [-0.435, -0.077] ❌ (plain [-0.400, -0.080]; 0/6, n=25, 22 clusters) | -0.100 [-0.300, 0.000] – (plain [-0.300, 0.000]; 0/1, n=10, 10 clusters) |
| baseline | -0.187 [-0.283, -0.094] ❌ (plain [-0.278, -0.103]; 7/31, n=126, 75 clusters) | -0.153 [-0.252, -0.049] ❌ (plain [-0.252, -0.054]; 7/23, n=101, 61 clusters) | -0.167 [-0.462, 0.154] – (plain [-0.500, 0.167]; 3/1, n=12, 10 clusters) | -0.091 [-0.360, 0.200] – (plain [-0.364, 0.182]; 6/4, n=22, 19 clusters) | -0.440 [-0.652, -0.227] ❌ (plain [-0.640, -0.240]; 0/11, n=25, 22 clusters) | -0.200 [-0.500, 0.000] – (plain [-0.500, 0.000]; 0/2, n=10, 10 clusters) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better. stale and fact_stale are decided by RANK for every run (Amendment 3b), so all runs share one scale; tie-tolerance variants are a secondary detail for cosine runs only.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| hybrid | 0.682 [0.59, 0.77] | 0.683 [0.59, 0.77] | 0.524 [0.44, 0.60] | 0.905 [0.84, 0.96] | 0.901 | 0.944 |
| hybrid_rerank30 | 0.710 [0.62, 0.79] | 0.718 [0.63, 0.79] | 0.600 [0.51, 0.68] | 0.857 [0.78, 0.92] | 0.901 | 0.944 |
| rerank30 | 0.671 [0.58, 0.76] | 0.688 [0.60, 0.77] | 0.580 [0.49, 0.67] | 0.841 [0.77, 0.91] | 0.786 | 0.873 |
| bge | 0.548 [0.46, 0.64] | 0.574 [0.47, 0.66] | 0.398 [0.33, 0.47] | 0.798 [0.72, 0.88] | 0.786 | 0.873 |
| baseline | 0.496 [0.40, 0.59] | 0.530 [0.43, 0.63] | 0.356 [0.28, 0.43] | 0.734 [0.65, 0.81] | 0.698 | 0.806 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) | secondary: fact_stale tol 0.001 / 0.005 / 0.01 (cosine only) |
|---|---|---|---|
| hybrid | 0.739 [0.55, 0.91] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| hybrid_rerank30 | 0.652 [0.48, 0.83] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| rerank30 | 0.647 [0.44, 0.87] | 0.680 [0.48, 0.85] | n/a / n/a / n/a |
| bge | 0.765 [0.58, 0.94] | 0.680 [0.48, 0.85] | 0.676 / 0.529 / 0.529 |
| baseline | 0.667 [0.38, 0.91] | 0.480 [0.27, 0.69] | 0.417 / 0.458 / 0.500 |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| hybrid | 2468 | 3.7 | 18.6 | 0.0 | 159/159 |
| hybrid_rerank30 | 2468 | 3.7 | 242.6 | 0.0 | 159/159 |
| rerank30 | 2468 | 3.7 | 233.0 | 0.0 | 159/159 |
| bge | 2468 | 3.7 | 10.9 | 0.0 | 159/159 |
| baseline | 2468 | 3.7 | 8.5 | 46.7 | 159/159 |

## Replication (frozen groups in eval/replication_groups.json)

An effect replicates if it has the same sign on the new questions; it is confirmed only if the combined interval excludes zero.

| run | Δ chunk R@5 (original, n=66) | Δ chunk R@5 (new only, n=60) | Δ chunk R@5 (combined, n=126) |
|---|---|---|---|
| hybrid_rerank30 | +0.030 [-0.052, 0.125] – (plain [-0.061, 0.121]; 7/4, n=66, 41 clusters) | +0.025 [-0.053, 0.106] – (plain [-0.042, 0.092]; 5/3, n=60, 36 clusters) | +0.028 [-0.033, 0.085] – (plain [-0.028, 0.083]; 12/7, n=126, 75 clusters) |
| rerank30 | -0.015 [-0.085, 0.052] – (plain [-0.091, 0.053]; 4/4, n=66, 41 clusters) | -0.008 [-0.086, 0.070] – (plain [-0.083, 0.067]; 3/4, n=60, 36 clusters) | -0.012 [-0.065, 0.038] – (plain [-0.063, 0.040]; 7/8, n=126, 75 clusters) |
| bge | -0.121 [-0.224, -0.018] ❌ (plain [-0.220, -0.038]; 3/11, n=66, 41 clusters) | -0.150 [-0.279, -0.025] ❌ (plain [-0.258, -0.042]; 4/13, n=60, 36 clusters) | -0.135 [-0.221, -0.055] ❌ (plain [-0.202, -0.063]; 7/24, n=126, 75 clusters) |
| baseline | -0.220 [-0.353, -0.092] ❌ (plain [-0.326, -0.121]; 1/16, n=66, 41 clusters) | -0.150 [-0.284, -0.014] ❌ (plain [-0.292, -0.008]; 6/15, n=60, 36 clusters) | -0.187 [-0.283, -0.094] ❌ (plain [-0.278, -0.103]; 7/31, n=126, 75 clusters) |

## chunk R@5 by question_type (`overall` questions)

| run | compound (n=7) | exact_term (n=7) | lookup (n=42) | multi_doc (n=15) | outdated_version (n=25) | paraphrase (n=30) |
|---|---|---|---|---|---|---|
| hybrid | 0.429 | 0.857 | 0.857 | 0.667 | 0.680 | 0.467 |
| hybrid_rerank30 | 0.429 | 0.714 | 0.929 | 0.767 | 0.680 | 0.467 |
| rerank30 | 0.286 | 0.714 | 0.881 | 0.767 | 0.600 | 0.467 |
| bge | 0.357 | 0.857 | 0.714 | 0.700 | 0.440 | 0.300 |
| baseline | 0.429 | 0.857 | 0.524 | 0.567 | 0.360 | 0.467 |

## chunk R@5 by doc_group (`overall` questions)

| run | finance (n=25) | hiring (n=6) | legal (n=1) | mixed (n=4) | pdf (n=27) | people-policies (n=7) | security (n=24) | support (n=5) | total-rewards (n=27) |
|---|---|---|---|---|---|---|---|---|---|
| hybrid | 0.640 | 0.833 | 1.000 | 0.375 | 0.648 | 0.286 | 0.688 | 0.400 | 0.907 |
| hybrid_rerank30 | 0.680 | 0.667 | 1.000 | 0.500 | 0.815 | 0.286 | 0.646 | 0.400 | 0.889 |
| rerank30 | 0.600 | 0.667 | 1.000 | 0.375 | 0.796 | 0.286 | 0.646 | 0.400 | 0.815 |
| bge | 0.440 | 0.333 | 1.000 | 0.375 | 0.722 | 0.286 | 0.521 | 0.000 | 0.722 |
| baseline | 0.360 | 0.167 | 1.000 | 0.375 | 0.667 | 0.286 | 0.375 | 0.200 | 0.741 |
