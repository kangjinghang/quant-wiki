Ingest a source file into the wiki.

**If $ARGUMENTS is provided:** ingest that specific file (e.g. `/ingest raw/articles/my-file.md`).

**If no arguments:** find unprocessed raw files automatically:

1. List all files in `raw/articles/`, `raw/papers/`, `raw/notes/` (not `raw/archive/`)
2. Read each existing source page in `wiki/sources/` and collect their `raw_path` frontmatter values
3. Show the user the list of unprocessed files (raw files NOT referenced by any source page)
4. If only one unprocessed file exists, proceed with it. If multiple, ask the user which to ingest first.

Then follow the ingest workflow defined in CLAUDE.md:
1. Read the source file in full
2. Present a structured summary (core thesis, new concepts/entities, relations to existing pages, claims to verify, proposed actions)
3. Wait for my confirmation before creating any pages
4. Create source summary page with `--raw-path` pointing back to the original file AND `--compute-hash`, concept/entity pages, cascade updates
5. Update wiki/index.md, log/{date}.md, hot.md
