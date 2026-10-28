#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret Gregorian pack, old gothic: five pattern presets for each of the drums, the bass,
# the lead and the chords (see ../patternkit.py). Written in scale degrees for the DORIAN mode
# (Rave.qml's "Dorian"), made for D Dorian: the first mode of the chant, the Dies Irae's.
#
#   - The Dies Irae (13th century, public domain), its first three phrases as the mfiles.co.uk
#     MIDI gives them: F E F D E C D D | F F G F E D C E | F E D A C D D (in D Dorian: 3 2 3 1
#     2 7 1 1 | 3 3 4 3 2 1 7 2 | 3 2 1 5 7 1 1).
#   - Organum, the first harmony (Musica enchiriadis, c. 895): the chant doubled a perfect fifth
#     above and a perfect fourth below, note for note: "Organum Above" (lead) and "Organum
#     Below" (bass) sing the Dies Irae in the same rhythm as "Dies Irae", so any two loop
#     together.
#   - The drone (bourdon, ison) under the chant; open fifths without thirds.
#   - Dead Can Dance's i v VII IV (In Power We Entrust the Love Advocated: Am Em G D), a
#     saltarello in 6/8, a breakbeat under the chant (the 90s' Enigma way).
# The chant's notes carry a free, sung feel: a soft velocity that swells to the phrase's high
# point, and small nudges either way.
#   python3 tools/packs/gregorian.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/gregorian/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "gregorian")
sys.path.insert(0, HERE)
from patternkit import Pack, N, C, R  # noqa: E402

DORIAN = [0, 2, 3, 5, 7, 9, 10]
pack = Pack("Gregorian", PACK, DORIAN)


def bars12(*parts):
    """Four 12-step bars (6/8) as the three 16-step bars they fill."""
    tokens = " ".join(parts).split()
    if len(tokens) != 48:
        raise ValueError(f"{len(tokens)} steps, not four bars of 12")
    return " | ".join(" ".join(tokens[i:i + 16]) for i in (0, 16, 32))


def rows12(*bars):
    row = "".join(bars).replace(" ", "")
    if len(row) != 48:
        raise ValueError(f"{len(row)} steps, not four bars of 12")
    return row


# the Dies Irae's three phrases, a syllable a quarter, each phrase's last note held three
DIES = [["3", "2", "3", "1", "2", "7-", "1", "1"],
        ["3", "3", "4", "3", "2", "1", "7-", "2"],
        ["3", "2", "1", "5-", "7-", "1", "1"]]
# a sung shape: louder towards the phrase's middle, a hair early or late here and there
SWELL = [80, 86, 92, 98, 96, 90, 86, 82]
NUDGE = ["", "<4", "", ">4", "", "<4", ">6", ""]


def chant(map_note=lambda n: n):
    """The three phrases as tokens (128 steps: eight bars), notes mapped (organum)."""
    tokens = []
    for phrase in DIES:
        for k, note in enumerate(phrase):
            last = k == len(phrase) - 1
            token = f"{map_note(note)}@{SWELL[k]}{NUDGE[k]}"
            tokens.append(N(token, 12 if last else 4))
    text = " ".join(tokens)
    rest = 128 - len(text.split())
    return " | ".join(" ".join((text + " " + R(rest)).split()[i:i + 16]) for i in range(0, 128, 16))


# the fifth above and the fourth below, in the mode (each a perfect interval on these notes)
FIFTH_ABOVE = {"3": "7", "2": "6", "1": "5", "7-": "4", "4": "1+", "5-": "2"}
FOURTH_BELOW = {"3": "7-", "2": "6-", "1": "5-", "7-": "4-", "4": "1", "5-": "2-"}

# --- drums --------------------------------------------------------------------------------------
# a processional: the timpani's D on one and A on three, the bass drum under one, the cymbal
# swelling into the next phrase
pack.drums("Processional", "ORCHESTRA_D", {
    "TOM":    "X............... | X...............",
    "HAT":    "........x....... | ........x.......",
    "KICK":   "x............... | x...........x...",
    "CYMBAL": "................ | ..............x.",
})
# a saltarello (the medieval leaping dance) in 6/8: the tambourine on every eighth, strong on 1
# and 4, the frame drum (the low floor tom) leaping
pack.drums("Saltarello", "FOLK", {
    "PERC": rows12("X.x.x.X.x.x.", "X.x.x.X.x.x.", "X.x.x.X.x.x.", "X.x.x.X.xxxx"),
    "TOM":  rows12("x.....x...x.", "x.....x...x.", "x.....x...x.", "x...x.x.x.x."),
    "KICK": rows12("x...........", "x...........", "x...........", "x.....x....."),
})
# a breakbeat under the chant (the 90s' monks and beats): a lazy kick, the snare on two and
# four, eighth hats, an open hat to turn
pack.drums("Chant Breakbeat", "SP1200", {
    "KICK":  "X.....x...x..... | X.....x.x.......",
    "SNARE": "....X.......X... | ....X.......X...",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x...",
    "OPEN":  "................ | ..............x.",
})
# the Dies Irae's timpani: the D on one, the A on three, a roll on the D into the bar, the
# cymbal crowning the second bar
pack.drums("Wrath Timpani", "ORCHESTRA_D", {
    "TOM":    "X...........xxxx | X...........xxxx",
    "HAT":    "........X....... | ........X.......",
    "KICK":   "X............... | X...............",
    "CYMBAL": "................ | X...............",
})
# a slow ritual on the frame drum: 3 + 3 + 2, the tambourine's shimmer on the off-beats
pack.drums("Ritual Frame", "FOLK", {
    "TOM":  "X..x..x.X..x..x. | X..x..x.X..x.xxx",
    "PERC": "....x.......x... | ....x.......x...",
    "KICK": "x............... | x...............",
})

# --- bass ---------------------------------------------------------------------------------------
# the drone (ison): the final, D, held under the chant, the fifth taking a bar, a soft
# re-strike as a breath
pack.bass("Ison Drone", "Organ · Bourdon 16", " ".join([
    N("1@84", 31), R(1), N("5-@80", 16), N("1@88", 15), R(1)]),
    mods={"ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 2400})
# organum below: the Dies Irae a perfect fourth under it, in its rhythm (pairs with the lead's
# "Dies Irae")
pack.bass("Organum Below", "Cello", chant(lambda n: FOURTH_BELOW[n]),
          mods={"ENVELOPE/ATTACK": 1200, "ENVELOPE/RELEASE": 1800})
# open fifths: D and A, two bars each, swelling
pack.bass("Open Fifths", "Contrabass", " ".join([
    N("1!@96", 16), N("5-@84", 16), N("1@100", 16), N("5-@90", 15), R(1)]),
    mods={"ENVELOPE/ATTACK": 1800, "ENVELOPE/RELEASE": 2400})
# an ostinato pulse: quarters on the D, growing from a whisper to full over two bars, then the A
# falling back
pack.bass("Ostinato Pulse", "Contrabass", " | ".join([
    " ".join(N(f"1@{40 + 10 * k}", 3, 1) for k in range(4)),
    " ".join(N(f"1@{80 + 10 * k}", 3, 1) for k in range(4)),
    " ".join(N(f"5-@{118 - 8 * k}", 3, 1) for k in range(4)),
    " ".join(N(f"1@{86 - 10 * k}", 3, 1) for k in range(4))]))
# Dead Can Dance's ground (i v VII IV: Dm Am C G), the roots held, a step into each
pack.bass("Dorian Ground", "Cello", " | ".join([
    " ".join([N("1!", 14), N("7-@84", 2)]), " ".join([N("5-", 14), N("6-@84", 2)]),
    " ".join([N("7-", 14), N("5-@84", 2)]), " ".join([N("4-", 12), N("6-@84", 2), N("7-@88", 2)])]),
    mods={"ENVELOPE/ATTACK": 600, "ENVELOPE/RELEASE": 1200})

# --- lead ---------------------------------------------------------------------------------------
# the Dies Irae (public domain), sung
pack.lead("Dies Irae", "Choir", chant(),
          mods={"ENVELOPE/ATTACK": 1200, "ENVELOPE/RELEASE": 1800})
# organum above: the Dies Irae a perfect fifth over it, the same rhythm
pack.lead("Organum Above", "Voice oohs", chant(lambda n: FIFTH_ABOVE[n]),
          mods={"ENVELOPE/ATTACK": 1200, "ENVELOPE/RELEASE": 1800})
# an estampie on the krummhorn: a lively Dorian dance tune in eighths, its downbeats leaned on
def dance(*notes):
    return " ".join(N(f"{n}@{106 if k % 4 == 0 else 86}", 2) for k, n in enumerate(notes))
pack.lead("Krummhorn Estampie", "Organ · Krummhorn", " | ".join([
    dance("1", "2", "3", "5", "4", "3", "2", "1"), dance("3", "4", "5", "6", "5", "4", "3", "2"),
    dance("5", "6", "7", "1+", "7", "6", "5", "4"), dance("3", "2", "1", "7-", "1", "2", "1", "1")]))
# a Kyrie's melisma: one syllable carried over many notes, stepwise, rising to the fifth and
# settling on the final
pack.lead("Kyrie Melisma", "Choir", " | ".join([
    " ".join([N("1@80", 4), N("2@84", 2), N("3@88", 2), N("2@86", 2), N("1@82", 2), N("7-@80", 2), N("1@84", 2)]),
    " ".join([N("3@88", 4), N("4@92", 2), N("5@98", 6), N("4@92", 2), N("3@88", 2)]),
    " ".join([N("5@96", 2), N("6@100", 2), N("5@96", 2), N("4@90", 2), N("3@88", 4), N("2@84", 4)]),
    " ".join([N("3@86", 2), N("2@84", 2), N("1@82", 11), R(1)])]),
    mods={"ENVELOPE/ATTACK": 1200, "ENVELOPE/RELEASE": 2400})
# a saltarello on the recorder in 6/8: leaping eighths, 1 and 4 leaned on
def leap(*notes):
    return " ".join(N(f"{n}@{108 if k % 3 == 0 else 84}", 2) for k, n in enumerate(notes))
pack.lead("Saltarello Recorder", "Recorder", bars12(
    leap("5", "4", "3", "5", "4", "3"), leap("2", "3", "4", "5", "4", "3"),
    leap("5", "6", "7", "1+", "7", "5"), leap("4", "3", "2", "1") + " " + N("1!@100", 4)))

# --- chords -------------------------------------------------------------------------------------
# in scale degrees from the final (0-based), as the mode has them; open fifths have no third
G = {"D5": ("x", [0, 4, 7]), "C5": ("x", [-1, 3, 6]), "A5": ("x", [-3, 1, 4]), "G5": ("x", [-4, 0, 3]),
     "i": ("x", [0, 2, 4, 7]), "IV": ("x", [-4, -2, 0, 3]), "VII": ("x", [-1, 1, 3, 6]),
     "v": ("x", [-3, -1, 1, 4]), "isus2": ("x", [0, 1, 4, 7]), "isus4": ("x", [0, 3, 4, 7])}
# organum's open fifths, sung: D, C, A, D, two bars each
pack.chords("Organum Fifths", "Choir", " ".join(
    C("@" + c, 31, 1) for c in ["D5", "C5", "A5", "D5"]), G,
    mods={"ENVELOPE/ATTACK": 1800, "ENVELOPE/RELEASE": 2400})
# the Dorian cadence on the pipe organ: i IV VII i (Dm G C Dm), the IV major (the mode's B)
pack.chords("Dorian Cadence", "Organ · Pipe 16+8+4", " | ".join(
    C("@" + c, 15, 1) for c in ["i", "IV", "VII", "i"]), G, mods={"ENVELOPE/RELEASE": 1800})
# Dead Can Dance's i v VII IV (Dm Am C G), the choir held
pack.chords("Gothic Choir", "Choir", " | ".join(C("@" + c, 15, 1) for c in ["i", "v", "VII", "IV"]), G,
            mods={"ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 2400})
# the vox humana's suspensions: Dsus2, Dm, Dsus4, Dm, slow
pack.chords("Vox Humana", "Organ · Vox humana", " | ".join(
    C("@" + c, 16) if k % 2 == 0 else C("@" + c, 15, 1) for k, c in enumerate(["isus2", "i", "isus4", "i"])), G,
    mods={"ENVELOPE/RELEASE": 2400}, ties="all")
# a psalter's harp in 6/8: the i and the VII struck on the dotted quarters
pack.chords("Harp Psalter", "Harp", bars12(
    C("@i", 5, 1), C("@i", 5, 1), C("@VII", 5, 1), C("@i", 5, 1),
    C("@i", 5, 1), C("@IV", 5, 1), C("@VII", 5, 1), C("@i", 5, 1)), G)

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(70, "D", "Dorian", echo=0.5,
              about="Chant in D Dorian, the first mode, slow and straight, in a cathedral's echo.")

if __name__ == "__main__":
    pack.done()
