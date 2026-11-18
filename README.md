# RAG System: Evaluating Retrieval Over Versioned Company Documents

A local question-answering system over ~300–500 company-style documents (GitLab public handbook
plus public policy PDFs). Answers come with `[1]`, `[2]` citations, or the system declines with
"I couldn't find this in the documents."

**Main focus: evaluation.** Retrieval is measured separately from answer generation.

**Research question:** when outdated and current versions of a policy both exist, how often does
the system use the old one, and which fix reduces that more: filtering to current versions or
date-aware reranking?

## Findings

_TODO (Phase 10): headline results._

## Results

_TODO (Phase 7–8): comparison table across runs 1–10 and charts._

## Failure analysis

_TODO (Phase 8): counts per failure category with examples._

## Limitations

_TODO (Phase 10)._

## How it works

```
Offline: load files -> extract text + metadata -> detect versions -> chunk -> embed + BM25 index -> chunk store
Online:  question -> vector + BM25 search (top 30 each) -> reciprocal rank fusion
         -> cross-encoder rerank (top 5) -> decline if best score < threshold
         -> LLM answers from those chunks only, with citations -> log everything
```

## How to run

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

### Data

Raw documents are **not** committed to git. Every source is listed in
[data/sources.yaml](data/sources.yaml); one command downloads them into `data/raw/`:

```bash
python -m src.download_data
python -m src.ingest
python -m src.inspect_docs --n 5
python -m src.chunking configs/baseline.yaml
python -m src.index configs/baseline.yaml --query "How many days do I have to submit an expense claim?"
python -m src.testset
```

- **Handbook:** selected sections of the [GitLab public handbook](https://gitlab.com/gitlab-com/content-sites/handbook)
  (people policies, total rewards, hiring, finance, legal, security policies, support licensing):
  393 markdown files, each with its last-commit date from the GitLab API.
- **PDFs:** 20 public policy documents from UK/NZ universities and councils (annual leave, sickness
  absence, hybrid working, whistleblowing, travel and expenses, data protection, IT acceptable use).
- Ingestion writes `data/processed/documents.jsonl` (380 documents after dropping 33 near-empty pages).

### Run an experiment

```bash
python run_experiment.py configs/baseline.yaml   # available from Phase 6
```

Each experiment is one YAML file in `configs/` that lists only what it changes from
`configs/default.yaml`. To print the final merged config:

```bash
python -m src.config configs/baseline.yaml
```

## Repo layout

```
data/raw/            source documents (git-ignored)
data/processed/      extracted text and chunk store (git-ignored)
data/synthetic/      hand-made outdated policy copies for evaluation (committed)
configs/             default.yaml + one YAML per experiment
src/                 pipeline code (config, ingest, chunking, index, retrieve, generate, evaluate)
eval/questions.jsonl test set (built from eval/questions_source.yaml by src/testset.py)
eval/results/<run>/  per-run metrics (CSV) and charts
tests/               pytest tests
NOTES.md             build log: decisions and results per phase
```
