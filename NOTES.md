# Build Notes

One entry per phase: what was built, key decisions, results so far.

## Phase 1: Project setup (2026-11-17)

**Built**
- Folder layout (`data/`, `configs/`, `src/`, `eval/`, `tests/`), `requirements.txt`, `.gitignore`, `pytest.ini`.
- `src/config.py`: loads `configs/default.yaml` and merges one experiment YAML on top.
- `configs/baseline.yaml` (run 1) and 7 config tests.

**Key decisions**
- **Defaults + overrides:** each experiment file lists only what it changes, so a diff between two
  configs shows exactly the one variable an experiment tests.
- **Unknown keys raise an error:** a typo like `chunk_sise` would otherwise be ignored silently and
  the run would use the default, giving a wrong result that looks valid.
- **Validation up front:** e.g. `chunk_overlap >= chunk_size` is rejected at load time instead of
  making the chunker loop forever later.
- **No raw data in git:** `data/raw/`, `data/processed/` and the Chroma DB are ignored; `.gitkeep`
  files keep the empty folders. The README will document how to download the corpus.
- Streamlit is not in `requirements.txt` yet (added in Phase 9), to keep the install smaller.

**Results so far**
- `pytest`: 7 passed.

## Phase 2: Ingestion (2026-11-17)

**Built**
- `data/sources.yaml`: the corpus definition (handbook include patterns, 20 PDF URLs, simulated access roles).
- `src/download_data.py`: downloads handbook sections as zips from the GitLab API, fetches each file's
  last-commit date, downloads PDFs (checks the `%PDF` signature), retries on timeouts and rate limits.
- `src/ingest.py`: markdown + PDF loaders, header/footer stripping, content-hash cache, version detection.
- `src/inspect_docs.py`: prints sample documents and the version groups for spot-checking.
- `tests/test_ingest.py`: 20 tests (27 total in the repo).

**Key decisions**
- **One record per document, text stored as `pages`.** PDFs keep page numbers (needed for citations);
  markdown is a single page with `page: null` and keeps its `##` headings for heading-based chunking.
- **Header/footer stripping:** a line is removed only if it sits in the top/bottom zone of a page
  (at most 8 lines, at most a third of the page) and repeats on >= 50% of pages after replacing digits
  with `#`. It must contain a letter, so clause numbers like `5.3` survive. Bare page numbers and
  table-of-contents residue is removed: dot-leader lines and runs of 3+ number-only lines.
- **Cache key = file hash + `EXTRACTOR_VERSION`.** Found during testing: hashing only the file meant a
  bug fix in the extractor never reached already-cached files. Metadata is rebuilt every run, so edits
  to `sources.yaml` always apply.
- **Version detection by file name, not title.** Four organisations have an "Annual Leave Policy";
  grouping by title would wrongly call them versions of each other. Handbook files are grouped only
  with evidence (`-vN` suffix or `legacy` marker); PDF pairs are declared in `sources.yaml`.
- **Commit dates are not trusted for "which is current".** `legacy-vendor-agreement-v1` was committed
  *after* the current vendor agreement (repo maintenance). Order: explicit flag > legacy/deprecated
  marker > unversioned file > highest `-vN` > newest date.
- **Only a first-line "deprecated" banner counts.** A support page that mentions "password login has been
  deprecated" was wrongly marked old; fixed and covered by a test.

**Results so far**
- 413 files -> 380 documents (360 markdown, 20 PDF); 33 dropped as empty/"moved" stubs.
- 11 version groups with real old versions (e.g. testing agreement v1-v5 + current, AI terms v1-v4 +
  current, 2 PDF pairs); 28 non-current documents. All documents have an `updated_date`.
- Second ingest run: 413/413 files skipped as unchanged.

## Phase 3: Chunking (2026-11-17)

**Built**
- `src/chunking.py`: fixed-size and heading-based chunking, title/section prefix (`index_text`),
  truncation report. Writes `data/processed/chunks/<strategy_key>.jsonl`.
- `tests/test_chunking.py`: 14 tests (41 total in the repo).

**Key decisions**
- **Tokens are counted with one fixed tokenizer** (MiniLM's BERT tokenizer, `chunking.tokenizer`), so
  run 5 (bge-small vs MiniLM) changes only the embedding model, not the chunk boundaries.
  Both models share the same 30,522-word vocabulary anyway.
- **Chunk text is cut from the original string** using the tokenizer's character offsets, not decoded
  from tokens (decoding would lower-case and re-space it). Window edges snap to word boundaries.
- **Heading strategy:** one chunk per markdown section; sections < 50 tokens merge into the next one (and
  the chunk is named after that section); sections > chunk_size are split with the fixed window.
  Headings inside ``` code blocks are ignored. PDFs have no reliable headings -> fixed window.
- **Prefix is applied at index time** (`index_text`), not stored in `text`, so one chunk file serves both
  run 1 and run 4, and the LLM / UI always see clean text.
- **Extra chunk fields:** `char_start`/`char_end` (position in the document) so Phase 6 can match retrieved
  chunks to gold evidence under any chunking strategy; also `token_count`, `chunk_index`.

**Results so far**
- Baseline (fixed 500/50): 2,314 chunks from 380 docs (2,117 markdown, 197 PDF), median 500 tokens.
- **Truncation finding:** MiniLM reads only 256 tokens (254 of text). With 500-token chunks,
  92.6% of chunks are cut off and 46.6% of all chunk tokens are never embedded.
  For comparison: heading-based 25.5% unseen; 250-token chunks 0%; bge-small (512 limit) 0%;
  the prefix makes it slightly worse (48.1%) because it adds ~12 tokens in front.

## Phase 4: Indexing (2026-11-17)

**Built**
- `src/index.py`: embeds chunks into a persistent Chroma collection (cosine distance) and builds a BM25
  index; `vector_search` / `bm25_search` return `(chunk_id, score)` lists; `build_indexes` returns an
  `IndexBundle` for retrieval. CLI `--query` compares both searches side by side.
- `tests/test_index.py`: 11 tests with a fake letter-count embedder (52 total in the repo).

**Key decisions**
- **One collection per index setup** (`<chunking>__<model>__<prefix>`), reused when a stored
  fingerprint of all chunk ids + content hashes matches; otherwise rebuilt. Same idea as Phase 2's cache.
- **`embedding_function=None` on every collection:** Chroma otherwise attaches its own default model and
  would silently download it; we always pass our own vectors.
- **Embeddings are normalized**, so cosine similarity = dot product; scores shown as 1 - distance.
- **Metadata:** Chroma 1.5 accepts lists, so `access_roles` stays a list (`$contains` filter); only
  `None` needs placeholders (`page` -> -1, missing date -> ""). `is_current` stays a boolean so run 8 is
  just `where={"is_current": True}`.
- **BM25 rebuilt in memory** on load (well under a second) instead of pickled to disk: no stale files.
  Plain lower-case word tokens, no stemming or stopword list (no extra libraries).
- **Truncation limit verified:** loading MiniLM checks `max_seq_length` (256) against the table used in
  Phase 3's truncation stats.

**Results so far**
- Baseline collection `fixed-500-50__minilm__noprefix`: 2,314 chunks embedded in ~11 s (Apple MPS);
  reused in 0.2 s on the next run.
- Spot check "How many days do I have to submit an expense claim?": vector search ranks the "90 days"
  chunk 1st; BM25 ranks it 3rd, pulled off course by common words ("days", "have") and an outdated legacy
  agreement. For the exact term "Navan", BM25's top 3 are all relevant. -> motivation for hybrid (run 6).

## Phase 5: Test set (2026-11-17), approved

**Built**
- `eval/questions_source.yaml`: 80 questions (20 lookup, 15 paraphrase, 10 exact_term, 10 multi_doc,
  15 outdated_version, 10 no_answer), each with an expected answer and exact supporting quote(s).
- `src/testset.py`: validates everything against the corpus and writes `eval/questions.jsonl`,
  `eval/questions_review.md` (table) and `eval/gold_review.md` (quotes + gold chunks + checks).
- `data/synthetic/`: 8 deliberately outdated copies of handbook pages (10 changed facts), committed,
  read by ingestion via `paths.synthetic_dir`. Corpus is now 388 documents / 2,325 baseline chunks.
- `tests/test_testset.py` (9 tests) + 1 ingestion test (62 total).

**Key decisions**
- **Automatic gold verification instead of trust:** a quote must appear in its gold doc AND inside a
  single baseline chunk; for non-outdated questions it must NOT appear in any other doc. This rejected
  10 first drafts whose facts were repeated unchanged inside a synthetic old copy.
- **`gold_evidence` (doc + quote) added to each question** so Phase 6 can score chunk-level hits under
  any chunking strategy (chunk ids change between runs; quotes don't). `gold_chunk_ids` = baseline chunks.
- **Two kinds of outdated cases:** 5 real version pairs (old text identical -> tests ranking only) and
  10 synthetic changed facts (old copy gives a wrong answer -> tests answer correctness too).
  `outdated_doc_ids` lists the old versions per question for the stale-rate metric.
- **No-answer topics proven absent** with regex checks scoped to the relevant organisation; the closest
  BM25 hits are recorded (they're same-organisation documents, so declining is genuinely hard).
- **Stratified split, seed 42:** 55 tune / 25 test with every type proportionally in test
  (6/5/3/3/5/3). Test questions are not to be used for any tuning.
- PDF questions always name the organisation (corpus option A: GitLab + labelled external PDFs).

**Known limitations**
- 17/80 questions use GitLab's expenses page (the richest policy page); results lean on that document.
- md-04 and md-08 both combine Middlesex + Waikato leave facts.

## Phase 6: Evaluation + baseline (2026-11-17)

**Built**
- `src/retrieve.py`: `retrieve()` (vector search for now); unimplemented options raise instead of being ignored.
- `src/evaluate.py`: doc/chunk recall@1/3/5 + MRR, stale and fact_stale (+ @5), fact_found, per-type
  table with 95% bootstrap CIs; groups `overall` (no history), `non_outdated`, each type, `history`.
- `run_experiment.py`: saves `metrics.csv`, `per_question.csv`, `run_info.yaml` (truncation, latency),
  `summary.md`, `config.yaml` (committed) and `per_question.jsonl` (git-ignored). Test split needs `--final`.
- `src/compare.py`: side-by-side with CIs + paired per-question better/worse counts with a paired CI.
- `src/make_synthetic.py` + `data/synthetic/changes.yaml`: minimal-edit outdated versions (see below).
- Tests: 88 total.

**Review-driven fixes (measurement and test data, so the baseline was re-run; system unchanged)**
1. *Checked, already fine:* all 80 original quotes sit inside one chunk at 500 and 250 tokens; tokens
   are counted with MiniLM's tokenizer (truncation 46.7% of tokens is correct).
2. *Uncertainty:* 95% bootstrap intervals everywhere, paired comparisons between runs.
3. *Old copies redesigned:* the 8 short excerpt copies favoured themselves in vector search ("short beats
   long"). Now 15 full-page copies with only the listed facts changed (31 changed facts).
4. *version_status:* current / superseded (old version of a live page) / legacy (no replacement:
   13 legacy agreements), so run 8 can separate version handling from legacy-noise removal.
5. *acceptable_doc_ids per evidence item:* old versions stating the SAME answer count as hits, with the
   same rule at doc and chunk level. Outdated quotes must contain the changed fact, so old copies never
   count there. The 5 real-pair questions had no changed fact -> reclassified as lookup (2 replaced
   because their quotes were legal boilerplate repeated in other agreements).
6. *Quote matching:* exact for < 8 words; for 8+ words, a continuous start or end of the quote with >= 80%
   of its words (a quote cut by a chunk boundary). A bag-of-words version produced false matches
   (md-02: scattered common words), so it was tightened.
7. *Ties:* identical text -> identical vectors -> Chroma breaks ties by insertion order (current docs
   first). This made a first re-run show stale 0.09, an artifact. Exact ties now count 0.5.
8. *fact_stale:* compares the chunk with the OLD fact vs the chunk with the CURRENT fact (what the LLM
   would see). Blank when neither is retrieved, with fact_found reporting that share.
9. *Test set v2:* 106 questions, existing splits frozen; 22 outdated questions in tune (was 10),
   5 history questions (gold = the old version) as a sanity check.

10. *Second review round:* deterministic, version-blind tie-breaking (hash of chunk_id; sorting by
    chunk_id would favour "hb:" over "syn:"); fact_stale made the headline version metric with fact_found;
    6 rule-change cases (approval level, allowed/not, who pays, required/optional) + 2 numeric cases;
    test split raised to 14 outdated questions; 2 real_pair checks (real rule changes: Testing Agreement
    feedback "will" -> "may" in v5/current; Cambridge 2023 adds "remote working environment ... within the UK");
    a builder check that stops a synthetic change from silently altering a normal question's quote.
11. *fact_found diagnosis (11 misses):* 8 list items, 3 table rows, 0 prose. Tables extract readably
    (pipe rows), so extraction is not the cause. In 7/11 the right document ranks in the top 7 but other
    chunks of the same long page fill the top 30; truncation contributes (fact in the unseen half for 7/11
    misses vs 5/11 hits); ov-33/34 lose to a different page on the same topic (legal record-retention policy).

12. *Third review round:* rp-02 scored by document order only (`stale_level: doc`; the old draft states no
    competing fact); 7 more history questions (tune 10, test 2); ov-33/34 checked: the legal record-retention
    policy states no retention period for those items, so they are genuine retrieval misses, not conflicts;
    ov-38 and ov-42 change separate bullet points of the co-working section.

**Results: run 1, baseline (fixed 500/50, MiniLM, vector only), tune split, test set v3 (123 questions)**

| | n | chunk R@5 | chunk MRR | doc R@5 | fact_stale | fact_found | stale (doc) |
|---|---|---|---|---|---|---|---|
| overall | 66 | **0.455** [0.33, 0.58] | 0.320 [0.23, 0.41] | 0.735 [0.63, 0.83] | **0.500** [0.29, 0.71] | 0.48 [0.28, 0.68] | 0.545 [0.43, 0.66] |
| non_outdated | 41 | 0.512 [0.35, 0.66] | 0.403 [0.28, 0.53] | 0.793 [0.67, 0.90] | | | |
| outdated_version | 25 | 0.360 [0.20, 0.56] | 0.185 [0.09, 0.29] | 0.640 [0.44, 0.80] | 0.500 | 0.48 | 0.545 |

- **fact_stale 0.50 = a coin flip** on the 12/25 outdated questions where a fact chunk was retrieved:
  old and current versions look identical to search. This is the starting point for runs 8, 9, 9b.
- **fact_found 0.48:** in about half of outdated questions neither version's fact chunk is in the top 30,
  a retrieval failure that version handling cannot fix.
- Outdated doc R@1 fell to 0.08 once ties stopped favouring current docs (the earlier 0.32 was partly
  an index-order artifact).
- Shared 45 questions vs baseline_v1: chunk recall identical; measurement fixes are neutral on them.
- Truncation unchanged: 92.7% of chunks cut, 46.7% of chunk tokens never embedded.
- Depth diagnostic: chunk recall overall 0.455 @5 -> 0.614 @30 -> 0.758 @100 (outdated: 0.36 -> 0.48 -> 0.72).
  The answer chunk is usually in the pool; it just isn't ranked high enough. History (n=10): chunk R@5 0.50.

## Pre-registration for Phase 7 (written 2026-11-17, before any Phase 7 run)

Decided now so results can't steer the analysis afterwards.

**Main metrics (tune split)**
- Retrieval: **chunk_recall@5** on `overall` (primary); chunk_mrr and doc_recall@5 secondary.
- Versions: **fact_stale** (only questions where a fact chunk was retrieved) on outdated_version questions
  (primary), always reported together with **fact_found**; doc-level stale secondary.
- Also reported every run: `non_outdated` chunk_recall@5 (side effects), history and real_pair (sanity,
  too small for conclusions), truncation % and latency.

**When does a change count as an improvement?**
- Only if the **paired 95% bootstrap interval of the per-question difference (run - baseline) excludes
  zero** in the right direction (above zero for recall/MRR/fact_found, below zero for fact_stale).
  Otherwise the result is reported as "no detectable difference", whatever the averages say.
- Better/worse/same question counts are reported for every comparison.
- Guardrail: a version strategy (runs 8, 8b, 9, 9b) does not count as better if it significantly lowers
  `non_outdated` chunk_recall@5 or fact_found, and its history-question results are reported next to it
  (a filter that hides old documents will fail them by design).

**Run plan (fixed; one change per run, each compared with the baseline)**
2 chunk size 250 / 1000 · 2b small-to-big (search 250-token pieces, return the 500-token chunk) ·
3 heading chunks · 4 title/section prefix · 5 bge-small · 6 BM25 hybrid (RRF) · 7 cross-encoder reranker ·
cap: max 2 chunks per version_group in the top results · 8 exclude superseded · 8b exclude legacy ·
9 date-aware rerank · 9b version swap (replace an old-version chunk with the current version's matching chunk).
Tunable settings (e.g. RRF k, date weight, cap size) are tried with at most 3 values each, on tune only.
With this many comparisons some will look significant by chance; results near the boundary are reported as such.

**Test split**
- The 39 test questions stay untouched until the end. **The baseline and the single best tune
  configuration** (by the primary metrics, with the guardrail; ties go to the simpler config) are each run
  **exactly once** on test with `--final`. The baseline run is the reference point; nothing is tuned on it.

### Amendment 1 (2026-11-17, before any Phase 7 run)
- **Diagnostic for every run:** chunk recall@30 and @100 (`eval.diagnostic_depths`), from a deeper
  candidate list, to show whether the answer chunk ever reaches the reranker. Diagnostic only, not a
  success criterion. Baseline: 0.614 @30, 0.758 @100.
- **Run 7b:** cross-encoder reranker over the top **100** candidates instead of 30.
- **Run 12:** two-stage search: pick the top 3 documents first, then search and rerank chunks only within
  them. Motivation: the fact_found diagnosis shows long pages crowding out the fact chunk as the main failure.
- **Note:** the "max 2 chunks per version_group" cap targets near-duplicate versions and multi_doc
  questions, not the long-page problem (that's runs 7b and 12).

## Phase 7a: chunking and embedding experiments (2026-11-18)

**Built**
- Configs: `chunk250`, `chunk1000` (run 2), `small2big` (run 2b), `heading` (3), `prefix` (4), `bge` (5).
- Small-to-big (`retrieval.small_to_big`): each 500-token chunk is split into 250-token pieces (25 overlap)
  in a separate Chroma collection; search ranks pieces and returns each parent chunk once, by its best piece.
- `src/report.py`: one table of all runs vs the reference, every column labelled with its question group;
  paired differences per group; verdicts on the pre-registered main metric.
- Chunk files carry a `.meta.json` (documents hash + content-affecting chunking settings + chunker
  version) and are rebuilt when stale (found because Phase 3 `chunk250`/`heading` files lacked `version_status`).
- Tie tolerance 0.005 for stale/fact_stale (`*_exact` columns keep the identical-score rule).
  **Introduced after seeing bge's 7a result** (gaps of 0.0001-0.003 decided "old wins").
- Cost columns: embedded vectors, HNSW vector-index size on disk, mean search latency. Tests: 100.

**Corrections made before merging**
- The first report's Δ column used ALL answerable questions (incl. history and real_pair) while the level
  column used `overall`. The pre-registration (above) says the main metric is chunk_recall@5 on `overall`,
  defined in the v0.1-baseline code as "all answerable questions except the sanity checks (history,
  real_pair)" (n = 66). Re-computed on that group, **small2big's ✅ disappeared**.
- fact_stale is now paired only on outdated questions where BOTH runs retrieved a fact chunk.
- All 7 runs (baseline included) were re-run after the stale-chunk fix and the tie-tolerance change; the
  baseline's retrieval metrics are identical (max change 0.000000). Version metrics moved with the tie rule:
  stale 0.545 -> 0.477, fact_stale 0.500 -> 0.458, fact_found unchanged 0.48.
- eval/results/baseline/ was re-run with the 0.005 tie rule. The original Phase 6 baseline numbers are preserved in tag v0.1-baseline and in eval/results/baseline_v1/ (baseline_v1 is the first, pre-correction Phase 6 run on the 80-question set; the corrected final Phase 6 baseline is the one in the tag).

**Results (tune; Δ = paired difference from baseline [95% CI], better/worse; – = no detectable difference)**

| run | MAIN Δ chunk R@5 (overall, n=66) | Δ chunk R@5 (non_outdated, n=41) | Δ fact_found (n=25) | vectors | index MB | search ms |
|---|---|---|---|---|---|---|
| baseline (0.455) | | | | 2,468 | 3.7 | 12 |
| chunk250 | -0.038 [-0.14, 0.07] – 6/8 | +0.012 – | +0.04 – | 4,774 | 7.4 | 11 |
| chunk1000 | +0.030 [-0.07, 0.13] – 7/5 | +0.073 – | +0.08 – | 1,330 | 1.8 | 11 |
| small2big | +0.068 [-0.008, 0.152] – 7/2 | **+0.110 [0.024, 0.220] ✅ 5/0** | **+0.24 [0.08, 0.40] ✅** | 7,189 | 16.5 | 20 |
| heading | +0.053 [-0.008, 0.121] – 5/1 | +0.037 – | **+0.28 [0.08, 0.48] ✅** | 4,704 | 7.4 | 11 |
| prefix | +0.015 [-0.07, 0.11] – 6/4 | +0.024 – | +0.04 – | 2,468 | 3.7 | 11 |
| bge | +0.098 [-0.015, 0.212] – 13/5 | +0.110 [-0.01, 0.24] – | +0.20 [0.00, 0.44] – | 2,468 | 3.7 | 14 |

bge vs baseline fact_stale (paired, both found, n=10): exact ties +0.400 [0.10, 0.65] ❌; tolerance 0.005
+0.150 [0.00, 0.40] – . The "bge is worse" effect came from score gaps of 0.0001-0.003.

**Interpretation**
- **No run is a pre-registered improvement on the main metric.** Power: with n = 66 and the observed
  spread of per-question differences (SD ~0.39), the smallest reliably detectable improvement is ~0.13;
  all 7a effects (-0.04 to +0.10) are below that. "No detectable difference" here means "too small for
  this test set to confirm", not "no effect".
- small2big and heading improve secondary measures (non_outdated recall; fact_found) significantly.
- Removing truncation alone (chunk250) doesn't help: twice as many competing chunks, less context each.
- Similarity search cannot tell old from new versions: ties under MiniLM (fact invisible), tiny arbitrary
  gaps under bge.

**Decision: small2big is the Phase 7b base.** Chosen as base because it removes MiniLM truncation, which is
needed for fair tests of the reranker and version runs. **Not a pre-registered improvement on the main
metric** (+0.068 [-0.008, 0.152]). heading and bge are promising but not confirmed. The pre-registered rule
is unchanged. Every 7b run is compared with both the base (small2big) and the original baseline.

### Amendment 2 (2026-11-18, before any Phase 7b run)
- **Expand the tune set by ~60 questions** (lookup, paraphrase, multi_doc), same writing rules, validator
  and approval process; **the test split is untouched**. Before 7b starts, re-run the baseline and all 7a
  runs on the expanded set and report them again.
- **Power note:** with SD of per-question differences ~0.39 (observed in 7a), the smallest improvement
  detectable at 80% power with a 95% interval is about 2.8 x 0.39 / sqrt(n): ~0.13 at n = 66, ~0.11 at
  n = 100, ~0.10 at n = 126, ~0.08 at n = 200. Effects smaller than that will usually read as "–".
- **Base = small2big** (see decision above). Each 7b run is compared with the base AND the original baseline.
- **Step 1: retest on the base, one change each:** bge, heading-as-parent (sections as parent chunks with
  250-token pieces inside them), prefix. Step 1 ends with **bge alone vs. small2big + bge**: if their
  intervals overlap, the final configuration uses the simpler one (bge alone).
- **Step 2: planned runs on the best base from step 1:** 6 hybrid BM25 (RRF), 6b max 2 chunks per
  version_group, 7 reranker top 30, 7b reranker top 100, 12 two-stage search (top 3 documents, then chunks
  within them), 8 exclude superseded, 9 date-aware rerank, 9b version swap.
- **Every run reports:** chunk recall@30 and @100, cost columns (vectors, index MB, search ms), and paired
  fact_stale (both found) plus stale at tie tolerances **0.001, 0.005 and 0.01**. The 0.005 tolerance
  was chosen after 7a; the other two show how much conclusions depend on it.
- Main metric, improvement rule, guardrail and test-split rule are unchanged.

## Test-set expansion (2026-11-18, written BEFORE the new questions are drafted or any run is repeated)

**Purpose and replication plan (fixed now)**
- ~60 new TUNE questions (lookup, paraphrase, multi_doc); the 39 test questions are untouched.
- **The new questions are a replication test of the 7a effects.** They will be drafted without looking at
  any per-question 7a results. After approval, the baseline and all 7a runs are re-run and every paired
  comparison is reported on three groups: the **original 66** `overall` questions, the **new ~60 only**, and
  **combined**. The effects to replicate are: small2big (+0.068 overall, secondary gains), bge (+0.098),
  heading (+0.053, fact_found gain). An effect "replicates" if it has the same sign on the new questions;
  it is "confirmed" only if the combined paired 95% interval excludes zero (unchanged pre-registered rule).
- Results are also reported by question type and by document group, because the new questions
  deliberately use documents that the test split does not.
- **Composition change:** outdated_version questions become a smaller share of `overall`
  (25/66 = 38% now, ~25/126 = 20% after). Overall chunk recall will therefore weigh ordinary retrieval
  more and version handling less; version results are judged on fact_stale / fact_found, not on overall.
- **Paraphrase check:** for every paraphrase question, the share of its content words that also appear in
  the gold quote is computed; any above 40% is rewritten. Distributions for old vs new are reported.
- About a third of the new questions are scenario-style (how an employee would really ask).
- Multi-doc questions must need both documents; scoring is per evidence item (each document counts half).

**Drafted (awaiting approval; no runs repeated yet)**
- 60 new tune questions: 25 lookup (lk-26..50), 20 paraphrase (pp-16..35), 15 multi_doc (md-11..25);
  20 scenario-style (1/3). 36 documents, max 3 new questions each. Test split unchanged (39).
- `overall` grows from 66 to 126; outdated_version share drops from 25/66 (38%) to 25/126 (20%).
- Paraphrase word overlap (content words of the question found in the gold quote; title words ignored):
  old 15: median 0%, max 40%; new 20: median 6%, max 30%. One old question (pp-02, 50%) was reworded,
  so one of the original 66 changed wording.
- Validator additions: overlap > 40% for paraphrase is an error; a quote may be reused only by a
  multi_doc question; every question gets `style` and `doc_group`. It rejected 3 drafts whose quotes
  also appear in unrelated documents (Ireland/France disconnect wording, a tier name).
- 7 of the 36 new-question documents are also used by test questions (different facts).
- Replication groups frozen in `eval/replication_groups.json` before any re-run.

**Revision after review (still before any re-run)**
- **pp-02 reworded inside the frozen original-66 group.** Its word overlap with the gold quote was 50%,
  above the 40% paraphrase limit adopted for this expansion (it shared "co-working", "month", "home",
  "internet"). New wording: "If the company covers a shared office desk for me all month, can I also get my
  broadband at home paid for?" (overlap 22%). Same fact, same gold; only the wording changed. Its 7a
  results were computed on the old wording, so the original-66 comparison includes this one change.
- **Fact independence check (validator):** two evidence items are the same fact if they come from the same
  document and one quote contains the other, or (when their numbers don't differ) they share >= 60% of their
  content words. Applies to all question types. Pairs involving a new question are errors; pairs among the
  original 123 are reported only (the test split can't change).
  Result on all 183: 42 pairs before the revision (12 among the original 123, 30 involving new questions,
  all through the first 15 new multi_doc questions); after: **0 involving new questions**; the 12 original
  pairs remain (10 are old multi_doc questions reusing lookup/exact_term facts, plus lk-04/ov-38 and md-04/md-08).
- **All 15 new multi_doc questions replaced** with pairs built only from facts no other question uses, and
  where the two facts differ (no "both the same" answers).
- pp-24 and pp-32 rewritten with specific answers (pp-32's old quote "Changes are approved by appropriate
  stakeholders" was generic process wording; similar phrasing appears in 3 documents).
- **lk-47 corrected:** the St Andrews rule is that leave *carried forward from the previous year* is lost if
  not used by 31 December; the first draft implied all unused leave is lost.

**Further changes approved before any re-run (2026-11-18)**
- **New question type `compound`** (added before any re-run): two UNRELATED facts from two documents in one
  question (md-12, md-13, md-14, md-15, md-21, md-23, md-25). multi_doc now means two RELATED facts that
  are compared or combined (md-01..11, md-16..20, md-22, md-24). compound is its own row and stays in
  `overall` and `non_outdated`.
- **Cluster bootstrap for all verdicts from now on.** Linked questions are resampled together: the 12
  reported same-fact pairs, plus questions whose gold quotes fall in the same baseline chunk. Each connected
  group of linked questions is one cluster; unlinked questions are their own cluster.
- **Candidate future run (not in 7b): query splitting for compound questions** - split a two-part question
  into two sub-queries, retrieve for each, merge the results. Listed only; not pre-registered.

**Results on the expanded tune set (2026-11-18; cluster bootstrap; reference = baseline)**

Clusters: 12 same-fact pairs + 124 same-chunk pairs -> 105 clusters overall; the 126 `overall` tune
questions form **75 clusters** (largest 15). Baseline: chunk R@5 0.496 [0.40, 0.59], R@100 0.806.
With ~75 independent units the detectable effect is still ~0.13 (2.8 x 0.39 / sqrt(75)): the expansion
added questions but, because many share chunks, much less independent evidence than hoped.

| run | Δ chunk R@5 original-66 | Δ new-60 | Δ combined (MAIN) | Δ non_outdated | Δ fact_found |
|---|---|---|---|---|---|
| chunk250 | -0.038 – | -0.067 – | -0.052 [-0.14, 0.05] – | -0.035 – | +0.04 – |
| chunk1000 | +0.015 – | +0.125 [0.00, 0.25] – | +0.067 [-0.02, 0.14] – | **+0.094 [0.005, 0.17] ✅** | +0.08 – |
| small2big | +0.068 – | +0.008 – | +0.040 [-0.02, 0.11] – | +0.050 – | **+0.24 [0.08, 0.44] ✅** |
| heading | +0.038 – | **-0.125** [-0.25, 0.00] – | -0.040 [-0.12, 0.03] – | -0.069 – | **+0.28 [0.08, 0.50] ✅** |
| prefix | +0.015 – | +0.075 – | +0.044 [-0.02, 0.11] – | +0.054 – | +0.04 – |
| bge | +0.098 – | +0.000 – | +0.052 [-0.05, 0.16] – | +0.045 – | +0.20 – |

**Replication verdicts (pre-registered above):**
- small2big: same sign on new questions (+0.008) -> "replicates" only in the weakest sense; effect is
  near zero on new questions. Not confirmed (combined interval includes zero). Its fact_found gain holds.
- bge: no replication (+0.000 on new). Not confirmed.
- heading: reversed (-0.125 on new). Not confirmed; its fact_found gain holds.
- chunk1000 (not one of the three effects under test): +0.125 on new, +0.094 non_outdated ✅ - a new,
  unpredicted result, treated as exploratory (one of many comparisons), not as a finding.
- **No run is a pre-registered improvement on the main metric.** The 7a "promising" effects were largely
  specific to the original 66 questions.

By document group (baseline chunk R@5): total-rewards 0.74, pdf 0.67, security 0.38, finance 0.36,
people-policies 0.29, support 0.20, hiring 0.17 - long policy pages (finance/expenses, security) are hard,
short benefit pages are easy. Compound (n=7, 5 clusters) 0.43; multi_doc (n=15, 8 clusters) 0.57.

**Consequence for 7b (decision unchanged, reasoning restated):** small2big stays the 7b base because it
removes truncation (measurement validity), not because of a recall gain - which did not replicate.

## Phase 7b: decisions recorded before any 7b run (2026-11-18)

- **Power decision:** we accept that only effects of about **0.13 or more** (chunk R@5, `overall`, ~75
  clusters) can be confirmed on the tune split. No more tune questions will be added. Smaller effects
  will be reported as "no detectable difference".
- **chunk1000 is not part of 7b.** Its non_outdated gain on the expanded set stays exploratory.
- **Intervals:** reports show the plain per-question interval next to the cluster interval for context;
  **all verdicts use the cluster interval**.
- **Run 8b (exclude legacy) is kept**, as in the original pre-registration (Amendment 2 did not remove it).
- **Candidate second research question:** *How reliable are chunking comparisons on small RAG test sets?*
  Evidence so far: (1) none of the 7a effects under test replicated on 60 new questions (bge +0.098 -> +0.000,
  heading +0.038 -> -0.125, small2big +0.068 -> +0.008); (2) gold-chunk sharing reduced 126 questions to
  75 independent clusters, so adding questions bought much less precision than their count suggests.

### End-of-Phase-7 checklist
- [ ] Decide whether to add **test-split questions with unique gold chunks** before the single test run
      (the test split has never been run; adding questions now would not leak results).
- [ ] Comparison table and charts across all Phase 7 runs.
- [ ] Choose the single best tune configuration (primary metrics + guardrail; ties -> simpler).
- [ ] Run the baseline and the chosen configuration once each on test with `--final`.
- [ ] Tag "retrieval done".

## Phase 7b step 1: retests on the small2big base (2026-11-18; tune; cluster intervals, 75 clusters)

| run | vs base small2big: Δ main chunk R@5 | vs baseline: Δ main | vs baseline: Δ non_outdated | vs baseline: Δ fact_found | level | vectors / MB / ms |
|---|---|---|---|---|---|---|
| small2big (base) | | +0.040 [-0.02, 0.11] – | +0.050 – | +0.24 ✅ | 0.536 | 7,189 / 16.5 / 15 |
| bge (no small2big) | | +0.052 [-0.05, 0.16] – | +0.045 – | +0.20 – | 0.548 | 2,468 / 3.7 / 9 |
| s2b_bge | -0.008 [-0.08, 0.06] – | +0.032 – | +0.050 – | +0.12 – | 0.528 | 7,189 / 16.5 / 17 |
| s2b_heading | -0.028 [-0.11, 0.05] – | +0.012 – | -0.025 – | +0.28 ✅ | 0.508 | 7,515 / 20.4 / 12 |
| s2b_prefix | +0.052 [-0.02, 0.12] – | +0.091 [0.000, 0.179] – (boundary) | **+0.094 ✅** | +0.16 – | 0.587 | 7,189 / 16.5 / 16 |

- **No step-1 change is an improvement over the base** (no cluster interval excludes zero).
- **Decision rule "bge alone vs small2big + bge":** s2b_bge - bge = -0.020 [-0.101, 0.052] (10/14): the
  intervals overlap, so by the pre-registered rule the simpler configuration, **bge alone**, is preferred over
  small2big + bge.
- s2b_prefix has the highest level (0.587) and is significant vs the baseline on non_outdated, but its main
  interval vs the baseline touches zero and it is not better than its own base.
- **Tie-tolerance sensitivity (fact_stale vs baseline):** bge-based runs look worse at tolerance 0.001
  (bge +0.35 [0.14, 0.60], s2b_bge +0.44 [0.19, 0.65]) but not at 0.01 (+0.05, +0.11). The "bge prefers old
  versions" effect lives entirely in score gaps between 0.001 and 0.01 - wording/boundary noise, as in 7a.
- Cross-check: all runs truncation-free except s2b_prefix (3.6% of piece tokens over MiniLM's limit).
- **Open decision (for the user): which configuration is the base for step 2.**

### Amendment 3 (2026-11-18, before any step-2 run; written before the paired recall@100 test was computed)
- **Step-2 base rule:** step-2 base = **bge alone**, unless small2big's chunk recall@100 is significantly higher
  than bge's (paired cluster interval excludes zero). In that case the base is small2big, because the reranker
  and two-stage search can't recover chunks that never reach them.
  Disclosure: the two point estimates (small2big 0.881, bge 0.873) were already printed in the step-1 report
  output; the paired cluster test had not been computed when this rule was written.
- **Run 6 (hybrid BM25 + vector, RRF): k = 60 is the pre-registered setting.** k = 10 and k = 100 are
  exploratory only.
- **New pre-registered run 6p: chosen base + title/section prefix**, reporting its truncation % against the
  embedding model's limit (512 tokens for bge, 256 for MiniLM).
- **Version verdicts:** tie tolerance **0.005 is primary**; 0.001 and 0.01 are sensitivity checks only.
- Reranker scores (runs 7, 7b, 12) are cross-encoder logits, not cosine similarities, so the 0.005 tie
  tolerance is applied on that scale; the sensitivity checks show whether this matters.
- **Rule applied:** small2big - bge, chunk recall@100 = +0.008, cluster [-0.054, 0.070] (8 better / 8 worse);
  recall@30 = +0.004 [-0.064, 0.081]. Interval includes zero -> **step-2 base = bge alone**.
- **Run definitions confirmed (2026-11-18):** run 8 excludes `version_status = superseded` only (old versions
  of pages that still have a current version). Run 8b excludes `version_status = legacy` only (old documents
  with no current replacement).
- **Legacy check (before the version branch):** no question's gold, acceptable or outdated document is legacy
  (13 legacy docs, all old legal agreements, none used by any question). rp-01's old Testing Agreement versions
  v1-v5 are *superseded*, not legacy. So 8b removes no question's only source; it can only remove noise.
  If that ever changes, those questions are reported separately under 8b.
- **History questions under run 8:** all 12 history questions (10 tune, 2 test) have a superseded gold
  document, so run 8 removes their only source **by design**. They will be reported explicitly under run 8
  as the cost of filtering (expected to drop to 0).

## Phase 7b step 2 results (2026-11-18; tune; base = bge; cluster intervals; 126 questions / 75 clusters)

| run | vs bge: Δ MAIN chunk R@5 | vs bge: Δ non_outdated | vs bge: Δ fact_found | vs baseline: Δ MAIN | R@5 | R@100 | search ms |
|---|---|---|---|---|---|---|---|
| bge (base) | | | | +0.052 – | 0.548 | 0.873 | 11 |
| 6p bge_prefix | +0.056 [-0.01, 0.12] – (14/7) | +0.050 – | +0.04 – | **+0.107 ✅** | 0.603 | 0.897 | 8 |
| **6 hybrid (k=60)** | **+0.135 [0.06, 0.22] ✅ (24/7)** | **+0.109 ✅** | **+0.24 ✅** | **+0.187 ✅** | **0.682** | **0.944** | 18 |
| 6b cap2 | -0.048 [-0.09, 0.00] – (3/11) | **-0.069 ❌** | **-0.20 ❌** | +0.004 – | 0.500 | 0.607 | 9 |
| **7 rerank top 30** | **+0.123 [0.05, 0.21] ✅ (23/7)** | **+0.114 ✅** | +0.00 – | **+0.175 ✅** | 0.671 | 0.873 | 294 |
| **7b rerank top 100** | **+0.151 [0.07, 0.24] ✅ (27/8)** | **+0.149 ✅** | +0.12 – | **+0.202 ✅** | **0.698** | 0.873 | 713 |
| 12 two-stage | +0.067 [0.00, 0.14] ✅ (16/8; lower bound just above 0) | +0.094 ✅ | +0.04 – | +0.119 ✅ | 0.615 | 0.758 | 406 |
| exploratory: hybrid k=10 / k=100 | +0.131 / +0.135 (both ✅) | | | | | | |

**First pre-registered improvements on the main metric:** hybrid (6), reranker top 30 (7) and top 100 (7b),
all with effects (+0.12 to +0.15) at or above the ~0.13 detectable size, and two-stage (12) just clearing zero.

**Interpretation**
- **Hybrid works because BM25 finds what embeddings miss** (exact names, numbers, policy terms): R@100 rises
  from 0.873 to 0.944 and fact_found from 0.68 to 0.92. RRF k barely matters for recall (10/60/100 all ~+0.13);
  k = 10 made fact_stale worse (exploratory, +0.27 ❌), k = 60/100 did not.
- **The reranker reorders the same candidates better:** R@100 is unchanged (same pool) but R@5 rises from
  0.548 to 0.671 (top 30) and 0.698 (top 100). Looking at 100 candidates instead of 30 adds +0.03 over run 7,
  at 2.4x the latency (713 vs 294 ms).
- **The cap hurts:** limiting each document to 2 chunks removes relevant chunks of long pages (R@100 0.873 ->
  0.607, fact_found ❌). The long-page problem needs better ranking, not fewer chunks per page.
- **Two-stage (12): not robust, not carried forward.** It helps less than the plain reranker: choosing only 3 documents first loses answers in other
  documents (R@100 0.758 < 0.873).
- **bge + prefix (6p): not robust, not carried forward.** Significant vs the baseline but not vs bge
  (+0.056 –); the gain over the baseline is mostly bge's.
- **[WITHDRAWN by Amendment 3b: invalid tolerance values for hybrid/reranker runs; re-reported on the rank
  scale below]** Version side effects (fact_stale, primary tolerance 0.005): no step-2 run changes fact_stale
  significantly vs bge. vs the original baseline, rerank100 looks worse (+0.36 [0.06, 0.60] ❌; +0.23 n.s. at
  tolerance 0.01): the cross-encoder breaks the old/new near-ties decisively, and with n = 11 the direction
  is noisy. Version handling is the job of runs 8, 8b, 9, 9b.
- **Cross-encoder truncation:** 83% of chunks exceed its 512-token budget with a median question (18 tokens),
  but only by ~8.5 tokens each: 1.5% of chunk text is unread. Minor.
- Multiple comparisons: hybrid and reranker effects are large and consistent across k values and candidate
  counts, so chance is an unlikely explanation for them; two-stage and bge_prefix are near the boundary.

### Amendment 3b (2026-11-18, written BEFORE the re-run results were seen): staleness is measured by rank

**Reason.** The 0.005 tie tolerance was designed for cosine similarities (0-1 scale), where gaps that small are
wording noise. It does not apply to other score scales:
- **Hybrid (RRF):** scores are 1/(k + rank), so neighbouring ranks differ by ~0.0003. At 0.005, 100% of found
  hybrid pairs were "ties", which made hybrid's fact_stale a constant 0.5.
- **Reranker / two-stage:** scores are cross-encoder logits (unbounded). A sigmoid doesn't fix this, because it
  compresses confident scores (logits 8 vs 10 become 0.9997 vs 0.99995, which is a "tie"), so the same tolerance
  means something different at each point of the curve.

**Changes.**
- **Primary for every run (cosine runs included):** `stale`, `stale@5`, `fact_stale` and `fact_stale@5` are
  decided by rank alone. Exact score ties are already ordered by the chunk_id-hash tie-break, so every run uses
  one scale and no run gets 0.5 tie credit that another can't get.
- **Secondary, cosine runs only:** the tolerance versions (`*_t001`, `*_t005`, `*_t01`). For hybrid, reranker
  and two-stage runs they are left empty.
- The primary tolerance of 0.005 from Amendment 2 now applies only to that secondary detail.

**Withdrawn.** The earlier statements "no step-2 run changes fact_stale significantly vs bge" and "rerank100
looks worse than the baseline on fact_stale (+0.36 ❌)" are withdrawn. They paired cosine runs (mostly ties at
0.5) with hybrid and reranker runs that had invalid or non-comparable tolerance values. The step-1 and step-2
fact_stale results will be re-reported on the rank scale.

### Step 1 + 2 version metrics re-reported on the rank scale (after Amendment 3b; all 14 runs re-run)

Retrieval didn't change, so every chunk/doc recall number above is identical (the step-1 decision stands:
small2big vs bge R@100 +0.008 [-0.054, 0.070] -> base = bge).

| run | fact_stale (rank) | doc stale (rank) | fact_found | Δ fact_stale vs bge (both found) | tolerance 0.001/0.005/0.01 (cosine only) |
|---|---|---|---|---|---|
| baseline | 0.667 | 0.591 | 0.48 | | 0.42 / 0.46 / 0.50 |
| small2big | 0.722 | 0.636 | 0.72 | | 0.58 / 0.50 / 0.56 |
| bge | 0.765 | 0.696 | 0.68 | | 0.68 / 0.53 / 0.53 |
| bge_prefix | 0.611 | 0.652 | 0.72 | -0.176 [-0.40, 0.00] – (3/0, n=17) | 0.56 / 0.47 / 0.50 |
| hybrid | 0.739 | 0.667 | 0.92 | +0.059 [-0.14, 0.22] – (1/2, n=17) | n/a |
| cap2 | 0.917 | 0.696 | 0.48 | +0.000 (n=12) | 0.79 / 0.54 / 0.54 |
| rerank30 | 0.647 | 0.522 | 0.68 | -0.118 [-0.44, 0.21] – (5/3, n=17) | n/a |
| rerank100 | 0.650 | 0.500 | 0.80 | -0.118 [-0.44, 0.21] – (5/3, n=17) | n/a |
| twostage | 0.611 | 0.500 | 0.72 | -0.214 [-0.57, 0.14] – (5/2, n=14); doc stale -0.333 ✅ | n/a |

- **No run changes fact_stale significantly** vs bge or vs the baseline on the rank scale (now a valid
  statement). The reranker runs point the right way (old fact first 65% vs 77%), n = 17 is too small to say.
- **Every run is stale most of the time:** with rank alone, the old fact comes first in 61-92% of found
  pairs. The near-identical synthetic copies are a coin flip at best for every ranker: version handling
  (runs 8-9b) is needed, retrieval quality alone doesn't fix it.
- **Sigmoid sensitivity (rejected):** with sigmoid(logit) and the cosine tolerances, 50-88% of reranker pairs
  become "ties", because confident logits saturate. That confirms the reason for rank-only.
- 7a-only result folders (chunk250, chunk1000, heading, prefix) were not re-run and keep the old columns;
  they are not used in any Phase 7b comparison.

**Replication (main metric vs bge):** hybrid is ✅ on both the original 66 (+0.121) and the new 60 (+0.150).
rerank30 / rerank100 are + on the original 66 (+0.106 / +0.114, intervals just include 0) and ✅ on the new 60
(+0.142 / +0.192): same sign, so they replicate; confirmed on the combined 126.

**Document groups (chunk R@5, small groups are noisy):** hybrid and the reranker help in different places.
Hybrid is strongest on handbook pages (finance 0.44 -> 0.64, hiring 0.33 -> 0.83, total-rewards 0.72 -> 0.91)
but slightly worse on PDFs (0.72 -> 0.65); the reranker gains on PDFs (0.72 -> 0.82). people-policies stays at
0.29 for every run (n = 7): a candidate for the failure analysis.

### Replication of the 7b effects, under the rule as written

The rule (Test-set expansion section, fixed before the new questions were drafted): *"An effect 'replicates'
if it has the same sign on the new questions; it is 'confirmed' only if the combined paired 95% interval
excludes zero (unchanged pre-registered rule)."*

| run (vs bge, chunk R@5) | original 66 | new 60 | same sign? | combined 126 | verdict |
|---|---|---|---|---|---|
| hybrid | +0.121 ✅ | +0.150 ✅ | yes | +0.135 ✅ | replicates, confirmed (significant in both groups on its own) |
| rerank30 | +0.106 – | +0.142 ✅ | yes | +0.123 ✅ | replicates, confirmed |
| rerank100 | +0.114 – | +0.192 ✅ | yes | +0.151 ✅ | replicates, confirmed |

No conclusion depends on the ambiguities below: hybrid passes under any reading. No new replication round.

### Check: do old/current fact chunks differ in anything besides the changed fact? (before the version runs)

- **Documents:** after undoing the listed replacements, every synthetic old version is character-identical to
  its current page (15/15), with the same chunk count. Generation is exact, and there is nothing to fix there.
- **Chunks:** 121 of 154 aligned chunk pairs are identical once the fact is undone. The other 33 (in 3 documents:
  expenses, phishing, inc-benefits-us) differ by 2-5 words at the chunk edges, out of ~370 words. The cause is
  fixed-size token chunking, not generation: a replacement that changes the token count ("allowable" ->
  "not reimbursable") shifts every later window. 8 fact chunks are affected.
- **Do the shifts explain the old-first lean? No.** On tune questions whose fact-chunk pairs are identical, the
  old fact still comes first in 59-78% of pairs (baseline 0.78 n=9, bge 0.73 n=15, hybrid 0.78 n=18,
  rerank30 0.60 n=15, rerank100 0.59 n=17).
- **Decision:** no regeneration and no re-run.
- **Finding:** all rankers prefer the OLD fact in most near-identical pairs (61-92% overall; 59-78% when the
  texts are identical apart from the fact). Nothing in the text marks which version is current, so the
  rankers' preference is arbitrary in direction. Only version-aware handling (runs 8-9b) can fix it.
  Small n, and pairs cluster on a few documents (expenses supplies many), so the size of the lean is uncertain.

### Methodology frozen for the rest of Phase 7 (2026-11-18)

No more metric or methodology changes in Phase 7, unless a bug would change a headline conclusion. Anything
smaller goes into the list below.

### Limitations

1. **The replication rule was written for the 7a effects.** Applying it to 7b effects (hybrid, reranker)
   extends it to effects first measured after the new questions existed, so the new 60 are not a true
   out-of-sample replication for 7b.
2. **"Same sign" doesn't require the original-66 effect to be significant** (the reranker's isn't), and the
   combined interval includes the original 66, so "confirmed" is not independent of them.
3. **Chunk-edge shifts:** 8 synthetic fact chunks differ from their current version by 2-5 edge words (fixed-size
   chunking after length-changing replacements). They are shown not to explain the old-first lean.
4. **Few staleness pairs:** fact_stale pairs only n = 10-23 questions in 8-14 clusters, so only large effects
   are detectable.
5. **The cross-encoder doesn't read ~1.5% of chunk text** (512-token limit).
6. **Small document groups** (support n=5, hiring n=6, people-policies n=7, legal n=1) are descriptive only.
7. **Step-1/2 multiplicity:** 9 step-2 comparisons with no correction. hybrid and the reranker are robust to
   this; two-stage and bge_prefix were not carried forward partly for this reason.
8. **7a-only result folders** (chunk250, chunk1000, heading, prefix) keep the old tolerance-based stale
   columns. No 7b comparison uses them.
