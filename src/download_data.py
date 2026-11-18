"""Download the corpus listed in data/sources.yaml into data/raw/ (which git ignores).

Run:  python -m src.download_data           skip anything already downloaded
      python -m src.download_data --force   download everything again
"""

from __future__ import annotations

import argparse
import fnmatch
import io
import json
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

from src.config import load_config, read_yaml, resolve_path

GITLAB_API = "https://gitlab.com/api/v4"
# Some university/council sites block clients that don't look like a browser.
USER_AGENT = "Mozilla/5.0 (compatible; rag-eval-research/0.1)"
PAUSE_SECONDS = 0.15  # GitLab allows 500 unauthenticated requests/minute; stay well under it


def http_get(url: str, timeout: int = 60, attempts: int = 4) -> bytes:
    """GET a URL and return the body.

    Retries on rate limiting (HTTP 429, wait 60 s) and on timeouts / dropped connections
    (wait 5, 10, 20 s). Other HTTP errors such as 404 are raised immediately.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except urllib.error.HTTPError as err:  # server answered with an error code
            if err.code != 429 or attempt == attempts:
                raise
            print("    rate-limited, waiting 60 s ...")
            time.sleep(60)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as err:  # network problem
            if attempt == attempts:
                raise
            wait = 5 * 2 ** (attempt - 1)
            print(f"    network error ({err}), retrying in {wait} s ...")
            time.sleep(wait)
    raise RuntimeError("unreachable")


def matches_include(rel_path: str, pattern: str) -> bool:
    """Check a handbook path against one include pattern from sources.yaml."""
    if pattern.endswith("/"):
        return rel_path.startswith(pattern)  # whole folder, any depth
    if "*" in pattern:
        # "support/*.md" should match support/x.md but not support/sub/x.md,
        # and fnmatch's "*" also matches "/", so compare folder depth too.
        return rel_path.count("/") == pattern.count("/") and fnmatch.fnmatch(rel_path, pattern)
    return rel_path == pattern


def download_handbook(cfg: dict[str, Any], out_dir: Path) -> list[str]:
    """Download each needed handbook section as a zip and keep only the included .md files."""
    project = urllib.parse.quote(cfg["project"], safe="")
    marker = f"/{cfg['base_path']}/"  # zip entries look like "<repo>-<sha>/content/handbook/..."
    sections = sorted({pattern.split("/")[0] for pattern in cfg["include"]})
    saved: list[str] = []

    for section in sections:
        print(f"  section: {section}")
        url = (f"{GITLAB_API}/projects/{project}/repository/archive.zip"
               f"?sha={cfg['ref']}&path={cfg['base_path']}/{section}")
        with zipfile.ZipFile(io.BytesIO(http_get(url))) as archive:
            for name in archive.namelist():
                if not name.endswith(".md") or marker not in name:
                    continue
                rel_path = name.split(marker, 1)[1]
                if not any(matches_include(rel_path, p) for p in cfg["include"]):
                    continue
                target = out_dir / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(name))
                saved.append(rel_path)
        time.sleep(PAUSE_SECONDS)
    return sorted(saved)


def fetch_commit_dates(cfg: dict[str, Any], rel_paths: list[str], dates_path: Path) -> dict[str, str]:
    """Look up each file's last-commit date (YYYY-MM-DD) via the GitLab API, one request per file.

    Results are saved to dates_path so re-runs only ask about files not seen before.
    """
    dates: dict[str, str] = json.loads(dates_path.read_text()) if dates_path.exists() else {}
    project = urllib.parse.quote(cfg["project"], safe="")
    missing = [p for p in rel_paths if p not in dates]
    print(f"  commit dates: {len(missing)} to fetch, {len(dates)} already known")

    for i, rel_path in enumerate(missing, start=1):
        file_path = urllib.parse.quote(f"{cfg['base_path']}/{rel_path}", safe="")
        url = (f"{GITLAB_API}/projects/{project}/repository/commits"
               f"?ref_name={cfg['ref']}&path={file_path}&per_page=1")
        commits = json.loads(http_get(url))
        if commits:
            dates[rel_path] = commits[0]["committed_date"][:10]
        if i % 50 == 0:
            print(f"    {i}/{len(missing)}")
            dates_path.write_text(json.dumps(dates, indent=1, sort_keys=True))  # save progress
        time.sleep(PAUSE_SECONDS)

    dates_path.write_text(json.dumps(dates, indent=1, sort_keys=True))
    return dates


def download_pdfs(entries: list[dict[str, Any]], out_dir: Path, force: bool) -> list[str]:
    """Download each PDF to out_dir/<id>.pdf. Returns the ids that failed."""
    out_dir.mkdir(parents=True, exist_ok=True)
    failed: list[str] = []
    for entry in entries:
        target = out_dir / f"{entry['id']}.pdf"
        if target.exists() and not force:
            continue
        try:
            data = http_get(entry["url"])
        except (urllib.error.URLError, TimeoutError) as err:
            print(f"  FAILED {entry['id']}: {err}")
            failed.append(entry["id"])
            continue
        if not data.startswith(b"%PDF"):  # site returned an HTML page (block, redirect, 404 page)
            print(f"  FAILED {entry['id']}: response is not a PDF")
            failed.append(entry["id"])
            continue
        target.write_bytes(data)
        print(f"  saved {target.name} ({len(data) // 1024} KB)")
    return failed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="download again even if files exist")
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()

    paths = load_config(args.config)["paths"]
    sources = read_yaml(resolve_path(paths["sources"]))
    raw_dir = resolve_path(paths["raw_dir"])
    handbook_dir = raw_dir / "handbook"

    print("Handbook (markdown):")
    if handbook_dir.exists() and not args.force:
        rel_paths = sorted(p.relative_to(handbook_dir).as_posix() for p in handbook_dir.rglob("*.md"))
        print(f"  already downloaded ({len(rel_paths)} files); use --force to refresh")
    else:
        rel_paths = download_handbook(sources["handbook"], handbook_dir)
        print(f"  saved {len(rel_paths)} markdown files")
    fetch_commit_dates(sources["handbook"], rel_paths, handbook_dir / "_dates.json")

    print("Policy PDFs:")
    failed = download_pdfs(sources["pdfs"], raw_dir / "pdfs", args.force)
    print(f"  {len(sources['pdfs']) - len(failed)}/{len(sources['pdfs'])} PDFs present")
    if failed:
        print(f"  failed: {failed} (check the URL in data/sources.yaml)")


if __name__ == "__main__":
    main()
