# Report: phase7b_step2_vs_baseline (reference: baseline, tune split)

- **baseline**: Run 1: baseline. Fixed 500-token chunks, 50 overlap, vector search only, MiniLM.
- **bge**: Run 5: bge-small instead of MiniLM. Reads 512 tokens, so 500-token chunks are not truncated.
- **bge_prefix**: Run 6p: bge + title/section prefix. Base = bge; only change: prefix on every chunk (truncation vs bge's 512 limit reported).
- **hybrid**: Run 6: bge + BM25 hybrid merged with reciprocal rank fusion, k = 60 (pre-registered). Base = bge.
- **cap2**: Run 6b: bge + at most 2 chunks per version_group in the results. Base = bge.
- **rerank30**: Run 7: bge + cross-encoder reranker over the top 30. Base = bge.
- **rerank100**: Run 7b: bge + cross-encoder reranker over the top 100. Base = bge.
- **twostage**: Run 12: two-stage search. Top 3 documents by best bge chunk, then cross-encoder over all their chunks. Base = bge.

**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes zero; – = no detectable difference. Verdicts use the CLUSTER interval (first bracket); the plain per-question interval is shown for context only.

## Paired differences from baseline

| run | Δ MAIN chunk R@5 (overall) | Δ chunk R@5 (non_outdated, guardrail) | Δ fact_stale (by rank, both found) | Δ stale doc-level (by rank) | Δ fact_found (outdated, guardrail) |
|---|---|---|---|---|---|
| baseline |  |  |  |  |  |
| bge | +0.052 [-0.051, 0.155] – (plain [-0.040, 0.147]; 26/18, n=126, 75 clusters) | +0.045 [-0.070, 0.146] – (plain [-0.059, 0.139]; 21/15, n=101, 61 clusters) | +0.200 [-0.167, 0.600] – (plain [-0.200, 0.600]; 1/3, n=10, 8 clusters) | +0.091 [-0.250, 0.429] – (plain [-0.182, 0.364]; 5/7, n=22, 19 clusters) | +0.200 [-0.040, 0.444] – (plain [0.000, 0.440]; 7/2, n=25, 22 clusters) |
| bge_prefix | +0.107 [0.009, 0.204] ✅ (plain [0.020, 0.198]; 28/13, n=126, 75 clusters) | +0.094 [-0.019, 0.192] – (plain [0.000, 0.188]; 21/10, n=101, 61 clusters) | +0.000 [-0.364, 0.334] – (plain [-0.364, 0.364]; 2/2, n=11, 9 clusters) | +0.048 [-0.273, 0.348] – (plain [-0.238, 0.333]; 4/5, n=21, 18 clusters) | +0.240 [0.038, 0.465] ✅ (plain [0.040, 0.440]; 7/1, n=25, 22 clusters) |
| hybrid | +0.187 [0.094, 0.283] ✅ (plain [0.103, 0.278]; 31/7, n=126, 75 clusters) | +0.153 [0.049, 0.252] ✅ (plain [0.054, 0.252]; 23/7, n=101, 61 clusters) | +0.167 [-0.154, 0.462] – (plain [-0.167, 0.500]; 1/3, n=12, 10 clusters) | +0.091 [-0.200, 0.360] – (plain [-0.182, 0.364]; 4/6, n=22, 19 clusters) | +0.440 [0.227, 0.652] ✅ (plain [0.240, 0.640]; 11/0, n=25, 22 clusters) |
| cap2 | +0.004 [-0.104, 0.109] – (plain [-0.095, 0.103]; 23/23, n=126, 75 clusters) | -0.025 [-0.134, 0.086] – (plain [-0.129, 0.074]; 17/20, n=101, 61 clusters) | +0.143 [-0.286, 0.571] – (plain [-0.286, 0.571]; 1/2, n=7, 7 clusters) | +0.091 [-0.250, 0.429] – (plain [-0.182, 0.364]; 5/7, n=22, 19 clusters) | +0.000 [-0.242, 0.261] – (plain [-0.240, 0.240]; 5/5, n=25, 22 clusters) |
| rerank30 | +0.175 [0.073, 0.273] ✅ (plain [0.087, 0.262]; 31/8, n=126, 75 clusters) | +0.158 [0.062, 0.258] ✅ (plain [0.069, 0.248]; 23/6, n=101, 61 clusters) | +0.100 [-0.333, 0.556] – (plain [-0.400, 0.600]; 3/4, n=10, 8 clusters) | -0.091 [-0.304, 0.136] – (plain [-0.318, 0.136]; 5/3, n=22, 19 clusters) | +0.200 [-0.040, 0.444] – (plain [0.000, 0.440]; 7/2, n=25, 22 clusters) |
| rerank100 | +0.202 [0.094, 0.305] ✅ (plain [0.115, 0.290]; 33/7, n=126, 75 clusters) | +0.193 [0.084, 0.301] ✅ (plain [0.104, 0.287]; 25/5, n=101, 61 clusters) | +0.091 [-0.300, 0.500] – (plain [-0.364, 0.545]; 3/4, n=11, 9 clusters) | -0.091 [-0.304, 0.136] – (plain [-0.318, 0.136]; 5/3, n=22, 19 clusters) | +0.320 [0.091, 0.556] ✅ (plain [0.120, 0.520]; 9/1, n=25, 22 clusters) |
| twostage | +0.119 [0.011, 0.219] ✅ (plain [0.028, 0.214]; 28/12, n=126, 75 clusters) | +0.139 [0.039, 0.231] ✅ (plain [0.045, 0.228]; 22/7, n=101, 61 clusters) | +0.000 [-0.625, 0.625] – (plain [-0.625, 0.625]; 3/3, n=8, 8 clusters) | -0.118 [-0.412, 0.176] – (plain [-0.412, 0.176]; 4/2, n=17, 16 clusters) | +0.240 [-0.083, 0.545] – (plain [-0.040, 0.520]; 10/4, n=25, 22 clusters) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better. stale and fact_stale are decided by RANK for every run (Amendment 4a), so all runs share one scale; tie-tolerance variants are a secondary detail for cosine runs only.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| baseline | 0.496 [0.40, 0.59] | 0.530 [0.43, 0.63] | 0.356 [0.28, 0.43] | 0.734 [0.65, 0.81] | 0.698 | 0.806 |
| bge | 0.548 [0.46, 0.64] | 0.574 [0.47, 0.66] | 0.398 [0.33, 0.47] | 0.798 [0.72, 0.88] | 0.786 | 0.873 |
| bge_prefix | 0.603 [0.51, 0.69] | 0.624 [0.52, 0.71] | 0.488 [0.40, 0.58] | 0.786 [0.71, 0.86] | 0.837 | 0.897 |
| hybrid | 0.682 [0.59, 0.77] | 0.683 [0.59, 0.77] | 0.524 [0.44, 0.60] | 0.905 [0.84, 0.96] | 0.901 | 0.944 |
| cap2 | 0.500 [0.42, 0.58] | 0.505 [0.41, 0.59] | 0.368 [0.29, 0.44] | 0.833 [0.76, 0.90] | 0.587 | 0.607 |
| rerank30 | 0.671 [0.58, 0.76] | 0.688 [0.60, 0.77] | 0.580 [0.49, 0.67] | 0.841 [0.77, 0.91] | 0.786 | 0.873 |
| rerank100 | 0.698 [0.60, 0.78] | 0.723 [0.63, 0.80] | 0.597 [0.51, 0.68] | 0.877 [0.81, 0.94] | 0.806 | 0.873 |
| twostage | 0.615 [0.53, 0.70] | 0.668 [0.57, 0.76] | 0.538 [0.45, 0.62] | 0.746 [0.66, 0.83] | 0.750 | 0.758 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) | secondary: fact_stale tol 0.001 / 0.005 / 0.01 (cosine only) |
|---|---|---|---|
| baseline | 0.667 [0.38, 0.91] | 0.480 [0.27, 0.69] | 0.417 / 0.458 / 0.500 |
| bge | 0.765 [0.58, 0.94] | 0.680 [0.48, 0.85] | 0.676 / 0.529 / 0.529 |
| bge_prefix | 0.611 [0.39, 0.81] | 0.720 [0.52, 0.88] | 0.556 / 0.472 / 0.500 |
| hybrid | 0.739 [0.55, 0.91] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| cap2 | 0.917 [0.75, 1.00] | 0.480 [0.31, 0.66] | 0.792 / 0.542 / 0.542 |
| rerank30 | 0.647 [0.44, 0.87] | 0.680 [0.48, 0.85] | n/a / n/a / n/a |
| rerank100 | 0.650 [0.45, 0.83] | 0.800 [0.62, 0.96] | n/a / n/a / n/a |
| twostage | 0.611 [0.39, 0.82] | 0.720 [0.54, 0.91] | n/a / n/a / n/a |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| baseline | 2468 | 3.7 | 8.5 | 46.7 | 159/159 |
| bge | 2468 | 3.7 | 10.9 | 0.0 | 159/159 |
| bge_prefix | 2468 | 3.7 | 10.4 | 1.1 | 159/159 |
| hybrid | 2468 | 3.7 | 18.6 | 0.0 | 159/159 |
| cap2 | 2468 | 3.7 | 10.3 | 0.0 | 159/159 |
| rerank30 | 2468 | 3.7 | 233.0 | 0.0 | 159/159 |
| rerank100 | 2468 | 3.7 | 716.0 | 0.0 | 159/159 |
| twostage | 2468 | 3.7 | 292.3 | 0.0 | 159/159 |

## Replication (frozen groups in eval/replication_groups.json)

An effect replicates if it has the same sign on the new questions; it is confirmed only if the combined interval excludes zero.

| run | Δ chunk R@5 (original, n=66) | Δ chunk R@5 (new only, n=60) | Δ chunk R@5 (combined, n=126) |
|---|---|---|---|
| bge | +0.098 [-0.025, 0.218] – (plain [-0.015, 0.212]; 13/5, n=66, 41 clusters) | +0.000 [-0.155, 0.152] – (plain [-0.150, 0.150]; 13/13, n=60, 36 clusters) | +0.052 [-0.051, 0.155] – (plain [-0.040, 0.147]; 26/18, n=126, 75 clusters) |
| bge_prefix | +0.129 [-0.008, 0.257] – (plain [0.015, 0.258]; 14/5, n=66, 41 clusters) | +0.083 [-0.056, 0.228] – (plain [-0.058, 0.217]; 14/8, n=60, 36 clusters) | +0.107 [0.009, 0.204] ✅ (plain [0.020, 0.198]; 28/13, n=126, 75 clusters) |
| hybrid | +0.220 [0.092, 0.353] ✅ (plain [0.121, 0.326]; 16/1, n=66, 41 clusters) | +0.150 [0.014, 0.284] ✅ (plain [0.008, 0.292]; 15/6, n=60, 36 clusters) | +0.187 [0.094, 0.283] ✅ (plain [0.103, 0.278]; 31/7, n=126, 75 clusters) |
| cap2 | +0.061 [-0.078, 0.192] – (plain [-0.061, 0.182]; 12/7, n=66, 41 clusters) | -0.058 [-0.208, 0.094] – (plain [-0.217, 0.092]; 11/16, n=60, 36 clusters) | +0.004 [-0.104, 0.109] – (plain [-0.095, 0.103]; 23/23, n=126, 75 clusters) |
| rerank30 | +0.205 [0.054, 0.352] ✅ (plain [0.091, 0.326]; 18/3, n=66, 41 clusters) | +0.142 [0.019, 0.273] ✅ (plain [0.017, 0.275]; 13/5, n=60, 36 clusters) | +0.175 [0.073, 0.273] ✅ (plain [0.087, 0.262]; 31/8, n=126, 75 clusters) |
| rerank100 | +0.212 [0.054, 0.364] ✅ (plain [0.091, 0.333]; 18/3, n=66, 41 clusters) | +0.192 [0.062, 0.339] ✅ (plain [0.075, 0.325]; 15/4, n=60, 36 clusters) | +0.202 [0.094, 0.305] ✅ (plain [0.115, 0.290]; 33/7, n=126, 75 clusters) |
| twostage | +0.136 [-0.016, 0.270] – (plain [0.015, 0.265]; 15/5, n=66, 41 clusters) | +0.100 [-0.038, 0.237] – (plain [-0.033, 0.233]; 13/7, n=60, 36 clusters) | +0.119 [0.011, 0.219] ✅ (plain [0.028, 0.214]; 28/12, n=126, 75 clusters) |

## chunk R@5 by question_type (`overall` questions)

| run | compound (n=7) | exact_term (n=7) | lookup (n=42) | multi_doc (n=15) | outdated_version (n=25) | paraphrase (n=30) |
|---|---|---|---|---|---|---|
| baseline | 0.429 | 0.857 | 0.524 | 0.567 | 0.360 | 0.467 |
| bge | 0.357 | 0.857 | 0.714 | 0.700 | 0.440 | 0.300 |
| bge_prefix | 0.429 | 0.857 | 0.762 | 0.667 | 0.520 | 0.400 |
| hybrid | 0.429 | 0.857 | 0.857 | 0.667 | 0.680 | 0.467 |
| cap2 | 0.357 | 0.714 | 0.619 | 0.567 | 0.480 | 0.300 |
| rerank30 | 0.286 | 0.714 | 0.881 | 0.767 | 0.600 | 0.467 |
| rerank100 | 0.357 | 0.714 | 0.929 | 0.767 | 0.600 | 0.500 |
| twostage | 0.429 | 0.857 | 0.881 | 0.633 | 0.400 | 0.400 |

## chunk R@5 by doc_group (`overall` questions)

| run | finance (n=25) | hiring (n=6) | legal (n=1) | mixed (n=4) | pdf (n=27) | people-policies (n=7) | security (n=24) | support (n=5) | total-rewards (n=27) |
|---|---|---|---|---|---|---|---|---|---|
| baseline | 0.360 | 0.167 | 1.000 | 0.375 | 0.667 | 0.286 | 0.375 | 0.200 | 0.741 |
| bge | 0.440 | 0.333 | 1.000 | 0.375 | 0.722 | 0.286 | 0.521 | 0.000 | 0.722 |
| bge_prefix | 0.480 | 0.333 | 1.000 | 0.375 | 0.796 | 0.286 | 0.604 | 0.200 | 0.759 |
| hybrid | 0.640 | 0.833 | 1.000 | 0.375 | 0.648 | 0.286 | 0.688 | 0.400 | 0.907 |
| cap2 | 0.440 | 0.333 | 1.000 | 0.375 | 0.537 | 0.286 | 0.562 | 0.000 | 0.648 |
| rerank30 | 0.600 | 0.667 | 1.000 | 0.375 | 0.796 | 0.286 | 0.646 | 0.400 | 0.815 |
| rerank100 | 0.640 | 0.667 | 1.000 | 0.375 | 0.815 | 0.286 | 0.667 | 0.400 | 0.870 |
| twostage | 0.560 | 0.500 | 1.000 | 0.375 | 0.815 | 0.286 | 0.562 | 0.000 | 0.759 |
