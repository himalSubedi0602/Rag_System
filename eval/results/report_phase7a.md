# Report: phase7a (reference: baseline, tune split)

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
| chunk250 | -0.038 [-0.144, 0.068] – (6/8, n=66) | +0.012 [-0.098, 0.134] – (4/3, n=41) | +0.050 [-0.150, 0.300] – (1/1, n=10) | +0.200 [-0.050, 0.450] – (1/4, n=10) | +0.040 [-0.120, 0.200] – (3/2, n=25) |
| chunk1000 | +0.030 [-0.068, 0.129] – (7/5, n=66) | +0.073 [-0.049, 0.207] – (6/3, n=41) | +0.045 [0.000, 0.136] – (0/1, n=11) | +0.000 [0.000, 0.000] – (0/0, n=11) | +0.080 [-0.080, 0.240] – (3/1, n=25) |
| small2big | +0.068 [-0.008, 0.152] – (7/2, n=66) | +0.110 [0.024, 0.220] ✅ (5/0, n=41) | +0.042 [0.000, 0.125] – (0/1, n=12) | +0.042 [-0.083, 0.167] – (1/2, n=12) | +0.240 [0.080, 0.400] ✅ (6/0, n=25) |
| heading | +0.053 [-0.008, 0.121] – (5/1, n=66) | +0.037 [-0.049, 0.122] – (3/1, n=41) | +0.045 [-0.091, 0.182] – (1/2, n=11) | -0.045 [-0.364, 0.273] – (4/3, n=11) | +0.280 [0.080, 0.480] ✅ (8/1, n=25) |
| prefix | +0.015 [-0.068, 0.106] – (6/4, n=66) | +0.024 [-0.049, 0.098] – (3/1, n=41) | -0.045 [-0.136, 0.000] – (1/0, n=11) | -0.091 [-0.273, 0.000] – (1/0, n=11) | +0.040 [-0.080, 0.200] – (2/1, n=25) |
| bge | +0.098 [-0.015, 0.212] – (13/5, n=66) | +0.110 [-0.012, 0.244] – (8/2, n=41) | +0.150 [0.000, 0.400] – (0/2, n=10) | +0.400 [0.100, 0.650] ❌ (1/7, n=10) | +0.200 [0.000, 0.440] – (7/2, n=25) |

fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; lower is better.

## Retrieval levels (95% bootstrap intervals)

| run | MAIN chunk R@5 (overall) | chunk R@5 (non_outdated) | chunk MRR (overall) | doc R@5 (overall) | chunk R@30 (overall) | chunk R@100 (overall) |
|---|---|---|---|---|---|---|
| baseline | 0.455 [0.33, 0.58] | 0.512 [0.35, 0.66] | 0.321 [0.23, 0.41] | 0.735 [0.63, 0.83] | 0.614 | 0.758 |
| chunk250 | 0.417 [0.30, 0.53] | 0.524 [0.37, 0.67] | 0.288 [0.20, 0.38] | 0.811 [0.71, 0.89] | 0.599 | 0.742 |
| chunk1000 | 0.485 [0.36, 0.61] | 0.585 [0.44, 0.73] | 0.338 [0.25, 0.43] | 0.644 [0.52, 0.75] | 0.659 | 0.833 |
| small2big | 0.523 [0.40, 0.64] | 0.622 [0.48, 0.76] | 0.371 [0.28, 0.47] | 0.758 [0.64, 0.85] | 0.758 | 0.864 |
| heading | 0.508 [0.39, 0.62] | 0.549 [0.39, 0.70] | 0.403 [0.30, 0.50] | 0.811 [0.72, 0.89] | 0.750 | 0.803 |
| prefix | 0.470 [0.36, 0.58] | 0.537 [0.39, 0.68] | 0.334 [0.25, 0.43] | 0.697 [0.59, 0.80] | 0.644 | 0.780 |
| bge | 0.553 [0.44, 0.67] | 0.622 [0.48, 0.76] | 0.377 [0.29, 0.47] | 0.833 [0.74, 0.92] | 0.780 | 0.864 |

## Version metrics (each run on its own found set; see the paired Δ above for comparisons)

| run | fact_stale (outdated, own found set) | fact_found (outdated) |
|---|---|---|
| baseline | 0.458 [0.33, 0.58] | 0.480 [0.28, 0.68] |
| chunk250 | 0.538 [0.38, 0.69] | 0.520 [0.32, 0.72] |
| chunk1000 | 0.536 [0.43, 0.64] | 0.560 [0.36, 0.76] |
| small2big | 0.500 [0.36, 0.64] | 0.720 [0.52, 0.88] |
| heading | 0.500 [0.37, 0.63] | 0.760 [0.60, 0.92] |
| prefix | 0.423 [0.27, 0.58] | 0.520 [0.32, 0.72] |
| bge | 0.529 [0.50, 0.59] | 0.680 [0.48, 0.84] |

## Cost and diagnostics

| run | embedded vectors | vector index MB | mean search ms | tokens unseen % | quotes reachable |
|---|---|---|---|---|---|
| baseline | 2468 | 3.7 | 12.0 | 46.7 | 84/84 |
| chunk250 | 4774 | 7.4 | 11.3 | 0.0 | 84/84 |
| chunk1000 | 1330 | 1.8 | 11.3 | 70.8 | 84/84 |
| small2big | 7189 | 16.5 | 19.5 | 0.0 | 84/84 |
| heading | 4704 | 7.4 | 10.6 | 25.2 | 84/84 |
| prefix | 2468 | 3.7 | 11.4 | 48.2 | 84/84 |
| bge | 2468 | 3.7 | 13.7 | 0.0 | 84/84 |
