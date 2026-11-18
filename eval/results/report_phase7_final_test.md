# Report: phase7_final_test (reference: test_baseline, tune split)

- **test_baseline**: FINAL TEST RUN (once): the baseline on the held-out test split. Reference point only; nothing is tuned on it.
- **test_final**: FINAL TEST RUN (once): the chosen configuration (hybrid_v9w10, Amendment 4) on the held-out test split.

**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes zero; – = no detectable difference. Verdicts use the CLUSTER interval (first bracket); the plain per-question interval is shown for context only.

## Paired differences from test_baseline

| run | Δ MAIN chunk R@5 (overall) | Δ chunk R@5 (non_outdated, guardrail) | Δ fact_stale (by rank, both found) | Δ stale doc-level (by rank) | Δ fact_found (outdated, guardrail) | Δ history chunk R@5 (guardrail) |
|---|---|---|---|---|---|---|
| test_baseline |  |  |  |  |  |  |
| test_final | +0.333 [0.161, 0.500] ✅ (plain [0.182, 0.485]; 11/0, n=33, 21 clusters) | +0.263 [0.105, 0.444] ✅ (plain [0.053, 0.474]; 5/0, n=19, 14 clusters) | -1.000 [-1.000, -1.000] ✅ (plain [-1.000, -1.000]; 6/0, n=6, 5 clusters) | -0.692 [-0.944, -0.333] ✅ (plain [-0.923, -0.462]; 9/0, n=13, 9 clusters) | +0.571 [0.182, 0.867] ✅ (plain [0.286, 0.786]; 8/0, n=14, 9 clusters) | +0.000 [0.000, 0.000] – (plain [0.000, 0.000]; 0/0, n=2, 2 clusters) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better. stale and fact_stale are decided by RANK for every run (Amendment 3b), so all runs share one scale; tie-tolerance variants are a secondary detail for cosine runs only.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| test_baseline | 0.364 [0.18, 0.55] | 0.368 [0.17, 0.59] | 0.288 [0.15, 0.43] | 0.849 [0.72, 0.95] | 0.576 | 0.818 |
| test_final | 0.697 [0.52, 0.84] | 0.632 [0.39, 0.81] | 0.549 [0.40, 0.70] | 0.970 [0.89, 1.00] | 0.924 | 1.000 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) | secondary: fact_stale tol 0.001 / 0.005 / 0.01 (cosine only) |
|---|---|---|---|
| test_baseline | 1.000 [1.00, 1.00] | 0.429 [0.13, 0.82] | 0.833 / 0.583 / 0.500 |
| test_final | 0.143 [0.00, 0.33] | 1.000 [1.00, 1.00] | n/a / n/a / n/a |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| test_baseline | 2468 | 3.7 | 18.5 | 46.7 | 39/39 |
| test_final | 2468 | 3.7 | 27.1 | 0.0 | 39/39 |

## chunk R@5 by question_type (`overall` questions)

| run | exact_term (n=3) | lookup (n=8) | multi_doc (n=3) | outdated_version (n=14) | paraphrase (n=5) |
|---|---|---|---|---|---|
| test_baseline | 0.333 | 0.375 | 0.667 | 0.357 | 0.200 |
| test_final | 0.667 | 0.625 | 0.667 | 0.786 | 0.600 |

## chunk R@5 by doc_group (`overall` questions)

| run | finance (n=11) | mixed (n=2) | pdf (n=5) | people-policies (n=2) | security (n=8) | support (n=1) | total-rewards (n=4) |
|---|---|---|---|---|---|---|---|
| test_baseline | 0.273 | 0.500 | 0.200 | 1.000 | 0.250 | 1.000 | 0.500 |
| test_final | 0.727 | 0.500 | 0.400 | 1.000 | 0.750 | 1.000 | 0.750 |
