#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret classical pack: five pattern presets for each of the drums, the bass, the lead
# and the chords, laid out as a USB stick holds them (see ../patternkit.py and the jazz pack):
#
#     ravving/presets/<drums|bass|lead|chords>/patterns/Classical · <name>.json
#
# Written in scale degrees for a MAJOR key. The quotes are public domain (Bach's C major
# prelude BWV 846, the Air's bass BWV 1068, Pachelbel's ground, Beethoven's Ode to Joy); the
# rest is idiomatic: Alberti bass, the lament bass, the Prinner, the circle of fifths, a
# chorale cadence in four voices, the waltz's oom-pah-pah. The waltz trio is in 3/4: three
# 16-step bars hold four 12-step waltz bars, so drums, bass and chords loop together.
#   python3 tools/packs/classical.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/classical/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "classical")
sys.path.insert(0, HERE)
from patternkit import MAJOR, Pack, N, C, R  # noqa: E402

pack = Pack("Classical", PACK, MAJOR)

# --- drums: the orchestra's percussion, as an orchestra writes it ------------------------------
# All five play the "Orchestra" kit (kits.json), whose rows are: KICK concert bass drum, SNARE
# concert (field) snare, TOM timpani on C, HAT timpani on G (the dominant below), OPEN
# triangle, CYMBAL concert crash (clash cymbals), PERC tambourine, CLAP castanets. The timpani
# are tuned for a key of C: a drum kit does not follow the session's key.

# a Viennese waltz in 3/4 (12 steps a bar, four bars in three, under I – IV – V – I): timpani
# on the downbeats of I (C) and V (G), the triangle on the "pah-pah", bass drum and cymbals
# together on the first downbeat, a snare roll lifting into the next phrase
pack.drums("Waltz", "ORCHESTRA", {
    "KICK":   "X........... ............ x........... ............",
    "TOM":    "x........... ............ ............ x...........",
    "HAT":    "............ ............ x........... ............",
    "OPEN":   "....x...x... ....x...x... ....x...x... ....x.......",
    "SNARE":  "............ ............ ............ ........xxxx",
    "CYMBAL": "X........... ............ ............ ............",
})
# an orchestral march in 2/4: the field snare's rudiments (flams on the beats, a closing
# roll), bass drum and clash cymbals together on the strong beats, the timpani's tonic and
# dominant under them
pack.drums("March", "ORCHESTRA", {
    "SNARE":  "X.xx x.x. X.xx x.x. | X.xx x.xx X.xx xxxx",
    "KICK":   "x... .... x... .... | x... .... x... ....",
    "CYMBAL": "x... .... x... .... | x... .... x... ....",
    "TOM":    "x... .... .... .... | x... .... .... ....",
    "HAT":    ".... .... x... .... | .... .... x... ....",
})
# Offenbach's galop (the can-can): the snare's "ta-ta-ta" on every beat, the bass drum's
# "oom" and the cymbals' "pah", the triangle on top, a stop-time ending on V – I
pack.drums("Galop", "ORCHESTRA", {
    "SNARE":  "x.xx x.xx x.xx x.xx | x.xx x.xx X.X. X...",
    "KICK":   "X... .... x... .... | X... .... .... ....",
    "CYMBAL": ".... x... .... x... | .... x... X... X...",
    "OPEN":   "x.x. x.x. x.x. x.x. | x.x. x.x. .... ....",
    "HAT":    ".... .... .... .... | .... .... X... ....",
    "TOM":    ".... .... .... .... | .... .... .... X...",
})
# the habanera (Bizet, Carmen): dotted eighth, sixteenth, two eighths on the castanets, the
# tambourine on each 2/4 bar's second beat, the timpani's tonic then dominant
pack.drums("Habanera", "ORCHESTRA", {
    "CLAP": "x..xx.x. x..xx.x. | x..xx.x. x..xx.x.",
    "PERC": "....x... ....x... | ....x... ....x...",
    "TOM":  "x....... ........ | ........ ........",
    "HAT":  "........ ........ | x....... ........",
})
# a maestoso cadence: the timpani alternating tonic and dominant, then rolling on the
# dominant into the final tonic stroke with the bass drum and the cymbals (V – I)
pack.drums("Timpani Cadence", "ORCHESTRA", {
    "TOM":    "X... .... x... .... | x... .... x... .... | .... .... x... .... | .... .... .... X...",
    "HAT":    ".... .... .... x... | .... x... .... .... | x... .... .... x... | xxxx xxxx xxxx ....",
    "KICK":   "X... .... .... .... | .... .... .... .... | .... .... .... .... | .... .... .... X...",
    "CYMBAL": ".... .... .... .... | .... .... .... .... | .... .... .... .... | .... .... .... X...",
})

# --- bass ---------------------------------------------------------------------------------------
I_, IV64, V65 = "1 _ 5 _ 3 _ 5 _", "1 _ 6 _ 4 _ 6 _", "7- _ 5 _ 4 _ 5 _"
# Alberti bass (low–high–middle–high in eighths) over I | IV6/4 I | V6/5 I | IV6/4 V6/5, the
# way a Classical sonata's left hand keeps the harmony moving
pack.bass("Alberti Bass", "Cello", " | ".join([
    "1! _ 5 _ 3 _ 5 _ " + I_, "1! _ 6 _ 4 _ 6 _ " + I_, "7-! _ 5 _ 4 _ 5 _ " + I_, "1! _ 6 _ 4 _ 6 _ " + V65]))
# Pachelbel's ground: the eight quarter notes the canon repeats 28 times
pack.bass("Pachelbel Ground", "Cello", " ".join([
    N("1!", 4), N("5-", 4), N("6-", 4), N("3-", 4), N("4-!", 4), N("1-", 4), N("4-", 4), N("5-", 4)]))
# the lament bass (passus duriusculus): the tonic sliding down by semitones to the dominant in
# half notes, then IV – ii – V home
pack.bass("Lament Bass", "Contrabass", " ".join([
    N("1!", 8), N("7-", 8), N("b7-", 8), N("6-", 8), N("b6-", 8), N("5-", 8), N("4-", 4), N("2-", 4), N("5-!", 8)]))
# the waltz's "oom": the root on the downbeat of each 3/4 bar (I, IV, V, I), the chords
# take the "pah-pah"
pack.bass("Waltz Oom", "Upright", " ".join([
    N("1!", 4), R(8), N("4-", 4), R(8), N("5-!", 4), R(8), N("1-", 4), R(8)]))
# a Baroque continuo in octave-leaping eighths stepping down the scale (after the Air,
# BWV 1068), turning on the dominant
pack.bass("Octave Continuo", "Contrabass", " ".join(
    [N(n, 2) for n in ["1!", "1+", "7-", "7", "6-", "6", "5-", "5", "4-!", "4", "3-", "3", "2-", "2", "5-", "5"]]))

# --- lead ---------------------------------------------------------------------------------------
def prelude(a, b, c, d, e):
    figure = [a, b, c, d, e, c, d, e]
    return " ".join([figure[0] + "!"] + figure[1:] + figure)


# Bach's C major prelude (BWV 846), bars 1–3 and 5: one broken chord a bar, in sixteenths
pack.lead("Prelude Arpeggio", "Harpsichord", " | ".join([
    prelude("1", "3", "5", "1+", "3+"), prelude("1", "2", "6", "2+", "4+"),
    prelude("7-", "2", "5", "2+", "4+"), prelude("1", "3", "6", "3+", "6+")]))
# a Classical period's first phrase: rising to the octave, stepping down, ending on a half
# cadence (the 2 over V)
pack.lead("Classical Phrase", "Violin", " | ".join([
    " ".join([N("5!", 4), N("3", 2), N("4", 2), N("5", 4), N("1+", 4)]),
    " ".join([N("7", 2), N("6", 2), N("5", 2), N("4", 2), N("3", 4), R(4)]),
    " ".join([N("4!", 4), N("6", 2), N("5", 2), N("4", 4), N("2", 4)]),
    " ".join([N("1", 2), N("7-", 2), N("1", 2), N("3", 2), N("2", 6), R(2)])]))
# Beethoven's Ode to Joy, the first four bars
pack.lead("Ode Theme", "Oboe", " | ".join([
    " ".join(N(n, 3, 1) for n in ["3!", "3", "4", "5"]),
    " ".join(N(n, 3, 1) for n in ["5!", "4", "3", "2"]),
    " ".join(N(n, 3, 1) for n in ["1!", "1", "2", "3"]),
    " ".join([N("3!", 6), N("2", 2), N("2", 7, 1)])]))
# a Baroque descending sequence: a turning figure in sixteenths, a step lower each beat
pack.lead("Baroque Sequence", "Flute",
          "3+! 2+ 3+ 1+ 2+ 1+ 2+ 7 1+ 7 1+ 6 7 6 7 5 | 6! 5 6 4 5 4 5 3 4 3 2 3 1 _ 5 7")
# a trumpet fanfare: dotted triad calls rising to the octave
pack.lead("Fanfare", "Trumpet", " | ".join([
    "1! _ _ 1 3 _ _ 3 5! _ _ _ 3 _ 5 _",
    "1+! _ _ _ _ _ 5 _ 3 _ 5 _ 1 _ _ ."]))

# --- chords: written in scale degrees (x), so each is the triad the period wants whatever the
# CHORD SET, voiced with the voice leading of the style ------------------------------------
# a four-part chorale (SATB, bass included): I vi | IV ii6 | I6/4 V7 | I, every voice moving
# by step or held, the 7th of V7 resolving down
CHORALE = {"I": ("x", [0, 4, 7, 9]), "vi": ("x", [-2, 5, 7, 9]), "IV": ("x", [-4, 5, 7, 10]),
           "ii6": ("x", [-4, 5, 8, 10]), "I64": ("x", [-3, 4, 7, 9]), "V7": ("x", [-3, 3, 6, 8]),
           "Iend": ("x", [0, 2, 7, 9])}
pack.chords("Chorale Cadence", "Choir", " ".join([
    C("@I", 8), C("@vi", 8), C("@IV", 8), C("@ii6", 8), C("@I64", 8), C("@V7", 8), C("@Iend", 15, 1)]), CHORALE, ties="all")
# Pachelbel's eight chords (I V vi iii IV I IV V), a quarter each, the upper voices stepping
# down as in the canon
CANON = {"I": ("x", [9, 11, 14]), "V": ("x", [8, 11, 13]), "vi": ("x", [7, 9, 12]), "iii": ("x", [6, 9, 11]),
         "IV": ("x", [5, 7, 10]), "I2": ("x", [4, 7, 9]), "V2": ("x", [6, 8, 11])}
pack.chords("Pachelbel Progression", "Strings · Ensemble", " ".join(
    C("@" + c, 4) for c in ["I", "V", "vi", "iii", "IV", "I2", "IV", "V2"]), CANON)
# the waltz's "pah-pah" on beats two and three (3/4, four bars in three): I IV6/4 V7 I
WALTZ = {"I": ("x", [7, 9, 11]), "IV": ("x", [7, 10, 12]), "V7": ("x", [6, 8, 10, 11])}
pack.chords("Waltz Pah-Pah", "Pizzicato strings", " ".join(
    " ".join([R(4), C("@" + c, 3, 1), C("@" + c, 3, 1)]) for c in ["I", "IV", "V7", "I"]), WALTZ)
# the Prinner (IV – I6 – vii°6 – I): the galant schema's soprano 6-5-4-3 over a bass 4-3-2-1,
# in repeated eighths like a Classical string accompaniment
PRINNER = {"IV": ("x", [3, 7, 12]), "I6": ("x", [2, 7, 11]), "vii6": ("x", [1, 6, 10]), "I": ("x", [0, 7, 9])}
pack.chords("Prinner Pulse", "Strings · Bowed", " ".join(
    " ".join([C("@" + c, 1, 1)] * 4) for c in ["IV", "I6", "vii6", "I"]), PRINNER)
# the circle of fifths down the key in half notes (I IV vii° iii vi ii V I), the Baroque
# sequence, on the harpsichord
CIRCLE = {"I": ("x", [0, 7, 9, 11]), "IV": ("x", [-4, 7, 10, 12]), "vii": ("x", [-1, 6, 8, 10]),
          "iii": ("x", [-5, 6, 9, 11]), "vi": ("x", [-2, 7, 9, 12]), "ii": ("x", [1, 8, 10, 12]),
          "V": ("x", [-3, 6, 8, 11])}
pack.chords("Circle of Fifths", "Harpsichord", " ".join(
    C("@" + c, 8) for c in ["I", "IV", "vii", "iii", "vi", "ii", "V", "I"]), CIRCLE)

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(100, "C", "Major", echo=0.2,
              about="A concert hall: C major (the timpani are tuned to C and G), moderato, straight; a little echo for the room, nothing squashed.")

if __name__ == "__main__":
    pack.done()
