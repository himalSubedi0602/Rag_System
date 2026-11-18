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
