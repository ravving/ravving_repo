#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret hip-hop pack: five pattern presets for each of the drums, the bass, the lead and
# the chords, laid out as a USB stick holds them (see ../patternkit.py and the jazz pack).
# Written in scale degrees for a NATURAL MINOR key: boom bap, golden-era swing (SWING 58–62),
# lo-fi, old-school 808 and jazz rap; everything original and idiomatic.
#   python3 tools/packs/hiphop.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/hiphop/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "hiphop")
sys.path.insert(0, HERE)
from patternkit import MINOR, Pack, N, C, R  # noqa: E402

pack = Pack("Hip-Hop", PACK, MINOR)

# --- drums --------------------------------------------------------------------------------------
# boom bap: the kick on one and pushing the "and"s, the snare cracking on two and four, eighth
# hats, a ghost snare and an open hat turning the second bar
pack.drums("Boom Bap", "SP1200", {
    "KICK":  "X......x..x..... | X.........x..x..",
    "SNARE": "....X.......X... | ....X.......X..x",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x...",
    "OPEN":  "................ | ..............x.",
})
# golden-era: sixteenth hats to swing (SWING 58–62), the kick skipping on the "a" of one, rim
# clicks between the snares
pack.drums("Golden Era Swing", "LINN", {
    "KICK":  "X..x......X..... | X..x....x.x.....",
    "SNARE": "....X.......X... | ....X.......X...",
    "HAT":   "xxxxxxxxxxxxxxxx | xxxxxxxxxxxxxx..",
    "OPEN":  "................ | ..............x.",
    "PERC":  "..x.......x..... | ......x....x....",
})
# lo-fi: lazy and soft, the hats only on the off-beats, the kick late in the bar, rim clicks
pack.drums("Lo-Fi Lazy", "SP1200", {
    "KICK":  "x.........x..... | x......x..x.....",
    "SNARE": "....x.......x... | ....x.......x...",
    "HAT":   "..x...x...x...x. | ..x...x...x.x.x.",
    "PERC":  "......x.......x. | ......x.......x.",
})
# old-school 808: the electro-rap kick, claps on two and four, the cowbell on top
pack.drums("Old School 808", "TR808", {
    "KICK": "X.....x...X.x... | X.....x...X...x.",
    "CLAP": "....X.......X... | ....X.......X...",
    "HAT":  "x.x.x.x.x.x.x.x. | x.x.x.x.x.xxx.x.",
    "PERC": "..x.....x....x.. | ..x.....x....x..",
})
# jazz rap: a ride cymbal's "ding, ding-a" and the hi-hat foot over a boom-bap kick and snare
pack.drums("Jazz Rap", "JAZZ", {
    "CYMBAL": "x...x.x.x...x.x. | x...x.x.x...x.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "KICK":   "X.......x.x..... | X.....x...x.....",
    "SNARE":  "....X.......X... | ....X.......X...",
})

# --- bass ---------------------------------------------------------------------------------------
# boom bap: the root with the kick (one, the "a" of two, the "and" of three), climbing i to
# iv, then VI walking back down through v and VII
pack.bass("Boom Bap Root", "Finger bass",
          "1! _ _ _ _ _ . 1 _ . 3 _ _ . 4 _ | 6-! _ _ _ _ _ _ _ _ _ 5- _ _ 7- _ _")
# jazz rap: an upright walking i – iv in quarters with eighth-note pickups
pack.bass("Jazz Rap Walk", "Upright", " | ".join([
    " ".join([N("1!", 3, 1), N("5-", 3, 1), N("7-", 3, 1), N("1", 2), N("2", 2)]),
    " ".join([N("3", 3, 1), N("4", 3, 1), N("5", 3, 1), N("5-", 2), N("7-", 2)])]))
# G-funk: a synth bass gliding up the octave and down through the minor pentatonic
pack.bass("G-Funk Glide", "Nekobi",
          "1! _ _ 1+~ 7 _ 5 _ . . 4 _ 3~ 1 _ . | 6-! _ _ _ . 6- 7- _ 1 _ . . 5-~ 7- _ .")
# lo-fi: long fretless notes under i – VI – iv – v, a pickup into each change
pack.bass("Lo-Fi Sub", "Fretless", " ".join([
    N("1!", 14), N("7-", 2), N("6-", 14), N("5-", 2), N("4-", 14), N("6-", 2), N("5-", 12), N("7-", 4)]))
# electro-funk: sixteenth octave pops answering each other, a slide in the turnaround
pack.bass("Electro Funk", "Nekobi",
          "1! . 1+ . . 1 . 1+ 7 . 5 . 3 . 4 . | 1! . 1+ . . 1 . 1+ 3+ . 1+ . 7 . 5~ 4")

# --- lead ---------------------------------------------------------------------------------------
# a Rhodes riff in the minor pentatonic, answered by a falling line
pack.lead("Rhodes Riff", "Rhodes", " | ".join([
    " ".join([N("5!", 2), R(1), N("7", 2), R(1), N("1+", 2), N("7", 2), N("5", 2), N("4", 2), N("3", 2)]),
    " ".join([N("1!", 6), R(2), N("3", 2), N("4", 2), N("3", 2), N("1", 2)])]))
# muted horn stabs like a chopped soul sample: two short hits and a fall
pack.lead("Horn Stabs", "Muted trumpet",
          "5! . . 5 . . . 7 _ 5 _ . . . . . | 4! . . 4 . . . 3 _ 1 _ _ _ . . .")
# vibes in eighths, up the i and the iv arpeggios
pack.lead("Vibes Loop", "Vibes", " | ".join([
    " ".join(N(n, 2) for n in ["1!", "3", "5", "1+", "3+", "1+", "5", "3"]),
    " ".join(N(n, 2) for n in ["4!", "6", "1+", "4+", "6+", "4+", "1+", "6"])]))
# the G-funk whistle: a high, gliding portamento line
pack.lead("G-Funk Whistle", "Calf Monosynth",
          "5+!~ _ _ _ _ _ 4+ _ 3+~ _ 1+ _ _ _ _ _ | 3+ _ _ _ 4+~ _ _ _ 5+ _ _ _ _ _ . .")
# a flute loop: falling from the octave, turning around the third
pack.lead("Flute Loop", "Flute",
          "1+! _ _ 7 _ 5 _ 7 _ _ _ . 4 _ 5 _ | 3! _ _ _ _ _ 1 _ 3 _ 4 _ 3 _ 1 _")

# --- chords -------------------------------------------------------------------------------------
# boom-bap keys: a chopped i, then iv with III and VII pushing back (the CHORD SET's sevenths)
pack.chords("Boom Bap Keys", "Rhodes",
            "1 = = . . . 1 = . . . . . . . . | 4 = = . . . 4 = . . 3 = . 7 = .")
# a soul loop: i7 – iv7 – VII – III, half a bar each
pack.chords("Soul Loop", "Strings · Ensemble", " ".join([C("1", 8), C("4", 8), C("7", 8), C("3", 8)]))
# lo-fi ninths (chromatic, from the chord base), each landing a sixteenth late:
# im9 – ivm9 – VImaj9 – v7
LOFI = {"i9": ("c", [0, 3, 7, 10, 14]), "iv9": ("c", [-7, -4, 0, 3, 7]),
        "VI9": ("c", [-4, 0, 3, 7, 10]), "v7": ("c", [-5, -2, 2, 5])}
pack.chords("Lo-Fi Ninths", "Upright piano", " ".join(
    " ".join([R(1), C("@" + c, 13), R(2)]) for c in ["i9", "iv9", "VI9", "v7"]), LOFI)
# dark strings: i held two bars, VI, then v (triads in scale degrees, any CHORD SET)
DARK = {"i": ("x", [0, 2, 4, 7]), "VI": ("x", [-2, 0, 2, 5]), "v": ("x", [-3, -1, 1, 4])}
pack.chords("Dark Strings", "Strings · Bowed", " ".join([C("@i", 32), C("@VI", 16), C("@v", 15, 1)]), DARK)
# a soul-jazz organ vamp: i7 – IV7 (the Dorian IV, chromatic), stabbed
ORGAN = {"i": ("c", [0, 3, 7, 10]), "IV": ("c", [5, 9, 12, 15])}
pack.chords("Organ Vamp", "Jazz organ", " | ".join([
    " ".join([C("@i", 2, 4), C("@i", 2, 2), C("@IV", 3, 3)]),
    " ".join([C("@i", 2, 4), C("@i", 2, 2), C("@IV", 2, 1), C("@i", 2, 1)])]), ORGAN)

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(90, "C", "Natural Minor", swing=56, echo=0.15, heavy=0.35,
              about="Boom bap at 90 in C minor with a light MPC swing; HEAVY squashes the drums as a sampler's compressor would.")

if __name__ == "__main__":
    pack.done()
