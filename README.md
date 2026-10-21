# The ravving community catalog

Patterns, sounds, templates, skins and projects to use with ravving on your MIKO. This repository supplies the content listed in ravving's **GET MORE** dialog.

ravving is the groovebox app; this repository holds downloadable content for it. The app's source is in [ravving/ravving](https://github.com/ravving/ravving).

## Find something to play

On your MIKO, open **MENU → GET MORE**, choose a category and select **GET** on an entry. This downloads the content into the appropriate library. Loading or playing it is the next step.

For individual patterns, open an instrument's presets dialog and choose **SOURCE → ONLINE**. You can try a pattern without downloading its whole pack. **SAVE TO DEVICE** adds it to your saved presets.

You can also [browse the web catalog](https://ravving.github.io/ravving_repo/). For a genre pack downloaded as a ZIP, extract its `ravving` folder to the root of a USB stick. The app's [pack guide](https://ravving.github.io/docs/packs.html) explains how to use it.

## What is in the catalog?

| Category | What it gives you |
|---|---|
| Packs | Collections of presets, often with templates for a genre or musical style. |
| Patterns | A ready-made pattern for one instrument, sometimes with its sound. |
| Sounds | Saved instrument sounds. |
| Templates | A starting setup for a new project. |
| Skins | Sets of instrument colours. |
| Soundfonts | Instrument or drum sounds in `.sf2` or `.sf3` format. |
| Projects | Projects to open and explore; `.ravv` bundles can include their samples. |

The repository supports all these categories; the available entries may change over time.

## Share your work

Start with [Contributing](CONTRIBUTING.md). It walks through choosing a folder, adding a file, describing it and checking it before you submit a pull request.

You can export content from ravving or [write a pattern from a text specification](PATTERN_AUTHORING.md). You do not need to build the app or the catalog website to contribute an exported preset.

## Licences and credits

See [LICENSE](LICENSE) for the repository's content licence. Check an entry's `license` and attribution information for material shared under another licence, including soundfonts.

## Maintaining the catalog

Each entry has its own folder and a `meta.json` description. The publishing workflow validates the entries, builds the catalog and downloads, then deploys them to GitHub Pages.

For the metadata rules, generated index and local preview instructions, see [Catalog maintenance](CATALOG.md).
