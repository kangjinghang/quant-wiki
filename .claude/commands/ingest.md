Ingest a source file into the wiki.

**If $ARGUMENTS is provided:** ingest that specific file (e.g. `/ingest raw/articles/my-file.md`).

**If no arguments:** find unprocessed raw files automatically:

1. List all files in `raw/articles/`, `raw/papers/`, `raw/notes/` (not `raw/archive/`)
2. Read each existing source page in `wiki/sources/` and collect their `raw_path` frontmatter values
3. Show the user the list of unprocessed files (raw files NOT referenced by any source page)
4. If only one unprocessed file exists, proceed with it. If multiple, ask the user which to ingest first.

Then follow the ingest workflow defined in CLAUDE.md — execute immediately without pausing for confirmation:
1. Read the source file in full
2. Create source summary page with `--raw-path` AND `--compute-hash`, concept/entity pages, cascade updates
3. Update wiki/index.md, log/{date}.md, hot.md, wiki/overview.md
4. Briefly report what was done
