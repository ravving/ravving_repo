#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret punk pack: five pattern presets for each of the drums, the bass, the lead and the
# chords, laid out as a USB stick holds them (see ../patternkit.py and the jazz pack).
# Written in scale degrees for a MAJOR key, with the borrowed ♭3, ♭7 and ♭VI/♭VII (ALTER'd
# degrees and chromatic power chords): the skate (polka) beat, the D-beat, Ramones eighths,
# the pop-punk half-time breakdown, ska-punk off-beats; power chords I–IV–V and I–V–vi–IV.
#   python3 tools/packs/punk.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/punk/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "punk")
sys.path.insert(0, HERE)
from patternkit import MAJOR, Pack, N, C, R, power, cpower  # noqa: E402

pack = Pack("Punk", PACK, MAJOR)

# --- drums --------------------------------------------------------------------------------------
# the skate beat (a fast polka): kick on the beats, snare on every "and", the crash riding
# the quarters, a snare fill into the top
pack.drums("Skate Beat", "POWER", {
    "KICK":   "X...x...x...x... | x...x...x...x...",
    "SNARE":  "..x...x...x...x. | ..x...x...x.xxxx",
    "CYMBAL": "X...x...x...x... | x...x...x...x...",
})
# the D-beat (Discharge): kick on one, the "and" of one, the "and" of two, three, the "and"s
# after it; snare on two and four; the crash in eighths, no hi-hat
pack.drums("D-Beat", "ROOM", {
    "KICK":   "X.x...x.x.x...x. | X.x...x.x.x...x.",
    "SNARE":  "....X.......X... | ....X.......X...",
    "CYMBAL": "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
})
# Ramones eighths: closed hats driving, kick on one and three with a push, snare on two and four
pack.drums("Straight Eighths", "STANDARD", {
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "KICK":  "X.......X.x..... | X.x.....X.x.....",
    "SNARE": "....X.......X... | ....X.......X...",
})
# the pop-punk breakdown: half time, the crash on the quarters, a tom fill
pack.drums("Half-Time Breakdown", "POWER", {
    "KICK":   "X.....x...x..... | X.....x.........",
    "SNARE":  "........X....... | ........X.......",
    "CYMBAL": "X...x...x...x... | x...x...x.......",
    "TOM":    "................ | ..........x.xxxx",
})
# ska-punk: hats on the off-beats (the upstroke), snare on two and four
pack.drums("Ska Offbeat", "STANDARD", {
    "KICK":  "X.......X....... | X.......X.....x.",
    "SNARE": "....X.......X... | ....X.......X...",
    "HAT":   "..x...x...x...x. | ..x...x...x...x.",
})

# --- bass ---------------------------------------------------------------------------------------
# down-picked staccato eighths on I – V – vi – IV
pack.bass("Pop-Punk Eighths", "Picked bass", " | ".join(
    " ".join([N(r + "!", 1, 1)] + [N(r, 1, 1)] * 7) for r in ["1", "5-", "6-", "4-"]))
# skate punk: eighths with a walk-up into each change (I – IV – V – I)
WALK = ["1 1 1 1 1 1 2 3", "4 4 4 4 4 4 3 2", "5- 5- 5- 5- 5- 5- 6- 7-", "1 1 1 1 5- 5- 6- 7-"]
pack.bass("Skate Walk-Up", "Picked bass", " | ".join(
    " ".join(N(n + ("!" if i == 0 else ""), 2) for i, n in enumerate(bar.split())) for bar in WALK))
# a D-beat riff: the ♭3 and the ♯4 crust-style over the major key
RIFF = ["1 1 b3 1 4 4 b3 1", "1 1 b3 1 #4 4 b3 b7-"]
pack.bass("D-Beat Riff", "Picked bass", " | ".join(
    " ".join(N(n + ("!" if i % 4 == 0 else ""), 2) for i, n in enumerate(bar.split())) for bar in RIFF))
# ska: a walking line in quarters over I – vi – IV – V
SKA = ["1 3 5 6", "6- 1 3 1", "4- 6- 1 #1", "5- 7- 2 7-"]
pack.bass("Ska Walk", "Finger bass", " | ".join(
    " ".join(N(n + ("!" if i == 0 else ""), 3, 1) for i, n in enumerate(bar.split())) for bar in SKA))
# new-wave punk: octave eighths on I – IV – I – V
pack.bass("New Wave Octaves", "Synth bass", " | ".join(
    " ".join([N(r + "-!", 2), N(r, 2)] + [N(r + "-", 2), N(r, 2)] * 3) for r in ["1", "4", "1", "5"]))

# --- lead ---------------------------------------------------------------------------------------
# a pop-punk hook: repeated notes, a step down and back, up to the fifth
pack.lead("Pop-Punk Hook", "Guitar · Overdrive", " | ".join([
    " ".join([N("3!", 2), N("3", 2), N("3", 2), N("2", 2), N("1", 4), N("2", 2), N("3", 2)]),
    " ".join([N("5!", 4), N("3", 4), N("2", 4), N("1", 4)])]))
# a ska horn line: off-beat pushes, a held fall
pack.lead("Ska Horns", "Trumpet",
          "5! . 5 . 6 . 5 . 3 _ _ . 1 _ 2 _ | 3! . 3 . 4 . 3 . 2 _ _ _ . . . .")
# a street-punk single-note riff: the ♭3, the ♯4 passing up to 5, the ♭7 answer
pack.lead("Street Riff", "Guitar · Overdrive",
          "1! _ 1 _ b3 _ 1 _ 4 _ #4 _ 5 _ . . | 5! _ 5 _ b7 _ 5 _ 4 _ b3 _ 1 _ . .")
# a gang chant ("whoa-oh"), long and simple
pack.lead("Gang Chant", "Calf Monosynth", " | ".join([
    " ".join([N("5!", 6), N("5", 2), N("6", 4), N("5", 4)]), " ".join([N("3!", 8), N("2", 4), N("1", 4)])]))
# pounding piano eighths high up, the octave against the fifth, then the sixth
pack.lead("Piano Pounding", "Grand piano",
          "1+! _ 5 _ 1+ _ 5 _ 1+ _ 5 _ 1+ _ 5 _ | 1+! _ 6 _ 1+ _ 6 _ 2+ _ 7 _ 2+ _ 7 _")

# --- chords: power chords are root, fifth and octave ----------------------------------------------
POWER = {"I": power(0), "IV": power(3), "V": power(4), "vi": power(5), "bVI": cpower(8), "bVII": cpower(10)}
# I – I – IV – V chugged in eighths
pack.chords("Power I–IV–V", "Guitar · Distortion", " | ".join(
    " ".join([C("@" + c, 1, 1)] * 8) for c in ["I", "I", "IV", "V"]), POWER)
# I – V – vi – IV held, each change pushed an eighth early
pack.chords("Pop-Punk Pushes", "Guitar · Distortion", " ".join(
    [C("@I", 14), C("@V", 16), C("@vi", 16), C("@IV", 16), C("@I", 2)]), POWER)
# ska upstrokes: short off-beat chops, I – vi – IV – V
SKA_CHORDS = {"I": ("x", [7, 9, 11]), "vi": ("x", [5, 7, 9]), "IV": ("x", [5, 7, 10]), "V": ("x", [4, 6, 8])}
pack.chords("Ska Upstrokes", "Guitar · Clean", " | ".join(
    " ".join([R(2), C("@" + c, 1, 1)] * 4) for c in ["I", "vi", "IV", "V"]), SKA_CHORDS)
# crust: I chugged, then ♭VI and ♭VII (chromatic power chords)
pack.chords("Crust I–♭VI–♭VII", "Guitar · Overdrive", " | ".join([
    " ".join([C("@I", 1, 1)] * 8), " ".join([C("@bVI", 1, 1)] * 4 + [C("@bVII", 1, 1)] * 4)]), POWER)
# pub-punk piano: straight eighth triads, I – IV – I – V
PIANO = {"I": ("x", [7, 9, 11]), "IV": ("x", [7, 10, 12]), "V": ("x", [6, 8, 11])}
pack.chords("Piano Bash", "Grand piano", " | ".join(
    " ".join([C("@" + c, 1, 1)] * 8) for c in ["I", "IV", "I", "V"]), PIANO)

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(170, "A", "Major", heavy=0.5,
              about="Fast punk at 170 in A major: no echo, everything slammed.")

if __name__ == "__main__":
    pack.done()
