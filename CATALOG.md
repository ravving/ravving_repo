# Maintain and preview the catalog

This page is for contributors working on catalog generation or publication. To add an exported preset, start with [Contributing](CONTRIBUTING.md).

## Sources and generated files

Entries live in `packs/`, `patterns/`, `sounds/`, `templates/`, `skins/`, `icons/`, `soundfonts/` and `projects/`. A category directory may be absent when it has no entries.

Each entry's `meta.json` supplies its ID, type, display name, version and optional descriptive fields. The [metadata schema](schemas/meta.schema.json) describes these fields. [The validator](tools/validate.py) also checks file formats, paths, size limits and repository-wide ID uniqueness.

For ordinary entries, `files` lists plain filenames beside `meta.json`. A pack uses `"files": ["ravving"]`; the builder packages that folder as a ZIP. A soundfont uses release-asset metadata instead of committed content.

The builder writes:

- `index.json`: the catalog consumed by ravving.
- `index.html`: the catalog's download page.
- The downloadable files and pack ZIPs.
- Individual pattern and template files extracted from packs for online browsing.
- `.nojekyll`: the GitHub Pages marker.

Generated file records contain a URL, byte size and SHA-256 checksum. The app uses these to check downloads. Entry versions let it identify updates to installed content.

## Individual presets and templates

A pattern entry or a pack can include a `presets` list in the generated index. It describes each pattern's name, genre, library, optional sound and downloadable file. The library identifies the instrument: for example, `drum-presets.json` or `bass-presets.json`.

Templates are listed there too. A template record has `type: "template"`, tempo/key information and an empty library. This lets the templates dialog offer them separately from instrument patterns.

These are generated records, not fields to copy into an entry's `meta.json`. Inspect a generated `index.json` when working on the consumer format.

## Build a local preview

Use Python 3; the automated workflow uses Python 3.12. Run these commands from the repository root:

```sh
python3 tools/validate.py
python3 tools/build-index.py /tmp/ravving-catalog-preview --base http://localhost:8100/
python3 -m http.server 8100 --directory /tmp/ravving-catalog-preview
```

Use a fresh output directory for a clean preview. The builder writes into the directory you supply.

Leave the server running and open `http://localhost:8100/` in a browser on the same computer. The builder also validates all entries before generating the site. It stops if validation fails.

This checks the generated catalog and downloads, not musical behaviour. The page's branding assets reference the main ravving website, so this preview is not entirely self-contained offline.

## Point a test app at a catalog

An existing ravving test environment can use `RAVVING_STORE_URL` to select another index. For example, on the same machine as the preview server:

```sh
RAVVING_STORE_URL=http://localhost:8100/index.json ravving
```

This assumes a working ravving installation; building the catalog does not install the instrument or its audio dependencies.

If ravving runs on another device, use the preview computer's reachable network address in **both** the builder's `--base` URL and `RAVVING_STORE_URL`. `localhost` on the MIKO refers to the MIKO, not your computer. Rebuild the catalog after changing the base URL.

## Publication

The `validate` workflow checks pull requests and pushes to branches other than `main`.

A push to `main`, or a manual run of the `publish` workflow, builds the site and deploys it to GitHub Pages. The builder runs validation first. A merge alone does not prove publication succeeded: check that the deployment completed.

The configured public endpoints are:

- Catalog page: `https://ravving.github.io/ravving_repo/`
- App index: `https://ravving.github.io/ravving_repo/index.json`

Before announcing an update, check the published entry, version and downloads. In ravving, refresh GET MORE and check the relevant ONLINE source where applicable.
