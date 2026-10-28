#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret jazz pack: five pattern presets for each of the drums, the bass, the lead and the
# chords, written as preset files laid out as a USB stick holds them (PresetExchange):
#
#     ravving/presets/<drums|bass|lead|chords>/patterns/<name>.json
#
# Copy the `ravving` folder this writes to a stick's root and the presets dialog's SOURCE ·
# USB plays them straight from there (usb.patternPresets / usb.loadPattern), or the USB page
# imports them. Not installed with ravving: a test of playing presets from a stick, and a gift.
#
# Everything is original, written in scale degrees for a minor key (the charts play in any
# key the header has; ALTER raises a degree by semitones where jazz leaves the natural minor):
#   python3 tools/packs/jazz.py            # writes ./ravving/presets/…

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/jazz/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "jazz")
OUT = os.path.join(PACK, "ravving", "presets")
MINOR = [0, 2, 3, 5, 7, 8, 10]  # what the degrees are measured in (C natural minor: C = 0)
STEPS = 16


def write(group, library, name, chart, genre="Jazz"):
    folder = os.path.join(OUT, group, "patterns")
    os.makedirs(folder, exist_ok=True)
    document = {"ravving": "preset", "type": "pattern", "library": library,
                "preset": {"name": name, "genre": genre, "chart": chart}}
    with open(os.path.join(folder, name.replace("/", "_") + ".json"), "w") as f:
        json.dump(document, f, indent=4, ensure_ascii=False)


# --- drums: a chart per role, x a hit, X an accented one ----------------------------------------
ROLES = ["KICK", "SNARE", "CLAP", "TOM", "HAT", "OPEN", "CYMBAL", "PERC"]


def drums(name, bars, hits):
    """hits: {role: [(step, accented)…]} over bars × 16 steps."""
    chart = {}
    for role, steps in hits.items():
        line = ["."] * (bars * STEPS)
        for step, accent in steps:
            line[step] = "X" if accent else "x"
        chart[role] = "".join(line)
    write("drums", "drum-presets.json", name, chart)


def every(bars, steps, accent=False, offset=0):
    return [(bar * STEPS + s + offset, accent) for bar in range(bars) for s in steps]


# the ride's "ding, ding-a ding, ding-a" (swung with SWING 8), the hi-hat foot on 2 and 4, the
# kick feathered on every beat, the snare dropping a few comping notes
drums("Jazz · Swing Ride", 2, {
    "CYMBAL": every(2, [0, 4, 6, 8, 12, 14]) + [(4, True), (12, True), (20, True), (28, True)],
    "HAT": every(2, [4, 12]),
    "KICK": every(2, [0, 4, 8, 12]),
    "SNARE": [(14, False), (26, False), (30, False)],
})
# bebop: the ride a touch busier, the snare chattering, the kick dropping accented "bombs"
drums("Jazz · Bebop Bombs", 2, {
    "CYMBAL": every(2, [0, 4, 6, 8, 12, 14]),
    "HAT": every(2, [4, 12]),
    "SNARE": [(2, False), (6, False), (10, False), (18, False), (22, False), (27, False), (30, False)],
    "KICK": [(7, True), (15, True), (24, True), (29, True)],
    "TOM": [(28, False), (31, False)],
})
# bossa nova: the rim's 3-2 pattern over two bars, the kick on one and three with its pickup,
# closed hats in eighths
drums("Jazz · Bossa Nova", 2, {
    "PERC": [(0, True), (3, False), (6, False), (10, False), (13, False), (18, True), (22, False), (25, False), (28, False)],
    "KICK": every(2, [0, 6, 8, 14]),
    "HAT": every(2, [0, 2, 4, 6, 8, 10, 12, 14]),
})
# samba: the surdo-like kick on every eighth's second half, sixteenth hats, the snare's
# syncopations and an open hat lifting the bar
drums("Jazz · Samba", 2, {
    "KICK": every(2, [0, 3, 4, 7, 8, 11, 12, 15]) + [(4, True), (12, True), (20, True), (28, True)],
    "HAT": every(2, list(range(16))),
    "SNARE": [(3, False), (6, True), (10, False), (13, False), (19, False), (22, True), (26, False), (29, False)],
    "OPEN": [(14, False), (30, False)],
})
# a ballad: the snare swept in quiet eighths (brushes), the foot on 2 and 4, a soft kick and a
# cymbal swell once in two bars
drums("Jazz · Ballad Brushes", 2, {
    "SNARE": every(2, [0, 2, 4, 6, 8, 10, 12, 14]),
    "HAT": every(2, [4, 12]),
    "KICK": [(0, False), (16, False)],
    "CYMBAL": [(0, False)],
})


# --- bass and lead: notes as semitones above the key's root, written as a chart -----------------
def mono(group, library, name, bars, events):
    """events: [(step, semitones above the root (−12…+23), steps long, accent, slide)]."""
    lanes = {lane: ["."] * (bars * STEPS) for lane in ("NOTES", "OCTAVE", "ACCENT", "SLIDE", "HOLD", "ALTER")}
    for step, semitones, length, accent, slide in events:
        octave = semitones // 12
        pc = semitones - 12 * octave
        degree = max(i for i, s in enumerate(MINOR) if s <= pc)
        lanes["NOTES"][step] = str(degree + 1)
        lanes["OCTAVE"][step] = "+" if octave > 0 else "-" if octave < 0 else "."
        if pc != MINOR[degree]:
            lanes["ALTER"][step] = str(pc - MINOR[degree])
        if accent:
            lanes["ACCENT"][step] = "x"
        if slide:
            lanes["SLIDE"][step] = "x"
        for s in range(step + 1, min(step + length, bars * STEPS)):
            lanes["HOLD"][s] = "x"
    write(group, library, name, {lane: "".join(chars) for lane, chars in lanes.items()})


def bass(name, bars, events):
    mono("bass", "bass-presets.json", name, bars, events)


def lead(name, bars, events):
    mono("lead", "lead-presets.json", name, bars, events)


def quarters(notes, length=3, accents=()):
    """A walking line: one note a beat."""
    return [(i * 4, n, length, i in accents, False) for i, n in enumerate(notes)]


# walking over ii – V – i – turnaround: chord tones on the beats, chromatic approaches into
# each change (F♯ into G, D♭ into C, E♭ down into D)
bass("Jazz · Walking ii–V–i", 4, quarters([2, 5, 8, 6,   7, -1, 2, 1,   0, 3, 7, 10,   9, 8, 7, 3]))
# the two-feel: half notes, root and fifth, a walk-up into the V
bass("Jazz · Two-Feel", 4, [(0, 0, 7, True, False), (8, -5, 7, False, False),
                            (16, 5, 7, True, False), (24, 0, 7, False, False),
                            (32, 2, 7, True, False), (40, 8, 7, False, False),
                            (48, 7, 4, True, False), (52, 9, 3, False, False), (56, 11, 3, False, True), (60, 12, 3, False, False)])
# bossa: root on the beat, the fifth below on the "and" of two, the pattern again
bass("Jazz · Bossa Root–Fifth", 4, [e for bar, root in enumerate([0, 0, 5, 7])
                                     for e in [(bar * 16, root, 6, True, False), (bar * 16 + 6, root - 5, 2, False, False),
                                               (bar * 16 + 8, root, 6, False, False), (bar * 16 + 14, root - 5, 2, False, False)]])
# bebop eighths: up the scale with the chromatic passing tone, down again from the octave
bass("Jazz · Bebop Walk", 2, [(i * 2, n, 2, i % 4 == 0, False) for i, n in enumerate([0, 2, 3, 4, 5, 7, 8, 11,   12, 10, 9, 8, 7, 5, 3, 2])])
# a tumbao: the "and" of two and beat four, anticipating the next chord, sliding between
bass("Jazz · Tumbao", 2, [(6, -5, 6, True, True), (12, 0, 10, False, False),
                          (22, 0, 6, True, True), (28, 5, 4, False, False)])

# a bebop line: eighths down through a chromatic neighbour, up the minor arpeggio, into a held
# note
lead("Jazz · Bebop Line", 2, [(i * 2, n, 2, i == 0, False) for i, n in enumerate([7, 5, 3, 2, 1, 2, 5, 8])]
                             + [(16, 10, 2, True, False), (18, 9, 2, False, False), (20, 8, 2, False, False), (22, 7, 2, False, False),
                                (24, 3, 6, True, False), (30, 2, 2, False, False)])
# blues: a call rising to the blue note (the ♭5, F♯) bending into G, an answer coming down
lead("Jazz · Blues Call & Answer", 2, [(0, 0, 2, True, False), (2, 3, 2, False, False), (4, 5, 2, False, False), (6, 6, 1, False, True),
                                       (7, 7, 5, True, False),
                                       (20, 10, 2, False, False), (22, 7, 2, False, False), (24, 5, 2, False, False), (26, 3, 2, False, False),
                                       (28, 0, 4, True, False)])
# a ballad: long notes coming down from the ninth, through the leading tone home
lead("Jazz · Ballad", 4, [(0, 14, 12, True, False), (12, 12, 4, False, True), (16, 10, 8, False, False), (24, 8, 8, False, False),
                          (32, 7, 12, True, False), (44, 5, 4, False, False), (48, 11, 8, True, False), (56, 12, 8, False, False)])
# dorian: the riff leans on the raised sixth (A natural in C minor), the second bar ends home
lead("Jazz · Dorian Riff", 2, [(0, 0, 2, True, False), (3, 3, 1, False, False), (4, 5, 2, False, False), (6, 9, 2, True, False),
                               (10, 7, 2, False, False), (12, 5, 2, False, False), (14, 3, 2, False, False),
                               (16, 0, 2, True, False), (19, 3, 1, False, False), (20, 5, 2, False, False), (22, 9, 2, True, False),
                               (26, 7, 2, False, False), (28, 2, 2, False, False), (30, 0, 2, False, False)])
# bossa: a syncopated melody that hangs over the bar lines
lead("Jazz · Bossa Melody", 4, [(0, 7, 3, True, False), (3, 8, 3, False, False), (6, 7, 8, False, False),
                                (14, 3, 6, True, False), (20, 5, 3, False, False), (23, 7, 7, False, False),
                                (30, 10, 3, True, False), (33, 8, 3, False, False), (36, 7, 10, False, False),
                                (46, 5, 4, False, False), (50, 3, 6, True, False), (56, 2, 8, False, False)])


sys.path.insert(0, HERE)
from patternkit import chord_ties, write_template  # noqa: E402

# --- chords: rootless jazz voicings, written as chromatic chords (semitones from the chord base) ---
V = {
    "Cm9": [3, 7, 10, 14], "Cm6": [3, 7, 9, 14], "Dm7b5": [5, 8, 12, 14], "G7b9": [11, 14, 17, 20],
    "Fm9": [8, 12, 15, 19], "Abmaj7#11": [8, 12, 14, 19], "Ab7": [8, 12, 15, 18], "Db7": [13, 17, 20, 23],
    "Ebmaj7": [7, 10, 14, 15], "Q1": [0, 5, 10, 15], "Q2": [2, 7, 12, 17], "Q3": [-2, 3, 8, 13],
}
CHARLESTON = [(0, 2), (6, 2)]
BOSSA = [(0, 2), (3, 2), (6, 2), (10, 2), (13, 2)]
WHOLE = [(0, 16)]


def chords(name, bars, plan, ties=None):
    """plan: [(bar, voicing name, [(step, steps)…])]: each hit a chromatic chord held for its steps;
    `ties` as patternkit's Pack.chords()."""
    line = ["."] * (bars * STEPS)
    voicings = {}
    for bar, chord, hits in plan:
        for start, length in hits:
            for s in range(bar * STEPS + start, min(bar * STEPS + start + length, bars * STEPS)):
                line[s] = "c"
                voicings[str(s)] = V[chord]
    chart = {"CHORDS": "".join(line), "VOICINGS": voicings}
    if ties:
        chart["TIES"] = chord_ties(chart, [], ties, name)
    write("chords", "chord-presets.json", name, chart)


chords("Jazz · ii–V–i Charleston", 4, [(0, "Dm7b5", CHARLESTON), (1, "G7b9", CHARLESTON), (2, "Cm9", CHARLESTON), (3, "Cm6", CHARLESTON)])
# an eight-bar minor blues, comped on the "and"s with a push into each next bar
chords("Jazz · Minor Blues", 8, [(bar, chord, [(2, 2), (10, 2), (14, 2)]) for bar, chord in
                                 enumerate(["Cm9", "Fm9", "Cm9", "Cm9", "Fm9", "Fm9", "Ab7", "G7b9"])])
chords("Jazz · Bossa i–iv", 4, [(0, "Cm6", BOSSA), (1, "Cm6", BOSSA), (2, "Fm9", BOSSA), (3, "G7b9", BOSSA)])
# a modal vamp in fourths, moving up a step and back, the hits off the beat
chords("Jazz · Quartal Vamp", 4, [(0, "Q1", [(0, 6), (10, 4)]), (1, "Q2", [(2, 6)]), (1, "Q1", [(12, 4)]),
                                  (2, "Q1", [(0, 6), (10, 4)]), (3, "Q3", [(2, 6)]), (3, "Q1", [(12, 4)])])
# a ballad's changes held a bar each, the tritone substitution (D♭7) before the last V
chords("Jazz · Ballad Changes", 8, [(bar, chord, WHOLE) for bar, chord in
                                    enumerate(["Cm9", "Abmaj7#11", "Dm7b5", "G7b9", "Ebmaj7", "Db7", "Cm6", "G7b9"])], ties="all")

# the template: how a project plays these best (the projects dialog's TEMPLATES)
write_template(OUT, "Jazz", 120, "C", "Natural Minor", swing=62, echo=0.1,
               about="Jazz in C minor (the charts' C = 0) at a medium 120, swung eighths-feel sixteenths, a little room.")

if __name__ == "__main__":
    count = sum(len(files) for _, _, files in os.walk(OUT))
    print(f"{count} presets under {OUT}")
