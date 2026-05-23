"""Tests for ingest_finish.py script."""

import sys
from pathlib import Path

# Add scripts/ to path so we can import functions
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from ingest_finish import format_log_entry


class TestFormatLogEntry:
    def test_basic_entry(self):
        """Minimal entry with title and source only."""
        result = format_log_entry(
            title="主动买卖因子的正确用法",
            source="raw/articles/[202009050948]主动买卖因子的正确用法.md",
            created=None,
            updated=None,
            notes=None,
        )
        assert "## Ingest: 主动买卖因子的正确用法" in result
        assert "- Source: `raw/articles/[202009050948]主动买卖因子的正确用法.md`" in result

    def test_entry_with_created(self):
        """Entry with created pages."""
        result = format_log_entry(
            title="主动买卖因子的正确用法",
            source="raw/articles/[202009050948]主动买卖因子的正确用法.md",
            created="wiki/sources/主动买卖因子的正确用法.md,wiki/concepts/主动买卖因子.md",
            updated=None,
            notes=None,
        )
        assert "- Created: `wiki/sources/主动买卖因子的正确用法.md`" in result
        assert "- Created: `wiki/concepts/主动买卖因子.md`" in result

    def test_entry_with_updated(self):
        """Entry with updated pages."""
        result = format_log_entry(
            title="昼夜分离隔夜跳空与日内反转选股因子",
            source="raw/articles/xxx.md",
            created=None,
            updated="wiki/entities/华安金工.md,wiki/index.md",
            notes=None,
        )
        assert "- Updated: `wiki/entities/华安金工.md`" in result
        assert "- Updated: `wiki/index.md`" in result

    def test_entry_with_notes(self):
        """Entry with notes appended."""
        result = format_log_entry(
            title="测试文章",
            source="raw/articles/test.md",
            created=None,
            updated=None,
            notes="开源金工市场微观结构研究系列第9篇",
        )
        assert "- 开源金工市场微观结构研究系列第9篇" in result

    def test_entry_ends_with_blank_line(self):
        """Each entry must end with a trailing newline for separation."""
        result = format_log_entry(
            title="测试",
            source="raw/test.md",
            created=None,
            updated=None,
            notes=None,
        )
        assert result.endswith("\n")

    def test_full_entry_matches_expected_format(self):
        """Full entry with all fields matches actual log format."""
        result = format_log_entry(
            title="主动买卖因子的正确用法",
            source="raw/articles/[202009050948]主动买卖因子的正确用法.md",
            created="wiki/sources/主动买卖因子的正确用法.md,wiki/concepts/主动买卖因子.md",
            updated="wiki/entities/开源金工.md,wiki/index.md",
            notes="ACT因子（主动买卖因子），因子切割论应用于主动买卖方向",
        )
        expected = (
            "## Ingest: 主动买卖因子的正确用法\n"
            "\n"
            "- Source: `raw/articles/[202009050948]主动买卖因子的正确用法.md`\n"
            "- Created: `wiki/sources/主动买卖因子的正确用法.md`\n"
            "- Created: `wiki/concepts/主动买卖因子.md`\n"
            "- Updated: `wiki/entities/开源金工.md`\n"
            "- Updated: `wiki/index.md`\n"
            "- ACT因子（主动买卖因子），因子切割论应用于主动买卖方向\n"
            "\n"
        )
        assert result == expected