# Report: phase7b_step1_vs_base (reference: small2big, tune split)

- **small2big**: Run 2b: small-to-big. Search 250-token pieces of each 500-token chunk, return the parent chunk.
- **s2b_bge**: Run 7b step 1: small2big + bge-small. Base = small2big; only change: the embedding model (embeds the 250-token pieces).
- **s2b_heading**: Run 7b step 1: small2big + heading-as-parent. Base = small2big; only change: parents are markdown sections
- **s2b_prefix**: Run 7b step 1: small2big + title/section prefix. Base = small2big; only change: "Doc title > Section" on every piece.

**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes zero; – = no detectable difference. Verdicts use the CLUSTER interval (first bracket); the plain per-question interval is shown for context only.

## Paired differences from small2big

| run | Δ MAIN chunk R@5 (overall) | Δ chunk R@5 (non_outdated, guardrail) | Δ fact_stale (by rank, both found) | Δ stale doc-level (by rank) | Δ fact_found (outdated, guardrail) |
|---|---|---|---|---|---|
| small2big |  |  |  |  |  |
| s2b_bge | -0.008 [-0.081, 0.059] – (plain [-0.079, 0.060]; 11/12, n=126, 75 clusters) | +0.000 [-0.082, 0.069] – (plain [-0.079, 0.074]; 9/9, n=101, 61 clusters) | +0.071 [-0.286, 0.417] – (plain [-0.214, 0.357]; 2/3, n=14, 12 clusters) | +0.045 [-0.136, 0.250] – (plain [-0.136, 0.227]; 2/3, n=22, 19 clusters) | -0.120 [-0.286, 0.042] – (plain [-0.280, 0.040]; 1/4, n=25, 22 clusters) |
| s2b_heading | -0.028 [-0.108, 0.047] – (plain [-0.099, 0.040]; 9/15, n=126, 75 clusters) | -0.074 [-0.157, 0.000] – (plain [-0.149, -0.005]; 4/14, n=101, 61 clusters) | -0.188 [-0.500, 0.188] – (plain [-0.562, 0.188]; 6/3, n=16, 13 clusters) | -0.182 [-0.435, 0.105] – (plain [-0.455, 0.091]; 7/3, n=22, 19 clusters) | +0.040 [-0.148, 0.217] – (plain [-0.120, 0.200]; 3/2, n=25, 22 clusters) |
| s2b_prefix | +0.052 [-0.024, 0.124] – (plain [-0.024, 0.131]; 19/10, n=126, 75 clusters) | +0.045 [-0.038, 0.124] – (plain [-0.035, 0.124]; 15/8, n=101, 61 clusters) | -0.200 [-0.529, 0.154] – (plain [-0.533, 0.133]; 5/2, n=15, 12 clusters) | +0.000 [-0.292, 0.300] – (plain [-0.286, 0.286]; 4/4, n=21, 18 clusters) | -0.080 [-0.250, 0.077] – (plain [-0.240, 0.080]; 1/3, n=25, 22 clusters) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better. stale and fact_stale are decided by RANK for every run (Amendment 4a), so all runs share one scale; tie-tolerance variants are a secondary detail for cosine runs only.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| small2big | 0.536 [0.45, 0.62] | 0.579 [0.48, 0.68] | 0.415 [0.34, 0.49] | 0.750 [0.66, 0.84] | 0.790 | 0.881 |
| s2b_bge | 0.528 [0.43, 0.62] | 0.579 [0.47, 0.68] | 0.391 [0.31, 0.47] | 0.754 [0.66, 0.84] | 0.750 | 0.869 |
| s2b_heading | 0.508 [0.42, 0.60] | 0.505 [0.40, 0.60] | 0.407 [0.33, 0.48] | 0.778 [0.70, 0.86] | 0.722 | 0.849 |
| s2b_prefix | 0.587 [0.49, 0.68] | 0.624 [0.52, 0.72] | 0.482 [0.38, 0.57] | 0.770 [0.67, 0.86] | 0.782 | 0.845 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) | secondary: fact_stale tol 0.001 / 0.005 / 0.01 (cosine only) |
|---|---|---|---|
| small2big | 0.722 [0.50, 0.90] | 0.720 [0.52, 0.88] | 0.583 / 0.500 / 0.556 |
| s2b_bge | 0.733 [0.47, 1.00] | 0.600 [0.42, 0.78] | 0.667 / 0.600 / 0.600 |
| s2b_heading | 0.526 [0.33, 0.72] | 0.760 [0.57, 0.92] | 0.526 / 0.500 / 0.500 |
| s2b_prefix | 0.562 [0.29, 0.85] | 0.640 [0.43, 0.81] | 0.438 / 0.469 / 0.438 |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| small2big | 7189 | 16.5 | 16.6 | 0.0 | 159/159 |
| s2b_bge | 7189 | 16.5 | 21.9 | 0.0 | 159/159 |
| s2b_heading | 7515 | 20.4 | 18.2 | 0.0 | 159/159 |
| s2b_prefix | 7189 | 16.5 | 14.8 | 3.6 | 159/159 |

## Replication (frozen groups in eval/replication_groups.json)

An effect replicates if it has the same sign on the new questions; it is confirmed only if the combined interval excludes zero.

| run | Δ chunk R@5 (original, n=66) | Δ chunk R@5 (new only, n=60) | Δ chunk R@5 (combined, n=126) |
|---|---|---|---|
| s2b_bge | -0.030 [-0.139, 0.065] – (plain [-0.136, 0.076]; 5/7, n=66, 41 clusters) | +0.017 [-0.078, 0.108] – (plain [-0.075, 0.108]; 6/5, n=60, 36 clusters) | -0.008 [-0.081, 0.059] – (plain [-0.079, 0.060]; 11/12, n=126, 75 clusters) |
| s2b_heading | +0.045 [-0.051, 0.143] – (plain [-0.045, 0.136]; 7/4, n=66, 41 clusters) | -0.108 [-0.218, -0.010] ❌ (plain [-0.208, -0.017]; 2/11, n=60, 36 clusters) | -0.028 [-0.108, 0.047] – (plain [-0.099, 0.040]; 9/15, n=126, 75 clusters) |
| s2b_prefix | -0.015 [-0.144, 0.099] – (plain [-0.129, 0.098]; 8/8, n=66, 41 clusters) | +0.125 [0.047, 0.223] ✅ (plain [0.033, 0.217]; 11/2, n=60, 36 clusters) | +0.052 [-0.024, 0.124] – (plain [-0.024, 0.131]; 19/10, n=126, 75 clusters) |

## chunk R@5 by question_type (`overall` questions)

| run | compound (n=7) | exact_term (n=7) | lookup (n=42) | multi_doc (n=15) | outdated_version (n=25) | paraphrase (n=30) |
|---|---|---|---|---|---|---|
| small2big | 0.429 | 0.857 | 0.667 | 0.567 | 0.360 | 0.433 |
| s2b_bge | 0.357 | 0.857 | 0.714 | 0.600 | 0.320 | 0.367 |
| s2b_heading | 0.214 | 0.857 | 0.571 | 0.500 | 0.520 | 0.400 |
| s2b_prefix | 0.500 | 0.714 | 0.643 | 0.700 | 0.440 | 0.567 |

## chunk R@5 by doc_group (`overall` questions)

| run | finance (n=25) | hiring (n=6) | legal (n=1) | mixed (n=4) | pdf (n=27) | people-policies (n=7) | security (n=24) | support (n=5) | total-rewards (n=27) |
|---|---|---|---|---|---|---|---|---|---|
| small2big | 0.360 | 0.333 | 1.000 | 0.375 | 0.685 | 0.286 | 0.521 | 0.000 | 0.778 |
| s2b_bge | 0.400 | 0.167 | 0.000 | 0.375 | 0.667 | 0.286 | 0.521 | 0.200 | 0.759 |
| s2b_heading | 0.440 | 0.500 | 1.000 | 0.250 | 0.685 | 0.286 | 0.354 | 0.000 | 0.704 |
| s2b_prefix | 0.360 | 0.333 | 0.000 | 0.500 | 0.759 | 0.571 | 0.521 | 0.200 | 0.852 |
