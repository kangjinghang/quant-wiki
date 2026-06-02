"""Tests for backfill_sources.py — wikilink reverse inference for sources field."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from backfill_sources import backfill_sources, build_source_map


class TestBuildSourceMap:
    """Test wikilink → source page mapping from source pages."""

    def test_extracts_wikilinks_from_source_body(self, tmp_path):
        """Wikilinks in source page body should map to source page slug."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        concepts = wiki / "concepts"
        sources.mkdir(parents=True)
        concepts.mkdir(parents=True)

        # Source page links to a concept
        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\nsources: []\n---\n"
            "This discusses [[动量因子]] and [[反转因子]].\n",
            encoding="utf-8",
        )
        # Concept pages exist
        (concepts / "动量因子.md").write_text(
            "---\ntitle: 动量因子\nsources: []\nstatus: seed\n---\nBody.\n",
            encoding="utf-8",
        )
        (concepts / "反转因子.md").write_text(
            "---\ntitle: 反转因子\nsources: []\nstatus: seed\n---\nBody.\n",
            encoding="utf-8",
        )

        source_map = build_source_map(wiki)
        assert source_map["动量因子"] == ["my-article"]
        assert source_map["反转因子"] == ["my-article"]

    def test_ignores_frontmatter_wikilinks(self, tmp_path):
        """Wikilinks inside frontmatter should not be included."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        concepts = wiki / "concepts"
        sources.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\nrelated: [[动量因子]]\n---\nBody only.\n",
            encoding="utf-8",
        )
        (concepts / "动量因子.md").write_text(
            "---\ntitle: 动量因子\nsources: []\nstatus: seed\n---\nBody.\n",
            encoding="utf-8",
        )

        source_map = build_source_map(wiki)
        # 动量因子 only appears in frontmatter, not body — should not be mapped
        assert "动量因子" not in source_map

    def test_multiple_sources_link_same_concept(self, tmp_path):
        """Multiple source pages linking the same concept should produce a list."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        concepts = wiki / "concepts"
        sources.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (sources / "article-a.md").write_text(
            "---\ntitle: A\n---\nSee [[动量因子]].\n", encoding="utf-8",
        )
        (sources / "article-b.md").write_text(
            "---\ntitle: B\n---\nAlso [[动量因子]].\n", encoding="utf-8",
        )
        (concepts / "动量因子.md").write_text(
            "---\ntitle: 动量因子\nsources: []\nstatus: seed\n---\nBody.\n",
            encoding="utf-8",
        )

        source_map = build_source_map(wiki)
        assert source_map["动量因子"] == ["article-a", "article-b"]

    def test_ignores_links_to_nonexistent_pages(self, tmp_path):
        """Wikilinks to pages that don't exist should be skipped."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        sources.mkdir(parents=True)

        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\n---\nSee [[不存在的概念]].\n",
            encoding="utf-8",
        )

        source_map = build_source_map(wiki)
        assert "不存在的概念" not in source_map


class TestBackfillSources:
    """Test the full backfill operation."""

    def test_fills_empty_sources_on_concept(self, tmp_path):
        """Concept page with empty sources should get source link from wikilink."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        concepts = wiki / "concepts"
        sources.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\n---\nThis discusses [[动量因子]].\n",
            encoding="utf-8",
        )
        (concepts / "动量因子.md").write_text(
            "---\ntitle: 动量因子\nsources: []\nstatus: seed\n---\nBody.\n",
            encoding="utf-8",
        )

        stats = backfill_sources(tmp_path)
        assert stats["filled"] == 1

        text = (concepts / "动量因子.md").read_text(encoding="utf-8")
        assert "[[my-article]]" in text

    def test_promotes_seed_to_developing(self, tmp_path):
        """Seed page that gains sources should be promoted to developing."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        concepts = wiki / "concepts"
        sources.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\n---\nThis discusses [[动量因子]].\n",
            encoding="utf-8",
        )
        (concepts / "动量因子.md").write_text(
            "---\ntitle: 动量因子\nsources: []\nstatus: seed\n---\nBody.\n",
            encoding="utf-8",
        )

        backfill_sources(tmp_path)

        text = (concepts / "动量因子.md").read_text(encoding="utf-8")
        assert "status: developing" in text
        assert "status: seed" not in text

    def test_does_not_promote_non_seed(self, tmp_path):
        """Already developing page should stay developing."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        concepts = wiki / "concepts"
        sources.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\n---\nThis discusses [[动量因子]].\n",
            encoding="utf-8",
        )
        (concepts / "动量因子.md").write_text(
            "---\ntitle: 动量因子\nsources: []\nstatus: developing\n---\nBody.\n",
            encoding="utf-8",
        )

        backfill_sources(tmp_path)

        text = (concepts / "动量因子.md").read_text(encoding="utf-8")
        assert "status: developing" in text

    def test_skips_pages_with_existing_sources(self, tmp_path):
        """Pages that already have sources should not be modified."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        concepts = wiki / "concepts"
        sources.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\n---\nThis discusses [[动量因子]].\n",
            encoding="utf-8",
        )
        (concepts / "动量因子.md").write_text(
            "---\ntitle: 动量因子\nsources:\n  - \"[[other-source]]\"\nstatus: developing\n---\nBody.\n",
            encoding="utf-8",
        )

        stats = backfill_sources(tmp_path)
        assert stats["skipped"] == 1

    def test_dry_run_does_not_write(self, tmp_path):
        """--dry-run should not modify any files."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        concepts = wiki / "concepts"
        sources.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\n---\nThis discusses [[动量因子]].\n",
            encoding="utf-8",
        )
        (concepts / "动量因子.md").write_text(
            "---\ntitle: 动量因子\nsources: []\nstatus: seed\n---\nBody.\n",
            encoding="utf-8",
        )

        stats = backfill_sources(tmp_path, dry_run=True)
        assert stats["filled"] == 1

        text = (concepts / "动量因子.md").read_text(encoding="utf-8")
        assert "sources: []" in text  # not modified

    def test_works_for_entities_too(self, tmp_path):
        """Entity pages should also get sources backfilled."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        entities = wiki / "entities"
        sources.mkdir(parents=True)
        entities.mkdir(parents=True)

        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\n---\nResearch by [[华创金工]].\n",
            encoding="utf-8",
        )
        (entities / "华创金工.md").write_text(
            "---\ntitle: 华创金工\nsources: []\nstatus: seed\n---\nBody.\n",
            encoding="utf-8",
        )

        stats = backfill_sources(tmp_path)
        assert stats["filled"] == 1

        text = (entities / "华创金工.md").read_text(encoding="utf-8")
        assert "[[my-article]]" in text
        assert "status: developing" in text

    def test_deduplicates_source_links(self, tmp_path):
        """If a source page links the same concept twice, only add once."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        concepts = wiki / "concepts"
        sources.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\n---\n[[动量因子]] is great. More on [[动量因子]].\n",
            encoding="utf-8",
        )
        (concepts / "动量因子.md").write_text(
            "---\ntitle: 动量因子\nsources: []\nstatus: seed\n---\nBody.\n",
            encoding="utf-8",
        )

        backfill_sources(tmp_path)

        text = (concepts / "动量因子.md").read_text(encoding="utf-8")
        # Should appear only once in sources list
        assert text.count("[[my-article]]") == 1

    def test_inline_sources_format(self, tmp_path):
        """Handle pages with inline sources format: sources: [a, b]."""
        wiki = tmp_path / "wiki"
        sources = wiki / "sources"
        concepts = wiki / "concepts"
        sources.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (sources / "my-article.md").write_text(
            "---\ntitle: My Article\n---\nSee [[动量因子]].\n",
            encoding="utf-8",
        )
        (concepts / "动量因子.md").write_text(
            "---\ntitle: 动量因子\nsources: [\"[[existing-source]]\"]\nstatus: developing\n---\nBody.\n",
            encoding="utf-8",
        )

        stats = backfill_sources(tmp_path)
        # Should skip — already has sources
        assert stats["skipped"] == 1

    def test_no_pages_to_fill(self, tmp_path):
        """Wiki with no empty-source pages should report zero fills."""
        wiki = tmp_path / "wiki"
        wiki.mkdir(parents=True)
        (wiki / "index.md").write_text("# Index\n", encoding="utf-8")

        stats = backfill_sources(tmp_path)
        assert stats["filled"] == 0
        assert stats["skipped"] == 0
