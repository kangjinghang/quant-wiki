# Backfill Concept/Entity Page Sources

**Date**: 2026-06-02
**Status**: Approved

## Problem

870/1017 concept pages and 172/185 entity pages have `sources: []` (empty). This breaks provenance tracking — the wiki's core promise that "every claim traces back to raw source."

**Root cause**: `create_pages_from_extract.py` → `_create_page()` accepts `tags` but not `sources`. Newly created concept/entity pages always get `sources: []`. Only cascade-updated existing pages receive source links via `_cascade_update()`.

## Solution

Three-part fix:

### 1. One-time backfill script (`scripts/backfill_sources.py`)

Scan all `wiki/sources/*.md` body text for `[[wikilink]]` targets. For each wikilink that resolves to a concept/entity page, add the source page to that concept/entity page's `sources` frontmatter field.

**Algorithm**:
1. Load all source pages from `wiki/sources/`
2. For each source page, extract wikilinks from body (skip frontmatter)
3. Map wikilink target → source page slug (using `[[source-slug]]` format)
4. For each concept/entity page with empty sources, write merged sources via `merge_array_field()`
5. If a seed page gains sources, promote status to `developing`

**CLI**:
```
python scripts/backfill_sources.py <wiki-root> [--dry-run] [--page <path>]
```

**Dependencies**: Reuses `merge_frontmatter.parse_frontmatter` and `merge_frontmatter.merge_array_field`.

**Status promotion rule**: If `status: seed` and sources go from empty to non-empty → set `status: developing` and update `updated` date.

### 2. Root cause fix (`scripts/create_pages_from_extract.py`)

Modify `_create_page()`:
- Add parameter `sources: list[str] | None = None`
- After filling template, if sources provided, call `merge_array_field()` to inject them

Modify `main()` call sites:
- New concept pages: pass `sources=[source_wikilink]`
- New entity pages: pass `sources=[source_wikilink]`

### 3. Lint safety net (`scripts/lint_wiki.py`)

Add check #21 (read-only warning):
- If a concept/entity page has `status != seed` and `sources` is empty/missing → report warning
- No auto-fix; this is a signal to investigate the pipeline

## Files Changed

| Action | File | Change |
|--------|------|--------|
| Create | `scripts/backfill_sources.py` | ~100 lines, one-time backfill |
| Modify | `scripts/create_pages_from_extract.py` | `_create_page()` gains `sources` param |
| Modify | `scripts/lint_wiki.py` | Add check #21 |
| No change | `_templates/*.md` | Templates unchanged |
| No change | `scripts/merge_frontmatter.py` | Reused as-is |

## Expected Outcome

- 870 concept pages gain sources (wikilink reverse inference)
- 172 entity pages gain sources
- ~650+ pages promoted from seed → developing
- Future ingests no longer produce empty-sources pages
- Lint catches any regression
