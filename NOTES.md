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
