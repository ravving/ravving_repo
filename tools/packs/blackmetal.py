#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret black metal pack: five pattern presets for each of the drums, the bass, the lead
# and the chords (see ../patternkit.py). Written in scale degrees for a NATURAL MINOR key, made
# for E minor. The figures are the second wave's (Ultimate Guitar's tabs, see the README):
# Transilvanian Hunger's tremolo line over an open pedal, Dunkelheit's minor arpeggios moving a
# half step up (the Phrygian ♭II), Freezing Moon's and Emperor's minor triads, Bathory's epic
# i–VII–VI; the lines are original. The drums are the blast beat (the kick and the snare
# alternating in sixteenths, a cymbal on every kick), the hammer blast (all three together) and
# the skank beat (the kick on the beat, the snare on the off-beat).
#
# Tremolo picking is sixteenths on one note, the down-stroke louder than the up-stroke (@ the
# velocities); a symphonic part holds long notes, swelling.
#   python3 tools/packs/blackmetal.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/blackmetal/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "blackmetal")
sys.path.insert(0, HERE)
from patternkit import MINOR, Pack, N, C, R, cpower  # noqa: E402

pack = Pack("Black Metal", PACK, MINOR)


def trem(note, steps, down=112, up=86):
    """Tremolo picking: `steps` sixteenths on one note, down-strokes louder."""
    return " ".join(f"{note}@{down if k % 2 == 0 else up}" for k in range(steps))


# --- drums --------------------------------------------------------------------------------------
# the traditional blast: the kick and the snare alternating in sixteenths, the crash ride with
# every kick
pack.drums("Traditional Blast", "BLACK_PEARL", {
    "KICK":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "SNARE":  ".x.x.x.x.x.x.x.x | .x.x.x.x.x.x.x.x",
    "CYMBAL": "X.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
})
# the hammer blast: the kick, the snare and the cymbal struck together on every eighth
pack.drums("Hammer Blast", "BLACK_PEARL", {
    "KICK":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "SNARE":  "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "CYMBAL": "X.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
})
# the skank beat (Transilvanian Hunger's, punk's): the kick on the beat, the snare on its "and",
# the hats with both
pack.drums("Skank Beat", "BLACK_PEARL", {
    "KICK":  "x...x...x...x... | x...x...x...x...",
    "SNARE": "..x...x...x...x. | ..x...x...x...x.",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "CYMBAL": "X............... | ................",
})
# mid-tempo double kick (Immortal, Emperor's slower parts): the kicks in sixteenths, the snare
# on three, the crash on one
pack.drums("Frozen March", "BLACK_PEARL", {
    "KICK":   "xxxxxxxxxxxxxxxx | xxxxxxxxxxxxxxxx",
    "SNARE":  "........X....... | ........X.......",
    "CYMBAL": "X.......x....... | X.......x.......",
    "TOM":    "................ | ............xxxx",
})
# Bathory's Viking march: slow and epic, the kick on one and two-and, the snare on three, the
# floor toms answering
pack.drums("Viking March", "BLACK_PEARL", {
    "KICK":   "X.....x.x....... | X.....x.x.....x.",
    "SNARE":  "........X....... | ........X.......",
    "TOM":    "............x.x. | ............xxxx",
    "CYMBAL": "X...x...x...x... | x...x...x...x...",
})

# --- bass ---------------------------------------------------------------------------------------
# the roots in eighths under i VI VII i (Em C D Em), picked evenly, a little behind
pack.bass("Tremolo Roots", "Picked bass", " | ".join([
    " ".join(f"1@{100 if k % 2 == 0 else 88}" for k in range(16)),
    " ".join([" ".join(f"6-@{100 if k % 2 == 0 else 88}" for k in range(8)),
              " ".join(f"7-@{100 if k % 2 == 0 else 88}" for k in range(8))])]),
    mods={"FILTER/CUTOFF": -2400})
# the open-string pedal (Transilvanian Hunger's A, here the root): sixteenths swelling across
# the bar and falling back
pack.bass("Pedal Swell", "Picked bass", " | ".join([
    " ".join(f"1-@{70 + 3 * k}" for k in range(16)),
    " ".join(f"1-@{118 - 3 * k}" for k in range(16))]))
# the Phrygian crawl: i and ♭II in half notes, a slide into the ♭II
pack.bass("Phrygian Crawl", "Picked bass", " | ".join([
    " ".join([N("1!", 8), N("1~", 8)]), " ".join([N("b2!", 8), N("1", 8)]),
    " ".join([N("1!", 8), N("#4-@96", 4), N("5-", 4)]), " ".join([N("b2!", 12), N("1", 4)])]))
# the symphonic drone (Emperor's keyboards): the organ's 16-foot under i VI VII i, held a bar
# each, swelling
pack.bass("Symphonic Drone", "Organ · Bourdon 16", " ".join([
    N("1@84", 16), N("6-@92", 16), N("7-@100", 16), N("1!@110", 15), R(1)]),
    mods={"ENVELOPE/ATTACK": 3600, "ENVELOPE/RELEASE": 2400})
# Bathory's epic walk (One Rode to Asa Bay's i VII i VII … VI): eighths under the march
pack.bass("Viking Walk", "Picked bass", " | ".join([
    " ".join([N("1!", 6), N("1", 2), N("7-", 6), N("7-", 2)]),
    " ".join([N("1!", 6), N("1", 2), N("7-", 6), N("7-", 2)]),
    " ".join([N("6-!", 6), N("6-", 2), N("5-", 6), N("7-", 2)]),
    " ".join([N("1!", 12), N("7-", 2), N("6-", 2)])]))

# --- lead ---------------------------------------------------------------------------------------
# after Transilvanian Hunger: a line falling by steps from the fourth over the open root, each
# note tremolo-picked for a beat
pack.lead("Hunger Tremolo", "Guitar · Heavy lead", " | ".join([
    " ".join([trem("4", 4), trem("3", 4), trem("2", 4), trem("3", 4)]),
    " ".join([trem("3", 4), trem("2", 4), trem("3", 4), trem("2", 4)]),
    " ".join([trem("5-", 4), trem("6-", 4), trem("5-", 4), trem("7-", 4)]),
    " ".join([trem("1", 8), trem("b2", 4), trem("1", 4)])]),
    mods={"FILTER/CUTOFF": -1200})
# after Dunkelheit: an E minor arpeggio in eighths, then the same shape a half step up (F major,
# the ♭II), ringing
def arp8(*notes):
    return " ".join(N(n, 2) for n in notes)
pack.lead("Dunkelheit Arpeggio", "Guitar · Heavy lead", " | ".join([
    arp8("1@104", "5@84", "1+@88", "3+@90", "5@84", "1+@88", "3+@90", "1+@84"),
    arp8("1@104", "5@84", "1+@88", "3+@90", "5@84", "1+@88", "3+@90", "1+@84"),
    arp8("b2@104", "6@84", "b2+@88", "4+@90", "6@84", "b2+@88", "4+@90", "b2+@84"),
    arp8("1@104", "5@84", "1+@88", "3+@90", "5@84", "1+@88", "3+@90", "5+@96")]))
# a frozen melody (Freezing Moon's kind): slow notes, each tremolo-picked for half a bar
pack.lead("Frozen Melody", "Guitar · Heavy lead", " | ".join([
    " ".join([trem("5", 8), trem("4", 8)]), " ".join([trem("3", 8), trem("2", 8)]),
    " ".join([trem("3", 8), trem("2", 8)]), " ".join([trem("1", 8), trem("7-", 8)])]))
# Emperor's choir: long sung notes over the symphonic drone, swelling into each
pack.lead("Symphonic Choir", "Choir", " ".join([
    N("5@84", 16), N("6@92", 16), N("7@100", 12), N("6@92", 4), N("5!@108", 15), R(1)]),
    mods={"ENVELOPE/ATTACK": 3000, "ENVELOPE/RELEASE": 2400})
# the tritone riff: the root, the ♭2 and the ♭5, picked in sixteenths and accented
pack.lead("Tritone Riff", "Guitar · Heavy lead", " | ".join([
    " ".join(["1!@120", "1@84", "b2@104", "1@86", "#4!@120", "4@100", "3@96", "1@88"] * 2),
    " ".join(["1!@120", "1@84", "b2@104", "1@86", "5!@120", "#4@100", "4@96", "3@88",
              "b2!@120", "_", "_", "_", "1@100", "_", "_", "_"])]))

# --- chords -------------------------------------------------------------------------------------
# semitones from the key's root (E): minor triads with their octave, power chords, the ♭II major
BM = {"i": ("c", [0, 7, 12, 15]), "VI": ("c", [-4, 3, 8, 12]), "VII": ("c", [-2, 5, 10, 14]),
      "iv": ("c", [-7, 0, 5, 8]), "V": ("c", [-5, 2, 7, 11]), "bII": ("c", [1, 8, 13, 17]),
      "i5": cpower(0), "bII5": cpower(1), "i6": ("c", [0, 7, 12, 15, 19]),
      "iorg": ("c", [-12, 0, 3, 7, 12]), "ivorg": ("c", [-7, 0, 5, 8, 12]), "Vorg": ("c", [-5, 2, 7, 11, 14])}
# after Transilvanian Hunger and Freezing Moon: i VI VII i, each held a bar (the tremolo
# guitar's chords)
pack.chords("Hunger Chords", "Guitar · Heavy rhythm", " | ".join([
    C("@i", 15, 1), C("@VI", 15, 1), C("@VII", 15, 1), C("@i6", 15, 1)]), BM)
# Phrygian dread: i for two bars, the ♭II for one, back
pack.chords("Phrygian Dread", "Guitar · Heavy rhythm", " | ".join([
    C("@i5", 16), C("@i", 15, 1), C("@bII5", 16), C("@i5", 15, 1)]), BM)
# a symphonic pad (Emperor, Dimmu Borgir's keyboards): i iv V i on bowed strings, slow
pack.chords("Symphonic Strings", "Strings · Bowed", " | ".join([
    C("@i", 16), C("@iv", 16), C("@V", 16), C("@i6", 15, 1)]), BM,
    mods={"ENVELOPE/ATTACK": 3600, "ENVELOPE/RELEASE": 3000}, ties="all")
# after Dunkelheit: Em, then the same chord a half step up (F), each held two bars
pack.chords("Dunkelheit Shapes", "Guitar · Heavy rhythm", " | ".join([
    C("@i6", 16), C("@i", 15, 1), C("@bII", 16), C("@i6", 15, 1)]), BM)
# a cathedral organ (the intros, the interludes): i iv i V, in full
pack.chords("Cathedral Organ", "Organ · Plein jeu", " | ".join([
    C("@iorg", 16), C("@ivorg", 16), C("@iorg", 8) + " " + C("@Vorg", 8), C("@iorg", 15, 1)]), BM,
    mods={"ENVELOPE/RELEASE": 2400}, ties="all")

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(170, "E", "Natural Minor", echo=0.25, heavy=0.55,
              about="Black metal in E minor at blast-beat speed, washed in echo, squashed like a cassette demo.")

if __name__ == "__main__":
    pack.done()
