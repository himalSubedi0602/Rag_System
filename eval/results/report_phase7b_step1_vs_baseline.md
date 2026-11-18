# Report: phase7b_step1_vs_baseline (reference: baseline, tune split)

- **baseline**: Run 1: baseline. Fixed 500-token chunks, 50 overlap, vector search only, MiniLM.
- **small2big**: Run 2b: small-to-big. Search 250-token pieces of each 500-token chunk, return the parent chunk.
- **bge**: Run 5: bge-small instead of MiniLM. Reads 512 tokens, so 500-token chunks are not truncated.
- **s2b_bge**: Run 7b step 1: small2big + bge-small. Base = small2big; only change: the embedding model (embeds the 250-token pieces).
- **s2b_heading**: Run 7b step 1: small2big + heading-as-parent. Base = small2big; only change: parents are markdown sections
- **s2b_prefix**: Run 7b step 1: small2big + title/section prefix. Base = small2big; only change: "Doc title > Section" on every piece.

**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes zero; – = no detectable difference. Verdicts use the CLUSTER interval (first bracket); the plain per-question interval is shown for context only.

## Paired differences from baseline

| run | Δ MAIN chunk R@5 (overall) | Δ chunk R@5 (non_outdated, guardrail) | Δ fact_stale (by rank, both found) | Δ stale doc-level (by rank) | Δ fact_found (outdated, guardrail) |
|---|---|---|---|---|---|
| baseline |  |  |  |  |  |
| small2big | +0.040 [-0.022, 0.109] – (plain [-0.028, 0.107]; 13/8, n=126, 75 clusters) | +0.050 [-0.022, 0.130] – (plain [-0.025, 0.124]; 11/6, n=101, 61 clusters) | +0.083 [0.000, 0.273] – (plain [0.000, 0.250]; 0/1, n=12, 10 clusters) | +0.045 [-0.150, 0.250] – (plain [-0.136, 0.227]; 2/3, n=22, 19 clusters) | +0.240 [0.077, 0.440] ✅ (plain [0.080, 0.400]; 6/0, n=25, 22 clusters) |
| bge | +0.052 [-0.051, 0.155] – (plain [-0.040, 0.147]; 26/18, n=126, 75 clusters) | +0.045 [-0.070, 0.146] – (plain [-0.059, 0.139]; 21/15, n=101, 61 clusters) | +0.200 [-0.167, 0.600] – (plain [-0.200, 0.600]; 1/3, n=10, 8 clusters) | +0.091 [-0.250, 0.429] – (plain [-0.182, 0.364]; 5/7, n=22, 19 clusters) | +0.200 [-0.040, 0.444] – (plain [0.000, 0.440]; 7/2, n=25, 22 clusters) |
| s2b_bge | +0.032 [-0.060, 0.116] – (plain [-0.056, 0.119]; 19/15, n=126, 75 clusters) | +0.050 [-0.051, 0.140] – (plain [-0.045, 0.139]; 16/11, n=101, 61 clusters) | +0.444 [0.125, 0.750] ❌ (plain [0.111, 0.778]; 0/4, n=9, 8 clusters) | +0.091 [-0.174, 0.348] – (plain [-0.182, 0.364]; 4/6, n=22, 19 clusters) | +0.120 [-0.125, 0.375] – (plain [-0.120, 0.360]; 6/3, n=25, 22 clusters) |
| s2b_heading | +0.012 [-0.076, 0.104] – (plain [-0.071, 0.091]; 16/17, n=126, 75 clusters) | -0.025 [-0.124, 0.069] – (plain [-0.119, 0.064]; 11/16, n=101, 61 clusters) | -0.182 [-0.636, 0.334] – (plain [-0.636, 0.273]; 5/3, n=11, 9 clusters) | -0.136 [-0.381, 0.143] – (plain [-0.455, 0.136]; 7/4, n=22, 19 clusters) | +0.280 [0.045, 0.520] ✅ (plain [0.080, 0.480]; 8/1, n=25, 22 clusters) |
| s2b_prefix | +0.091 [0.000, 0.179] – (plain [0.004, 0.179]; 26/12, n=126, 75 clusters) | +0.094 [0.005, 0.182] ✅ (plain [0.005, 0.183]; 21/9, n=101, 61 clusters) | +0.000 [-0.333, 0.400] – (plain [-0.364, 0.364]; 2/2, n=11, 9 clusters) | +0.048 [-0.190, 0.319] – (plain [-0.190, 0.286]; 3/4, n=21, 18 clusters) | +0.160 [-0.040, 0.370] – (plain [0.000, 0.360]; 5/1, n=25, 22 clusters) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better. stale and fact_stale are decided by RANK for every run (Amendment 4a), so all runs share one scale; tie-tolerance variants are a secondary detail for cosine runs only.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| baseline | 0.496 [0.40, 0.59] | 0.530 [0.43, 0.63] | 0.356 [0.28, 0.43] | 0.734 [0.65, 0.81] | 0.698 | 0.806 |
| small2big | 0.536 [0.45, 0.62] | 0.579 [0.48, 0.68] | 0.415 [0.34, 0.49] | 0.750 [0.66, 0.84] | 0.790 | 0.881 |
| bge | 0.548 [0.46, 0.64] | 0.574 [0.47, 0.66] | 0.398 [0.33, 0.47] | 0.798 [0.72, 0.88] | 0.786 | 0.873 |
| s2b_bge | 0.528 [0.43, 0.62] | 0.579 [0.47, 0.68] | 0.391 [0.31, 0.47] | 0.754 [0.66, 0.84] | 0.750 | 0.869 |
| s2b_heading | 0.508 [0.42, 0.60] | 0.505 [0.40, 0.60] | 0.407 [0.33, 0.48] | 0.778 [0.70, 0.86] | 0.722 | 0.849 |
| s2b_prefix | 0.587 [0.49, 0.68] | 0.624 [0.52, 0.72] | 0.482 [0.38, 0.57] | 0.770 [0.67, 0.86] | 0.782 | 0.845 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) | secondary: fact_stale tol 0.001 / 0.005 / 0.01 (cosine only) |
|---|---|---|---|
| baseline | 0.667 [0.38, 0.91] | 0.480 [0.27, 0.69] | 0.417 / 0.458 / 0.500 |
| small2big | 0.722 [0.50, 0.90] | 0.720 [0.52, 0.88] | 0.583 / 0.500 / 0.556 |
| bge | 0.765 [0.58, 0.94] | 0.680 [0.48, 0.85] | 0.676 / 0.529 / 0.529 |
| s2b_bge | 0.733 [0.47, 1.00] | 0.600 [0.42, 0.78] | 0.667 / 0.600 / 0.600 |
| s2b_heading | 0.526 [0.33, 0.72] | 0.760 [0.57, 0.92] | 0.526 / 0.500 / 0.500 |
| s2b_prefix | 0.562 [0.29, 0.85] | 0.640 [0.43, 0.81] | 0.438 / 0.469 / 0.438 |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| baseline | 2468 | 3.7 | 8.5 | 46.7 | 159/159 |
| small2big | 7189 | 16.5 | 16.6 | 0.0 | 159/159 |
| bge | 2468 | 3.7 | 10.9 | 0.0 | 159/159 |
| s2b_bge | 7189 | 16.5 | 21.9 | 0.0 | 159/159 |
| s2b_heading | 7515 | 20.4 | 18.2 | 0.0 | 159/159 |
| s2b_prefix | 7189 | 16.5 | 14.8 | 3.6 | 159/159 |

## Replication (frozen groups in eval/replication_groups.json)

An effect replicates if it has the same sign on the new questions; it is confirmed only if the combined interval excludes zero.

| run | Δ chunk R@5 (original, n=66) | Δ chunk R@5 (new only, n=60) | Δ chunk R@5 (combined, n=126) |
|---|---|---|---|
| small2big | +0.068 [-0.013, 0.153] – (plain [-0.008, 0.152]; 7/2, n=66, 41 clusters) | +0.008 [-0.086, 0.109] – (plain [-0.092, 0.117]; 6/6, n=60, 36 clusters) | +0.040 [-0.022, 0.109] – (plain [-0.028, 0.107]; 13/8, n=126, 75 clusters) |
| bge | +0.098 [-0.025, 0.218] – (plain [-0.015, 0.212]; 13/5, n=66, 41 clusters) | +0.000 [-0.155, 0.152] – (plain [-0.150, 0.150]; 13/13, n=60, 36 clusters) | +0.052 [-0.051, 0.155] – (plain [-0.040, 0.147]; 26/18, n=126, 75 clusters) |
| s2b_bge | +0.038 [-0.100, 0.164] – (plain [-0.076, 0.152]; 10/7, n=66, 41 clusters) | +0.025 [-0.091, 0.141] – (plain [-0.100, 0.150]; 9/8, n=60, 36 clusters) | +0.032 [-0.060, 0.116] – (plain [-0.056, 0.119]; 19/15, n=126, 75 clusters) |
| s2b_heading | +0.114 [0.016, 0.223] ✅ (plain [0.023, 0.205]; 10/2, n=66, 41 clusters) | -0.100 [-0.233, 0.034] – (plain [-0.233, 0.042]; 6/15, n=60, 36 clusters) | +0.012 [-0.076, 0.104] – (plain [-0.071, 0.091]; 16/17, n=126, 75 clusters) |
| s2b_prefix | +0.053 [-0.100, 0.189] – (plain [-0.076, 0.182]; 13/8, n=66, 41 clusters) | +0.133 [0.039, 0.246] ✅ (plain [0.025, 0.242]; 13/4, n=60, 36 clusters) | +0.091 [0.000, 0.179] – (plain [0.004, 0.179]; 26/12, n=126, 75 clusters) |

## chunk R@5 by question_type (`overall` questions)

| run | compound (n=7) | exact_term (n=7) | lookup (n=42) | multi_doc (n=15) | outdated_version (n=25) | paraphrase (n=30) |
|---|---|---|---|---|---|---|
| baseline | 0.429 | 0.857 | 0.524 | 0.567 | 0.360 | 0.467 |
| small2big | 0.429 | 0.857 | 0.667 | 0.567 | 0.360 | 0.433 |
| bge | 0.357 | 0.857 | 0.714 | 0.700 | 0.440 | 0.300 |
| s2b_bge | 0.357 | 0.857 | 0.714 | 0.600 | 0.320 | 0.367 |
| s2b_heading | 0.214 | 0.857 | 0.571 | 0.500 | 0.520 | 0.400 |
| s2b_prefix | 0.500 | 0.714 | 0.643 | 0.700 | 0.440 | 0.567 |

## chunk R@5 by doc_group (`overall` questions)

| run | finance (n=25) | hiring (n=6) | legal (n=1) | mixed (n=4) | pdf (n=27) | people-policies (n=7) | security (n=24) | support (n=5) | total-rewards (n=27) |
|---|---|---|---|---|---|---|---|---|---|
| baseline | 0.360 | 0.167 | 1.000 | 0.375 | 0.667 | 0.286 | 0.375 | 0.200 | 0.741 |
| small2big | 0.360 | 0.333 | 1.000 | 0.375 | 0.685 | 0.286 | 0.521 | 0.000 | 0.778 |
| bge | 0.440 | 0.333 | 1.000 | 0.375 | 0.722 | 0.286 | 0.521 | 0.000 | 0.722 |
| s2b_bge | 0.400 | 0.167 | 0.000 | 0.375 | 0.667 | 0.286 | 0.521 | 0.200 | 0.759 |
| s2b_heading | 0.440 | 0.500 | 1.000 | 0.250 | 0.685 | 0.286 | 0.354 | 0.000 | 0.704 |
| s2b_prefix | 0.360 | 0.333 | 0.000 | 0.500 | 0.759 | 0.571 | 0.521 | 0.200 | 0.852 |
