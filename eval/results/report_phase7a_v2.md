# Report: phase7a_v2 (reference: baseline, tune split)

- **baseline**: Run 1: baseline. Fixed 500-token chunks, 50 overlap, vector search only, MiniLM.
- **chunk250**: Run 2a: smaller chunks (250 tokens). Only change vs baseline: chunk size/overlap.
- **chunk1000**: Run 2c: larger chunks (1000 tokens). Only change vs baseline: chunk size/overlap.
- **small2big**: Run 2b: small-to-big. Search 250-token pieces of each 500-token chunk, return the parent chunk.
- **heading**: Run 3: heading-based chunks (one chunk per markdown section; long sections split at 500 tokens,
- **prefix**: Run 4: title/section prefix. "Doc title > Section" is prepended to each chunk before embedding.
- **bge**: Run 5: bge-small instead of MiniLM. Reads 512 tokens, so 500-token chunks are not truncated.

**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes zero; – = no detectable difference. (better/worse counts, n = paired questions.)

## Paired differences from baseline

| run | Δ MAIN chunk R@5 (overall) | Δ chunk R@5 (non_outdated, guardrail) | Δ fact_stale (both found, tol 0.005) | Δ fact_stale (both found, exact ties) | Δ fact_found (outdated, guardrail) |
|---|---|---|---|---|---|
| baseline |  |  |  |  |  |
| chunk250 | -0.052 [-0.137, 0.048] – (11/19, n=126, 75 clusters) | -0.035 [-0.122, 0.066] – (9/14, n=101, 61 clusters) | +0.050 [-0.150, 0.333] – (1/1, n=10, 9 clusters) | +0.200 [-0.050, 0.450] – (1/4, n=10, 9 clusters) | +0.040 [-0.172, 0.231] – (3/2, n=25, 22 clusters) |
| chunk1000 | +0.067 [-0.016, 0.141] – (19/9, n=126, 75 clusters) | +0.094 [0.005, 0.170] ✅ (18/7, n=101, 61 clusters) | +0.045 [0.000, 0.150] – (0/1, n=11, 10 clusters) | +0.000 [0.000, 0.000] – (0/0, n=11, 10 clusters) | +0.080 [-0.071, 0.250] – (3/1, n=25, 22 clusters) |
| small2big | +0.040 [-0.022, 0.109] – (13/8, n=126, 75 clusters) | +0.050 [-0.022, 0.130] – (11/6, n=101, 61 clusters) | +0.042 [0.000, 0.136] – (0/1, n=12, 10 clusters) | +0.042 [-0.091, 0.182] – (1/2, n=12, 10 clusters) | +0.240 [0.077, 0.440] ✅ (6/0, n=25, 22 clusters) |
| heading | -0.040 [-0.115, 0.034] – (9/16, n=126, 75 clusters) | -0.069 [-0.160, 0.015] – (7/16, n=101, 61 clusters) | +0.045 [-0.100, 0.222] – (1/2, n=11, 9 clusters) | -0.045 [-0.350, 0.250] – (4/3, n=11, 9 clusters) | +0.280 [0.077, 0.500] ✅ (8/1, n=25, 22 clusters) |
| prefix | +0.044 [-0.023, 0.109] – (15/8, n=126, 75 clusters) | +0.054 [-0.005, 0.115] – (12/5, n=101, 61 clusters) | -0.045 [-0.150, 0.000] – (1/0, n=11, 9 clusters) | -0.091 [-0.250, 0.000] – (1/0, n=11, 9 clusters) | +0.040 [-0.087, 0.182] – (2/1, n=25, 22 clusters) |
| bge | +0.052 [-0.051, 0.155] – (26/18, n=126, 75 clusters) | +0.045 [-0.070, 0.146] – (21/15, n=101, 61 clusters) | +0.150 [0.000, 0.375] – (0/2, n=10, 8 clusters) | +0.400 [0.200, 0.625] ❌ (1/7, n=10, 8 clusters) | +0.200 [-0.040, 0.444] – (7/2, n=25, 22 clusters) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| baseline | 0.496 [0.40, 0.59] | 0.530 [0.43, 0.63] | 0.356 [0.28, 0.43] | 0.734 [0.65, 0.81] | 0.698 | 0.806 |
| chunk250 | 0.444 [0.37, 0.53] | 0.495 [0.41, 0.60] | 0.344 [0.28, 0.42] | 0.798 [0.72, 0.87] | 0.675 | 0.786 |
| chunk1000 | 0.564 [0.46, 0.66] | 0.624 [0.52, 0.72] | 0.433 [0.33, 0.52] | 0.702 [0.60, 0.79] | 0.758 | 0.853 |
| small2big | 0.536 [0.45, 0.62] | 0.579 [0.48, 0.68] | 0.415 [0.34, 0.49] | 0.750 [0.66, 0.84] | 0.790 | 0.881 |
| heading | 0.456 [0.36, 0.55] | 0.460 [0.36, 0.56] | 0.377 [0.30, 0.46] | 0.770 [0.69, 0.85] | 0.679 | 0.774 |
| prefix | 0.540 [0.44, 0.63] | 0.584 [0.49, 0.68] | 0.417 [0.33, 0.50] | 0.734 [0.64, 0.82] | 0.750 | 0.841 |
| bge | 0.548 [0.46, 0.64] | 0.574 [0.47, 0.66] | 0.398 [0.33, 0.47] | 0.798 [0.72, 0.88] | 0.786 | 0.873 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) |
|---|---|---|
| baseline | 0.458 [0.33, 0.60] | 0.480 [0.27, 0.69] |
| chunk250 | 0.538 [0.38, 0.71] | 0.520 [0.33, 0.72] |
| chunk1000 | 0.536 [0.43, 0.65] | 0.560 [0.36, 0.76] |
| small2big | 0.500 [0.37, 0.65] | 0.720 [0.52, 0.88] |
| heading | 0.500 [0.38, 0.64] | 0.760 [0.58, 0.92] |
| prefix | 0.423 [0.29, 0.58] | 0.520 [0.30, 0.73] |
| bge | 0.529 [0.50, 0.60] | 0.680 [0.48, 0.85] |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| baseline | 2468 | 3.7 | 9.9 | 46.7 | 159/159 |
| chunk250 | 4774 | 7.4 | 8.6 | 0.0 | 159/159 |
| chunk1000 | 1330 | 1.8 | 7.7 | 70.8 | 159/159 |
| small2big | 7189 | 16.5 | 13.1 | 0.0 | 159/159 |
| heading | 4704 | 7.4 | 5.8 | 25.2 | 159/159 |
| prefix | 2468 | 3.7 | 5.5 | 48.2 | 159/159 |
| bge | 2468 | 3.7 | 9.8 | 0.0 | 159/159 |

## Replication (frozen groups in eval/replication_groups.json)

An effect replicates if it has the same sign on the new questions; it is confirmed only if the combined interval excludes zero.

| run | Δ chunk R@5 (original, n=66) | Δ chunk R@5 (new only, n=60) | Δ chunk R@5 (combined, n=126) |
|---|---|---|---|
| chunk250 | -0.038 [-0.154, 0.077] – (6/8, n=66, 41 clusters) | -0.067 [-0.184, 0.059] – (5/11, n=60, 36 clusters) | -0.052 [-0.137, 0.048] – (11/19, n=126, 75 clusters) |
| chunk1000 | +0.015 [-0.103, 0.103] – (7/6, n=66, 41 clusters) | +0.125 [0.000, 0.245] – (12/3, n=60, 36 clusters) | +0.067 [-0.016, 0.141] – (19/9, n=126, 75 clusters) |
| small2big | +0.068 [-0.013, 0.153] – (7/2, n=66, 41 clusters) | +0.008 [-0.086, 0.109] – (6/6, n=60, 36 clusters) | +0.040 [-0.022, 0.109] – (13/8, n=126, 75 clusters) |
| heading | +0.038 [-0.034, 0.117] – (5/2, n=66, 41 clusters) | -0.125 [-0.250, 0.000] – (4/14, n=60, 36 clusters) | -0.040 [-0.115, 0.034] – (9/16, n=126, 75 clusters) |
| prefix | +0.015 [-0.090, 0.105] – (6/4, n=66, 41 clusters) | +0.075 [-0.008, 0.170] – (9/4, n=60, 36 clusters) | +0.044 [-0.023, 0.109] – (15/8, n=126, 75 clusters) |
| bge | +0.098 [-0.025, 0.218] – (13/5, n=66, 41 clusters) | +0.000 [-0.155, 0.152] – (13/13, n=60, 36 clusters) | +0.052 [-0.051, 0.155] – (26/18, n=126, 75 clusters) |

## chunk R@5 by question_type (`overall` questions)

| run | compound (n=7) | exact_term (n=7) | lookup (n=42) | multi_doc (n=15) | outdated_version (n=25) | paraphrase (n=30) |
|---|---|---|---|---|---|---|
| baseline | 0.429 | 0.857 | 0.524 | 0.567 | 0.360 | 0.467 |
| chunk250 | 0.286 | 0.857 | 0.548 | 0.467 | 0.240 | 0.400 |
| chunk1000 | 0.429 | 0.714 | 0.738 | 0.667 | 0.320 | 0.467 |
| small2big | 0.429 | 0.857 | 0.667 | 0.567 | 0.360 | 0.433 |
| heading | 0.286 | 0.857 | 0.476 | 0.500 | 0.440 | 0.367 |
| prefix | 0.571 | 0.857 | 0.619 | 0.600 | 0.360 | 0.467 |
| bge | 0.357 | 0.857 | 0.714 | 0.700 | 0.440 | 0.300 |

## chunk R@5 by doc_group (`overall` questions)

| run | finance (n=25) | hiring (n=6) | legal (n=1) | mixed (n=4) | pdf (n=27) | people-policies (n=7) | security (n=24) | support (n=5) | total-rewards (n=27) |
|---|---|---|---|---|---|---|---|---|---|
| baseline | 0.360 | 0.167 | 1.000 | 0.375 | 0.667 | 0.286 | 0.375 | 0.200 | 0.741 |
| chunk250 | 0.320 | 0.167 | 1.000 | 0.375 | 0.648 | 0.286 | 0.354 | 0.000 | 0.611 |
| chunk1000 | 0.360 | 0.167 | 1.000 | 0.375 | 0.778 | 0.143 | 0.458 | 0.400 | 0.870 |
| small2big | 0.360 | 0.333 | 1.000 | 0.375 | 0.685 | 0.286 | 0.521 | 0.000 | 0.778 |
| heading | 0.320 | 0.333 | 1.000 | 0.250 | 0.667 | 0.286 | 0.271 | 0.000 | 0.704 |
| prefix | 0.320 | 0.167 | 1.000 | 0.625 | 0.722 | 0.286 | 0.521 | 0.400 | 0.722 |
| bge | 0.440 | 0.333 | 1.000 | 0.375 | 0.722 | 0.286 | 0.521 | 0.000 | 0.722 |
