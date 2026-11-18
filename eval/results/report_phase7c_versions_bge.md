# Report: phase7c_versions_bge (reference: bge, tune split)

- **bge**: Run 5: bge-small instead of MiniLM. Reads 512 tokens, so 500-token chunks are not truncated.
- **bge_v8**: Run 8: exclude superseded versions before search. Base = bge (Amendment 4).
- **bge_v8b**: Run 8b: exclude legacy documents before search. Base = bge (Amendment 4).
- **bge_v9w10**: Run 9: date-aware rerank, w = 0.1. Base = bge (Amendment 4).
- **bge_v9w25**: Run 9: date-aware rerank, w = 0.25. Base = bge (Amendment 4).
- **bge_v9w50**: Run 9: date-aware rerank, w = 0.5. Base = bge (Amendment 4).
- **bge_v9b**: Run 9b: version swap (superseded chunk -> current version's most similar chunk). Base = bge (Amendment 4).

**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes zero; – = no detectable difference. Verdicts use the CLUSTER interval (first bracket); the plain per-question interval is shown for context only.

## Paired differences from bge

| run | Δ MAIN chunk R@5 (overall) | Δ chunk R@5 (non_outdated, guardrail) | Δ fact_stale (by rank, both found) | Δ stale doc-level (by rank) | Δ fact_found (outdated, guardrail) | Δ history chunk R@5 (guardrail) |
|---|---|---|---|---|---|---|
| bge |  |  |  |  |  |  |
| bge_v8 | +0.040 [0.008, 0.077] ✅ (plain [0.008, 0.079]; 5/0, n=126, 75 clusters) | +0.030 [0.000, 0.070] – (plain [0.000, 0.069]; 3/0, n=101, 61 clusters) | -0.765 [-0.938, -0.579] ✅ (plain [-0.941, -0.529]; 13/0, n=17, 14 clusters) | -0.696 [-0.880, -0.500] ✅ (plain [-0.870, -0.478]; 16/0, n=23, 20 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | -0.600 [-0.900, -0.300] ❌ (plain [-0.900, -0.300]; 0/6, n=10, 10 clusters) |
| bge_v8b | +0.008 [0.000, 0.026] – (plain [0.000, 0.024]; 1/0, n=126, 75 clusters) | +0.010 [0.000, 0.033] – (plain [0.000, 0.030]; 1/0, n=101, 61 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=17, 14 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=23, 20 clusters) | +0.040 [0.000, 0.130] – (plain [0.000, 0.120]; 1/0, n=25, 22 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=10, 10 clusters) |
| bge_v9w10 | -0.004 [-0.014, 0.000] – (plain [-0.012, 0.000]; 0/1, n=126, 75 clusters) | -0.005 [-0.017, 0.000] – (plain [-0.015, 0.000]; 0/1, n=101, 61 clusters) | -0.588 [-0.765, -0.400] ✅ (plain [-0.824, -0.353]; 10/0, n=17, 14 clusters) | -0.609 [-0.818, -0.400] ✅ (plain [-0.783, -0.391]; 14/0, n=23, 20 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=10, 10 clusters) |
| bge_v9w25 | +0.012 [-0.018, 0.049] – (plain [-0.016, 0.044]; 3/3, n=126, 75 clusters) | +0.015 [-0.021, 0.064] – (plain [-0.020, 0.054]; 3/3, n=101, 61 clusters) | -0.647 [-0.824, -0.471] ✅ (plain [-0.882, -0.412]; 11/0, n=17, 14 clusters) | -0.652 [-0.864, -0.454] ✅ (plain [-0.826, -0.435]; 15/0, n=23, 20 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | -0.200 [-0.500, 0.000] – (plain [-0.500, 0.000]; 0/2, n=10, 10 clusters) |
| bge_v9w50 | +0.016 [-0.036, 0.069] – (plain [-0.032, 0.067]; 7/7, n=126, 75 clusters) | +0.000 [-0.059, 0.066] – (plain [-0.054, 0.059]; 5/7, n=101, 61 clusters) | -0.765 [-0.938, -0.579] ✅ (plain [-0.941, -0.529]; 13/0, n=17, 14 clusters) | -0.696 [-0.880, -0.500] ✅ (plain [-0.870, -0.478]; 16/0, n=23, 20 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | -0.600 [-0.900, -0.300] ❌ (plain [-0.900, -0.300]; 0/6, n=10, 10 clusters) |
| bge_v9b | +0.040 [0.008, 0.077] ✅ (plain [0.008, 0.079]; 5/0, n=126, 75 clusters) | +0.030 [0.000, 0.070] – (plain [0.000, 0.069]; 3/0, n=101, 61 clusters) | -0.765 [-0.938, -0.579] ✅ (plain [-0.941, -0.529]; 13/0, n=17, 14 clusters) | -0.696 [-0.880, -0.500] ✅ (plain [-0.870, -0.478]; 16/0, n=23, 20 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | -0.600 [-0.900, -0.300] ❌ (plain [-0.900, -0.300]; 0/6, n=10, 10 clusters) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better. stale and fact_stale are decided by RANK for every run (Amendment 3b), so all runs share one scale; tie-tolerance variants are a secondary detail for cosine runs only.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| bge | 0.548 [0.46, 0.64] | 0.574 [0.47, 0.66] | 0.398 [0.33, 0.47] | 0.798 [0.72, 0.88] | 0.786 | 0.873 |
| bge_v8 | 0.587 [0.50, 0.67] | 0.604 [0.50, 0.70] | 0.449 [0.37, 0.52] | 0.821 [0.75, 0.89] | 0.798 | 0.885 |
| bge_v8b | 0.556 [0.47, 0.64] | 0.584 [0.48, 0.67] | 0.401 [0.33, 0.47] | 0.814 [0.74, 0.89] | 0.794 | 0.881 |
| bge_v9w10 | 0.544 [0.46, 0.63] | 0.569 [0.47, 0.66] | 0.438 [0.36, 0.51] | 0.794 [0.71, 0.87] | 0.786 | 0.873 |
| bge_v9w25 | 0.559 [0.48, 0.64] | 0.589 [0.49, 0.68] | 0.443 [0.36, 0.51] | 0.802 [0.73, 0.87] | 0.782 | 0.873 |
| bge_v9w50 | 0.564 [0.48, 0.65] | 0.574 [0.48, 0.66] | 0.400 [0.33, 0.47] | 0.782 [0.71, 0.86] | 0.778 | 0.873 |
| bge_v9b | 0.587 [0.50, 0.67] | 0.604 [0.50, 0.70] | 0.450 [0.38, 0.52] | 0.821 [0.75, 0.89] | 0.798 | 0.881 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) | secondary: fact_stale tol 0.001 / 0.005 / 0.01 (cosine only) |
|---|---|---|---|
| bge | 0.765 [0.58, 0.94] | 0.680 [0.48, 0.85] | 0.676 / 0.529 / 0.529 |
| bge_v8 | 0.000 [0.00, 0.00] | 0.680 [0.48, 0.85] | 0.000 / 0.000 / 0.000 |
| bge_v8b | 0.778 [0.60, 0.94] | 0.720 [0.52, 0.88] | 0.667 / 0.528 / 0.528 |
| bge_v9w10 | 0.176 [0.00, 0.38] | 0.680 [0.48, 0.85] | 0.176 / 0.265 / 0.382 |
| bge_v9w25 | 0.118 [0.00, 0.29] | 0.680 [0.48, 0.85] | 0.118 / 0.088 / 0.088 |
| bge_v9w50 | 0.000 [0.00, 0.00] | 0.680 [0.48, 0.85] | 0.000 / 0.000 / 0.000 |
| bge_v9b | 0.000 [0.00, 0.00] | 0.680 [0.48, 0.85] | 0.000 / 0.000 / 0.000 |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| bge | 2468 | 3.7 | 10.9 | 0.0 | 159/159 |
| bge_v8 | 2468 | 3.7 | 24.0 | 0.0 | 159/159 |
| bge_v8b | 2468 | 3.7 | 19.6 | 0.0 | 159/159 |
| bge_v9w10 | 2468 | 3.7 | 11.1 | 0.0 | 159/159 |
| bge_v9w25 | 2468 | 3.7 | 11.2 | 0.0 | 159/159 |
| bge_v9w50 | 2468 | 3.7 | 11.2 | 0.0 | 159/159 |
| bge_v9b | 2468 | 3.7 | 17.7 | 0.0 | 159/159 |

## Replication (frozen groups in eval/replication_groups.json)

An effect replicates if it has the same sign on the new questions; it is confirmed only if the combined interval excludes zero.

| run | Δ chunk R@5 (original, n=66) | Δ chunk R@5 (new only, n=60) | Δ chunk R@5 (combined, n=126) |
|---|---|---|---|
| bge_v8 | +0.061 [0.015, 0.116] ✅ (plain [0.015, 0.121]; 4/0, n=66, 41 clusters) | +0.017 [0.000, 0.060] – (plain [0.000, 0.050]; 1/0, n=60, 36 clusters) | +0.040 [0.008, 0.077] ✅ (plain [0.008, 0.079]; 5/0, n=126, 75 clusters) |
| bge_v8b | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=66, 41 clusters) | +0.017 [0.000, 0.056] – (plain [0.000, 0.050]; 1/0, n=60, 36 clusters) | +0.008 [0.000, 0.026] – (plain [0.000, 0.024]; 1/0, n=126, 75 clusters) |
| bge_v9w10 | -0.008 [-0.024, 0.000] – (plain [-0.023, 0.000]; 0/1, n=66, 41 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=60, 36 clusters) | -0.004 [-0.014, 0.000] – (plain [-0.012, 0.000]; 0/1, n=126, 75 clusters) |
| bge_v9w25 | +0.023 [-0.015, 0.071] – (plain [-0.015, 0.076]; 2/1, n=66, 41 clusters) | +0.000 [-0.043, 0.055] – (plain [-0.033, 0.042]; 1/2, n=60, 36 clusters) | +0.012 [-0.018, 0.049] – (plain [-0.016, 0.044]; 3/3, n=126, 75 clusters) |
| bge_v9w50 | +0.023 [-0.050, 0.094] – (plain [-0.053, 0.098]; 4/3, n=66, 41 clusters) | +0.008 [-0.063, 0.092] – (plain [-0.059, 0.083]; 3/4, n=60, 36 clusters) | +0.016 [-0.036, 0.069] – (plain [-0.032, 0.067]; 7/7, n=126, 75 clusters) |
| bge_v9b | +0.061 [0.015, 0.116] ✅ (plain [0.015, 0.121]; 4/0, n=66, 41 clusters) | +0.017 [0.000, 0.060] – (plain [0.000, 0.050]; 1/0, n=60, 36 clusters) | +0.040 [0.008, 0.077] ✅ (plain [0.008, 0.079]; 5/0, n=126, 75 clusters) |

## chunk R@5 by question_type (`overall` questions)

| run | compound (n=7) | exact_term (n=7) | lookup (n=42) | multi_doc (n=15) | outdated_version (n=25) | paraphrase (n=30) |
|---|---|---|---|---|---|---|
| bge | 0.357 | 0.857 | 0.714 | 0.700 | 0.440 | 0.300 |
| bge_v8 | 0.357 | 0.857 | 0.738 | 0.700 | 0.520 | 0.367 |
| bge_v8b | 0.357 | 0.857 | 0.714 | 0.700 | 0.440 | 0.333 |
| bge_v9w10 | 0.357 | 0.857 | 0.714 | 0.667 | 0.440 | 0.300 |
| bge_v9w25 | 0.357 | 0.857 | 0.738 | 0.600 | 0.440 | 0.367 |
| bge_v9w50 | 0.286 | 0.857 | 0.690 | 0.533 | 0.520 | 0.433 |
| bge_v9b | 0.357 | 0.857 | 0.738 | 0.700 | 0.520 | 0.367 |

## chunk R@5 by doc_group (`overall` questions)

| run | finance (n=25) | hiring (n=6) | legal (n=1) | mixed (n=4) | pdf (n=27) | people-policies (n=7) | security (n=24) | support (n=5) | total-rewards (n=27) |
|---|---|---|---|---|---|---|---|---|---|
| bge | 0.440 | 0.333 | 1.000 | 0.375 | 0.722 | 0.286 | 0.521 | 0.000 | 0.722 |
| bge_v8 | 0.480 | 0.333 | 1.000 | 0.375 | 0.722 | 0.429 | 0.604 | 0.000 | 0.759 |
| bge_v8b | 0.480 | 0.333 | 1.000 | 0.375 | 0.722 | 0.286 | 0.521 | 0.000 | 0.722 |
| bge_v9w10 | 0.440 | 0.333 | 1.000 | 0.250 | 0.722 | 0.286 | 0.521 | 0.000 | 0.722 |
| bge_v9w25 | 0.440 | 0.333 | 1.000 | 0.250 | 0.685 | 0.429 | 0.562 | 0.000 | 0.759 |
| bge_v9w50 | 0.520 | 0.333 | 1.000 | 0.125 | 0.630 | 0.429 | 0.604 | 0.000 | 0.741 |
| bge_v9b | 0.480 | 0.333 | 1.000 | 0.375 | 0.722 | 0.429 | 0.604 | 0.000 | 0.759 |
