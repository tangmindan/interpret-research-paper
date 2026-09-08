# Obsidian output

Read this only for Obsidian notes or literature-library imports. Resolve all paths through [configuration.md](configuration.md).

## Note format

- Use YAML properties, stable headings, Obsidian embeds, callouts, and wiki-links where useful.
- Start a new note from `assets/literature-note-template.md`.
- Use `$...$` and `$$...$$` for LaTeX; convert `\(...\)` and `\[...\]` before delivery while preserving valid display blocks.
- Keep each claim beside its evidence and caveat.
- Preserve existing embeds and user-written interpretations. Back up before a substantial authorized in-place rewrite.

## Portable library layout

When `vault_root` is configured, default to:

```text
<vault_root>/
  <paper-note>.md
  source/
    <FirstAuthor>_<YYYY>_<Journal>_<ShortTopic>.pdf
  图片/
    <FirstAuthor>_<YYYY>_<Journal>_<ShortTopic>/
      Fig_01.png
      figure-manifest.json
      candidates/
  PPT/
```

Explicit `note_dir`, `source_dir`, `figure_dir`, and `ppt_dir` override derived locations.

Read first author, year, journal, and topic from the paper before naming. Sanitize invalid filename characters, keep names concise, copy rather than move the supplied PDF, and never silently replace a different file. On collision, use a DOI suffix or numeric suffix.

Store resolved PDF and figure locations in YAML. Derive vault-relative embeds such as `![[图片/<paper-folder>/Fig_01.png]]`; do not place host absolute paths in note content.

Keep temporary renders and rejected candidates out of the note body. Retain candidates only while review is needed.
