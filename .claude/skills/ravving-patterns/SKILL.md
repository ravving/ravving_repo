---
name: ravving-patterns
description: Research and write pattern presets for ravving as entries of this catalog (patterns/<id>, or a whole pack) - the grid, the drum rows, the melodic rows, the accents, the kits, the tags people search for, the validator and the pull request. Use when asked for a new drum pattern, bassline, melody or chord progression in a style, or a pack of them, for ravving's GET MORE.
---

# ravving patterns

An entry is what ravving itself writes to a USB stick (FILES → SEND…): one JSON document per
pattern. Write it from a spec with `tools/write-pattern.py SPEC.json`, which checks the bars
and places `patterns/<id>/meta.json` + `preset.json`; `tools/examples/dark-techno-drive.json`
is a spec to copy. Then `python3 tools/validate.py` (0 errors) and a pull request
(CONTRIBUTING.md). Never commit on the user's behalf unless asked.

## The grid

- 16 steps a bar: step 0 is beat 1, 4 beat 2, 8 beat 3, 12 beat 4; 2/6/10/14 the off-beat
  eighths; the "e" and "a" of a beat are the odd steps. Up to 8 bars; every row of a pattern
  has the same number of bars (a 4-bar pattern: 64 characters a row).
- A pattern holds no tempo, key or swing: say them in the tags ("130 bpm", "C minor") and the
  line about it; a pack's template sets them (packs/*/ravving/presets/templates).
- GET MORE's FIND matches words in the name, the line, the author, the group and the tags:
  tag the genre, the sub-style, the tempo, the bar count, a mood word, and for melodic
  patterns the scale and key.

## Drums (`drum-presets.json`)

- Rows: KICK, SNARE, CLAP, TOM, HAT, OPEN (open hat), CYMBAL, PERC. "." nothing, "x" a hit.
- Accents are the whole step's: `accents: [0, 16]` makes every row that hits those steps "X".
  Accent the downbeats, a drop's hits, or every kick for a hard style; never a step nothing hits.
- A kit (optional) is a path on the device, as the packs name them:
  `/zynthian/zynthian-data/soundfonts/SFZ Drum Machines/Roland TR909.sf3`, `Roland TR808.sf3`,
  `Alesis HR16.sf3`… (the folder's other kits: see the packs' drum presets). A kit without a
  role (no OPEN) just drops that row's hits.
- Leave a row out rather than empty.

## Bass and lead (`bass-presets.json`, `lead-presets.json`), chords (`chord-presets.json`)

Written in scale degrees so a pattern plays in any key: NOTES 1–7 (a digit is a note on, "."
nothing), OCTAVE (+ or - under a note), ACCENT and SLIDE ("x" under a note), HOLD ("x" after a
note stretches it, 64 steps at most), ALTER (a digit: semitones up, for the ♭3 and ♭7 of rock
or trap's ♭2 written against the scale). Chords: CHORDS 1–7 ("x" repeats the last chord, "c"
a chord on a step) and VOICINGS by step. Copy the shape from a pack's file
(`packs/jazz/ravving/presets/bass/patterns/*.json`, `…/chords/patterns/*.json`): the writer
checks only the lengths of these rows. One scale per pack, every line on its degrees.

### Chords that are played, not just held (ravving 0.6)

`CHORDS` steps holding the same voicing are one held chord. To strike it again, list the step
in `STRIKES`. Each chord, by its first step, can carry `VELOCITY` (1–127), `NUDGE` (% of a step,
±50) and `STRUM` (% of a step between one note and the next, ±25: positive is a downstroke,
the lowest string first; negative an upstroke). A strummed guitar: the shapes on the beats and
offbeats, `STRIKES` where the same shape is hit again, downstrokes `STRUM` 4–8 with the beat's
velocity higher, upstrokes `STRUM` −3 to −5, softer, a touch late (`NUDGE` 5–15). Older
ravvings ignore these keys and play the chords held.

## Research before writing

Name the records that define the style and read how their grid goes (kick, clap/snare, hats,
percussion; the tempo range), then write original parts in that language: no transcribed
melodies unless public domain. Put the references in the line about it ("after …") so people
can hear what it is after. Make the five (or however many) clearly different from each other:
sub-styles, tempos, bar counts, density.

## Checks

- `python3 tools/write-pattern.py SPEC.json …` writes the entries or says what is wrong.
- `python3 tools/validate.py` checks every entry as the pull request will.
- `python3 tools/build-index.py /tmp/site --base file:///tmp/site/` builds the catalog; with
  ravving at hand, `RAVVING_STORE_URL=file:///tmp/site/index.json ravving` lists it in GET MORE.
