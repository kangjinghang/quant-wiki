#!/usr/bin/env python3
"""backfill_source_tags.py — 用 extract JSON 顶层 tags 回填空 tags 的 source 页面。

历史 bug（create_pages_from_extract.py 建 source 页面时漏传 tags，已修复）导致
大量 source 页面 frontmatter `tags: []`。本脚本一次性回填存量：扫描
wiki/meta/ 与 wiki/meta/archive/ 下的 extract-*.json，按 title 规范化匹配
（文件名 slug 不一致也能命中），对 tags 为空且 origin 非 self-written 的
source 页面写入 JSON 顶层 tags。

护栏：
  - origin: self-written 的页面永不触碰
  - tags 已非空的页面不覆盖（只补空 tags）
  - 非 taxonomy 的 tag 过滤掉

用法:
    python scripts/backfill_source_tags.py <wiki-root> [--dry-run]

--dry-run 只报告将改动的页面，不写盘。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Ensure stdout/stderr handle Unicode on Windows (GBK console default)
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from create_page import fill_fm_field
from lint_wiki import load_tag_taxonomy
from merge_frontmatter import parse_frontmatter


def _tags_empty(fm: dict) -> bool:
    """parse_frontmatter 返回的 dict 值为 raw 字符串；判断 tags 是否为空。"""
    tags = fm.get("tags")
    if tags is None:
        return True
    if isinstance(tags, str):
        return tags.strip() in ("", "[]")
    if isinstance(tags, list):
        return len(tags) == 0
    return False


def _norm_title(title: str) -> str:
    """规范化 title：去标点/空格/破折号并小写，用于跨文件名与归档目录匹配。"""
    return re.sub(r"[\s\-—：:，,。.（()）【】、·]+", "", title).lower()


def backfill(wiki_root: Path, dry_run: bool = False) -> dict:
    """回填空 tags 的 source 页面，返回统计字典。"""
    meta_dir = wiki_root / "wiki" / "meta"
    sources_dir = wiki_root / "wiki" / "sources"
    archive_dir = meta_dir / "archive"
    stats = {
        "filled": 0, "skip_self_written": 0, "skip_nonempty": 0,
        "no_tags_in_json": 0, "no_valid_tags": 0, "no_source_page": 0, "bad": 0,
        "dropped_tags": 0,
    }

    taxonomy = load_tag_taxonomy(wiki_root)

    if not sources_dir.is_dir():
        print(f"ERROR: {sources_dir} not found", file=sys.stderr)
        return stats

    # 1. 建 tags-empty source 索引: norm_title -> path（只含待回填的页面）。
    #    origin=self-written / tags 已非空 的页面不进索引，天然受保护。
    empty_sources: dict[str, Path] = {}
    for sp in sorted(sources_dir.glob("*.md")):
        text = sp.read_text(encoding="utf-8")
        fm, _body, _raw_fm = parse_frontmatter(text)
        if fm is None:
            continue
        origin = str(fm.get("origin", "")).strip().strip('"').strip("'")
        if origin == "self-written":
            stats["skip_self_written"] += 1
            continue
        if not _tags_empty(fm):
            stats["skip_nonempty"] += 1
            continue
        title = str(fm.get("title", "")).strip().strip('"').strip("'")
        if title:
            empty_sources[_norm_title(title)] = sp

    # 2. 扫 meta/ 与 meta/archive/ 的 extract JSON（按 title 规范化匹配 source）。
    json_files = sorted(meta_dir.glob("extract-*.json"))
    if archive_dir.is_dir():
        json_files += sorted(archive_dir.glob("extract-*.json"))

    for ej in json_files:
        try:
            data = json.loads(ej.read_text(encoding="utf-8"))
        except Exception as e:
            stats["bad"] += 1
            print(f"  bad json, skip: {ej.name} ({e})", file=sys.stderr)
            continue

        title = data.get("title", "")
        tags = data.get("tags", [])
        if not title:
            continue
        if not tags:
            stats["no_tags_in_json"] += 1
            continue

        # Only backfill tags present in the CLAUDE.md taxonomy; report others.
        if taxonomy is not None:
            dropped = [t for t in tags if t not in taxonomy]
            if dropped:
                stats["dropped_tags"] += len(dropped)
                print(f"  (dropped non-taxonomy tags in {ej.name}: {dropped})", file=sys.stderr)
            tags = [t for t in tags if t in taxonomy]
            if not tags:
                stats["no_valid_tags"] += 1
                continue

        # pop 去重：同 title 的 JSON（meta + archive 各一份）只填一次。
        source_page = empty_sources.pop(_norm_title(title), None)
        if source_page is None:
            stats["no_source_page"] += 1
            continue

        # fill_fm_field 整行替换 tags，格式与 fill_template（concept/entity）一致。
        text = source_page.read_text(encoding="utf-8")
        tags_str = "[" + ", ".join(tags) + "]"
        new_text = fill_fm_field(text, "tags", tags_str)
        verb = "WOULD FILL" if dry_run else "FILLED"
        print(f"  [{verb}] {source_page.name}  tags={tags}")
        stats["filled"] += 1
        if not dry_run:
            source_page.write_text(new_text, encoding="utf-8")

    label = "DRY RUN. " if dry_run else ""
    print(
        f"\n{label}"
        f"filled={stats['filled']}, skip_self_written={stats['skip_self_written']}, "
        f"skip_nonempty={stats['skip_nonempty']}, no_tags_in_json={stats['no_tags_in_json']}, "
        f"no_valid_tags={stats['no_valid_tags']}, dropped_tags={stats['dropped_tags']}, "
        f"no_source_page={stats['no_source_page']}, bad={stats['bad']}"
    )
    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description="Backfill empty source-page tags from extract JSONs.")
    ap.add_argument("wiki_root", help="wiki root directory (contains wiki/)")
    ap.add_argument("--dry-run", action="store_true", help="report only, do not write")
    args = ap.parse_args()
    backfill(Path(args.wiki_root).resolve(), args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
