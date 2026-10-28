#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret pop pack: five pattern presets for each of the drums, the bass, the lead and the
# chords, laid out as a USB stick holds them (see ../patternkit.py and the jazz pack).
# Written in scale degrees for a MAJOR key: four-on-the-floor dance pop, the half-time
# ballad, 80s gated drums, the modern 808 hybrid and Motown; the axis progression
# (I–V–vi–IV) and its rotations, the 50s doo-wop changes, the "royal road" (IV–V–iii–vi).
# Everything original and idiomatic.
#   python3 tools/packs/pop.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/pop/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "pop")
sys.path.insert(0, HERE)
from patternkit import MAJOR, Pack, N, C, R  # noqa: E402

pack = Pack("Pop", PACK, MAJOR)

# --- drums --------------------------------------------------------------------------------------
# dance pop: four on the floor, claps on two and four, open hats on the off-beats, a clap
# flam into the next bar
pack.drums("Four on the Floor", "TR909", {
    "KICK": "X...x...X...x... | X...x...X...x...",
    "CLAP": "....x.......x... | ....x.......x.xx",
    "HAT":  "xx.xxx.xxx.xxx.x | xx.xxx.xxx.xxx.x",
    "OPEN": "..x...x...x...x. | ..x...x...x...x.",
})
# the half-time ballad: one snare a bar on beat three, the kick leaning on the "and"s
pack.drums("Half-Time Ballad", "STANDARD", {
    "KICK":   "X.....x.......x. | X.....x..x......",
    "SNARE":  "........X....... | ........X.....x.",
    "HAT":    "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "CYMBAL": "X............... | ................",
})
# 80s gated: a big snare on two and four, the kick doubled on three, a tom run into the top
pack.drums("80s Gated", "LINN", {
    "KICK":   "X.......X.x..... | X.......X.x.....",
    "SNARE":  "....X.......X... | ....X...........",
    "HAT":    "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.....",
    "TOM":    "................ | ............xxxx",
    "CYMBAL": "X............... | ................",
})
# modern pop on the 808: half-time claps, sparse kicks, hats breaking into sixteenth rolls
pack.drums("808 Pop", "TR808", {
    "KICK": "X.........X..... | X......x..X.....",
    "CLAP": "........X....... | ........X.......",
    "HAT":  "x.x.x.x.x.xxx.x. | x.x.x.x.xxxxx.x.",
    "OPEN": "..............x. | ................",
})
# Motown: the snare on all four beats (two and four harder, with the tambourine), the kick
# skipping in between
pack.drums("Motown Stomp", "ROOM", {
    "SNARE": "x...X...x...X... | x...X...x...X...",
    "KICK":  "x.....x.x.....x. | x.....x.x...x.x.",
    "PERC":  "....x.......x... | ....x.......x...",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
})

# --- bass ---------------------------------------------------------------------------------------
# pumping eighths on the roots of I – V – vi – IV
pack.bass("Axis Eighths", "Finger bass", " | ".join(
    " ".join([N(root + "!", 2)] + [N(root, 2)] * 7) for root in ["1", "5-", "6-", "4-"]))
# synth pop: eighths jumping the octave over vi – IV – I – V
pack.bass("Synth Octaves", "Synth bass", " | ".join(
    " ".join([N(root + "-!", 1, 1), N(root, 1, 1)] + [N(root + "-", 1, 1), N(root, 1, 1)] * 3)
    for root in ["6", "4", "1", "5"]))
# the ballad's descending bass (I – V/7 – vi – IV), a walk-up from IV back home
pack.bass("Ballad Descent", "Fretless", " | ".join([
    N("1!", 16), N("7-", 16), " ".join([N("6-", 12), N("5-", 4)]), " ".join([N("4-", 12), N("5-", 4)])]))
# funk-pop sixteenths: octave pops and a slide into each bar's last note
pack.bass("Funk-Pop Sixteenths", "Slap bass",
          "1! . . 1 . . 1+ . 1 . . 5- . 6- 7-~ 1 | 4-! . . 4- . . 4 . 4- . . 1 . 2 3~ 4")
# a Motown line: melodic, pickups into every chord (I – vi – IV – V), a leading tone home
pack.bass("Motown Walk", "Finger bass", " | ".join([
    "1! _ . 1 3 _ 5 _ 6-! _ . 6- 1 _ 3 _", "4-! _ . 4- 6- _ 1 _ 5-! _ . 5- 2 _ 7- _"]))

# --- lead ---------------------------------------------------------------------------------------
# a sung-style hook: repeated notes stepping down, an answer leaping to the fifth
pack.lead("Axis Hook", "Calf Monosynth",
          "3! _ . 3 _ . 2 _ 1 _ . 2 _ 3 _ . | 5! _ . 5 _ . 3 _ 2 _ _ _ . . . .")
# a piano ostinato in sixteenths, grouped 3+3+2 against the beat
pack.lead("Piano Ostinato", "Grand piano",
          "5! 3 1 5! 3 1 5! 3 5! 3 1 5! 3 1 5! 3 | 6! 4 1 6! 4 1 6! 4 5! 3 1 5! 3 1 5! 2")
# an 80s pop sax hook: up to the octave and down through the major pentatonic
pack.lead("Sax Hook", "Alto sax",
          "5! _ 6 1+ _ _ 6 _ 5 _ _ _ 3 _ 5 _ | 6! _ _ 5 _ 3 _ 2 _ _ _ _ 1 _ _ .")
# a pluck arpeggio in sixteenths over I – V – vi – IV
ARP = {"1": "1 3 5 1+ 3+ 1+ 5 3", "5": "5- 7- 2 5 7 5 2 7-", "6": "6- 1 3 6 1+ 6 3 1", "4": "4- 6- 1 4 6 4 1 6-"}
pack.lead("Pluck Arp", "Vibes", " | ".join(
    (ARP[c].split()[0] + "! " + " ".join(ARP[c].split()[1:]) + " " + ARP[c]) for c in ["1", "5", "6", "4"]))
# a ballad melody: long notes, a lift to the sixth, ending open on the second
pack.lead("Ballad Melody", "Rhodes", " | ".join([
    " ".join([N("3!", 6), N("2", 2), N("1", 8)]), " ".join([N("2", 4), N("3", 4), N("5", 8)]),
    " ".join([N("6!", 6), N("5", 2), N("3", 4), N("1", 4)]), " ".join([N("2", 12), R(4)])]))

# --- chords: digits are the CHORD SET's chords on the degree ------------------------------------
# I – V – vi – IV in quarter notes, a bar each
pack.chords("Axis Quarters", "Grand piano", " | ".join(" ".join([C(d, 3, 1)] * 4) for d in "1564"))
# vi – IV – I – V pulsing in eighths, the synth-pop way
pack.chords("Minor-Start Pulse", "TAL NoiseMaker", " | ".join(" ".join([C(d, 1, 1)] * 8) for d in "6415"))
# the 50s doo-wop changes I – vi – IV – V, half a bar each, plain triads (any CHORD SET)
DOOWOP = {"I": ("x", [7, 9, 11]), "vi": ("x", [5, 7, 9]), "IV": ("x", [5, 7, 10]), "V": ("x", [4, 6, 8])}
pack.chords("Doo-Wop Changes", "Upright piano", " ".join(C("@" + c, 7, 1) for c in ["I", "vi", "IV", "V"]), DOOWOP)
# the "royal road" IV – V – iii – vi, each bar in a 3+3+2 push
pack.chords("Royal Road", "Rhodes", " | ".join(" ".join([C(d, 2, 1), C(d, 2, 1), C(d, 9, 1)]) for d in "4536"))
# ballad strings with a stepping bass in the voicing: I – V/7 – vi – IV V
BALLAD = {"I": ("x", [0, 4, 7, 9]), "V6": ("x", [-1, 1, 4, 8]), "vi": ("x", [-2, 2, 7, 9]),
          "IV": ("x", [-4, 5, 7, 10]), "V": ("x", [-3, 4, 6, 8])}
pack.chords("Ballad Strings", "Strings · Ensemble", " ".join(
    [C("@I", 16), C("@V6", 16), C("@vi", 16), C("@IV", 8), C("@V", 7, 1)]), BALLAD, ties="all")

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(116, "C", "Major", echo=0.15, heavy=0.25,
              about="Radio pop in C major at the pack's middle tempo, straight, a touch of echo and glue.")

if __name__ == "__main__":
    pack.done()
