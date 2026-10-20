#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret "Vuelo" pack: Flight Facilities' nu-disco (Crave You, Arty Boy, Need You, Two
# Bodies, Stranded), five pattern presets each for the drums, the bass, the lead and the chords,
# laid out as a USB stick holds them (../patternkit.py). Written in scale degrees for a
# NATURAL MINOR key: A minor is Arty Boy's, C# minor Crave You's (the two templates). The
# bands' own progressions (their chord sheets, 2026-10-11), the lines original and idiomatic:
# four-on-the-floor 909s with claps and open hats on the off-beats, octave disco basses that
# ride the kick, a funk guitar riff with muted 16ths, Rhodes hooks, string swells. Every
# per-note setting the charts keep is used: @velocity (muted strokes, ghost notes), <n / >n
# nudges (a lazy clap, a bass behind the beat), holds (_), slides (~), accents (!), chromatic
# voicings (the dim7 and the major V), and the sounds' MODS.
#   python3 tools/packs/vuelo.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/vuelo/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "vuelo")
sys.path.insert(0, HERE)
from patternkit import MINOR, Pack, N, C, R  # noqa: E402

pack = Pack("Vuelo", PACK, MINOR)


def bar(text):
    """One bar's tokens, checked to be sixteen (a miscount is the usual slip)."""
    tokens = text.split()
    if len(tokens) != 16:
        raise ValueError(f"{len(tokens)} tokens in bar: {text!r}")
    return text

# --- drums --------------------------------------------------------------------------------------
# four on the floor: the 909 kick on every beat, the clap on two and four (a hair late, as a
# sampled clap sits), open hats on every off-beat, soft closed 16ths under them
pack.drums("Four On The Floor", "TR909", {
    "KICK":  "X...X...X...X... | X...X...X...X...",
    "CLAP":  "....X.......X... | ....X.......X...",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "OPEN":  "..x...x...x...x. | ..x...x...x...x.",
}, mods={"TONE/CUTOFF": -1200})
# Crave You's groove: the 808, the kick skipping the "a" of two, rim clicks (PERC) in the
# syncopation, the clap with the snare, a cowbell-less, laid-back house pulse
pack.drums("Crave Groove", "TR808", {
    "KICK":  "X.....x.X.....x. | X.....x.X....x..",
    "SNARE": "....X.......X... | ....X.......X...",
    "CLAP":  "....x.......x... | ....x.......x..x",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.xxx.",
    "PERC":  "..x.....x..x.... | ..x.....x..x..x.",
})
# the disco shuffle: the Linn with 16th hats accented on the off-beats, the snare on two and
# four, the kick on one and the "and" of three, a tambourine (PERC) in 8ths
pack.drums("Disco Shuffle", "LINN", {
    "KICK":  "X.........x..... | X.........x...x.",
    "SNARE": "....X.......X... | ....X.......X...",
    "HAT":   "xXxXxXxXxXxXxXxX | xXxXxXxXxXxXxXxX",
    "OPEN":  "..............x. | ..............x.",
    "PERC":  "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
})
# Arty Boy's funk: the kick on one and the "and" of two, pushing into three, the snare with
# a ghost before four, 16th hats with the open hat on the "and" of four
pack.drums("Arty Funk", "TR909", {
    "KICK":  "X.....x.X.....x. | X.....x.X..x....",
    "SNARE": "....X......xX... | ....X......xX...",
    "HAT":   "xxxxxxxxxxxxxxxx | xxxxxxxxxxxxxx..",
    "OPEN":  "..............x. | ..............x.",
    "CLAP":  "............X... | ............X...",
}, mods={"SHAPE/LENGTH": -1500})
# the build: four on the floor with the snare rolling up the second bar into a crash
pack.drums("Build And Crash", "TR909", {
    "KICK":   "X...X...X...X... | X...X...X...X...",
    "CLAP":   "....X.......X... | ....X.......X...",
    "SNARE":  "................ | x.x.x.x.xxxxxxxx",
    "HAT":    "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "OPEN":   "..x...x...x...x. | ..x...x...x.....",
    "CYMBAL": "X............... | ................",
})

# --- bass ---------------------------------------------------------------------------------------
# Crave You's walk: i – ♯iv° – iv – VII, one bar each, an octave pop on the "and"s and a
# chromatic pass (ALTER) into the dim chord, behind the beat a little as a played bass sits
pack.bass("Crave Walk", "Finger bass", " | ".join([
    bar("1! _ . 1+ . 1 . 1+ . 3 _ . 4 . #4 ."),
    bar("#4! _ . #4+ . #4 . 7- _ . 6- . 7- . #4 ."),
    bar("4! _ . 4+ . 4 . 4+ . 6 _ . 1+ . 7 ."),
    bar("7-! _ . 7 . 7- . 7 . 2 _ . 7- . 5- 6-")]))
# Arty Boy's pulse: VI for a bar and a half, i for two beats, then v and III: root 8ths on the
# off-beats (the disco bass riding between the kicks), the octave up on the last of each
pack.bass("Arty Pulse", "Synth bass", " | ".join([
    bar(". 6- . . 6- . . 6- . 6 . . 6- . . 6-"),
    bar(". 6- . . 6- . . 6 . 1 . . 1 . . 1+"),
    bar(". 5- . . 5- . . 5- . 5 . . 5- . . 5-"),
    bar(". 5- . . 5- . . 5 . 3- . . 3- . . 3")]))
# the octave disco: root–octave 16ths with ghosted in-betweens (@40), the fifth before each
# change; i – VI – III – VII (Two Bodies' loop in the relative minor)
def disco(root, up):
    return bar(" ".join([f"{root}!", up, f"{root}@40", up] * 4))
pack.bass("Octave Disco", "Picked bass", " | ".join([disco("1", "1+"), disco("6-", "6"), disco("3", "3+"), disco("7-", "7")]))
# the sub: long roots under Need You's i – VII – VI – VII, each slid into (~) from the step
# before, a 16th late (>10) so the kick speaks first
pack.bass("Sub Pulse", "Sine sub", " | ".join([
    bar(N("1!>10", 14) + " " + N("7-~", 2)),
    bar(N("7-!>10", 14) + " " + N("6-~", 2)),
    bar(N("6-!>10", 14) + " " + N("7-~", 2)),
    bar(N("7-!>10", 12) + " " + N("5-", 2) + " " + N("7-~", 2))]))
# the funk riff: slap pops on the octave, the ♭7 and the 5th answering, 16th ghosts (@36)
pack.bass("Slap Riff", "Slap bass", " | ".join([
    bar("1! . 1+! 1@36 . 1 . 7-@36 5- . 7- . 1+! . 1@36 ."),
    bar("1! . 1+! 1@36 . 1 . 7-@36 5- 6-@36 7- . 1+! . 3~ 4")]))

# --- lead ---------------------------------------------------------------------------------------
# the Arty Boy guitar: a clean funk riff in 16ths, muted strokes (@42) between the notes,
# the 5th and the ♭7 around the root, a slide up to the octave on the turn
pack.lead("Guitar Riff", "Guitar · Clean", " | ".join([
    bar("5! 5@42 7 5@42 1+ . 5@42 7 5! . 5@42 4 3 . 1@42 ."),
    bar("5! 5@42 7 5@42 1+ . 5@42 7 1+! 7@42 5 . 4~ 5 _ .")]))
# a Rhodes hook over two bars: the minor pentatonic, the octave answered by the 7th and 5th
pack.lead("Rhodes Hook", "Rhodes", " | ".join([
    bar(" ".join([N("1+!", 3), N("7", 1), N("5", 2), R(2), N("3", 2), N("4", 2), N("5", 4)])),
    bar(" ".join([N("1+!", 2), N("3+", 2), N("1+", 2), N("7", 2), N("5", 4), R(4)]))]))
# disco strings: a rising 8th-note line into a held top, the swell written as velocities
pack.lead("String Rise", "Violin", " | ".join([
    bar(" ".join([N("1@70", 2), N("3@78", 2), N("5@86", 2), N("1+@94", 2), N("3+@102", 2), N("5+@110", 2), N("7+!", 4)])),
    bar(" ".join([N("7+", 2), N("5+", 2), N("3+", 4), N("1+", 8)]))]))
# an 80s synth lead: slides between the 5th, the 4th and the root, a hold on the 7th
pack.lead("Synth Slide", "Calf Monosynth", " | ".join([
    bar("5! _ _ _ 4~ _ _ _ 3~ _ 1 _ _ _ . ."),
    bar("7-! _ _ _ 1~ _ _ _ 3 _ _ _ 5~ _ _ _")]))
# a lazy sax phrase (Crave You's late-night mood): long notes landing a touch late (>8)
pack.lead("Sax Line", "Alto sax", " | ".join([
    bar(" ".join([R(2), N("5!>8", 6), N("4", 2), N("3>8", 6)])),
    bar(" ".join([N("1>8", 4), R(2), N("7-", 2), N("1>8", 8)]))]))

# --- chords -------------------------------------------------------------------------------------
# Arty Boy's verse, the band's own timing: the first chord a bar and a half, the second the
# last two beats (| F F F F | F F Am Am |), VI → i then v → III, strummed in 8th stabs
ARTY = {"VI": ("x", [5, 7, 9]), "i": ("x", [0, 2, 4]), "v": ("x", [4, 6, 8]), "III": ("x", [2, 4, 6]),
        "iv": ("x", [3, 5, 7]), "V": ("c", [7, 11, 14])}  # the pre-chorus's E major: chromatic
def strums(name, count):
    """`count` 8th-note stabs of a chord (two steps each)."""
    return " ".join(C("@" + name, 1, 1) for _ in range(count))
pack.chords("Arty Verse", "Guitar · Chorus", " | ".join([
    bar(strums("VI", 8)), bar(strums("VI", 4) + " " + strums("i", 4)),
    bar(strums("v", 8)), bar(strums("v", 4) + " " + strums("III", 4))]), ARTY)
# the pre-chorus: VI → i, then iv → V (the major V, chromatic), held as a Rhodes pad with a
# stab on the "and" of two
pack.chords("Arty Pre", "Rhodes", " | ".join([
    bar(C("@VI", 5, 1) + " " + C("@VI", 1, 1) + " " + C("@VI", 7, 1)),
    bar(C("@VI", 7, 1) + " " + C("@i", 8)),
    bar(C("@iv", 5, 1) + " " + C("@iv", 1, 1) + " " + C("@iv", 7, 1)),
    bar(C("@iv", 7, 1) + " " + C("@V", 8))]), ARTY)
# Crave You's loop: i7 – ♯iv°7 – iv7 – VII7sus4 (chromatic where the key has no such chord),
# one bar each, struck once and let ring, a staccato down-stroke on the "and" of three
CRAVE = {"i7": ("x", [0, 2, 4, 6]), "dim7": ("c", [6, 9, 12, 15]), "iv7": ("x", [3, 5, 7, 9]), "VII7sus4": ("c", [10, 15, 17, 20])}
pack.chords("Crave Loop", "Jazz guitar", " | ".join(
    bar(C("@" + name, 9, 1) + " " + C("@" + name, 1, 1) + " " + C("@" + name, 3, 1)) for name in ["i7", "dim7", "iv7", "VII7sus4"]), CRAVE)
# the chorus: VI – v in a steady down-up rhythm (house piano stabs on every 8th, the
# "and"s softer), building as the hook lands
pack.chords("Chorus Stabs", "Organ · House", " | ".join([bar(strums("VI", 8)), bar(strums("v", 8))]), ARTY)
# string pads: Stranded's VI – VII – iv – VII – i, long bows, the last chord held a bar
STRANDED = {"VI": ("x", [5, 7, 9, 11]), "VII": ("x", [6, 8, 10]), "iv": ("x", [3, 5, 7, 9]), "i": ("x", [0, 2, 4])}
pack.chords("String Pads", "Strings · Ensemble", " | ".join([
    bar(C("@VI", 16)), bar(C("@VII", 8) + " " + C("@iv", 8)), bar(C("@VII", 16)), bar(C("@i", 15, 1))]), STRANDED)

# the templates: Arty Boy's key and Crave You's, both at the pack's 120 (the projects dialog's
# TEMPLATES)
pack.template(120, "A", "Natural Minor", phaser=0.1, echo=0.15, heavy=0.3,
              about="Nu-disco at 120 in A minor (Arty Boy): four on the floor, a touch of phaser on the guitar, HEAVY to glue the drums.")
pack.template(120, "C#", "Natural Minor", name="Vuelo · Crave", swing=52, echo=0.25, heavy=0.25,
              about="Crave You's late-night groove at 120 in C# minor, a hair of swing, the echo throw on the vocals' gaps.")

if __name__ == "__main__":
    pack.done()
