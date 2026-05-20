Process open audit feedback in the wiki.

If $ARGUMENTS is provided, focus on that specific audit file. Otherwise process all open audits.

Follow the audit workflow defined in CLAUDE.md:
1. Run `python scripts/audit_review.py . --open` to see pending feedback
2. Read each audit item and check the correction against the original raw/ source
3. Fix the wiki page and any related pages
4. Move the processed audit file to audit/resolved/
5. Log the correction in log/{date}.md
