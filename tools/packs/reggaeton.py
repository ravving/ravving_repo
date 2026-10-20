#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret reggaeton pack: five pattern presets for each of the drums, the bass, the lead
# and the chords, laid out as a USB stick holds them (see ../patternkit.py and the jazz pack).
# Written in scale degrees for a NATURAL MINOR key (the harmonic minor's leading tone as an
# ALTER'd degree): the dembow (kick on every beat, the snare on the 3-3-2 "a" of one, "and"
# of two, "a" of three, "and" of four), perreo, timbal fills, Dominican dembow, moombahton;
# i–VI–III–VII, i–iv–VII–III and the Andalusian cadence i–VII–VI–V.
#   python3 tools/packs/reggaeton.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/reggaeton/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "reggaeton")
sys.path.insert(0, HERE)
from patternkit import MINOR, Pack, N, C, R  # noqa: E402

pack = Pack("Reggaeton", PACK, MINOR)

# --- drums --------------------------------------------------------------------------------------
# the dembow: boom-ch-boom-chick, the kick on every beat, the snare on the 3-3-2 off-beats
pack.drums("Dembow Clásico", "TR808", {
    "KICK":  "X...x...X...x... | X...x...X...x...",
    "SNARE": "...x..x....x..x. | ...x..x....x.xx.",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
})
# perreo lento: the kick on one and three, the clap only on the "and"s, off-beat hats
pack.drums("Perreo Lento", "TR808", {
    "KICK": "X.......X....... | X.......X.......",
    "CLAP": "......x.......x. | ...x..x.......x.",
    "HAT":  "..x...x...x...x. | ..x...x...x.x.x.",
    "PERC": "...x.......x.... | ...x.......x....",
})
# the dembow with timbal: a cowbell line and a tom roll turning the second bar
pack.drums("Dembow Timbal", "TR808", {
    "KICK":  "X...x...X...x... | X...x...X...x...",
    "SNARE": "...x..x....x..x. | ...x..x....x....",
    "PERC":  "x.x...x.x.x...x. | x.x...x.x.x.....",
    "TOM":   "................ | ............x.xx",
})
# Dominican dembow: faster, the snare doubled on the "and" of two, sixteenth hats, claps on
# two and four
pack.drums("Dembow Dominicano", "TR808", {
    "KICK":  "X...x...X...x... | X...x...X...x...",
    "SNARE": "...x..xx...x..x. | ...x..xx...x.xx.",
    "HAT":   "xxxxxxxxxxxxxxxx | xxxxxxxxxxxxxxxx",
    "CLAP":  "....x.......x... | ....x.......x...",
})
# moombahton: the dembow under house claps on two and four, open hats lifting the bar
pack.drums("Moombahton", "TR909", {
    "KICK":  "X...x...X...x... | X...x...X...x...",
    "SNARE": "...x..x....x..x. | ...x..x....x..x.",
    "CLAP":  "....x.......x... | ....x.......x...",
    "OPEN":  "..x.......x..... | ..x.......x.....",
})

# --- bass ---------------------------------------------------------------------------------------
# the 808 on the tresillo (3+3+2 twice a bar) under i – VI – III – VII
pack.bass("Dembow 808", "808 · Monosynth", " | ".join(
    " ".join([N(r + "!", 3), N(r, 3), N(r, 2), N(r, 3), N(r, 3), N(r, 2)]) for r in ["1", "6-", "3", "7-"]))
# perreo: the root held, sliding down through VII into VI (the 808 glides on SLIDE)
pack.bass("Perreo Sub", "808 · Monosynth",
          "1! _ _ _ _ _ _ _ _ _ _ _ _ _ 7-~ 6- | 6- _ _ _ _ _ _ _ _ _ _ _ _ _ 7-~ 1")
# a syncopated synth bass jumping the octave on the off-beats
pack.bass("Syncopated Synth", "Synth bass",
          "1! . . 1 . . 1+ . . 1 . . 7 . 5 . | 6-! . . 6- . . 6 . . 6- . . 5 . 3 .")
# reggaeton romántico: a bass guitar walking i – iv – VII – III in eighths
pack.bass("Romántico Walk", "Finger bass",
          "1! _ 5- _ 1 _ 3 _ 4-! _ 1 _ 4 _ 3 _ | 7-! _ 2 _ 4 _ 2 _ 3! _ 7- _ 5- _ 7- _")
# Dominican dembow: the bass pumping the off-beat eighths, i then VI
pack.bass("Offbeat Pump", "808 · Monosynth", " | ".join(
    " ".join([R(2), N(r + "!", 2)] + [R(2), N(r, 2)] * 3) for r in ["1", "6-"]))

# --- lead ---------------------------------------------------------------------------------------
# a synth pluck hook on the tresillo
pack.lead("Pluck Hook", "Calf Monosynth",
          "5! _ _ 5 _ _ 3 _ 4 _ _ 3 _ _ 1 _ | 7-! _ _ 1 _ _ 3 _ 1 _ _ 7- _ _ 5- _")
# a romántico nylon guitar over the Andalusian cadence: 3-2-1 and the raised 7
pack.lead("Guitarra Romántica", "Nylon guitar",
          "3! _ _ _ 5 _ 3 _ 2 _ _ _ 4 _ 2 _ | 1! _ _ _ 3 _ 1 _ #7- _ _ _ 2 _ #7- _")
# a high flute line, short syncopated notes falling then rising
pack.lead("Flauta Perreo", "Flute",
          "1+! _ . 7 _ . 5 _ . 4 _ . 5 _ _ _ | 3! _ . 4 _ . 5 _ . 7 _ . 5 _ _ _")
# a marimba playing the dembow's own rhythm
pack.lead("Marimba Dembow", "Marimba",
          "1+! . . 5 . . 1+ . 7 . . 5 . . 7 . | 6! . . 3 . . 6 . 5 . . 3 . . 5 .")
# a romántico sax: long notes, a turn into the leading tone
pack.lead("Sax Romántico", "Alto sax", " | ".join([
    " ".join([N("5!", 6), N("4", 2), N("3", 8)]), " ".join([N("4", 6), N("3", 2), N("2", 4), N("#7-", 4)])]))

# --- chords -------------------------------------------------------------------------------------
# i – VI – III – VII stabbed on the dembow (3+3+2 a half bar)
pack.chords("i–VI–III–VII Dembow", "TAL NoiseMaker", " | ".join(
    " ".join([C(d, 2, 1), C(d, 2, 1), C(d, 1, 1)] * 2) for d in "1637"))
# romántico piano: i – iv – VII – III held a bar each
pack.chords("Romántico Piano", "Grand piano", " ".join([C("1", 16), C("4", 16), C("7", 16), C("3", 16)]))
# the Andalusian cadence i – VII – VI – V strummed (the V major, chromatic), guitar voicings
ANDALUSIAN = {"i": ("x", [0, 2, 4, 7]), "VII": ("x", [-1, 1, 3, 6]), "VI": ("x", [-2, 0, 2, 5]), "V": ("c", [-5, -1, 2, 7])}
pack.chords("Andalusian Strum", "Nylon guitar", " | ".join(
    " ".join([C("@" + c, 2, 1), C("@" + c, 1, 1), C("@" + c, 2, 1), C("@" + c, 1, 1), C("@" + c, 3, 1), C("@" + c, 1, 1)])
    for c in ["i", "VII", "VI", "V"]), ANDALUSIAN)
# a pad: VI – VII – i (two bars on i)
pack.chords("Pad VI–VII–i", "Strings · Digital", " ".join([C("6", 16), C("7", 16), C("1", 32)]))
# moombahton organ: stabs on the off-beat eighths, i – VI – i – v
pack.chords("Organ Offbeats", "Organ · House", " | ".join(
    " ".join([R(2), C(d, 1, 1)] * 4) for d in "1615"))

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(93, "A", "Natural Minor", echo=0.1, heavy=0.4,
              about="The dembow at 93 in A minor, straight, the kick pumped by HEAVY.")

if __name__ == "__main__":
    pack.done()
