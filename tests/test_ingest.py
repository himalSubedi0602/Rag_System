"""Tests for src/ingest.py and the include-pattern matcher in src/download_data.py."""

from pathlib import Path

import pymupdf

from src.download_data import matches_include
from src.ingest import (
    assign_versions,
    clean_markdown,
    extract_pdf,
    remove_table_of_contents,
    handbook_doc_id,
    ingest_all,
    load_documents,
    split_front_matter,
    strip_headers_footers,
)

SOURCES = {"access_roles": {"default": ["all_employees"], "by_department": {"legal": ["legal"]}}, "pdfs": []}


# --- markdown ---------------------------------------------------------------

def test_split_front_matter():
    meta, body = split_front_matter('---\ntitle: "Expenses"\ndescription: x\n---\n\n## Rules\nText')
    assert meta == {"title": "Expenses"}  # only keys we use are kept
    assert body.strip().startswith("## Rules")


def test_split_front_matter_key_case_ignored():
    meta, _ = split_front_matter("---\nTitle: GitLab Testing Agreement\n---\nBody")
    assert meta == {"title": "GitLab Testing Agreement"}


def test_split_front_matter_missing():
    meta, body = split_front_matter("# Just a heading\n")
    assert meta == {}
    assert body == "# Just a heading\n"


def test_clean_markdown_removes_markup_keeps_structure():
    raw = (
        "## Travel {#travel}\n"
        "<!-- hidden note -->\n"
        "See [the policy](https://example.com/p) for details.\n"
        "{{< youtube abc >}}\n"
        "<details><summary>More</summary>Inner text</details>\n"
        "![diagram](img.png)\n"
        "| Item | Limit |\n|---|---|\n| Hotel | $200 |\n"
    )
    text = clean_markdown(raw)
    assert text.startswith("## Travel")          # heading kept, anchor removed
    assert "{#travel}" not in text
    assert "hidden note" not in text
    assert "See the policy for details." in text  # link text kept, URL removed
    assert "youtube" not in text
    assert "MoreInner text" in text               # HTML tags removed, inner text kept
    assert "diagram" not in text
    assert "| Hotel | $200 |" in text             # tables untouched


def test_handbook_doc_id():
    assert handbook_doc_id("handbook/finance/expenses.md") == "hb:finance/expenses"
    assert handbook_doc_id("handbook/finance/_index.md") == "hb:finance"


# --- PDF ----------------------------------------------------------------------

def test_strip_headers_footers():
    pages = [
        ["ACME Council Leave Policy", f"Body text for page {i}.", "More body.", f"Page {i} of 4"]
        for i in range(1, 5)
    ]
    cleaned = strip_headers_footers(pages)
    for i, lines in enumerate(cleaned, start=1):
        assert lines == [f"Body text for page {i}.", "More body."]


def test_strip_headers_footers_keeps_clause_numbers():
    # "2.1", "3.4", ... at the top of each page all normalize to "#.#" but are real headings.
    pages = [[f"{i}.{i + 1}", "Clause heading", "Body one.", "Body two.", "Body three.", f"Page {i} of 4"]
             for i in range(1, 5)]
    cleaned = strip_headers_footers(pages)
    assert cleaned[1][0] == "2.3"
    assert all(not any(line.startswith("Page") for line in page) for page in cleaned)


def test_strip_headers_footers_leaves_short_docs_alone():
    pages = [["Title", "Body"], ["Title", "Body 2"]]  # < 3 pages: can't tell header from content
    assert strip_headers_footers(pages) == pages


def test_extract_pdf_end_to_end(tmp_path):
    path = tmp_path / "policy.pdf"
    doc = pymupdf.open()
    for i in range(1, 4):
        page = doc.new_page()
        page.insert_text((72, 50), "Example Org - Staff Handbook")
        page.insert_text((72, 200), f"Staff get {20 + i} days of leave in case {i}.")
        page.insert_text((72, 780), f"Page {i} of 3")
    doc.save(path)

    result = extract_pdf(path)
    assert [p["page"] for p in result["pages"]] == [1, 2, 3]
    assert result["pages"][1]["text"] == "Staff get 22 days of leave in case 2."


def test_extract_pdf_drops_table_of_contents_lines(tmp_path):
    path = tmp_path / "toc.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 100), "Contents")
    page.insert_text((72, 120), "Purpose ........................ 3")
    page.insert_text((72, 140), "Staff must book leave in advance.")
    doc.save(path)
    assert extract_pdf(path)["pages"][0]["text"] == "Contents\nStaff must book leave in advance."


# --- versions -----------------------------------------------------------------

def make_record(doc_id, title=None, date="2025-01-01", source_type="markdown", text="body text",
                group=None, current=None):
    """Minimal document record for version tests."""
    return {
        "doc_id": doc_id, "doc_title": title or doc_id, "source_type": source_type,
        "source_path": doc_id.replace("hb:", "handbook/") + ".md", "updated_date": date,
        "version_group": group, "version_number": None, "is_current": current,
        "pages": [{"page": None, "text": text}],
    }


def by_id(records):
    return {r["doc_id"]: r for r in records}


def test_versions_unversioned_file_is_current():
    records = [make_record("hb:legal/testing-agreement-v1"), make_record("hb:legal/testing-agreement-v2"),
               make_record("hb:legal/testing-agreement", date="2020-01-01")]  # oldest date, still current
    assign_versions(records)
    r = by_id(records)
    assert {x["version_group"] for x in records} == {"hb:legal/testing-agreement"}
    assert r["hb:legal/testing-agreement"]["is_current"] is True
    assert r["hb:legal/testing-agreement-v2"]["is_current"] is False
    assert r["hb:legal/testing-agreement-v2"]["version_number"] == 2


def test_versions_legacy_never_current_even_if_newer():
    records = [make_record("hb:finance/legacy-vendor-agreement-v1", date="2026-01-01"),
               make_record("hb:finance/vendor-agreement", date="2024-01-01")]
    assign_versions(records)
    r = by_id(records)
    assert r["hb:finance/vendor-agreement"]["is_current"] is True
    assert r["hb:finance/legacy-vendor-agreement-v1"]["is_current"] is False


def test_versions_deprecated_text_marks_old():
    records = [make_record("hb:legal/ai-terms-v3", text="*deprecated 2025-03-31*\nTerms..."),
               make_record("hb:legal/ai-terms-v4")]
    assign_versions(records)
    r = by_id(records)
    assert r["hb:legal/ai-terms-v4"]["is_current"] is True
    assert r["hb:legal/ai-terms-v3"]["is_current"] is False


def test_versions_mentioning_deprecated_later_is_still_current():
    text = "## Overview\nSometimes customers have trouble.\nPassword login has been deprecated."
    records = [make_record("hb:support/account", text=text)]
    assign_versions(records)
    assert records[0]["is_current"] is True


def test_versions_same_name_without_evidence_not_grouped():
    # Two unrelated pages called "policy" in different folders must not become versions.
    records = [make_record("hb:security/a/policy"), make_record("hb:security/b/policy")]
    assign_versions(records)
    assert all(r["version_group"] == r["doc_id"] for r in records)
    assert all(r["is_current"] for r in records)


def test_versions_explicit_values_win():
    records = [make_record("pdf:x-2022", source_type="pdf", group="pdf:x", current=False, date="2030-01-01"),
               make_record("pdf:x-2023", source_type="pdf", group="pdf:x", current=True, date="2023-01-01")]
    assign_versions(records)
    r = by_id(records)
    assert r["pdf:x-2023"]["is_current"] is True
    assert r["pdf:x-2022"]["is_current"] is False


# --- pipeline: hashing and skipping -----------------------------------------------

def test_ingest_skips_unchanged_files(tmp_path, monkeypatch):
    raw, processed = tmp_path / "raw", tmp_path / "processed"
    page = raw / "handbook" / "legal" / "policy.md"
    page.parent.mkdir(parents=True)
    page.write_text("---\ntitle: Policy\n---\n" + "The rule is simple. " * 20)

    first = ingest_all(raw, processed, SOURCES)
    assert first["extracted"] == 1 and first["skipped_unchanged"] == 0

    second = ingest_all(raw, processed, SOURCES)
    assert second["extracted"] == 0 and second["skipped_unchanged"] == 1

    page.write_text("---\ntitle: Policy\n---\n" + "The rule changed. " * 20)
    third = ingest_all(raw, processed, SOURCES)
    assert third["extracted"] == 1

    # Changing the extractor code (simulated by bumping its version) also forces re-extraction.
    monkeypatch.setattr("src.ingest.EXTRACTOR_VERSION", 999)
    fourth = ingest_all(raw, processed, SOURCES)
    assert fourth["extracted"] == 1

    [doc] = load_documents(processed)
    assert doc["doc_title"] == "Policy"
    assert doc["department"] == "legal"
    assert doc["access_roles"] == ["legal"]
    assert "The rule changed." in doc["pages"][0]["text"]


def test_ingest_drops_near_empty_pages(tmp_path):
    raw, processed = tmp_path / "raw", tmp_path / "processed"
    (raw / "handbook" / "hr").mkdir(parents=True)
    (raw / "handbook" / "hr" / "_index.md").write_text("---\ntitle: HR\n---\n[Link](x)\n")
    stats = ingest_all(raw, processed, SOURCES)
    assert stats["dropped_too_short"] == 1
    assert stats["documents"] == 0


# --- download include patterns ---------------------------------------------------

def test_matches_include():
    assert matches_include("finance/expenses.md", "finance/")
    assert matches_include("finance/a/b.md", "finance/")
    assert matches_include("support/on-call.md", "support/*.md")
    assert not matches_include("support/workflows/x.md", "support/*.md")
    assert matches_include("security/x.md", "security/x.md")
    assert not matches_include("security/y.md", "security/x.md")


def test_remove_table_of_contents_number_column():
    lines = ["Table of Contents", "1.", "1.1", "1.2", "2.", "Introduction", "5.3", "Leave rules apply."]
    assert remove_table_of_contents(lines) == ["Table of Contents", "Introduction", "5.3", "Leave rules apply."]


def test_ingest_reads_synthetic_old_versions(tmp_path):
    raw, processed, synthetic = tmp_path / "raw", tmp_path / "processed", tmp_path / "synthetic"
    (raw / "handbook" / "finance").mkdir(parents=True)
    synthetic.mkdir()
    (raw / "handbook" / "finance" / "expenses.md").write_text(
        "---\ntitle: Expenses\n---\n" + "Hotels are capped at $300 per night. " * 10)
    (synthetic / "expenses-2023.md").write_text(
        '---\ntitle: Expenses\nversion_group: "hb:finance/expenses"\nis_current: false\n'
        'synthetic_old_version: true\nupdated_date: "2023-03-01"\ndepartment: finance\n---\n'
        + "Hotels are capped at $250 per night. " * 10)

    stats = ingest_all(raw, processed, SOURCES, synthetic)
    docs = {d["doc_id"]: d for d in load_documents(processed)}
    assert stats["documents"] == 2
    old, new = docs["syn:expenses-2023"], docs["hb:finance/expenses"]
    assert old["synthetic_old_version"] is True and old["is_current"] is False
    assert old["version_group"] == new["version_group"] == "hb:finance/expenses"
    assert new["is_current"] is True
    assert old["updated_date"] == "2023-03-01" and old["department"] == "finance"
