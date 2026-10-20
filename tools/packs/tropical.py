#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret tropical pack: Latin "música tropical" without cumbia, which has its own pack.
# Five pattern presets for each of the drums, the bass, the lead and the chords, laid out as a
# USB stick holds them (see ../patternkit.py and the jazz pack). Each instrument has one
# preset per style:
#
#   salsa      2-3 son clave, conga marcha, bass tumbao, piano montuno, mambo horns
#   merengue   güira, tambora (with its quintillo), sax jaleo, I – V
#   bachata    bongos and güira, requinto arpeggios, segunda strums
#   vallenato  caja and guacharaca (paseo), accordion, guitar
#   champeta   drum machine, soukous ("sebene") guitar, synth bass
#
# Written in scale degrees for a MAJOR key. Salsa and bachata are minor styles, so they sit on
# degree 6 (the relative minor): in C major they play in A minor, with i – iv – V
# (vi – ii – III of the key, the V major through a chromatic voicing or a ♯5).
#
# The drums play kits.json's Latin kits:
#   Latin · congas  SNARE open conga, CLAP conga slap, TOM tumba, HAT claves, OPEN maracas,
#                   CYMBAL cowbell (campana), PERC güiro
#   Latin · güira   SNARE high bongo, TOM low bongo, CLAP conga slap, OPEN tumba (the
#                   tambora's low stroke), HAT maracas, CYMBAL cowbell, PERC cabasa (the
#                   metal güira)
#   python3 tools/packs/tropical.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/tropical/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "tropical")
sys.path.insert(0, HERE)
from patternkit import MAJOR, Pack, N, C, R  # noqa: E402

pack = Pack("Tropical", PACK, MAJOR)

# --- drums --------------------------------------------------------------------------------------
# salsa: the 2-3 son clave on the claves, the conga's marcha (slap on two, open tones on four
# and its "and", the tumba answering in the 3-side bar), the campana on the beats, the bombo
# on the 3-side's "and" of two
pack.drums("Salsa", "CONGAS", {
    "HAT":    "....x...x....... | x.....x.....x...",
    "CLAP":   "....x.......x... | ....x.......x...",
    "SNARE":  "............x.x. | ............x...",
    "TOM":    "................ | ..............x.",
    "CYMBAL": "X...x...x...x... | X...x...x...x...",
    "KICK":   "................ | ......x.........",
})
# merengue: the güira brushed on every beat with its "and-a", the tambora's hand stroke on the
# downbeats and stick on the off-beats, the quintillo's five strokes into the third beat, the
# orquesta's kick on every beat
pack.drums("Merengue", "GUIRA", {
    "PERC": "X.xx X.xx X.xx X.xx | X.xx X.xx X.xx X.xx",
    "OPEN": "x... .... x... .... | x... .x.x x... ....",
    "CLAP": "..x. ..x. ..x. ..x. | ..x. x.x. ..x. ..x.",
    "KICK": "x... x... x... x... | x... x... x... x...",
})
# bachata: the bongo's martillo in eighths, the low bongo's open tone on four, the güira
# keeping time, the tumba pushing the second bar
pack.drums("Bachata", "GUIRA", {
    "SNARE": "x.x. x.x. x.x. ..x. | x.x. x.x. x.x. ..x.",
    "TOM":   ".... .... .... X... | .... .... .... X.x.",
    "PERC":  "x.xx x.xx x.xx x.xx | x.xx x.xx x.xx x.xx",
    "OPEN":  ".... .... .... .... | .... ..x. .... ....",
})
# vallenato paseo: the caja's hand strokes on the beats and the off-beats of two and four,
# its rim (a conga slap) between, the guacharaca's scrape keeping the bar moving
pack.drums("Vallenato", "CUMBIA_ROOM", {
    "TOM":  "x... x.x. x... x.x. | x... x.x. x... xxx.",
    "CLAP": "..x. .... ..x. .... | ..x. .... ..x. ....",
    "PERC": "x.xx x.xx x.xx x.xx | x.xx x.xx x.xx x.xx",
})
# champeta: drum machine in front, the kick on one, the "and" of two and three, snare on two
# and four, the soukous cavacha in running sixteenths on the hats, a cowbell on the off-beats
pack.drums("Champeta", "TR808", {
    "KICK":  "X... ..x. X... ..x. | X... ..x. X... x.x.",
    "SNARE": ".... X... .... X... | .... X... .... X..x",
    "HAT":   "xxxx xxxx xxxx xxxx | xxxx xxxx xxxx xxxx",
    "PERC":  "..x. ..x. ..x. ..x. | ..x. ..x. ..x. ..x.",
})

# --- bass ---------------------------------------------------------------------------------------
# the salsa tumbao (relative minor: i – iv – V – i): only the tresillo's off-beats sound, the
# "and" of two and beat four, the note on four held over the bar line (anticipating the
# next chord); beat one is left to the previous note
pack.bass("Salsa Tumbao", "Upright", " ".join([
    N("6-!", 6), N("3", 6), N("2-", 10),    # Am: its fifth on the "and" of two, then Dm early
    N("6-", 6), N("3-", 10),                # Dm: its fifth, then E early
    N("7-", 6), N("6-", 10),                # E: its fifth, then Am early
    N("3", 6), N("6-", 4)]))                # Am: its fifth, the root into the top again
# merengue: the bass on the beat and the "and" of two, I and V alternating
pack.bass("Merengue Bass", "Finger bass", " | ".join(
    f"{r}! _ . {r} . . {f} _ {r} _ . {r} . . {f} _" for r, f in [("1", "5-"), ("5-", "2"), ("5-", "2"), ("1", "5-")]))
# bachata: root, fifth and back on the syncopations, under i – iv – V – i of the relative minor
pack.bass("Bachata Bass", "Acoustic bass", " | ".join(
    f"{r}! _ _ {f} _ . {r} _ {r} _ . {f} _ {r} _ ." for r, f in [("6-", "3-"), ("2-", "6-"), ("3-", "7-"), ("6-", "3-")]))
# vallenato paseo: root and fifth on the beats with a pickup into each chord, I – IV – V – I
PASEO = [("1", "5-", "3-"), ("4-", "1", "#4-"), ("5-", "2", "7-"), ("1", "5-", "7-")]
pack.bass("Vallenato Paseo", "Picked bass", " | ".join(
    " ".join([N(r + "!", 3, 1), N(f, 2), N(r, 3, 1), N(f, 2), N(p, 2), R(2)]) for r, f, p in PASEO))
# champeta: a fast bass jumping the octave on the sixteenths, I – IV – V – IV
pack.bass("Champeta Bass", "Synth bass", " | ".join(
    f"{r}! . {o} . . {r} . {o} {r} . . {o} . {r} {o} ." for r, o in [("1", "1+"), ("4-", "4"), ("5-", "5"), ("4-", "4")]))

# --- lead ---------------------------------------------------------------------------------------
# salsa mambo horns (relative minor): a syncopated call falling from the octave, the answer
# rising through the leading tone (♯5 of the key)
pack.lead("Mambo Horns", "Trumpet",
          "3+! _ . 3+ . 2+ 1+ _ 7 _ . 6 _ _ . . | #5! _ . #5 . 6 7 _ 1+ _ . 3+ _ _ . .")
# the merengue sax jaleo: a running sixteenth arpeggio on I, then on V7
pack.lead("Sax Jaleo", "Alto sax",
          "1+! 5 3 5 1+ 5 3 5 1+ 5 3 5 1+ 5 3 5 | 7! 5 2 5 7 5 2 5 4+ 2+ 7 2+ 4+ 2+ 7 5")
# the bachata requinto: arpeggios up and down the relative minor's i, then its V (♯5)
pack.lead("Requinto", "Nylon guitar",
          "6! 1+ 3+ 6+ 3+ 1+ 6 1+ 3+ 1+ 6 3 6 1+ 3+ _ | 3+! #5 7 3+ 7 #5 3 #5 7 3+ 2+ 1+ 7 #5 6 _")
# the vallenato accordion: a paseo melody turning around the third, V then I
pack.lead("Acordeón Paseo", "Accordion",
          "5! _ 6 5 3 _ 2 1 _ 2 3 _ 5 _ 3 _ | 4! _ 5 4 2 _ 1 7- _ 1 2 _ 5- _ 1 _")
# the champeta sebene: soukous guitar picking sixteenths high on the neck, I then IV – V
pack.lead("Sebene Guitar", "Guitar · Clean",
          "3+! 5 1+ 5 3+ 5 1+ 5 2+ 5 7 5 2+ 5 7 5 | 4+! 6 1+ 6 4+ 6 1+ 6 3+ 5 1+ 5 2+ 5 7 5")

# --- chords -------------------------------------------------------------------------------------
VOICINGS = {
    # the relative minor's i, iv and V (A minor in C): montuno and bachata shapes
    "i": ("x", [5, 7, 9, 12]), "iv": ("x", [3, 5, 8, 10]), "V7": ("c", [4, 8, 11, 14]),
    "iLow": ("x", [-2, 0, 2, 5]), "ivLow": ("x", [1, 3, 5, 8]), "VLow": ("c", [4, 8, 11, 16]),
    # the major key's I, IV and V, close up and guitar-low
    "I": ("x", [7, 9, 11]), "V": ("x", [6, 8, 10, 11]),
    "Ig": ("x", [0, 2, 4, 7]), "IVg": ("x", [-4, -2, 0, 3]), "Vg": ("x", [-3, -1, 1, 4]),
}
# the salsa piano montuno: syncopated stabs (1, the "a" of one, the "and" of two, three…),
# i – iv – V7 – i of the relative minor
pack.chords("Piano Montuno", "Grand piano", " | ".join(
    " ".join([C("@" + c, 1, 2), C("@" + c, 1, 2), C("@" + c, 1, 1)] * 2) for c in ["i", "iv", "V7", "i"]), VOICINGS)
# merengue brass: off-beat hits, I – I – V7 – V7
pack.chords("Merengue Brass", "Brass section", " | ".join(
    " ".join([R(2), C("@" + c, 1, 1)] * 4) for c in ["I", "I", "V", "V"]), VOICINGS)
# the bachata segunda: strummed on each beat, the fourth held (bachata leans on four)
pack.chords("Segunda Strum", "Guitar · Clean", " | ".join(
    " ".join([C("@" + c, 2, 2), C("@" + c, 2, 2), C("@" + c, 2, 2), C("@" + c, 4)]) for c in ["iLow", "ivLow", "VLow", "iLow"]), VOICINGS)
# vallenato guitar: a strum pattern over I – IV – V – I
pack.chords("Vallenato Guitar", "Nylon guitar", " | ".join(
    " ".join([C("@" + c, 3, 1), C("@" + c, 1, 1), C("@" + c, 2, 1), C("@" + c, 3, 1), R(3)]) for c in ["Ig", "IVg", "Vg", "Ig"]), VOICINGS)
# champeta synth: stabs on the "e" after each beat, I – IV – V – IV (the CHORD SET's chords)
pack.chords("Champeta Stabs", "TAL NoiseMaker", " | ".join(
    " ".join([R(1), C(d, 2, 1)] * 4) for d in "1454"))

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(130, "C", "Major", echo=0.1, heavy=0.2,
              about="Música tropical at 130 in C major (salsa and bachata on A minor, its relative), straight.")

if __name__ == "__main__":
    pack.done()
