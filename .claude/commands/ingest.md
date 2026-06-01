Ingest a source file into the wiki.

**If $ARGUMENTS is provided:** ingest that specific file (e.g. `/ingest raw/articles/my-file.md`).

**If no arguments:** run `extract_knowledge.py --next` directly. It auto-finds the first unprocessed article. Do NOT manually list files, grep, or ask the user which to process — `--next` handles everything.

Then follow the ingest workflow defined in CLAUDE.md — execute immediately without pausing for confirmation:
1. Run `python scripts/extract_knowledge.py . --next`
2. Read `wiki/meta/.last-extract` to get the extract JSON path
3. Run `python scripts/create_pages_from_extract.py . <path-from-.last-extract>`
4. Run `python scripts/update_overview.py . --content "### heading\n\nparagraph with [[wikilinks]]"`
5. Run `python scripts/ingest_finish.py . --title "..." --source "raw/..." --notes "key concepts"`
6. Run `python scripts/lint_wiki.py .` to verify
7. Briefly report what was done (files created/updated, key concepts)
