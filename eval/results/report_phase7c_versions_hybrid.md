# Report: phase7c_versions_hybrid (reference: hybrid, tune split)

- **hybrid**: Run 6: bge + BM25 hybrid merged with reciprocal rank fusion, k = 60 (pre-registered). Base = bge.
- **hybrid_v8**: Run 8: exclude superseded versions before search. Base = hybrid (Amendment 4).
- **hybrid_v8b**: Run 8b: exclude legacy documents before search. Base = hybrid (Amendment 4).
- **hybrid_v9w10**: Run 9: date-aware rerank, w = 0.1. Base = hybrid (Amendment 4).
- **hybrid_v9w25**: Run 9: date-aware rerank, w = 0.25. Base = hybrid (Amendment 4).
- **hybrid_v9w50**: Run 9: date-aware rerank, w = 0.5. Base = hybrid (Amendment 4).
- **hybrid_v9b**: Run 9b: version swap (superseded chunk -> current version's most similar chunk). Base = hybrid (Amendment 4).

**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes zero; – = no detectable difference. Verdicts use the CLUSTER interval (first bracket); the plain per-question interval is shown for context only.

## Paired differences from hybrid

| run | Δ MAIN chunk R@5 (overall) | Δ chunk R@5 (non_outdated, guardrail) | Δ fact_stale (by rank, both found) | Δ stale doc-level (by rank) | Δ fact_found (outdated, guardrail) | Δ history chunk R@5 (guardrail) |
|---|---|---|---|---|---|---|
| hybrid |  |  |  |  |  |  |
| hybrid_v8 | +0.008 [-0.026, 0.045] – (plain [-0.024, 0.040]; 3/2, n=126, 75 clusters) | +0.000 [-0.040, 0.040] – (plain [-0.040, 0.040]; 2/2, n=101, 61 clusters) | -0.739 [-0.913, -0.545] ✅ (plain [-0.913, -0.565]; 17/0, n=23, 20 clusters) | -0.667 [-0.857, -0.455] ✅ (plain [-0.833, -0.458]; 16/0, n=24, 21 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | -0.700 [-1.000, -0.400] ❌ (plain [-1.000, -0.400]; 0/7, n=10, 10 clusters) |
| hybrid_v8b | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=126, 75 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=101, 61 clusters) | +0.043 [0.000, 0.137] – (plain [0.000, 0.130]; 0/1, n=23, 20 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=24, 21 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=10, 10 clusters) |
| hybrid_v9w10 | +0.008 [0.000, 0.027] – (plain [0.000, 0.024]; 1/0, n=126, 75 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=101, 61 clusters) | -0.522 [-0.731, -0.286] ✅ (plain [-0.739, -0.348]; 12/0, n=23, 20 clusters) | -0.500 [-0.720, -0.273] ✅ (plain [-0.708, -0.292]; 12/0, n=24, 21 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=10, 10 clusters) |
| hybrid_v9w25 | +0.016 [-0.010, 0.051] – (plain [-0.016, 0.048]; 3/1, n=126, 75 clusters) | +0.010 [-0.022, 0.046] – (plain [-0.020, 0.050]; 2/1, n=101, 61 clusters) | -0.739 [-0.913, -0.545] ✅ (plain [-0.913, -0.565]; 17/0, n=23, 20 clusters) | -0.667 [-0.857, -0.455] ✅ (plain [-0.833, -0.458]; 16/0, n=24, 21 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | -0.200 [-0.500, 0.000] – (plain [-0.500, 0.000]; 0/2, n=10, 10 clusters) |
| hybrid_v9w50 | +0.012 [-0.029, 0.056] – (plain [-0.032, 0.056]; 5/3, n=126, 75 clusters) | -0.005 [-0.049, 0.041] – (plain [-0.050, 0.040]; 3/3, n=101, 61 clusters) | -0.739 [-0.913, -0.545] ✅ (plain [-0.913, -0.565]; 17/0, n=23, 20 clusters) | -0.667 [-0.857, -0.455] ✅ (plain [-0.833, -0.458]; 16/0, n=24, 21 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | -0.700 [-1.000, -0.400] ❌ (plain [-1.000, -0.400]; 0/7, n=10, 10 clusters) |
| hybrid_v9b | +0.032 [0.007, 0.069] ✅ (plain [0.008, 0.071]; 4/0, n=126, 75 clusters) | +0.020 [0.000, 0.053] – (plain [0.000, 0.050]; 2/0, n=101, 61 clusters) | -0.739 [-0.913, -0.545] ✅ (plain [-0.913, -0.565]; 17/0, n=23, 20 clusters) | -0.667 [-0.857, -0.455] ✅ (plain [-0.833, -0.458]; 16/0, n=24, 21 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=25, 22 clusters) | -0.700 [-1.000, -0.400] ❌ (plain [-1.000, -0.400]; 0/7, n=10, 10 clusters) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better. stale and fact_stale are decided by RANK for every run (Amendment 3b), so all runs share one scale; tie-tolerance variants are a secondary detail for cosine runs only.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| hybrid | 0.682 [0.59, 0.77] | 0.683 [0.59, 0.77] | 0.524 [0.44, 0.60] | 0.905 [0.84, 0.96] | 0.901 | 0.944 |
| hybrid_v8 | 0.691 [0.60, 0.77] | 0.683 [0.59, 0.77] | 0.578 [0.50, 0.65] | 0.897 [0.83, 0.95] | 0.913 | 0.968 |
| hybrid_v8b | 0.682 [0.59, 0.77] | 0.683 [0.59, 0.77] | 0.525 [0.44, 0.60] | 0.905 [0.84, 0.96] | 0.905 | 0.944 |
| hybrid_v9w10 | 0.691 [0.60, 0.77] | 0.683 [0.59, 0.77] | 0.557 [0.47, 0.63] | 0.905 [0.84, 0.96] | 0.901 | 0.944 |
| hybrid_v9w25 | 0.698 [0.62, 0.78] | 0.693 [0.61, 0.77] | 0.563 [0.48, 0.64] | 0.889 [0.82, 0.94] | 0.893 | 0.944 |
| hybrid_v9w50 | 0.694 [0.61, 0.77] | 0.678 [0.59, 0.76] | 0.509 [0.43, 0.59] | 0.893 [0.83, 0.95] | 0.889 | 0.944 |
| hybrid_v9b | 0.714 [0.63, 0.79] | 0.703 [0.62, 0.78] | 0.586 [0.50, 0.66] | 0.905 [0.84, 0.96] | 0.913 | 0.944 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) | secondary: fact_stale tol 0.001 / 0.005 / 0.01 (cosine only) |
|---|---|---|---|
| hybrid | 0.739 [0.55, 0.91] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| hybrid_v8 | 0.000 [0.00, 0.00] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| hybrid_v8b | 0.783 [0.59, 0.93] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| hybrid_v9w10 | 0.217 [0.07, 0.41] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| hybrid_v9w25 | 0.000 [0.00, 0.00] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| hybrid_v9w50 | 0.000 [0.00, 0.00] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |
| hybrid_v9b | 0.000 [0.00, 0.00] | 0.920 [0.80, 1.00] | n/a / n/a / n/a |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| hybrid | 2468 | 3.7 | 18.6 | 0.0 | 159/159 |
| hybrid_v8 | 2468 | 3.7 | 30.3 | 0.0 | 159/159 |
| hybrid_v8b | 2468 | 3.7 | 31.1 | 0.0 | 159/159 |
| hybrid_v9w10 | 2468 | 3.7 | 19.5 | 0.0 | 159/159 |
| hybrid_v9w25 | 2468 | 3.7 | 21.5 | 0.0 | 159/159 |
| hybrid_v9w50 | 2468 | 3.7 | 20.1 | 0.0 | 159/159 |
| hybrid_v9b | 2468 | 3.7 | 28.2 | 0.0 | 159/159 |

## Replication (frozen groups in eval/replication_groups.json)

An effect replicates if it has the same sign on the new questions; it is confirmed only if the combined interval excludes zero.

| run | Δ chunk R@5 (original, n=66) | Δ chunk R@5 (new only, n=60) | Δ chunk R@5 (combined, n=126) |
|---|---|---|---|
| hybrid_v8 | +0.045 [0.000, 0.104] – (plain [0.000, 0.106]; 3/0, n=66, 41 clusters) | -0.033 [-0.085, 0.000] – (plain [-0.083, 0.000]; 0/2, n=60, 36 clusters) | +0.008 [-0.026, 0.045] – (plain [-0.024, 0.040]; 3/2, n=126, 75 clusters) |
| hybrid_v8b | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=66, 41 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=60, 36 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=126, 75 clusters) |
| hybrid_v9w10 | +0.015 [0.000, 0.051] – (plain [0.000, 0.045]; 1/0, n=66, 41 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=60, 36 clusters) | +0.008 [0.000, 0.027] – (plain [0.000, 0.024]; 1/0, n=126, 75 clusters) |
| hybrid_v9w25 | +0.030 [-0.027, 0.092] – (plain [-0.030, 0.091]; 3/1, n=66, 41 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=60, 36 clusters) | +0.016 [-0.010, 0.051] – (plain [-0.016, 0.048]; 3/1, n=126, 75 clusters) |
| hybrid_v9w50 | +0.023 [-0.054, 0.108] – (plain [-0.053, 0.106]; 5/3, n=66, 41 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=60, 36 clusters) | +0.012 [-0.029, 0.056] – (plain [-0.032, 0.056]; 5/3, n=126, 75 clusters) |
| hybrid_v9b | +0.061 [0.014, 0.125] ✅ (plain [0.015, 0.121]; 4/0, n=66, 41 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=60, 36 clusters) | +0.032 [0.007, 0.069] ✅ (plain [0.008, 0.071]; 4/0, n=126, 75 clusters) |

## chunk R@5 by question_type (`overall` questions)

| run | compound (n=7) | exact_term (n=7) | lookup (n=42) | multi_doc (n=15) | outdated_version (n=25) | paraphrase (n=30) |
|---|---|---|---|---|---|---|
| hybrid | 0.429 | 0.857 | 0.857 | 0.667 | 0.680 | 0.467 |
| hybrid_v8 | 0.429 | 0.857 | 0.881 | 0.667 | 0.720 | 0.433 |
| hybrid_v8b | 0.429 | 0.857 | 0.857 | 0.667 | 0.680 | 0.467 |
| hybrid_v9w10 | 0.429 | 0.857 | 0.857 | 0.667 | 0.720 | 0.467 |
| hybrid_v9w25 | 0.429 | 0.857 | 0.905 | 0.667 | 0.720 | 0.433 |
| hybrid_v9w50 | 0.429 | 0.857 | 0.857 | 0.700 | 0.760 | 0.433 |
| hybrid_v9b | 0.429 | 0.857 | 0.905 | 0.667 | 0.760 | 0.467 |

## chunk R@5 by doc_group (`overall` questions)

| run | finance (n=25) | hiring (n=6) | legal (n=1) | mixed (n=4) | pdf (n=27) | people-policies (n=7) | security (n=24) | support (n=5) | total-rewards (n=27) |
|---|---|---|---|---|---|---|---|---|---|
| hybrid | 0.640 | 0.833 | 1.000 | 0.375 | 0.648 | 0.286 | 0.688 | 0.400 | 0.907 |
| hybrid_v8 | 0.720 | 0.833 | 1.000 | 0.375 | 0.648 | 0.429 | 0.646 | 0.400 | 0.870 |
| hybrid_v8b | 0.640 | 0.833 | 1.000 | 0.375 | 0.648 | 0.286 | 0.688 | 0.400 | 0.907 |
| hybrid_v9w10 | 0.680 | 0.833 | 1.000 | 0.375 | 0.648 | 0.286 | 0.688 | 0.400 | 0.907 |
| hybrid_v9w25 | 0.720 | 0.667 | 1.000 | 0.375 | 0.648 | 0.429 | 0.688 | 0.400 | 0.907 |
| hybrid_v9w50 | 0.760 | 0.667 | 1.000 | 0.375 | 0.593 | 0.429 | 0.688 | 0.400 | 0.907 |
| hybrid_v9b | 0.760 | 0.833 | 1.000 | 0.375 | 0.648 | 0.429 | 0.688 | 0.400 | 0.907 |
