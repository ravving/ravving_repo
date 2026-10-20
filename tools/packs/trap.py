#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret trap pack: five pattern presets for each of the drums, the bass, the lead and the
# chords, laid out as a USB stick holds them (see ../patternkit.py and the jazz pack).
# Written in scale degrees for a NATURAL MINOR key, with the harmonic minor's leading tone and
# the Phrygian ♭2 as ALTER'd degrees: the half-time clap on beat three, hi-hat rolls, the
# 3-3-2 "triplet" hats a 16-step grid can hold, drill, phonk's cowbell; gliding 808 lines.
# The grid is in sixteenths at the track's tempo (130–150, felt in half time).
#   python3 tools/packs/trap.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/trap/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "trap")
sys.path.insert(0, HERE)
from patternkit import MINOR, Pack, N, C, R  # noqa: E402

pack = Pack("Trap", PACK, MINOR)

# --- drums --------------------------------------------------------------------------------------
# classic trap: one clap a bar on beat three (half time), eighth hats breaking into sixteenth
# rolls, an open hat, the kick placed around the 808
pack.drums("Classic Trap", "TR808", {
    "KICK": "X.........x..... | X......x..x...x.",
    "CLAP": "........X....... | ........X.......",
    "HAT":  "x.x.x.x.xxx.x... | x.x.xxxxx.x.x.xx",
    "OPEN": "..............x. | ................",
})
# triplet flow: the hats grouped in threes against the beat, a sixteenth burst at the end
pack.drums("Triplet Flow", "TR808", {
    "KICK": "X.....x......... | X.........x..x..",
    "CLAP": "........X....... | ........X.......",
    "HAT":  "x..x..x..x..x.x. | x..x..x..x..xxxx",
})
# drill: the snare on three and a late one in the second bar, the hats skipping 3-3-2,
# kicks sliding between them
pack.drums("Drill", "TR808", {
    "KICK":  "X.........x..x.. | X......x...x....",
    "SNARE": "........X....... | ...x....X.....x.",
    "HAT":   "x..x..x.x..x..x. | x..x..x.x..x..xx",
})
# phonk: the cowbell riff on top, claps on two and four, the Memphis kick
pack.drums("Phonk Cowbell", "TR808", {
    "KICK": "X.....x...x..x.. | X.....x...x.....",
    "CLAP": "....X.......X... | ....X.......X...",
    "HAT":  "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "PERC": "x..x..x...x..x.. | x..x..x...x.xx..",
})
# sparse: quarter-note hats with one roll, a snap on three, rim clicks, lots of room for the 808
pack.drums("Sparse Snap", "SP1200", {
    "KICK": "X..........x.... | X......x........",
    "CLAP": "........X....... | ........X.......",
    "HAT":  "x...x...x...xxxx | x...x...x...x.x.",
    "PERC": "......x........x | ......x.........",
})

# --- bass: 808 lines ---------------------------------------------------------------------------
# the root held long, gliding up the octave; VI and VII sliding home (the 808 glides on SLIDE)
pack.bass("808 Root Glide", "808 · Monosynth",
          "1! _ _ _ _ _ _ _ _ 1~ 1+ _ _ _ _ _ | 1! _ _ _ _ _ _ 6- _ _ 7-~ _ _ _ 1 _")
# the 808 in threes, against the half-time clap
pack.bass("Triplet 808", "808 · Monosynth",
          "1! _ _ 1 _ _ 1 _ . . 6- _ _ 7- _ _ | 1! _ _ 1 _ _ 3 _ . . 4 _ _ 3 _ _")
# drill: sliding through the Phrygian ♭2 and up from the leading note below
pack.bass("Drill Slides", "808 · Monosynth",
          "1! _ _ _ _ _ b2~ _ 1 _ _ . 7-~ _ 1 _ | 6-! _ _ _ _ _ 5-~ _ 6- _ _ . 1~ _ b2 _")
# phonk: short, punchy 808 hits that leave the cowbell room
pack.bass("Phonk Bounce", "808 · Monosynth",
          "1! . . 1 . . 1 . . . 1 . 3 . 1 . | 6-! . . 6- . . 6- . . . 7- . 7- . 1 .")
# harmonic minor: the raised seventh pulling back to the root
pack.bass("Harmonic Minor 808", "808 · Monosynth", " | ".join([
    " ".join([N("1!", 8), N("5-", 4), N("#7-", 4)]), " ".join([N("6-!", 8), N("5-", 6), N("#7-", 2)])]))

# --- lead ---------------------------------------------------------------------------------------
# a flute riff in the minor pentatonic, grouped 3-3-2
pack.lead("Flute Riff", "Flute",
          "5! _ _ 4 _ _ 3 _ 1 _ _ 3 _ _ 4 _ | 5! _ _ 7 _ _ 1+ _ 7 _ _ 5 _ _ 4 _")
# a music-box bell figure in sixteenths, the top note moving
pack.lead("Bell Melody", "Music box",
          "1+! 5 3 5 1+ 5 3 5 1+ 5 3 5 2+ 5 3 5 | 7! 5 3 5 7 5 3 5 6 4 1 4 6 4 2 4")
# a dark, sparse piano line: the leading tone (harmonic minor) resolving to the octave
pack.lead("Dark Piano", "Grand piano", " | ".join([
    " ".join([N("1!", 4), R(2), N("3", 2), N("5", 4), N("#7", 4)]), " ".join([N("1+!", 8), N("5", 4), N("3", 4)])]))
# a synth lead in threes, falling then climbing back
pack.lead("Triplet Synth", "Calf Monosynth",
          "1+! _ _ 1+ _ _ 7 _ 5 _ _ 4 _ _ 3 _ | 1! _ _ 3 _ _ 4 _ 5 _ _ 7 _ _ 5 _")
# a drill string riff on the Phrygian ♭2
pack.lead("Phrygian Riff", "Violin",
          "1! _ b2 _ 1 _ 7- _ 1 _ _ _ 5- _ 6- _ | 1! _ b2 _ 3 _ b2 _ 1 _ _ _ . . . .")

# --- chords -------------------------------------------------------------------------------------
# i – VI held two bars each (the CHORD SET's chords)
pack.chords("i–VI Pad", "Strings · Ensemble", " ".join([C("1", 32), C("6", 31, 1)]))
# i – iv – VI – V (the harmonic minor's major V, chromatic): a stab and an echo each bar
PIANO = {"i": ("x", [7, 9, 11]), "iv": ("x", [7, 10, 12]), "VI": ("x", [7, 9, 12]), "V": ("c", [11, 14, 19])}
pack.chords("i–iv–VI–V Stabs", "Grand piano", " | ".join(
    " ".join([C("@" + c, 6, 2), C("@" + c, 2, 6)]) for c in ["i", "iv", "VI", "V"]), PIANO)
# a choir on i – VII – VI – VII, a bar each
pack.chords("Choir i–VII–VI–VII", "Choir", " ".join([C("1", 16), C("7", 16), C("6", 16), C("7", 15, 1)]))
# drill: pizzicato strings plucking i and the Phrygian ♭II in 3-3-2
DRILL = {"i": ("c", [0, 3, 7]), "bII": ("c", [1, 5, 8])}
pack.chords("Drill Pizzicato", "Pizzicato strings", " | ".join(
    " ".join([C("@" + c, 1, 2), C("@" + c, 1, 2), C("@" + c, 1, 1)] * 2) for c in ["i", "bII"]), DRILL)
# glassy stabs on i – v – VI – VII, each half bar in 3-3-2
pack.chords("Glassy Stabs", "Alien · Glassy", " ".join(
    " ".join([C(d, 2, 1), C(d, 2, 1), C(d, 1, 1)]) for d in "1567"))

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(140, "F", "Natural Minor", echo=0.15, heavy=0.45,
              about="Trap at 140 (a half-time 70) in F minor, straight hats, hard-squashed 808s.")

if __name__ == "__main__":
    pack.done()
