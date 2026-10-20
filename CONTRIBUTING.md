# Contributing

Thanks for sharing. Everything here lands on other people's devices, so the rules are few
and firm.

## What goes in

- Only ravving's own file formats: what FILES → SEND… writes to a USB stick (pattern presets,
  saved sounds, templates, skins) or a `.ravv` project bundle, plus `.sf2` / `.sf3` soundfonts.
- Only data. A skin is colours; a preset is a chart and a sound's settings. Nothing that runs.
- Only what you may share under the repository's licence (CC-BY-4.0), or a licence you name in
  `meta.json` that lets anyone download, use and remix it. A soundfont keeps its own licence:
  name it.

## How

1. Fork the repository and make a folder for your entry: `<kind>/<id>/`, the id in lower-case
   letters, digits and dashes (`my-techno-kit`), unique in the whole repository.
2. Put the file (or, for a pack, the `ravving` folder a stick holds) in it, and a `meta.json`
   beside it (README.md shows one; `schemas/meta.schema.json` says what it holds). A pattern
   can be written from a spec of bars instead: `python3 tools/write-pattern.py SPEC.json`
   (`tools/examples/dark-techno-drive.json`); `.claude/skills/ravving-patterns/SKILL.md` has
   the grid, the rows and the accents, for people and for agents.
3. Run `python3 tools/validate.py`. It says what is missing or wrong, and exits 1 until it is
   right.
4. Open a pull request. The same check runs there; a maintainer reviews it and merges.

## Sizes

| Kind | Limit |
|---|---|
| a preset, sound, template or skin file | 256 KB |
| a pack (its `ravving` folder) | 8 MB, 400 files |
| a project `.json` or `.ravv` bundle | 64 MB |
| a soundfont | attached to a release by a maintainer, under 2 GB |

A soundfont is not committed: attach it to the pull request (or link it), and a maintainer
uploads it to a release and fills in `asset` in your `meta.json`.

## Updating an entry

Change the files, bump `version` in `meta.json` (`1.0.0` → `1.1.0`), open a pull request.
Devices that have the older version see UPDATE.
