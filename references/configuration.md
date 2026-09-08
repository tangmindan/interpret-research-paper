# Output configuration

Do not encode a user's absolute path in this public Skill.

## Resolution order

Resolve every location independently in this order:

1. explicit parameter in the current request;
2. project configuration file `.interpret-research-paper.json` in the working directory;
3. derivation from `vault_root` when applicable;
4. current task workspace for non-persistent artifacts.

Only ask the user for a path when they explicitly request persistent Obsidian or final-slide delivery and no safe destination is available.

## Parameters

- `vault_root`: root folder for the user's literature library.
- `note_dir`: Markdown note destination; defaults to `vault_root` when configured.
- `source_dir`: archived paper destination; defaults to `<vault_root>/source`.
- `figure_dir`: extracted figure destination; defaults to `<vault_root>/图片`.
- `ppt_dir`: final slide destination; defaults to `<vault_root>/PPT`.
- `cache_dir`: cache destination; defaults to `<workspace>/.paper-cache`.

Explicit child directories may live outside `vault_root`. Normalize and resolve paths before writing. Do not create or modify a persistent directory until the task authorizes that output.

## Project configuration

Copy `config.example.json` to `.interpret-research-paper.json` and replace example values locally. The real configuration is ignored by Git and must never be committed when it contains personal paths.

Relative configuration paths resolve from the configuration file's directory. Environment variables and home-directory shorthand are not expanded implicitly; use already-resolved paths or a runtime-specific configuration layer when required.

## Portable embeds

When a note and figures share an Obsidian vault, prefer vault-relative embeds. Derive the embed path from resolved locations; never encode the host's absolute path into the note body.
