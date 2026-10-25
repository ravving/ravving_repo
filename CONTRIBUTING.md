# Share something you made with ravving

You can contribute patterns, sounds, templates, skin sets, icon packs, genre packs, soundfonts and projects. After review and a successful publication, your contribution becomes available through ravving's **GET MORE** catalog.

This guide takes you through adding one entry. An **entry** is a folder containing your files and a `meta.json` file that describes them.

## Before you start

You will need:

- The files you want to share, preferably exported and tested in ravving.
- A GitHub account and a local copy of your fork of this repository.
- Python 3 to check your contribution. The repository's automated checks use Python 3.12; the validation script needs no additional Python packages.

A **fork** is your own GitHub copy of the repository. A **pull request** asks the maintainers to review changes from your fork and add them here.

Share data files only, not executable code. Check that you have permission to share all included material, including samples in a project. Follow the repository's [licence policy](LICENSE), and identify an entry's different licence in `meta.json` where applicable. Include the source and attribution information in your pull request so the maintainer can review it.

**Contributing a soundfont?** Follow [Soundfonts](#soundfonts) below. They use a different upload process.

## 1. Choose a folder and an ID

Choose the folder that matches your contribution:

| You are sharing | Folder | `type` in `meta.json` |
|---|---|---|
| A collection of presets, such as a genre pack | `packs/` | `pack` |
| A pattern for one instrument | `patterns/` | `pattern` |
| A saved sound | `sounds/` | `sound` |
| A starting setup for a project | `templates/` | `template` |
| A set of instrument colours | `skins/` | `skin` |
| A set of drawings for ravving's icons | `icons/` | `icons` |
| A project JSON file or `.ravv` bundle | `projects/` | `project` |
| A soundfont, coordinated with a maintainer | `soundfonts/` | `soundfont` |

Create the category folder if it does not exist yet.

Give your entry an **ID**, such as `my-house-beat`. Use lowercase letters, digits and dashes, starting with a letter or digit. The ID must be no more than 64 characters and unique across all categories.

For example, a single pattern would have this layout:

```text
patterns/
  my-house-beat/
    meta.json
    preset.json
```

The folder name and the `id` in `meta.json` must match. The display name can be more descriptive, such as “House · Evening Beat”.

## 2. Add your file

For a pattern, sound, template, skin or icon pack, copy the corresponding ravving JSON file into your entry's folder. Keep the exported document intact: renaming another kind of JSON file does not convert it into a preset.

A project can be a `.json` file or a `.ravv` bundle. Use a bundle when you need to include the project's samples. Test the shared version and note any additional sound requirements in your pull request.

For a pack, copy its `ravving` folder into the entry. For example:

```text
packs/
  my-house-pack/
    meta.json
    ravving/
      presets/
        drums/
          patterns/
            Evening Beat.json
        bass/
          patterns/
            Evening Bass.json
        templates/
          Evening House.json
```

The drum folder is **`drums`**, not `drum`. Other pattern groups are `bass`, `lead`, `chords`, `sampler` and `pads`. Packs can also contain saved sounds under `<machine>/sounds/`, skin files under `skins/` and icon packs under `icons/`, within `ravving/presets/`.

## 3. Describe your entry

Create `meta.json` beside your file. For the single-pattern example:

```json
{
  "id": "my-house-beat",
  "type": "pattern",
  "name": "House · Evening Beat",
  "about": "A one-bar house drum pattern with off-beat hi-hats.",
  "author": "Your name",
  "version": "1.0.0",
  "license": "CC-BY-4.0",
  "tags": ["house", "drums", "1 bar"],
  "files": ["preset.json"]
}
```

Replace the example values with your own. In particular, describe the file you actually supplied and use its appropriate licence.

| Field | What to write |
|---|---|
| `id` | The entry's folder name. |
| `type` | The singular type from the table above. |
| `name` | The catalog display name, up to 64 characters. |
| `version` | Start at `1.0.0`; increase it when the shared files change. |
| `about` | A useful description, up to 240 characters. Say what it sounds like or helps someone do. |
| `author` | The name you want displayed, up to 64 characters. |
| `license` | The licence identifier for this material. |
| `tags` | Up to 12 searchable terms, each no more than 32 characters. |
| `files` | The exact filenames in this folder. For a pack, use `["ravving"]`. |
| `minAppVersion` | Optional: the oldest ravving version known to support the entry. Do not guess it. |

The validator requires `id`, `type`, `name` and `version`, plus `files` for entries other than soundfonts. The descriptive fields help people decide what to download. The full field rules are in [the metadata schema](schemas/meta.schema.json).

Use plain filenames in `files`, not absolute paths or paths containing `/`. List every supplied file; extra files beside `meta.json` fail validation. Put review notes in the pull request rather than adding an unlisted README to the entry.

For patterns, also check the **preset file's** `name` and `genre`. The preset's genre controls its grouping in the presets dialog; catalog `tags` do not replace it.

## 4. Check the contribution

Open a terminal in the repository's top-level folder—the one containing this guide—and run:

```sh
python3 tools/validate.py
```

A successful check ends with a summary such as:

```text
62 entries, 0 errors
```

The entry count depends on the repository. The important part is **`0 errors`**.

If the check reports an error, fix the named file and run it again:

| Message | What to check |
|---|---|
| `no meta.json` | Put `meta.json` directly inside the entry folder. |
| `id ... is not the folder's name` | Make the ID and folder name identical. |
| `type ... does not match the folder` | Use the singular type for that category, such as `pattern` inside `patterns/`. |
| `missing (or a symlink)` | Check that each filename in `files` exists and is a regular file, not a symbolic link. |
| `not a ravving preset file` | Use the correct ravving export format. |
| `files not named in meta.json` | Remove unrelated files or list the intended files. |

You can check just your entry while working:

```sh
python3 tools/validate.py patterns/my-house-beat
```

Run the full check before submitting: an entry-only check cannot detect duplicate IDs elsewhere in the repository.

Validation checks structure and size. It does not listen to a pattern or confirm that a project sounds right. Try the contribution in ravving and describe what you tested.

## 5. Submit a pull request

Commit the entry folder to a branch in your fork, push that branch to GitHub, and open a pull request against this repository.

In the description, include:

- What you are sharing and where its entry folder is.
- The ravving version and device used for testing, or what you could not test.
- Any required sounds, samples or soundfonts.
- The source, licence and attribution for material you did not create yourself.
- The result of `python3 tools/validate.py`.

The automated validation runs on the pull request. A maintainer reviews the contribution and may ask for changes before merging it.

After the merge **and successful catalog deployment**, the entry becomes available through GET MORE. Refresh the catalog if it has not appeared yet. Individual patterns also become available under **SOURCE → ONLINE** in the presets dialog; templates have an ONLINE source in their own dialog.

## File limits

| Contribution | Limit |
|---|---|
| Each pattern, sound, template, skin or icon pack JSON file | 256 KiB (262,144 bytes) |
| A pack's `ravving` folder | 8 MiB total and no more than 400 files |
| Each project JSON file or `.ravv` bundle | 64 MiB |
| Soundfont | The contribution policy requires under 2 GB; a maintainer handles the release upload |

These pack and JSON limits are checked by the validator. The soundfont size policy requires maintainer review; the current validator checks its metadata, not the uploaded file's contents or that upper limit.

## Soundfonts

Do not commit `.sf2` or `.sf3` files to Git. Provide a download link and the source, licence and attribution information for the maintainer to review.

The soundfont's `meta.json` needs an `asset` object containing a release tag, asset filename, byte size and SHA-256 checksum. The maintainer uploads the accepted file and supplies these values. Only `meta.json` belongs in the soundfont entry folder.

An entry without its release metadata will fail validation. Coordinate the upload and metadata with the maintainer before expecting the contribution check to pass. Do not invent a checksum or use placeholder release information to get past the check.

## Update an existing entry

Keep its ID and folder name. Change the files, increase `version` in `meta.json`—for example, from `1.0.0` to `1.1.0`—and run validation again.

Open a pull request explaining the changes and any new requirements. After successful publication, ravving can offer UPDATE to people who installed the older entry.

## Optional: write a pattern from a specification

If you prefer editing a pattern as text, use [the pattern-writing guide](PATTERN_AUTHORING.md). It explains the input file and the generated output. This is an alternative to exporting a pattern from ravving, not a requirement for contributing one.
