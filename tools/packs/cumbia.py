#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret cumbia pack (it replaced the tropical one): five pattern presets for each of the
# drums, the bass, the lead and the chords, laid out as a USB stick holds them (see
# ../patternkit.py and the jazz pack). Colombian cumbia, Mexican sonidera, Argentine villera,
# Peruvian chicha and digital cumbia.
#
# Written in scale degrees for a MAJOR key. The minor-mode styles (villera, chicha: i – VII,
# the leading tone of harmonic minor) sit on degree 6, the relative minor, so the whole pack
# shares one key: in C major they play in A minor (vi – V is A minor's i – VII).
#
# The drums play kits.json's "Cumbia" kits: PERC the güiro (the guacharaca's "chu-chucu"),
# CLAP a conga (the llamador), TOM a timbale, CYMBAL the cowbell (the campana); KICK is the
# tambora's low stroke.
#   python3 tools/packs/cumbia.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/cumbia/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "cumbia")
sys.path.insert(0, HERE)
from patternkit import MAJOR, Pack, N, C, R  # noqa: E402

pack = Pack("Cumbia", PACK, MAJOR)

# --- drums --------------------------------------------------------------------------------------
GUIRO = "x.xx x.xx x.xx x.xx"  # a stroke on the beat, then down-up on its "and-a"
# Colombian cumbia: the tambora on one and three, the llamador on two and four, the güiro
# every beat, the alegre (a timbale) answering in the second bar
pack.drums("Colombiana", "CUMBIA_ROOM", {
    "PERC": f"{GUIRO} | {GUIRO}",
    "KICK": "X... .... x... .... | X... .... x... ....",
    "CLAP": ".... x... .... x... | .... x... .... x...",
    "TOM":  ".... .... .... .... | ..x. .x.. ..x. x.x.",
})
# sonidera: slower, the kick with a pickup into three, the llamador on every "and", the
# campana's quarters for the climax and a timbal fill
pack.drums("Sonidera", "CUMBIA", {
    "PERC":   f"{GUIRO} | {GUIRO}",
    "KICK":   "X... .... x... ..x. | X... .... x... ....",
    "CLAP":   "..x. ..x. ..x. ..x. | ..x. ..x. ..x. ....",
    "CYMBAL": ".... .... .... .... | x... x... x... ....",
    "TOM":    ".... .... .... .... | .... .... .... xxxx",
})
# villera: harder, electronic: a snare cracking on two and four, the kick on one, the "a" of
# two and three, timbal rolls at the end of the phrase
pack.drums("Villera", "CUMBIA", {
    "PERC":  f"{GUIRO} | {GUIRO}",
    "KICK":  "X... ...x x... .... | X... ...x x... ....",
    "SNARE": ".... X... .... X... | .... X... .... X...",
    "TOM":   ".... .... .... .... | .... .... ..xx .xxx",
})
# chicha: the timbales' pattern over the güiro, a conga on the off-beat eighths, the kick on
# one and three
pack.drums("Chicha", "CUMBIA_ROOM", {
    "PERC": f"{GUIRO} | {GUIRO}",
    "KICK": "X... .... x... .... | X... .... x... ....",
    "TOM":  "x.x. .xx. x.x. .x.x | x.x. .xx. x.x. xxxx",
    "CLAP": "..x. ..x. ..x. ..x. | ..x. ..x. ..x. ..x.",
})
# digital cumbia: drum machine, the hats playing the güiro's figure, kick on one, three and the
# "and" of four, claps on two and four
pack.drums("Digital", "TR808", {
    "HAT":  f"{GUIRO} | x.xx x.xx x.xx x...",
    "OPEN": ".... .... .... .... | .... .... .... ..x.",
    "KICK": "X... .... X... ..x. | X... .... X... ..x.",
    "CLAP": ".... x... .... x... | .... x... .... x...",
    "PERC": "..x. ..x. ..x. ..x. | ..x. ..x. ..x. ..x.",
})

# --- bass ---------------------------------------------------------------------------------------
# the cumbia tumbao: the root for a dotted quarter, the fifth below anticipating, I then V
pack.bass("Root–Fifth Tumbao", "Finger bass", " | ".join([
    " ".join([N("1!", 6), N("5-", 2), N("1", 6), N("5-", 2)]),
    " ".join([N("5-!", 6), N("2", 2), N("5-", 6), N("7-", 2)])]))
# Colombian two-beat: root on one, fifth on three, a pickup on the "and" of four into the
# next chord, I – IV – V – I
TWO_BEAT = [("1", "5-", "3-"), ("4-", "1", "#4-"), ("5-", "2", "7-"), ("1", "5-", "7-")]
pack.bass("Tónica-Dominante", "Acoustic bass", " | ".join(
    " ".join([N(r + "!", 3, 1), R(4), N(f, 3, 1), R(2), N(p, 2)]) for r, f, p in TWO_BEAT))
# sonidera: a round bass walking up from I to IV and back
pack.bass("Sonidera Walk", "Fretless",
          "1! _ _ . 5- _ _ . 1 _ 2 _ 3 _ . . | 4-! _ _ . 1 _ _ . 4- _ 5- _ 6- _ 7- _")
# villera: a keyboard bass repeating the relative minor's i – VII (vi – V of the key)
pack.bass("Villera i–VII", "Synth bass",
          "6-! _ . 6- . . 3- _ 6- _ . 6- . . 3- _ | 5-! _ . 5- . . 2- _ 5- _ . 5- . . 2- _")
# digital cumbia: the tumbao's rhythm on an 808 over vi – IV – I – V, each bar's last note
# gliding into the next root
DIGITAL = [("6-", "3-"), ("4-", "1"), ("1", "5-"), ("5-", "2")]
pack.bass("Digital 808", "808 · Monosynth", " | ".join(
    " ".join([N(r + "!", 6), N(f, 2), N(r, 7), N(f + "~", 1)]) for r, f in DIGITAL))

# --- lead ---------------------------------------------------------------------------------------
# the accordion: eighth runs down the scale and back up to the dominant
pack.lead("Acordeón", "Accordion", " | ".join(
    " ".join(N(n + ("!" if i == 0 else ""), 2) for i, n in enumerate(bar.split()))
    for bar in ["1+ 7 6 5 6 5 4 3", "2 3 4 5 4 3 2 5-"]))
# the caña de millo (the cumbia's original flute): sixteenth trills around the top notes
pack.lead("Caña de Millo", "Flute",
          "5+! 6+ 5+ 3+ 5+ 6+ 5+ 3+ 2+ 3+ 2+ 1+ 2+ _ . . | 1+! 2+ 1+ 6 1+ 2+ 1+ 6 5 6 5 3 5 _ . .")
# chicha guitar: tremolo-picked pairs falling in the relative minor, the raised seventh
# (♯5 of the key) leading back to its tonic
pack.lead("Chicha Guitar", "Guitar · Overdrive",
          "3+! 3+ 3+ 3+ 2+ 2+ 1+ 1+ 7 7 6 6 #5 #5 6 _ | 6! 6 1+ 1+ 3+ 3+ 2+ 2+ 1+ 1+ 7 7 6 _ _ _")
# villera: a sharp keyboard lead turning around the relative minor's tonic
pack.lead("Villera Lead", "Calf Monosynth",
          "6! _ 7 1+ _ 7 6 _ 5 _ 6 _ 3 _ _ . | 6! _ 7 1+ _ 2+ 3+ _ 2+ _ 1+ _ 7 _ _ .")
# the orquesta's brass (the big-band cumbia of the 1950s): a call falling from the octave and
# its answer from the fourth
pack.lead("Orquesta Brass", "Trumpet",
          "1+! _ . 1+ . 7 6 _ 5 _ . 3 _ _ . . | 4! _ . 4 . 5 6 _ 5 _ . 2 _ _ . .")

# --- chords -------------------------------------------------------------------------------------
TRIADS = {"I": ("x", [7, 9, 11]), "IV": ("x", [7, 10, 12]), "V": ("x", [6, 8, 11]),
          "vi": ("x", [5, 7, 9]), "Vlow": ("x", [4, 6, 8]), "III": ("c", [4, 8, 11])}
# the accordion's off-beat chords, I – V – V – I
pack.chords("Accordion Offbeats", "Accordion", " | ".join(
    " ".join([R(2), C("@" + c, 1, 1)] * 4) for c in ["I", "V", "V", "I"]), TRIADS)
# a sonidera combo organ: chords on the "and" of one and three, held, I – IV – V – I
pack.chords("Sonidera Organ", "Jazz organ", " | ".join(
    " ".join([R(2), C("@" + c, 5, 1), R(2), C("@" + c, 5, 1)]) for c in ["I", "IV", "V", "I"]), TRIADS)
# villera keyboard: two quick stabs every half bar on the relative minor's i – VII
# (vi – V of the key, the CHORD SET's sevenths)
pack.chords("Villera Stabs", "TAL NoiseMaker", " | ".join(
    " ".join([R(2), C(d, 1, 1), C(d, 1, 3)] * 2) for d in "6565"))
# chicha surf guitar: i – VII – i – V of the relative minor (Am G Am E in C; E major chromatic),
# strummed on the beats
pack.chords("Chicha Surf", "Guitar · Clean", " | ".join(
    " ".join([C("@" + c, 3, 1)] * 4) for c in ["vi", "Vlow", "vi", "III"]), TRIADS)
# the orquesta's brass hits on the "and" of two and on four, I – IV – V – I
pack.chords("Orquesta Hits", "Brass section", " | ".join(
    " ".join([R(6), C("@" + c, 2, 2), C("@" + c, 4, 2)]) for c in ["I", "IV", "V", "I"]), TRIADS)

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(95, "G", "Major", phaser=0.15, echo=0.3, heavy=0.2,
              about="Cumbia at 95 in G major, straight; the sonidero's echo and a little phaser.")

if __name__ == "__main__":
    pack.done()
