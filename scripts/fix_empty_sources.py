#!/usr/bin/env python3
"""Fix empty sources on non-seed concept/entity pages.

Strategy:
1. Reverse-index source page wikilinks (source -> concept/entity)
2. Map extract JSONs to source pages via title matching, then extract concept/entity names
3. Scan concept/entity page bodies for wikilinks to source pages
4. Combine all maps and populate empty sources fields

Usage:
    python scripts/fix_empty_sources.py .
"""

import os
import re
import sys
import json
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_frontmatter import parse_frontmatter, _extract_existing_list_items, merge_array_field

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def slugify(text):
    """Slugify text for matching."""
    s = text.strip().lower()
    s = re.sub(r'[：:—\-–、，。？！""''（）()\[\]【】《》·\.\?\!\,\;]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    s = re.sub(r'[^\w\u4e00-\u9fff-]', '', s)
    return s


def fix_frontmatter_blanks(wiki_root):
    """Fix pages with extra blank lines after the opening --- delimiter."""
    fixed = 0
    for d in ["wiki/concepts", "wiki/entities", "wiki/sources", "wiki/syntheses"]:
        full_dir = os.path.join(wiki_root, d)
        if not os.path.isdir(full_dir):
            continue
        for f in os.listdir(full_dir):
            if not f.endswith(".md"):
                continue
            full_path = os.path.join(wiki_root, d, f)
            with open(full_path, "r", encoding="utf-8") as fh:
                text = fh.read()
            # Fix: ---\n\n\n... -> ---\n...
            new_text = re.sub(r"^---\n\n+", "---\n", text)
            if new_text != text:
                with open(full_path, "w", encoding="utf-8") as fh:
                    fh.write(new_text)
                fixed += 1
    return fixed


def build_wikilink_reverse_map(wiki_root):
    """Build reverse map from source page wikilinks."""
    concept_pages = {}
    for d in ["wiki/concepts", "wiki/entities"]:
        full_dir = os.path.join(wiki_root, d)
        if not os.path.isdir(full_dir):
            continue
        for f in os.listdir(full_dir):
            if f.endswith(".md"):
                name = f[:-3]
                concept_pages[name] = os.path.join(d, f)

    reverse_map = {}
    sources_dir = os.path.join(wiki_root, "wiki/sources")
    for f in glob.glob(os.path.join(sources_dir, "*.md")):
        source_name = os.path.basename(f)[:-3]
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read()
        links = re.findall(r"\[\[([^\]]+)\]\]", content)
        for link in links:
            link = link.split("|")[0].strip()
            if link in concept_pages:
                fp = concept_pages[link]
                if fp not in reverse_map:
                    reverse_map[fp] = set()
                reverse_map[fp].add(source_name)
    return reverse_map


def build_extract_reverse_map(wiki_root):
    """Build reverse map from extract JSON files."""
    # concept/entity name-slug -> relative path
    name_to_file = {}
    for d in ["wiki/concepts", "wiki/entities"]:
        full_dir = os.path.join(wiki_root, d)
        if not os.path.isdir(full_dir):
            continue
        for f in os.listdir(full_dir):
            if f.endswith(".md"):
                name_to_file[f[:-3]] = os.path.join(d, f)

    # source title-slug -> source page name
    source_title_map = {}
    sources_dir = os.path.join(wiki_root, "wiki/sources")
    for f in sorted(os.listdir(sources_dir)):
        if not f.endswith(".md"):
            continue
        with open(os.path.join(sources_dir, f), "r", encoding="utf-8") as fh:
            text = fh.read()
        fm, _, _ = parse_frontmatter(text)
        if fm:
            title = fm.get("title", "").strip('"').strip("'")
            title_slug = slugify(title)
            source_name = f[:-3]
            source_title_map[title_slug] = source_name

    reverse_map = {}
    meta_dir = os.path.join(wiki_root, "wiki/meta")
    for ef in glob.glob(os.path.join(meta_dir, "extract-*.json")):
        with open(ef, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        title = data.get("title", "")
        title_slug = slugify(title)
        source_match = source_title_map.get(title_slug)
        if not source_match:
            continue

        for item_list in [data.get("concepts", []), data.get("entities", [])]:
            for item in item_list:
                name = item.get("name", "")
                name_slug = slugify(name)
                if name_slug in name_to_file:
                    fp = name_to_file[name_slug]
                    if fp not in reverse_map:
                        reverse_map[fp] = set()
                    reverse_map[fp].add(source_match)

    return reverse_map


def build_body_wikilink_map(wiki_root):
    """Build map by scanning concept/entity page bodies for source page wikilinks."""
    source_names = set(
        f[:-3]
        for f in os.listdir(os.path.join(wiki_root, "wiki/sources"))
        if f.endswith(".md")
    )

    body_map = {}
    for d in ["wiki/concepts", "wiki/entities"]:
        full_dir = os.path.join(wiki_root, d)
        if not os.path.isdir(full_dir):
            continue
        for f in os.listdir(full_dir):
            if not f.endswith(".md"):
                continue
            rel_path = os.path.join(d, f)
            full_path = os.path.join(wiki_root, rel_path)

            with open(full_path, "r", encoding="utf-8") as fh:
                text = fh.read()

            # Only scan body (after frontmatter)
            parts = text.split("---", 2)
            if len(parts) < 3:
                continue
            body = parts[2]

            links = re.findall(r"\[\[([^\]]+)\]\]", body)
            found_sources = set()
            for link in links:
                link = link.split("|")[0].strip()
                if link in source_names:
                    found_sources.add(link)

            if found_sources:
                body_map[rel_path] = found_sources

    return body_map


def build_keyword_reverse_map(wiki_root, remaining_pages):
    """Build map by searching source page bodies for page titles/keywords."""
    # Load all source page bodies
    sources = {}
    sources_dir = os.path.join(wiki_root, "wiki/sources")
    for f in os.listdir(sources_dir):
        if not f.endswith(".md"):
            continue
        with open(os.path.join(sources_dir, f), "r", encoding="utf-8") as fh:
            sources[f[:-3]] = fh.read()

    reverse_map = {}
    for rel_path in remaining_pages:
        full_path = os.path.join(wiki_root, rel_path)
        with open(full_path, "r", encoding="utf-8") as fh:
            text = fh.read()

        # Extract title from frontmatter
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        raw_fm = parts[1]
        title_match = re.search(r'^title:\s*"?([^"\n]+)"?', raw_fm, re.MULTILINE)
        if not title_match:
            continue
        title = title_match.group(1).strip()

        # Skip very generic titles (too many matches)
        generic = {"因子", "债券", "打新"}
        if title in generic:
            continue

        # Search source bodies for exact title match
        matches = set()
        for sname, content in sources.items():
            if re.search(re.escape(title), content, re.IGNORECASE):
                matches.add(sname)

        # If no exact match, try splitting title into words and searching for each
        if not matches:
            # Split on Chinese/English boundary and common separators
            title_parts = re.split(r'(?<=[\u4e00-\u9fff])(?=[A-Za-z])|(?<=[A-Za-z])(?=[\u4e00-\u9fff])|[·\-—]', title)
            title_parts = [p.strip() for p in title_parts if len(p.strip()) >= 2]
            for sname, content in sources.items():
                for part in title_parts:
                    if re.search(re.escape(part), content, re.IGNORECASE):
                        matches.add(sname)
                        break

        if matches:
            reverse_map[rel_path] = matches

    return reverse_map


def main(wiki_root):
    wiki_root = os.path.abspath(wiki_root)

    # Step 0: Fix malformed frontmatter
    fm_fixed = fix_frontmatter_blanks(wiki_root)
    if fm_fixed:
        print(f"Fixed frontmatter blanks in {fm_fixed} pages")

    # Build all reverse maps (strategies 1-3)
    wikilink_map = build_wikilink_reverse_map(wiki_root)
    extract_map = build_extract_reverse_map(wiki_root)
    body_map = build_body_wikilink_map(wiki_root)

    # Merge: combine all sources
    combined = {}
    for src_map in [wikilink_map, extract_map, body_map]:
        for fp, sources in src_map.items():
            if fp not in combined:
                combined[fp] = set()
            combined[fp].update(sources)

    # First pass: fix what we can with strategies 1-3
    fixed = 0
    skipped_has_sources = 0
    skipped_seed = 0
    unfixable = []

    for d in ["wiki/concepts", "wiki/entities"]:
        full_dir = os.path.join(wiki_root, d)
        if not os.path.isdir(full_dir):
            continue
        for f in sorted(os.listdir(full_dir)):
            if not f.endswith(".md"):
                continue
            rel_path = os.path.join(d, f)
            full_path = os.path.join(wiki_root, rel_path)

            with open(full_path, "r", encoding="utf-8") as fh:
                text = fh.read()

            fm, body, raw_fm = parse_frontmatter(text)
            if fm is None:
                continue

            existing_sources = _extract_existing_list_items(raw_fm, "sources")
            status = fm.get("status", "seed")

            if status == "seed":
                skipped_seed += 1
                continue

            if len(existing_sources) > 0:
                skipped_has_sources += 1
                continue

            if rel_path not in combined:
                unfixable.append(rel_path)
                continue

            source_names = sorted(combined[rel_path])
            new_sources = [f"[[{s}]]" for s in source_names]

            # Check if sources field exists in frontmatter
            has_sources_field = bool(re.search(r"^sources:", raw_fm, re.MULTILINE))
            if has_sources_field:
                new_raw_fm = merge_array_field(raw_fm, "sources", new_sources)
            else:
                # Inject sources field before 'origin:' or at end
                sources_block = "sources:\n" + "\n".join(f'  - "{s}"' for s in new_sources)
                if "origin:" in raw_fm:
                    new_raw_fm = re.sub(r"(\norigin:)", f"\n{sources_block}\\1", raw_fm)
                else:
                    new_raw_fm = raw_fm.rstrip() + "\n" + sources_block
            new_content = f"---\n{new_raw_fm}\n---{body}"

            with open(full_path, "w", encoding="utf-8") as fh:
                fh.write(new_content)
            fixed += 1

    print(f"Fixed (strategies 1-3): {fixed}")

    # Second pass: keyword search for remaining unfixable
    if unfixable:
        keyword_map = build_keyword_reverse_map(wiki_root, unfixable)
        kw_fixed = 0
        still_unfixable = []

        for rel_path in unfixable:
            if rel_path not in keyword_map:
                still_unfixable.append(rel_path)
                continue

            full_path = os.path.join(wiki_root, rel_path)
            with open(full_path, "r", encoding="utf-8") as fh:
                text = fh.read()

            fm, body, raw_fm = parse_frontmatter(text)
            if fm is None:
                still_unfixable.append(rel_path)
                continue

            source_names = sorted(keyword_map[rel_path])
            new_sources = [f"[[{s}]]" for s in source_names]

            has_sources_field = bool(re.search(r"^sources:", raw_fm, re.MULTILINE))
            if has_sources_field:
                new_raw_fm = merge_array_field(raw_fm, "sources", new_sources)
            else:
                sources_block = "sources:\n" + "\n".join(f'  - "{s}"' for s in new_sources)
                if "origin:" in raw_fm:
                    new_raw_fm = re.sub(r"(\norigin:)", f"\n{sources_block}\\1", raw_fm)
                else:
                    new_raw_fm = raw_fm.rstrip() + "\n" + sources_block
            new_content = f"---\n{new_raw_fm}\n---{body}"

            with open(full_path, "w", encoding="utf-8") as fh:
                fh.write(new_content)
            kw_fixed += 1

        print(f"Fixed (keyword strategy): {kw_fixed}")
        unfixable = still_unfixable

    print(f"Skipped (already have sources): {skipped_has_sources}")
    print(f"Skipped (seed status): {skipped_seed}")
    print(f"Remaining unfixable: {len(unfixable)}")
    if unfixable:
        print("\nUnfixable pages:")
        for p in unfixable:
            print(f"  {p}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_empty_sources.py <wiki-root>")
        sys.exit(1)
    main(sys.argv[1])
