#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Gives a chord pattern's custom shapes their home (HOMES: by step, the degree 1–7 of the key
whose chord the shape is), so ravving draws each on its chord's row and names it from that
root ("Emaj9/D#" for an upstroke on an E shape's top strings). The root is found as ravving's
KeySpelling::voicingName finds it: each note tried, a third and a fifth above it counting most,
then the bass; a shape whose root is outside the key gets none.

    python3 tools/add-homes.py patterns/<id> --key E --scale Mixolydian [--bump]

--bump raises meta.json's version's minor number (devices with the entry see UPDATE).
"""
import argparse, json, pathlib

SCALES = {"Major": [0, 2, 4, 5, 7, 9, 11], "Natural Minor": [0, 2, 3, 5, 7, 8, 10], "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
          "Dorian": [0, 2, 3, 5, 7, 9, 10], "Lydian": [0, 2, 4, 6, 7, 9, 11], "Phrygian": [0, 1, 3, 5, 7, 8, 10]}
NOTES = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}


def root_of(notes):
    classes = sorted({n % 12 for n in notes})
    bass = min(notes) % 12
    best, root = -1, None
    for c in classes:
        has = {(p - c) % 12 for p in classes}
        score = (3 if 3 in has or 4 in has else 0) + (2 if 7 in has else 1 if 6 in has or 8 in has else 0) + (0.5 if c == bass else 0)
        if score > best:
            best, root = score, c
    return root


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("entry", type=pathlib.Path); ap.add_argument("--key", required=True)
    ap.add_argument("--scale", default="Major", choices=SCALES); ap.add_argument("--bump", action="store_true")
    a = ap.parse_args()
    key = NOTES[a.key]; scale = SCALES[a.scale]
    path = a.entry / "preset.json"
    document = json.loads(path.read_text())
    chart = document["preset"]["chart"]
    homes, seen = {}, {}
    for step, voicing in chart.get("VOICINGS", {}).items():
        if chart["CHORDS"][int(step)] != "c":
            continue  # scale-degree voicings ("x") keep ravving's own reading
        notes = [48 + key + s for s in voicing]
        root = root_of(notes)
        degree = scale.index((root - key) % 12) + 1 if (root - key) % 12 in scale else None
        if degree:
            homes[step] = degree
        seen[tuple(voicing)] = degree
    chart["HOMES"] = dict(sorted(homes.items(), key=lambda kv: int(kv[0])))
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
    if a.bump:
        meta_path = a.entry / "meta.json"
        meta = json.loads(meta_path.read_text())
        major, minor, *_ = (meta["version"].split(".") + ["0", "0"])
        meta["version"] = f"{major}.{int(minor) + 1}.0"
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    shapes = ", ".join(f"{'?' if d is None else d}" for d in seen.values())
    print(f"{a.entry.name}: {len(homes)} steps homed, shapes' degrees {shapes}")


if __name__ == "__main__":
    main()
