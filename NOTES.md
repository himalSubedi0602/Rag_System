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
