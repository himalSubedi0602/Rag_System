# Report: phase7b_step1_decision (reference: bge, tune split)

- **bge**: Run 5: bge-small instead of MiniLM. Reads 512 tokens, so 500-token chunks are not truncated.
- **s2b_bge**: Run 7b step 1: small2big + bge-small. Base = small2big; only change: the embedding model (embeds the 250-token pieces).

**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes zero; – = no detectable difference. Verdicts use the CLUSTER interval (first bracket); the plain per-question interval is shown for context only.

## Paired differences from bge

| run | Δ MAIN chunk R@5 (overall) | Δ chunk R@5 (non_outdated, guardrail) | Δ fact_stale (by rank, both found) | Δ stale doc-level (by rank) | Δ fact_found (outdated, guardrail) |
|---|---|---|---|---|---|
| bge |  |  |  |  |  |
| s2b_bge | -0.020 [-0.101, 0.052] – (plain [-0.087, 0.048]; 10/14, n=126, 75 clusters) | +0.005 [-0.082, 0.089] – (plain [-0.069, 0.089]; 10/11, n=101, 61 clusters) | -0.071 [-0.357, 0.250] – (plain [-0.357, 0.214]; 3/2, n=14, 12 clusters) | -0.043 [-0.292, 0.208] – (plain [-0.304, 0.217]; 5/4, n=23, 20 clusters) | -0.080 [-0.222, 0.077] – (plain [-0.240, 0.080]; 1/3, n=25, 22 clusters) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better. stale and fact_stale are decided by RANK for every run (Amendment 4a), so all runs share one scale; tie-tolerance variants are a secondary detail for cosine runs only.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| bge | 0.548 [0.46, 0.64] | 0.574 [0.47, 0.66] | 0.398 [0.33, 0.47] | 0.798 [0.72, 0.88] | 0.786 | 0.873 |
| s2b_bge | 0.528 [0.43, 0.62] | 0.579 [0.47, 0.68] | 0.391 [0.31, 0.47] | 0.754 [0.66, 0.84] | 0.750 | 0.869 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) | secondary: fact_stale tol 0.001 / 0.005 / 0.01 (cosine only) |
|---|---|---|---|
| bge | 0.765 [0.58, 0.94] | 0.680 [0.48, 0.85] | 0.676 / 0.529 / 0.529 |
| s2b_bge | 0.733 [0.47, 1.00] | 0.600 [0.42, 0.78] | 0.667 / 0.600 / 0.600 |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| bge | 2468 | 3.7 | 10.9 | 0.0 | 159/159 |
| s2b_bge | 7189 | 16.5 | 21.9 | 0.0 | 159/159 |

## Replication (frozen groups in eval/replication_groups.json)

An effect replicates if it has the same sign on the new questions; it is confirmed only if the combined interval excludes zero.

| run | Δ chunk R@5 (original, n=66) | Δ chunk R@5 (new only, n=60) | Δ chunk R@5 (combined, n=126) |
|---|---|---|---|
| s2b_bge | -0.061 [-0.139, 0.006] – (plain [-0.129, 0.000]; 1/6, n=66, 41 clusters) | +0.025 [-0.108, 0.158] – (plain [-0.092, 0.142]; 9/8, n=60, 36 clusters) | -0.020 [-0.101, 0.052] – (plain [-0.087, 0.048]; 10/14, n=126, 75 clusters) |

## chunk R@5 by question_type (`overall` questions)

| run | compound (n=7) | exact_term (n=7) | lookup (n=42) | multi_doc (n=15) | outdated_version (n=25) | paraphrase (n=30) |
|---|---|---|---|---|---|---|
| bge | 0.357 | 0.857 | 0.714 | 0.700 | 0.440 | 0.300 |
| s2b_bge | 0.357 | 0.857 | 0.714 | 0.600 | 0.320 | 0.367 |

## chunk R@5 by doc_group (`overall` questions)

| run | finance (n=25) | hiring (n=6) | legal (n=1) | mixed (n=4) | pdf (n=27) | people-policies (n=7) | security (n=24) | support (n=5) | total-rewards (n=27) |
|---|---|---|---|---|---|---|---|---|---|
| bge | 0.440 | 0.333 | 1.000 | 0.375 | 0.722 | 0.286 | 0.521 | 0.000 | 0.722 |
| s2b_bge | 0.400 | 0.167 | 0.000 | 0.375 | 0.667 | 0.286 | 0.521 | 0.200 | 0.759 |
