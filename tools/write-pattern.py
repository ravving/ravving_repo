#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Writes a single-pattern entry (patterns/<id>/meta.json + preset.json) from a spec, so a
pattern is written as bars of 16 steps and checked before it lands:

    python3 tools/write-pattern.py SPEC.json [SPEC.json ...]

A spec (tools/examples/dark-techno-drive.json is one):

    {
      "id": "dark-techno-drive",                 lower-case letters, digits, dashes
      "name": "Techno · Dark Drive",             the preset's name, "<Genre> · <Name>"
      "genre": "Techno",                         the group the presets dialog shows it under
      "about": "one line on it and its references",
      "tags": ["techno", "dark techno", "130 bpm", "2 bars", "brooding"],
      "library": "drum-presets.json",            drum- | bass- | lead- | chord-presets.json
      "kit": "/zynthian/zynthian-data/soundfonts/SFZ Drum Machines/Roland TR909.sf3",   (drums, optional)
      "sound": {"soundSource": "Nylon guitar", "sourceSound": {"ENVELOPE/RELEASE": 0.4}},
                                                 (bass, lead, chords, optional: a source by its name
                                                 in ravving's kits.json and its MODS, 0..1)
      "voicings": {"0": [0, 4, 7], "16": [-3, 0, 4, 9]},   (chords: each "c" or "x" step's notes)
      "accents": [0, 16],                        the steps hit harder (the whole step's, every row)
      "rows": {                                  a row per role, each a list of 16-character bars
        "KICK": ["x...x...x...x...", "x...x...x...x..."],
        "HAT":  ["..x...x...x...x.", "..x...x...x.x.x."]
      }
    }

Drum rows are KICK, SNARE, CLAP, TOM, HAT, OPEN, CYMBAL and PERC; a step is "." (nothing) or
"x" (a hit); an accented step is written "X" on every row that hits it (ravving accents the
step, not one row). Every row has the same number of bars, 8 at most. The bass and lead rows
(NOTES 1–7, OCTAVE + -, ACCENT, SLIDE, HOLD, ALTER) and the chords' (CHORDS 1–7 x c,
VOICINGS) are written as the packs write them (packs/*/ravving/presets): the script only
checks their lengths, and for the chords that every "c" or "x" step has its voicing (semitones
from the key's root for "c", scale degrees for "x") and no voicing sits on another step. Exit 1
with the reasons when a spec is wrong.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRUM_ROLES = ("KICK", "SNARE", "CLAP", "TOM", "HAT", "OPEN", "CYMBAL", "PERC")
LIBRARIES = ("drum-presets.json", "bass-presets.json", "lead-presets.json", "chord-presets.json")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
MAX_BARS = 8


def check(spec, errors):
    for key in ("id", "name", "genre", "about", "rows"):
        if key not in spec:
            errors.append(f"the spec lacks {key}")
    if not ID_RE.match(str(spec.get("id", ""))):
        errors.append("id: lower-case letters, digits and dashes (64 at most)")
    library = spec.get("library", "drum-presets.json")
    if library not in LIBRARIES:
        errors.append(f"library: one of {', '.join(LIBRARIES)}")
    rows = spec.get("rows", {})
    if not isinstance(rows, dict) or not rows:
        return errors.append("rows: a row per role")
    bars = {len(bar_list) for bar_list in rows.values() if isinstance(bar_list, list)}
    if len(bars) != 1:
        errors.append(f"every row has the same number of bars (found {sorted(bars)})")
    elif next(iter(bars)) > MAX_BARS:
        errors.append(f"{next(iter(bars))} bars: {MAX_BARS} at most")
    for role, bar_list in rows.items():
        if library == "drum-presets.json" and role not in DRUM_ROLES:
            errors.append(f"{role}: a drum row is one of {', '.join(DRUM_ROLES)}")
        if not isinstance(bar_list, list) or not bar_list:
            errors.append(f"{role}: a list of bars")
            continue
        for n, bar in enumerate(bar_list, 1):
            if not isinstance(bar, str) or len(bar) != 16:
                errors.append(f"{role} bar {n}: 16 characters, found {len(bar) if isinstance(bar, str) else bar!r}")
            elif library == "drum-presets.json" and not re.match(r"^[.xX]{16}$", bar):
                errors.append(f"{role} bar {n}: only . x X")
        if library == "drum-presets.json" and all(c == "." for c in "".join(b for b in bar_list if isinstance(b, str))):
            errors.append(f"{role}: an empty row (leave it out)")
    voicings = spec.get("voicings")
    if voicings is not None:
        if library != "chord-presets.json" or not isinstance(voicings, dict):
            errors.append("voicings: a map of step to notes, for the chords only")
        else:
            chords = "".join(b for b in rows.get("CHORDS", []) if isinstance(b, str))
            custom = {str(i) for i, c in enumerate(chords) if c in "cx"}
            for step in sorted(custom - set(voicings), key=int):
                errors.append(f"CHORDS step {step}: a \"c\" or \"x\" without its voicing")
            for step, notes in voicings.items():
                if step not in custom:
                    errors.append(f"voicings {step}: not a \"c\" or \"x\" step of CHORDS")
                elif not isinstance(notes, list) or not notes or any(not isinstance(n, int) for n in notes):
                    errors.append(f"voicings {step}: a list of whole numbers")
    sound = spec.get("sound")
    if sound is not None and (not isinstance(sound, dict) or not isinstance(sound.get("soundSource", ""), str)):
        errors.append("sound: a map with the soundSource's name (and its sourceSound MODS)")
    accents = spec.get("accents", [])
    if not isinstance(accents, list) or any(not isinstance(a, int) or a < 0 for a in accents):
        errors.append("accents: a list of step numbers (0 is the first step of bar 1)")


def chart_of(spec):
    rows = {role: "".join(bars) for role, bars in spec["rows"].items()}
    if spec.get("library", "drum-presets.json") != "drum-presets.json":
        if spec.get("voicings"):
            rows["VOICINGS"] = {step: spec["voicings"][step] for step in sorted(spec["voicings"], key=int)}
        return rows
    accents = set(spec.get("accents", []))
    chart = {}
    for role, row in rows.items():
        chart[role] = "".join("X" if (c == "x" and i in accents) else c for i, c in enumerate(row))
    return chart


def write(spec_path):
    errors = []
    try:
        spec = json.loads(pathlib.Path(spec_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f"{spec_path}: not JSON ({error})"]
    check(spec, errors)
    if errors:
        return [f"{spec_path}: {e}" for e in errors]
    chart = chart_of(spec)
    for step in spec.get("accents", []):
        if not any(isinstance(row, str) and step < len(row) and row[step] != "." for row in chart.values()):
            return [f"{spec_path}: accent on step {step}, which nothing hits"]
    preset = {"name": spec["name"], "genre": spec["genre"], "chart": chart}
    if spec.get("kit"):
        preset["sound"] = {"kit": spec["kit"]}
    elif spec.get("sound"):
        preset["sound"] = spec["sound"]
    document = {"ravving": "preset", "type": "pattern", "library": spec.get("library", "drum-presets.json"), "preset": preset}
    bars = len(next(iter(spec["rows"].values())))
    meta = {"id": spec["id"], "type": "pattern", "name": spec["name"], "about": spec["about"],
            "author": spec.get("author", "ravving"), "version": spec.get("version", "1.0.0"),
            "license": spec.get("license", "CC-BY-4.0"), "tags": spec.get("tags", []),
            "minAppVersion": spec.get("minAppVersion", "0.4.0"), "files": ["preset.json"]}
    folder = ROOT / "patterns" / spec["id"]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "preset.json").write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{folder.relative_to(ROOT)}: {spec['name']} · {bars} bar{'s' if bars != 1 else ''} · {len(chart)} rows")
    return []


def main(argv):
    if not argv:
        print(__doc__.split("\n\n")[1])
        return 2
    errors = []
    for spec_path in argv:
        errors.extend(write(spec_path))
    for line in errors:
        print(line)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
