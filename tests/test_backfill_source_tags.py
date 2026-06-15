"""Tests for backfill_source_tags.py — guard rails for historical tag backfill.

The backfill mutates hundreds of source pages, so the skip conditions
(self-written pages, already-tagged pages, dry-run) must be airtight.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from backfill_source_tags import backfill


def _write_source(path: Path, tags_line: str, origin: str = "agent-compiled") -> None:
    path.write_text(
        "---\n"
        'title: "T"\n'
        f"{tags_line}\n"
        f"origin: {origin}\n"
        "---\nbody\n",
        encoding="utf-8",
    )


def _make(tmp_path, title, tags, source_tags_line="tags: []", origin="agent-compiled"):
    # wiki_root = tmp_path; the script looks for wiki_root/wiki/{sources,meta}
    root = tmp_path
    (root / "wiki" / "sources").mkdir(parents=True)
    (root / "wiki" / "meta").mkdir(parents=True)
    src = root / "wiki" / "sources" / f"{title}.md"
    _write_source(src, source_tags_line, origin)
    ej = root / "wiki" / "meta" / f"extract-{title}.json"
    ej.write_text(json.dumps({
        "title": title, "tags": tags,
        "source_content": "x", "concepts": [], "entities": [],
    }, ensure_ascii=False), encoding="utf-8")
    return root, src


class TestBackfillSourceTags:
    def test_fills_empty_tags(self, tmp_path):
        wiki, src = _make(tmp_path, "alpha", ["可转债", "回测"])
        backfill(wiki, dry_run=False)
        assert "tags: [可转债" in src.read_text(encoding="utf-8")
        assert "tags: []" not in src.read_text(encoding="utf-8")

    def test_dry_run_does_not_write(self, tmp_path):
        wiki, src = _make(tmp_path, "alpha", ["可转债", "回测"])
        backfill(wiki, dry_run=True)
        assert "tags: []" in src.read_text(encoding="utf-8")

    def test_skips_self_written(self, tmp_path):
        """Never overwrite pages with origin: self-written."""
        wiki, src = _make(tmp_path, "alpha", ["可转债"], origin="self-written")
        backfill(wiki, dry_run=False)
        assert "tags: []" in src.read_text(encoding="utf-8")

    def test_skips_nonempty_tags(self, tmp_path):
        """Pages that already have tags are left untouched."""
        wiki, src = _make(tmp_path, "alpha", ["可转债"], source_tags_line="tags: [已有]")
        backfill(wiki, dry_run=False)
        assert "tags: [已有]" in src.read_text(encoding="utf-8")
        assert "可转债" not in src.read_text(encoding="utf-8")

    def test_filters_non_taxonomy_tags(self, tmp_path, monkeypatch):
        """Tags not in the taxonomy are dropped before writing."""
        import backfill_source_tags
        monkeypatch.setattr(
            backfill_source_tags, "load_tag_taxonomy",
            lambda root: {"可转债", "回测"},
        )
        wiki, src = _make(tmp_path, "alpha", ["可转债", "非法tag", "回测"])
        backfill(wiki, dry_run=False)
        text = src.read_text(encoding="utf-8")
        assert "tags: [可转债" in text
        assert "回测" in text
        assert "非法tag" not in text
        assert "tags: []" not in text
