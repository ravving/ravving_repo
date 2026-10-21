# Write a pattern from a text specification

Use `tools/write-pattern.py` to turn a JSON description of notes or drum hits into a pattern entry. The script writes both `meta.json` and `preset.json` under `patterns/<id>/`.

This guide starts with a drum pattern. Run the commands from the repository's top-level folder, using Python 3.

## Create a specification

Save the following as `my-house-beat-spec.json` in your local working copy. Change the author to your name and choose an ID not already used in the repository.

```json
{
  "id": "my-house-beat",
  "name": "House · Evening Beat",
  "genre": "House",
  "about": "A one-bar house drum pattern with off-beat hi-hats.",
  "author": "Your name",
  "version": "1.0.0",
  "license": "CC-BY-4.0",
  "tags": ["house", "drums", "1 bar"],
  "library": "drum-presets.json",
  "rows": {
    "KICK": ["x...x...x...x..."],
    "SNARE": ["....x.......x..."],
    "HAT": ["..x...x...x...x."]
  }
}
```

Each string is one bar of **16 steps**, read from left to right:

- `.` is an empty step.
- `x` is a hit.
- `X` is an accented hit. Drum accents apply to the step; keep accent markings consistent across rows that hit together.

Each row's list holds its bars. All rows must have the same number of bars, from one to eight. Leave out rows that contain no hits at all.

The drum row names are `KICK`, `SNARE`, `CLAP`, `TOM`, `HAT`, `OPEN`, `CYMBAL` and `PERC`.

## Generate the entry

```sh
python3 tools/write-pattern.py my-house-beat-spec.json
```

This creates:

```text
patterns/my-house-beat/meta.json
patterns/my-house-beat/preset.json
```

**The script replaces these files if that ID already exists.** Choose a new ID for a new contribution. Only reuse an existing ID when you intend to update that entry.

Review the generated metadata. The script uses defaults for omitted fields, including author, licence and minimum app version; those defaults are not evidence that your pattern has been tested with that version.

## Validate and listen

```sh
python3 tools/validate.py
```

Fix any reported errors, then test the pattern in ravving. This example does not select a drum kit; listen with the kit you intend it to accompany and document any requirements.

Submit the generated entry folder following [Contributing](CONTRIBUTING.md). Keep your working specification outside that folder: unlisted files inside an entry fail validation. You do not need to include the local specification in the pull request for an exported entry.

## More complex patterns

The script also supports `bass-presets.json`, `lead-presets.json` and `chord-presets.json`. Their note rows and chord voicings differ from drum rows; do not reuse the drum notation unchanged.

For existing examples and current format details, consult [the example specification](tools/examples/dark-techno-drive.json), [the script's format notes](tools/write-pattern.py) and the presets in [packs](packs/). The drum guide above is a complete starting route; a separate melodic/chord notation reference would be useful before teaching those formats as a beginner workflow.
