# ravving_repo

The free things ravving's GET MORE dialog lists: genre packs of pattern presets, single
presets and sounds, project templates, skin sets, soundfonts and demo projects. Everything
here is free to download, use and remix (see LICENSE); ravving itself is at
[ravving/ravving](https://github.com/ravving/ravving).

ravving never browses this repository: a workflow builds one catalog, `index.json`, from
every entry's `meta.json` and publishes it with the files to this repository's GitHub Pages
site. The device fetches that one file, shows the list, and downloads only what you pick,
checking each file's SHA-256 against the catalog.

## Layout

One folder per kind, one folder per entry, a `meta.json` in each. The files are the ones
ravving writes itself (FILES → SEND… to a USB stick), so a contribution is what a stick holds:

```
packs/<id>/meta.json          a whole pack: ravving/presets/<drum|bass|lead|chords>/patterns/*.json
          ravving/presets/…   and ravving/presets/templates/*.json, as on a stick
patterns/<id>/meta.json       one pattern preset file  {"ravving": "preset", "type": "pattern", …}
sounds/<id>/meta.json         one saved sound          {"ravving": "preset", "type": "sound", …}
templates/<id>/meta.json      one project template     {"ravving": "preset", "type": "template", …}
skins/<id>/meta.json          one skin set             {"ravving": "preset", "type": "skin", …}
soundfonts/<id>/meta.json     an .sf2 or .sf3, attached to a release (not committed)
projects/<id>/meta.json       a .ravv bundle or a project .json
schemas/meta.schema.json      what a meta.json holds
tools/validate.py             checks every entry (the pull request check)
tools/build-index.py          writes the site: index.json, the files, the packs as zips
```

`<id>` is lower-case letters, digits and dashes, unique across the repository.

## A meta.json

```json
{
  "id": "jazz",
  "type": "pack",
  "name": "Jazz",
  "about": "Jazz in C minor at a medium 120, swung eighths.",
  "author": "ravving",
  "version": "1.0.0",
  "license": "CC-BY-4.0",
  "tags": ["jazz", "natural minor"],
  "minAppVersion": "0.4.0",
  "files": ["ravving"]
}
```

`files` names what the entry ships, relative to its folder: the files themselves, or for a pack
the `ravving` folder (zipped as one download). A soundfont names its release asset instead:

```json
"asset": {"release": "soundfonts-v1", "file": "vintage-keys.sf2", "size": 12345678, "sha256": "…"}
```

Bump `version` whenever the files change: ravving offers UPDATE to whoever has the older one.

## The catalog

`tools/build-index.py SITE_DIR [--base URL]` writes `index.json` with every entry, each file's
URL, size and SHA-256, and copies the files beside it (packs zipped under `packs/`). The
`publish` workflow runs it on every push to `main` and deploys the result to GitHub Pages, so
`https://ravving.github.io/ravving_repo/index.json` is always the current list, and
`https://ravving.github.io/ravving_repo/` the same catalog as a page, with a download per
entry. Try it locally:

```sh
python3 tools/validate.py
python3 tools/build-index.py /tmp/site --base file:///tmp/site/
RAVVING_STORE_URL=file:///tmp/site/index.json ravving
```

## Contributing

See CONTRIBUTING.md: fork, add your entry's folder, run `tools/validate.py`, open a pull
request. The check runs on every pull request; a maintainer reviews and merges.
