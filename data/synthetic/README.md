# Synthetic old policy versions

These files are **deliberately outdated copies** of real GitLab handbook pages, written for the
evaluation (Phase 5). Each one copies the relevant section of a current page, changes one or more
facts and gives it an earlier date. They exist so the test set can measure how often the system
answers from an outdated version (`outdated_version` questions, `stale rate`).

Every file's front matter marks it clearly:

- `synthetic_old_version: true` and `is_current: false`
- `version_group` = the doc_id of the real current page it belongs to
- a comment listing exactly which facts were changed (`'old text' -> 'new text'`)

They are committed to git (unlike `data/raw/`) because they cannot be downloaded.
Source pages: GitLab handbook, CC BY-SA 4.0. Ingestion reads this folder (`paths.synthetic_dir`)
and skips this README.
