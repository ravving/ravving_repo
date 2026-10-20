#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret Piig pack: three pattern presets for each of the drums, the bass, the lead and the
# chords, after the candle-lit lo-fi / neo-soul of Biig Piig's early EPs (Big Fan of the Sesh,
# A World Without Snooze, No Place for Patience), laid out as a USB stick holds them (see
# ../patternkit.py). Written in scale degrees for a NATURAL MINOR key, made for D minor at
# 79 BPM with SWING 56–60, as 24K plays.
#
# Three families, one preset of each instrument in each, sharing their chord changes so any
# drums, bass, lead and chords of a family play together (and the 2-bar drums under the
# 4-bar loops):
#   Smoke     i – IV – iv – VI VII     24K's chords (Dm G Gm Bb C): the Dorian IV (raised 6th)
#                                      falling to the minor iv
#   Lay Here  i7 – V7                  Perdida's two-chord loop (Gm7 D7 there), the V with
#                                      its raised third
#   Daffodil  VII – iv – i – i         Sunny's turn (Dm Am Em there)
# Everything original; only the progressions come from the songs.
#
# Every bass, lead and chords preset brings MODS for its sound (patternkit.mods_state), for
# the records' smoky, low-passed tone: the soundfonts' CUTOFF in cents below the preset's own
# (heard below about -3600: -4800 is about 1.2 kHz from an open filter, -5400 about 880 Hz),
# softer ATTACKs and longer RELEASEs in timecents (+1200 doubles), a little CHORUS on the keys;
# the 808 a sine with a short filter click; the drums' kits darker and softer (TONE, SHAPE on
# the whole kit), the "deadened", "round kick, little click" of the records. Loading one WITH
# ITS SOUND + MODS sets them.
#   python3 tools/packs/piig.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/piig/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "piig")
sys.path.insert(0, HERE)
from patternkit import MINOR, Pack, N, C, R  # noqa: E402

pack = Pack("Piig", PACK, MINOR)

# --- drums --------------------------------------------------------------------------------------
# smoke: a lazy, dusty boom bap: the kick on one and the "a" of two, the snare on two and four,
# sixteenth hats with holes in them (to swing), rim ghosts and an open hat turning bar two
pack.drums("Smoke Dust", "SP1200", {
    "KICK":  "X......x..x..... | X......x...x....",
    "SNARE": "....X.......X... | ....X.......X...",
    "HAT":   "x.xxx.x.x.xxx.x. | x.xxx.x.x.xx..x.",
    "OPEN":  "................ | ............x...",
    "PERC":  "..........x..... | ...x..........x.",
}, mods={"TONE/CUTOFF": -3000, "SHAPE/ATTACK": 1200})
# lay here: muted and organic, a lazy bossa: the surdo-like kick, the side stick playing the
# bossa clave across the two bars, a closed hat as the shaker in eighths
pack.drums("Lay Here Bossa", "STANDARD", {
    "KICK": "x.....x.x.....x. | x.....x.x.....x.",
    "PERC": "x.....x.....x... | ....x.....x.....",
    "HAT":  "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.xxx.",
}, mods={"TONE/CUTOFF": -2400, "SHAPE/LENGTH": -1200})
# daffodil: brushes late at night: the ride's "ding, ding-a", the hat foot on two and four, a
# soft feathered kick, the brush snare on two and four with a ghost into the turn
pack.drums("Daffodil Brushes", "BRUSH_RIDE", {
    "CYMBAL": "x...x.x.x...x.x. | x...x.x.x...x.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "KICK":   "x.........x..... | x......x........",
    "SNARE":  "....X.......X... | ....X.......X.x.",
}, mods={"TONE/CUTOFF": -2400, "PITCH/TUNE": -1})

# --- bass ---------------------------------------------------------------------------------------
# smoke: a round sub, sustained and legato, gliding from the i into the IV and home again; the
# IV's B natural (the raised 6th) then the iv's B flat; Bb – C under the last bar
pack.bass("Smoke Sub", "808 · Monosynth", " | ".join([
    "1! _ _ _ _ _ _ _ _ _ 1 _ _ _ 3~ _",
    "4! _ _ _ _ _ _ _ _ _ 4 _ #6- _ 1 _",
    "4! _ _ _ _ _ _ _ _ _ 4 _ 1 _ 7- _",
    "6-! _ _ _ _ _ 6- _ 7-! _ _ _ _ _ 7-~ _"]),
    # a round sine: the filter low and its envelope short, little click; a slow glide
    mods={"WAVE/WAVE": "SIN", "FILTER/CUTOFF": 350, "FILTER/ENV": 600, "VOICE/GLIDE": 120, "VOICE/LENGTH": 400})
# lay here: an upright's bossa root and fifth (dotted quarter, eighth), the raised 7th leading
# back to the i
pack.bass("Lay Here Upright", "Upright", " | ".join([
    " ".join([N("1!", 6), N("5-", 2), N("1", 6), N("5-", 2)]),
    " ".join([N("5-!", 6), N("2-", 2), N("5-", 6), N("#7-", 2)])]),
    mods={"FILTER/CUTOFF": -3600, "ENVELOPE/RELEASE": 600})
# daffodil: a filtered finger bass holding each root and walking into the next chord
pack.bass("Daffodil Walk", "Finger bass", " | ".join([
    "7-! _ _ _ _ _ _ _ _ _ 7- _ 2 _ 3 _",
    "4! _ _ _ _ _ _ _ _ _ 4 _ 3 _ 2 _",
    "1! _ _ _ _ _ _ _ _ _ 1 _ 5- _ _ _",
    " ".join([N("1", 6), N("5-", 2), N("7-", 4), N("6-", 4)])]),
    # the "filtered-down electric bass"
    mods={"FILTER/CUTOFF": -4800, "ENVELOPE/RELEASE": 600})

# --- lead ---------------------------------------------------------------------------------------
# smoke: an alto sax in the background, rising to the octave over the i, then the same falling
# figure over the IV (to its third, B natural) and the iv (to B flat)
pack.lead("Smoke Alto", "Alto sax", " | ".join([
    " ".join([R(6), N("5", 2), N("7", 2), N("1+!", 6)]),
    " ".join([R(2), N("2+", 4), N("1+", 2), N("#6", 8)]),
    " ".join([R(2), N("1+", 4), N("7", 2), N("6", 8)]),
    " ".join([N("5", 6), R(2), N("2", 6), R(2)])]),
    mods={"FILTER/CUTOFF": -4200, "ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 1200, "MOTION/VIBRATO": 20})
# lay here: a tenor answering late in the bar: down to the third over the i, the V's raised
# 7th (its third) resolving to the root
pack.lead("Lay Here Tenor", "Tenor sax", " | ".join([
    " ".join([R(8), N("5!", 2), N("4", 2), N("3", 4)]),
    " ".join([N("#7-", 6), N("2", 2), N("1", 6), R(2)])]),
    mods={"FILTER/CUTOFF": -4200, "ENVELOPE/ATTACK": 1800, "ENVELOPE/RELEASE": 1200})
# daffodil: long alto tones between the chords: the VII's ninth, the iv's third, the i's third
# held, then a falling answer
pack.lead("Daffodil Alto", "Alto sax", " | ".join([
    " ".join([R(4), N("2!", 6), N("3", 2), N("5", 4)]),
    " ".join([N("6", 8), R(4), N("5", 2), N("4", 2)]),
    " ".join([N("3", 10), R(6)]),
    " ".join([R(8), N("1+", 2), N("7", 2), N("5", 4)])]),
    mods={"FILTER/CUTOFF": -4800, "ENVELOPE/ATTACK": 3600, "ENVELOPE/RELEASE": 2400})

# --- chords -------------------------------------------------------------------------------------
# chromatic voicings, semitones from the key's root, so the Dorian IV and the V7 can sound:
# i9 (D F A C E), IV9 (G B F A), iv9 (G Bb F A), VImaj7 (Bb D F A), VIIadd9 (C E G D),
# i7 (D F A C), V7 (A C# E G), i11 (D G C F)
PIIG = {"i9": ("c", [0, 3, 7, 10, 14]), "IV9": ("c", [-7, -3, 3, 7]), "iv9": ("c", [-7, -4, 3, 7]),
        "VI7": ("c", [-4, 0, 3, 7]), "VII9": ("c", [-2, 2, 5, 12]), "i7": ("c", [0, 3, 7, 10]),
        "V7": ("c", [-5, -1, 2, 5]), "i11": ("c", [0, 5, 10, 15]),
        "iv9low": ("c", [-7, -4, 0, 3, 7])}
# smoke: soft Rhodes, each chord a sixteenth late with a pushed re-hit; VI and VII share bar four
pack.chords("Smoke Rhodes", "Rhodes", " | ".join(
    [" ".join([R(1), C("@" + c, 11), R(1), C("@" + c, 2), R(1)]) for c in ["i9", "IV9", "iv9"]]
    + [" ".join([R(1), C("@VI7", 7), C("@VII9", 7), R(1)])]), PIIG,
    mods={"FILTER/CUTOFF": -5400, "ENVELOPE/RELEASE": 1200, "MOTION/CHORUS": 400})
# lay here: a jazz guitar comping in the bossa's eighths
pack.chords("Lay Here Guitar", "Jazz guitar", " | ".join(
    " ".join([C("@" + c, 2, 2), C("@" + c, 2, 4), C("@" + c, 2, 2), C("@" + c, 2)])
    for c in ["i7", "V7"]), PIIG,
    mods={"FILTER/CUTOFF": -4800, "ENVELOPE/RELEASE": 600, "MOTION/CHORUS": 200})
# daffodil: a lo-fi piano laying each chord late and touching it again; the i turns to i11
pack.chords("Daffodil Keys", "Upright piano", " | ".join(
    " ".join([R(1), C("@" + c, 7), R(1), C("@" + c, 5), R(2)]) for c in ["VII9", "iv9low", "i9", "i11"]), PIIG,
    # a felted piano: the hammer softened, the notes left to ring
    mods={"FILTER/CUTOFF": -4800, "ENVELOPE/ATTACK": 4800, "ENVELOPE/RELEASE": 1200})

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(79, "D", "Natural Minor", swing=58, phaser=0.15, echo=0.25, heavy=0.3,
              about="Biig Piig's 24K: D minor at 79 BPM with the lazy MPC swing, a lo-fi wobble and echo.")

if __name__ == "__main__":
    pack.done()
