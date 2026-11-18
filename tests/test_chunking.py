"""Tests for src/chunking.py."""

import pytest

from src.chunking import (
    chunk_document,
    find_headings,
    get_tokenizer,
    heading_spans,
    index_text,
    strategy_key,
    truncation_stats,
    window_spans,
)

TOKENIZER_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SPEC_FIELDS = {"chunk_id", "doc_id", "doc_title", "version_group", "is_current", "source_type",
               "source_path", "section_path", "page", "updated_date", "department", "access_roles",
               "content_hash", "chunk_strategy", "text"}


def word_offsets(n: int) -> list[tuple[int, int]]:
    """Offsets for n one-letter words separated by spaces: 'a a a ...' -> [(0,1), (2,3), ...]."""
    return [(2 * i, 2 * i + 1) for i in range(n)]


def make_doc(pages, source_type="markdown", doc_id="hb:test/doc"):
    """Minimal document record as produced by ingestion."""
    return {
        "doc_id": doc_id, "doc_title": "Test Policy", "version_group": doc_id, "is_current": True,
        "version_status": "current",
        "source_type": source_type, "source_path": "handbook/test/doc.md", "updated_date": "2025-01-01",
        "department": "finance", "access_roles": ["finance"],
        "pages": [{"page": (i + 1 if source_type == "pdf" else None), "text": t} for i, t in enumerate(pages)],
    }


def cfg(strategy="fixed", size=500, overlap=50, min_section=50):
    return {"strategy": strategy, "chunk_size": size, "chunk_overlap": overlap,
            "min_section_tokens": min_section, "add_prefix": False, "tokenizer": TOKENIZER_NAME}


@pytest.fixture(scope="module")
def tokenizer():
    return get_tokenizer(TOKENIZER_NAME)


# --- sliding window --------------------------------------------------------------

def test_window_spans_size_and_overlap():
    # 10 tokens, windows of 4, overlap 1 -> step 3
    assert window_spans(word_offsets(10), 0, 10, size=4, overlap=1) == [(0, 4), (3, 7), (6, 10)]


def test_window_spans_short_input_is_one_window():
    assert window_spans(word_offsets(3), 0, 3, size=4, overlap=1) == [(0, 3)]


def test_window_spans_never_splits_a_word():
    # "reimbursement" split into 3 pieces with no space between them: tokens 3, 4, 5.
    offsets = [(0, 1), (2, 3), (4, 5), (6, 9), (9, 12), (12, 19), (20, 21), (22, 23)]
    spans = window_spans(offsets, 0, len(offsets), size=4, overlap=0)
    for a, b in spans:
        assert a == 0 or offsets[a][0] > offsets[a - 1][1]          # starts at a word start
        assert b == len(offsets) or offsets[b][0] > offsets[b - 1][1]  # ends at a word end
    covered = sorted({t for a, b in spans for t in range(a, b)})
    assert covered == list(range(len(offsets)))                      # nothing lost


# --- headings --------------------------------------------------------------------

def test_find_headings_builds_paths_and_ignores_code():
    text = "# Expenses\nintro\n## Travel\n### Hotels\n```bash\n# not a heading\n```\n## Meals\n"
    paths = [h.path for h in find_headings(text)]
    assert paths == ["Expenses", "Expenses > Travel", "Expenses > Travel > Hotels", "Expenses > Meals"]


def test_find_headings_strips_emphasis():
    assert find_headings("## **Bold** heading ##\n")[0].path == "Bold heading"


def test_heading_spans_merges_tiny_and_splits_big():
    # Sections (token ranges): [0,2) tiny intro, [2,30) normal, [30,100) big, [100,103) tiny last.
    offsets = word_offsets(103)

    class H:  # stand-in for Heading: only char_pos is used here
        def __init__(self, token):
            self.char_pos = offsets[token][0]

    spans = heading_spans(offsets, [H(2), H(30), H(100)], size=40, overlap=5, min_tokens=5)
    assert spans[0] == (0, 30, 2)                      # tiny intro merged forward, named after section 2
    assert spans[1][:2] == (30, 70)                    # big section split into windows ...
    assert spans[-1][1] == 103                         # ... and the tiny last section attached to it
    assert all(b - a <= 40 for a, b, _ in spans[1:])


# --- full documents --------------------------------------------------------------------

def test_fixed_chunks_keep_original_text_and_overlap(tokenizer):
    sentences = " ".join(f"Rule {i}: Expense claims over ${i}0 need Manager approval." for i in range(60))
    chunks = chunk_document(make_doc([sentences]), cfg(size=100, overlap=20), tokenizer)
    assert len(chunks) > 3
    for c in chunks:
        assert c["text"] in sentences            # exact slice: capitals and "$" kept, not lower-cased
        assert c["token_count"] <= 100
    # Overlap: the end of each chunk reappears at the start of the next one.
    for prev, nxt in zip(chunks, chunks[1:]):
        assert nxt["char_start"] < prev["char_end"]


def test_chunks_have_all_spec_fields(tokenizer):
    [chunk] = chunk_document(make_doc(["## Travel\nHotels are capped at $200 per night."]), cfg(), tokenizer)
    assert SPEC_FIELDS <= set(chunk)
    assert chunk["chunk_id"] == "hb:test/doc::fixed-500-50::0"
    assert chunk["section_path"] == "Travel"
    assert chunk["access_roles"] == ["finance"]


def test_heading_strategy_one_chunk_per_section(tokenizer):
    body = " ".join(["Staff must follow this rule carefully."] * 12)  # ~70 tokens per section
    text = f"# Policy\n\n## Travel\n{body}\n\n## Meals\n{body}\n"
    chunks = chunk_document(make_doc([text]), cfg("heading", min_section=20), tokenizer)
    assert [c["section_path"] for c in chunks] == ["Policy > Travel", "Policy > Meals"]
    assert chunks[1]["text"].startswith("## Meals")
    assert chunks[0]["chunk_strategy"] == "heading-500-50-min20"


def test_pdf_chunks_track_pages_and_ignore_heading_strategy(tokenizer):
    page1 = " ".join(["Annual leave must be booked in advance."] * 30)
    page2 = " ".join(["Sick leave must be reported by 9am."] * 30)
    doc = make_doc([page1, page2], source_type="pdf", doc_id="pdf:x")
    fixed = chunk_document(doc, cfg(size=100, overlap=10), tokenizer)
    heading = chunk_document(doc, cfg("heading", size=100, overlap=10), tokenizer)
    assert fixed[0]["page"] == 1 and fixed[-1]["page"] == 2
    assert [c["text"] for c in heading] == [c["text"] for c in fixed]  # PDFs fall back to fixed
    assert all(c["section_path"] == "" for c in fixed)


# --- prefix, truncation, naming ------------------------------------------------------------

def test_index_text_prefix():
    chunk = {"doc_title": "Expenses", "section_path": "Travel > Hotels", "text": "Max $200."}
    assert index_text(chunk, add_prefix=False) == "Max $200."
    assert index_text(chunk, add_prefix=True) == "Expenses > Travel > Hotels\n\nMax $200."
    assert index_text({**chunk, "section_path": ""}, add_prefix=True) == "Expenses\n\nMax $200."


def test_truncation_stats():
    # limit 12 -> 10 usable text tokens. Chunks of 5, 10, 20 tokens: only the 20 is cut, losing 10.
    stats = truncation_stats([5, 10, 20], max_tokens=12)
    assert stats["usable_tokens"] == 10
    assert stats["chunks_truncated_pct"] == pytest.approx(100 / 3)
    assert stats["tokens_unseen_pct"] == pytest.approx(100 * 10 / 35)


def test_strategy_key():
    assert strategy_key(cfg()) == "fixed-500-50"
    assert strategy_key(cfg("heading", 250, 25, 30)) == "heading-250-25-min30"
