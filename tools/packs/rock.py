#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret rock pack: five pattern presets for each of the drums, the bass, the lead and the
# chords, laid out as a USB stick holds them (see ../patternkit.py and the jazz pack).
# Written in scale degrees for a MAJOR key, with rock's borrowed notes (♭3, ♭7, ♭6) as
# ALTER'd degrees and borrowed chords (♭VII, ♭VI) as chromatic voicings: the backbeat, the
# half-time shuffle (SWING about 66), the Bo Diddley beat, the gallop; power chords, boogie,
# blues-rock pentatonics, I–♭VII–IV and ♭VI–♭VII–I. Everything original and idiomatic.
#   python3 tools/packs/rock.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/rock/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "rock")
sys.path.insert(0, HERE)
from patternkit import MAJOR, Pack, N, C, R, power, cpower  # noqa: E402

pack = Pack("Rock", PACK, MAJOR)

# --- drums --------------------------------------------------------------------------------------
# the straight rock backbeat: kick on one and three (and its "and"), snare on two and four
pack.drums("Straight Backbeat", "POWER", {
    "KICK":   "X.......x.x..... | X.......x.x...x.",
    "SNARE":  "....X.......X... | ....X.......X...",
    "HAT":    "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "CYMBAL": "X............... | ................",
})
# arena rock: driving eighths on the ride, the kick doubling one and three
pack.drums("Arena Ride", "POWER", {
    "CYMBAL": "X.x.x.x.X.x.x.x. | x.x.x.x.x.x.x.x.",
    "KICK":   "X.x.....X.x..... | X.x.....X.x...x.",
    "SNARE":  "....X.......X... | ....X.......X...",
})
# the half-time shuffle: one backbeat on three, ghost notes around it; play with SWING ~66
pack.drums("Half-Time Shuffle", "ROOM", {
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "KICK":  "X......x..x..... | X......x.....x..",
    "SNARE": "...x...xX..x.... | ...x...xX..x..x.",
})
# the Bo Diddley beat: the 3-2 "shave and a haircut" on the toms, maracas in sixteenths
pack.drums("Bo Diddley Toms", "ROOM", {
    "TOM":  "X..x..x...x.x... | X..x..x...x.x...",
    "KICK": "x.......x....... | x.......x.......",
    "PERC": "xxxxxxxxxxxxxxxx | xxxxxxxxxxxxxxxx",
})
# the gallop: an eighth and two sixteenths on the kick every beat, crashes on the quarters
pack.drums("Gallop", "POWER", {
    "KICK":   "x.xxx.xxx.xxx.xx | x.xxx.xxx.xxx.xx",
    "SNARE":  "....X.......X... | ....X.......X.xx",
    "CYMBAL": "X...x...x...x... | x...x...x...x...",
})

# --- bass ---------------------------------------------------------------------------------------
# pumping eighths: I – ♭VII – IV – I
pack.bass("Root Eighths", "Picked bass", " | ".join(
    " ".join([N(root + "!", 2)] + [N(root, 2)] * 7) for root in ["1", "b7-", "4-", "1"]))
# the boogie: root, third, fifth, sixth, ♭7 and back, over I – IV – I – V
BOOGIE = {"I": "1 3 5 6 b7 6 5 3", "IV": "4- 6- 1 2 b3 2 1 6-", "V": "5- 7- 2 3 4 3 2 7-"}
pack.bass("Boogie Walk", "Finger bass", " | ".join(
    " ".join(N(n + ("!" if i == 0 else ""), 2) for i, n in enumerate(BOOGIE[c].split())) for c in ["I", "IV", "I", "V"]))
# a blues-rock unison riff: the minor pentatonic over the major key, the ♯4 passing tone
pack.bass("Blues-Rock Riff", "Finger bass",
          "1! _ . b3 _ . 4 _ _ _ . . 1 _ b3 _ | #4 4 _ . b3 _ 1 _ _ _ . . . . . .")
# the gallop under I – ♭VI – ♭VII – I
pack.bass("Gallop Bass", "Picked bass", " | ".join(
    " ".join([r + "! _ " + r + " " + r] + [r + " _ " + r + " " + r] * 3) for r in ["1", "b6-", "b7-", "1"]))
# root and fifth on one and three (the country-rock two-beat), I – IV – V – I, a walk home
pack.bass("Root–Fifth Two-Beat", "Acoustic bass", " | ".join([
    " ".join([N("1!", 6, 2), N("5-", 6, 2)]), " ".join([N("4-!", 6, 2), N("1", 6, 2)]),
    " ".join([N("5-!", 6, 2), N("2", 6, 2)]),
    " ".join([N("1!", 6, 2), N("5-", 2), N("6-", 2), N("7-", 2), R(2)])]))

# --- lead ---------------------------------------------------------------------------------------
# a blues-rock lick: the ♭3 bent (slid) into the 3, the ♭7 into the octave
pack.lead("Pentatonic Lick", "Guitar · Overdrive",
          "1+! _ b3+~ 3+ _ _ 1+ _ b7 _ 5 _ b7~ 1+ _ . | 5! _ _ _ b7 5 4 _ b3~ 3 _ 1 _ _ _ .")
# rock'n'roll sax: honks on the fifth, a ♭7 growl, down to the root
pack.lead("Honking Sax", "Tenor sax",
          "5! . 5 . 5 . b7 _ _ 5 _ . 3 _ 1 _ | 1+! _ _ _ b7 _ 5 _ b7 _ _ _ 5 _ . .")
# an arena hook ("whoa-oh"): long notes around the fifth and the sixth
pack.lead("Anthem Hook", "Guitar · Overdrive", " | ".join([
    " ".join([N("5!", 6), N("6", 2), N("5", 8)]), " ".join([N("3", 6), N("2", 2), N("1", 8)]),
    " ".join([N("5!", 6), N("6", 2), N("1+", 8)]), " ".join([N("7", 6), N("6", 2), N("5", 6), R(2)])]))
# open-chord picking in eighths: Iadd9 – IV – vi – Vsus
PICKING = ["1 5 1+ 2+ 3+ 2+ 1+ 5", "4- 1 4 5 6 5 4 1", "6- 3 6 7 1+ 7 6 3", "5- 2 5 1+ 7 5 2 5-"]
pack.lead("Clean Arpeggio", "Nylon guitar", " | ".join(
    " ".join(N(n + ("!" if i == 0 else ""), 2) for i, n in enumerate(bar.split())) for bar in PICKING))
# boogie piano: a tremolo between the third and the fifth, then a run down with a ♭3–3 crush
pack.lead("Boogie Piano", "Grand piano", " | ".join([
    " ".join(("5+!" if i % 4 == 0 else "5+") if i % 2 == 0 else "3+" for i in range(16)),
    "6+! 5+ 3+ 2+ 1+ 6 5 3 2 1 b3 3 5 _ 1+ _"]))

# --- chords -------------------------------------------------------------------------------------
# power chords (root, fifth, octave) chugging eighths: I – ♭VII – IV – I, a push at the end
POWER = {"I": power(0), "bVII": cpower(10), "IV": power(3)}
pack.chords("Power I–♭VII–IV", "Guitar · Distortion", " | ".join([
    " ".join([C("@I", 1, 1)] * 8), " ".join([C("@bVII", 1, 1)] * 8), " ".join([C("@IV", 1, 1)] * 8),
    " ".join([C("@I", 1, 1)] * 4 + [C("@bVII", 3, 1), C("@IV", 3, 1)])]), POWER)
# an R&B-rock organ: held chords with a stab before each change (I – IV/I – I, IV – I – V)
ORGAN = {"I": ("x", [7, 9, 11, 14]), "IV": ("x", [7, 10, 12, 14]), "V": ("x", [6, 8, 11, 13])}
pack.chords("Organ Pushes", "Jazz organ", " | ".join([
    " ".join([C("@I", 6, 1), C("@IV", 2, 1), C("@I", 5, 1)]),
    " ".join([C("@IV", 6, 1), C("@I", 2, 1), C("@V", 5, 1)])]), ORGAN)
# the Aeolian rock cadence ♭VI – ♭VII – I, parallel triads (chromatic: outside the major key)
AEOLIAN = {"bVI": ("c", [8, 12, 15]), "bVII": ("c", [10, 14, 17]), "I": ("c", [12, 16, 19])}
pack.chords("♭VI–♭VII–I", "Guitar · Overdrive", " ".join([C("@bVI", 8), C("@bVII", 8), C("@I", 15, 1)]), AEOLIAN)
# rock piano: I – IV – V – IV in a "1 2 3, 1 2 3, 1 2" push, triads close to each other
PIANO = {"I": ("x", [7, 9, 11]), "IV": ("x", [7, 10, 12]), "V": ("x", [6, 8, 11])}
pack.chords("Piano Pump", "Grand piano", " | ".join(
    " ".join([C("@" + c, 1, 1), C("@" + c, 1, 1), C("@" + c, 3, 1)] * 2) for c in ["I", "IV", "V", "IV"]), PIANO)
# a clean electric strum (down, down-up, …) over I – V – IV – V, guitar-shaped voicings
STRUM = {"I": ("x", [0, 2, 4, 7]), "V": ("x", [-3, -1, 1, 4]), "IV": ("x", [-4, -2, 0, 3])}
pack.chords("Clean Strum", "Guitar · Clean", " | ".join(
    " ".join([C("@" + c, 2, 1), C("@" + c, 1, 2), C("@" + c, 2, 1), C("@" + c, 1, 1), C("@" + c, 3, 1), R(1)])
    for c in ["I", "V", "IV", "V"]), STRUM)

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(122, "E", "Major", echo=0.05, heavy=0.35,
              about="Guitar rock in E major (the guitar's own key), straight eighths, compressed like a live room.")

if __name__ == "__main__":
    pack.done()
