# Report: phase7b_step2_vs_base (reference: bge, tune split)

- **bge**: Run 5: bge-small instead of MiniLM. Reads 512 tokens, so 500-token chunks are not truncated.
- **bge_prefix**: Run 6p: bge + title/section prefix. Base = bge; only change: prefix on every chunk (truncation vs bge's 512 limit reported).
- **hybrid**: Run 6: bge + BM25 hybrid merged with reciprocal rank fusion, k = 60 (pre-registered). Base = bge.
- **hybrid_k10**: Run 6 EXPLORATORY: hybrid with RRF k = 10 (not pre-registered).
- **hybrid_k100**: Run 6 EXPLORATORY: hybrid with RRF k = 100 (not pre-registered).
- **cap2**: Run 6b: bge + at most 2 chunks per version_group in the results. Base = bge.
- **rerank30**: Run 7: bge + cross-encoder reranker over the top 30. Base = bge.
- **rerank100**: Run 7b: bge + cross-encoder reranker over the top 100. Base = bge.
- **twostage**: Run 12: two-stage search. Top 3 documents by best bge chunk, then cross-encoder over all their chunks. Base = bge.

**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes zero; – = no detectable difference. Verdicts use the CLUSTER interval (first bracket); the plain per-question interval is shown for context only.

## Paired differences from bge

| run | Δ MAIN chunk R@5 (overall) | Δ chunk R@5 (non_outdated, guardrail) | Δ fact_stale (by rank, both found) | Δ stale doc-level (by rank) | Δ fact_found (outdated, guardrail) |
|---|---|---|---|---|---|
| bge |  |  |  |  |  |
| bge_prefix | +0.056 [-0.009, 0.125] – (plain [-0.004, 0.119]; 14/7, n=126, 75 clusters) | +0.050 [-0.015, 0.127] – (plain [-0.015, 0.119]; 11/6, n=101, 61 clusters) | -0.176 [-0.400, 0.000] – (plain [-0.353, 0.000]; 3/0, n=17, 14 clusters) | -0.091 [-0.350, 0.150] – (plain [-0.318, 0.182]; 5/3, n=22, 19 clusters) | +0.040 [0.000, 0.130] – (plain [0.000, 0.120]; 1/0, n=25, 22 clusters) |
| hybrid | +0.135 [0.055, 0.221] ✅ (plain [0.063, 0.202]; 24/7, n=126, 75 clusters) | +0.109 [0.022, 0.202] ✅ (plain [0.035, 0.188]; 18/7, n=101, 61 clusters) | +0.059 [-0.143, 0.222] – (plain [-0.118, 0.294]; 1/2, n=17, 14 clusters) | +0.000 [-0.238, 0.231] – (plain [-0.217, 0.217]; 3/3, n=23, 20 clusters) | +0.240 [0.077, 0.435] ✅ (plain [0.080, 0.400]; 6/0, n=25, 22 clusters) |
| hybrid_k10 | +0.131 [0.052, 0.217] ✅ (plain [0.063, 0.202]; 24/7, n=126, 75 clusters) | +0.104 [0.019, 0.197] ✅ (plain [0.035, 0.183]; 18/7, n=101, 61 clusters) | +0.059 [-0.143, 0.222] – (plain [-0.118, 0.294]; 1/2, n=17, 14 clusters) | +0.000 [-0.238, 0.231] – (plain [-0.217, 0.217]; 3/3, n=23, 20 clusters) | +0.240 [0.077, 0.435] ✅ (plain [0.080, 0.400]; 6/0, n=25, 22 clusters) |
| hybrid_k100 | +0.135 [0.055, 0.221] ✅ (plain [0.063, 0.202]; 24/7, n=126, 75 clusters) | +0.109 [0.022, 0.202] ✅ (plain [0.035, 0.188]; 18/7, n=101, 61 clusters) | +0.059 [-0.143, 0.222] – (plain [-0.118, 0.294]; 1/2, n=17, 14 clusters) | +0.000 [-0.238, 0.231] – (plain [-0.217, 0.217]; 3/3, n=23, 20 clusters) | +0.240 [0.077, 0.435] ✅ (plain [0.080, 0.400]; 6/0, n=25, 22 clusters) |
| cap2 | -0.048 [-0.094, 0.004] – (plain [-0.099, 0.000]; 3/11, n=126, 75 clusters) | -0.069 [-0.118, -0.018] ❌ (plain [-0.124, -0.020]; 1/10, n=101, 61 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=12, 12 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=23, 20 clusters) | -0.200 [-0.333, -0.083] ❌ (plain [-0.360, -0.040]; 0/5, n=25, 22 clusters) |
| rerank30 | +0.123 [0.050, 0.206] ✅ (plain [0.052, 0.198]; 23/7, n=126, 75 clusters) | +0.114 [0.040, 0.203] ✅ (plain [0.045, 0.188]; 17/5, n=101, 61 clusters) | -0.118 [-0.438, 0.211] – (plain [-0.412, 0.176]; 5/3, n=17, 14 clusters) | -0.174 [-0.455, 0.125] – (plain [-0.435, 0.130]; 8/4, n=23, 20 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) |
| rerank100 | +0.151 [0.066, 0.237] ✅ (plain [0.075, 0.234]; 27/8, n=126, 75 clusters) | +0.149 [0.062, 0.247] ✅ (plain [0.069, 0.233]; 21/6, n=101, 61 clusters) | -0.118 [-0.438, 0.211] – (plain [-0.412, 0.176]; 5/3, n=17, 14 clusters) | -0.174 [-0.455, 0.125] – (plain [-0.435, 0.130]; 8/4, n=23, 20 clusters) | +0.120 [0.000, 0.269] – (plain [0.000, 0.240]; 3/0, n=25, 22 clusters) |
| twostage | +0.067 [0.004, 0.136] ✅ (plain [0.004, 0.139]; 16/8, n=126, 75 clusters) | +0.094 [0.024, 0.178] ✅ (plain [0.030, 0.163]; 14/5, n=101, 61 clusters) | -0.214 [-0.571, 0.143] – (plain [-0.571, 0.143]; 5/2, n=14, 13 clusters) | -0.333 [-0.588, -0.059] ✅ (plain [-0.611, -0.056]; 7/1, n=18, 17 clusters) | +0.040 [-0.185, 0.273] – (plain [-0.160, 0.240]; 4/3, n=25, 22 clusters) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better. stale and fact_stale are decided by RANK for every run (Amendment 4a), so all runs share one scale; tie-tolerance variants are a secondary detail for cosine runs only.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| bge | 0.548 [0.46, 0.64] | 0.574 [0.47, 0.66] | 0.398 [0.33, 0.47] | 0.798 [0.72, 0.88] | 0.786 | 0.873 |
| bge_prefix | 0.603 [0.51, 0.69] | 0.624 [0.52, 0.71] | 0.488 [0.40, 0.58] | 0.786 [0.71, 0.86] | 0.837 | 0.897 |
| hybrid | 0.682 [0.59, 0.77] | 0.683 [0.59, 0.77] | 0.524 [0.44, 0.60] | 0.905 [0.84, 0.96] | 0.901 | 0.944 |
| hybrid_k10 | 0.679 [0.59, 0.76] | 0.678 [0.58, 0.76] | 0.517 [0.44, 0.59] | 0.905 [0.84, 0.96] | 0.889 | 0.944 |
| hybrid_k100 | 0.682 [0.59, 0.77] | 0.683 [0.59, 0.77] | 0.524 [0.44, 0.60] | 0.905 [0.84, 0.96] | 0.893 | 0.944 |
| cap2 | 0.500 [0.42, 0.58] | 0.505 [0.41, 0.59] | 0.368 [0.29, 0.44] | 0.833 [0.76, 0.90] | 0.587 | 0.607 |
| rerank30 | 0.671 [0.58, 0.76] | 0.688 [0.60, 0.77] | 0.580 [0.49, 0.67] | 0.841 [0.77, 0.91] | 0.786 | 0.873 |
| rerank100 | 0.698 [0.60, 0.78] | 0.723 [0.63, 0.80] | 0.597 [0.51, 0.68] | 0.877 [0.81, 0.94] | 0.806 | 0.873 |
| twostage | 0.615 [0.53, 0.70] | 0.668 [0.57, 0.76] | 0.538 [0.45, 0.62] | 0.746 [0.66, 0.83] | 0.750 | 0.758 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) | secondary: fact_stale tol 0.001 / 0.005 / 0.01 (cosine only) |
|---|---|---|---|
| bge | 0.765 [0.58, 0.94] | 0.680 [0.48, 0.85] | 0.676 / 0.529 / 0.529 |
| bge_prefix | 0.611 [0.39, 0.81] | 0.720 [0.52, 0.88] | 0.556 / 0.472 / 0.500 |
| hybrid | 0.739 [0.55, 0.91] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| hybrid_k10 | 0.739 [0.55, 0.91] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| hybrid_k100 | 0.739 [0.55, 0.91] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| cap2 | 0.917 [0.75, 1.00] | 0.480 [0.31, 0.66] | 0.792 / 0.542 / 0.542 |
| rerank30 | 0.647 [0.44, 0.87] | 0.680 [0.48, 0.85] | n/a / n/a / n/a |
| rerank100 | 0.650 [0.45, 0.83] | 0.800 [0.62, 0.96] | n/a / n/a / n/a |
| twostage | 0.611 [0.39, 0.82] | 0.720 [0.54, 0.91] | n/a / n/a / n/a |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| bge | 2468 | 3.7 | 10.9 | 0.0 | 159/159 |
| bge_prefix | 2468 | 3.7 | 10.4 | 1.1 | 159/159 |
| hybrid | 2468 | 3.7 | 18.6 | 0.0 | 159/159 |
| hybrid_k10 | 2468 | 3.7 | 18.6 | 0.0 | 159/159 |
| hybrid_k100 | 2468 | 3.7 | 18.4 | 0.0 | 159/159 |
| cap2 | 2468 | 3.7 | 10.3 | 0.0 | 159/159 |
| rerank30 | 2468 | 3.7 | 233.0 | 0.0 | 159/159 |
| rerank100 | 2468 | 3.7 | 716.0 | 0.0 | 159/159 |
| twostage | 2468 | 3.7 | 292.3 | 0.0 | 159/159 |

## Replication (frozen groups in eval/replication_groups.json)

An effect replicates if it has the same sign on the new questions; it is confirmed only if the combined interval excludes zero.

| run | Δ chunk R@5 (original, n=66) | Δ chunk R@5 (new only, n=60) | Δ chunk R@5 (combined, n=126) |
|---|---|---|---|
| bge_prefix | +0.030 [-0.031, 0.094] – (plain [-0.045, 0.114]; 5/4, n=66, 41 clusters) | +0.083 [-0.024, 0.202] – (plain [-0.008, 0.183]; 9/3, n=60, 36 clusters) | +0.056 [-0.009, 0.125] – (plain [-0.004, 0.119]; 14/7, n=126, 75 clusters) |
| hybrid | +0.121 [0.018, 0.224] ✅ (plain [0.038, 0.220]; 11/3, n=66, 41 clusters) | +0.150 [0.025, 0.279] ✅ (plain [0.042, 0.258]; 13/4, n=60, 36 clusters) | +0.135 [0.055, 0.221] ✅ (plain [0.063, 0.202]; 24/7, n=126, 75 clusters) |
| hybrid_k10 | +0.121 [0.016, 0.230] ✅ (plain [0.030, 0.220]; 11/3, n=66, 41 clusters) | +0.142 [0.019, 0.277] ✅ (plain [0.042, 0.250]; 13/4, n=60, 36 clusters) | +0.131 [0.052, 0.217] ✅ (plain [0.063, 0.202]; 24/7, n=126, 75 clusters) |
| hybrid_k100 | +0.121 [0.018, 0.224] ✅ (plain [0.038, 0.220]; 11/3, n=66, 41 clusters) | +0.150 [0.025, 0.279] ✅ (plain [0.042, 0.258]; 13/4, n=60, 36 clusters) | +0.135 [0.055, 0.221] ✅ (plain [0.063, 0.202]; 24/7, n=126, 75 clusters) |
| cap2 | -0.038 [-0.113, 0.033] – (plain [-0.114, 0.038]; 2/5, n=66, 41 clusters) | -0.058 [-0.127, 0.010] – (plain [-0.133, 0.008]; 1/6, n=60, 36 clusters) | -0.048 [-0.094, 0.004] – (plain [-0.099, 0.000]; 3/11, n=126, 75 clusters) |
| rerank30 | +0.106 [-0.016, 0.217] – (plain [0.000, 0.212]; 12/4, n=66, 41 clusters) | +0.142 [0.041, 0.263] ✅ (plain [0.050, 0.242]; 11/3, n=60, 36 clusters) | +0.123 [0.050, 0.206] ✅ (plain [0.052, 0.198]; 23/7, n=126, 75 clusters) |
| rerank100 | +0.114 [-0.016, 0.231] – (plain [0.008, 0.220]; 12/4, n=66, 41 clusters) | +0.192 [0.075, 0.325] ✅ (plain [0.092, 0.308]; 15/4, n=60, 36 clusters) | +0.151 [0.066, 0.237] ✅ (plain [0.075, 0.234]; 27/8, n=126, 75 clusters) |
| twostage | +0.038 [-0.052, 0.129] – (plain [-0.053, 0.136]; 7/5, n=66, 41 clusters) | +0.100 [0.008, 0.203] ✅ (plain [0.017, 0.192]; 9/3, n=60, 36 clusters) | +0.067 [0.004, 0.136] ✅ (plain [0.004, 0.139]; 16/8, n=126, 75 clusters) |

## chunk R@5 by question_type (`overall` questions)

| run | compound (n=7) | exact_term (n=7) | lookup (n=42) | multi_doc (n=15) | outdated_version (n=25) | paraphrase (n=30) |
|---|---|---|---|---|---|---|
| bge | 0.357 | 0.857 | 0.714 | 0.700 | 0.440 | 0.300 |
| bge_prefix | 0.429 | 0.857 | 0.762 | 0.667 | 0.520 | 0.400 |
| hybrid | 0.429 | 0.857 | 0.857 | 0.667 | 0.680 | 0.467 |
| hybrid_k10 | 0.500 | 0.857 | 0.857 | 0.667 | 0.680 | 0.433 |
| hybrid_k100 | 0.429 | 0.857 | 0.857 | 0.667 | 0.680 | 0.467 |
| cap2 | 0.357 | 0.714 | 0.619 | 0.567 | 0.480 | 0.300 |
| rerank30 | 0.286 | 0.714 | 0.881 | 0.767 | 0.600 | 0.467 |
| rerank100 | 0.357 | 0.714 | 0.929 | 0.767 | 0.600 | 0.500 |
| twostage | 0.429 | 0.857 | 0.881 | 0.633 | 0.400 | 0.400 |

## chunk R@5 by doc_group (`overall` questions)

| run | finance (n=25) | hiring (n=6) | legal (n=1) | mixed (n=4) | pdf (n=27) | people-policies (n=7) | security (n=24) | support (n=5) | total-rewards (n=27) |
|---|---|---|---|---|---|---|---|---|---|
| bge | 0.440 | 0.333 | 1.000 | 0.375 | 0.722 | 0.286 | 0.521 | 0.000 | 0.722 |
| bge_prefix | 0.480 | 0.333 | 1.000 | 0.375 | 0.796 | 0.286 | 0.604 | 0.200 | 0.759 |
| hybrid | 0.640 | 0.833 | 1.000 | 0.375 | 0.648 | 0.286 | 0.688 | 0.400 | 0.907 |
| hybrid_k10 | 0.640 | 0.667 | 1.000 | 0.500 | 0.648 | 0.286 | 0.688 | 0.400 | 0.907 |
| hybrid_k100 | 0.640 | 0.833 | 1.000 | 0.375 | 0.648 | 0.286 | 0.688 | 0.400 | 0.907 |
| cap2 | 0.440 | 0.333 | 1.000 | 0.375 | 0.537 | 0.286 | 0.562 | 0.000 | 0.648 |
| rerank30 | 0.600 | 0.667 | 1.000 | 0.375 | 0.796 | 0.286 | 0.646 | 0.400 | 0.815 |
| rerank100 | 0.640 | 0.667 | 1.000 | 0.375 | 0.815 | 0.286 | 0.667 | 0.400 | 0.870 |
| twostage | 0.560 | 0.500 | 1.000 | 0.375 | 0.815 | 0.286 | 0.562 | 0.000 | 0.759 |
