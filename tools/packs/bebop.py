#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret "Bebop" pack (the first Solos pack, kept when Solos became ballads, 2026-10-12): six horn solos for the LEAD machine in the styles of Charlie Parker
# (alto), John Coltrane (tenor, soprano) and Chet Baker (trumpet), each with the chords, the
# bass and the drums it is heard over (six of each, see ../patternkit.py). Written in scale
# degrees for a MAJOR key, made for Bb major (the horn key): the lead's degree 1 is Bb4, "-"
# the octave under it, so the alto plays "1-".."7", the tenor "5-".."4", the soprano "1".."4+",
# the trumpet "6-".."7".
#
# Nothing is quoted (their recorded solos and compositions are copyrighted): the vocabulary was
# studied (tools/genre-research/bebop.md) and every line, progression and rhythm here is
# original. Parker: eighth-note lines on the chord tones with chromatic approach notes and
# enclosures, the off-beats leaned on (@ +8), the approach notes snapped in early (<8), the
# blue 3rd scooped (~), a breath between phrases. Coltrane: the Countdown reharm of a ii–V–I
# run through in sixteenth 1-2-3-5 cells (sheets of sound), and a modal vamp with pentatonic
# cells, stacked fourths and repeated cries. Baker: few notes, long, soft (@62–84), all behind
# the beat (>8–14), a scoop, air.
#   python3 tools/packs/bebop.py

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/bebop/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "bebop")
sys.path.insert(0, HERE)
from patternkit import MAJOR, Pack, N, C, R  # noqa: E402

pack = Pack("Bebop", PACK, MAJOR)


def bar(text):
    """One bar's tokens, checked to be sixteen (a miscount is the usual slip)."""
    tokens = text.split()
    if len(tokens) != 16:
        raise ValueError(f"{len(tokens)} tokens in bar: {text!r}")
    return text


def ph(text, bars, base=None, lean=0):
    """A phrase: tokens `note[/steps]` or `.[/steps]`, an eighth (2 steps) unless `/steps`
    says; a note without its own @velocity gets `base`, plus `lean` when it starts on an
    off-beat eighth (bebop's upbeat accent). Checked to fill `bars` bars."""
    out, at = [], 0
    for token in text.split():
        head, _, steps = token.partition("/")
        steps = int(steps) if steps else 2
        if head == ".":
            out.append(R(steps))
        else:
            m = re.fullmatch(r"([^@<>]+)(@\d+)?([<>]\d+)?", head)
            if not m:
                raise ValueError(f"bad token {token!r}")
            note, velocity, nudge = m.groups()
            if velocity is None and base is not None:
                velocity = f"@{base + (lean if at % 4 == 2 else 0)}"
            out.append(N(note + (velocity or "") + (nudge or ""), steps))
        at += steps
    if at != bars * 16:
        raise ValueError(f"{at} steps, not {bars} bars: {text[:40]!r}")
    return " ".join(out)


def walk(*beats):
    """A walking bar: four quarters (a token each, `note@velocity`), each held three steps."""
    if len(beats) != 4:
        raise ValueError(f"{len(beats)} beats in a walking bar")
    return " ".join(N(b, 3, 1) for b in beats)


# --- drums --------------------------------------------------------------------------------------
# Bird's tempo: the ride's "ding, ding-a ding, ding-a" (2 and 4 leaned on), the hi-hat foot on
# 2 and 4, the snare chattering between, the kick dropping bombs on the off-beats
pack.drums("Bird Bop", "JAZZ", {
    "CYMBAL": "x...X.x.x...X.x. | x...X.x.x...X.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "SNARE":  "..x.......x..... | ......x....x..x.",
    "KICK":   "..............x. | ......x.......x.",
})
# a medium bop blues: the ride even, the foot, the snare taking 2 and 4 with a ghost, the kick
# on 1 and 3, a tom turning the second bar
pack.drums("Bird Blues Swing", "JAZZ", {
    "CYMBAL": "x...x.x.x...x.x. | x...x.x.x...x.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "SNARE":  "....x.....x.x... | ....x.......x...",
    "KICK":   "x.......x....... | x.......x.......",
    "TOM":    "................ | ..........x...x.",
})
# the drive under the sheets (Philly Joe's): the ride in eighths, the foot, the snare's
# off-beat accents, a snare roll into the loop
pack.drums("Trane Drive", "JAZZ", {
    "CYMBAL": "X.x.x.x.X.x.x.x. | X.x.x.x.X.x.x.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "SNARE":  "...x...x...x..x. | ...x...x....xxxx",
    "KICK":   "x.......x....... | x...............",
})
# Elvin's polyrhythm under the modal vamp: the ride, the toms rolling every three steps and
# the kick every six against the four, the snare cracking
pack.drums("Elvin Fourths", "JAZZ", {
    "CYMBAL": "x...X.x.x...X.x. | x...X.x.x...X.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "TOM":    "...x..x..x..x..x | ..x..x..x..x..x.",
    "KICK":   "x.....x.....x... | ..x.....x.....x.",
    "SNARE":  "....X.......x..x | ....x..X....x...",
})
# a ballad with brushes: the snare swept in eighths, the foot on 2 and 4, the kick once a
# bar, the ride touched on 3 of the second bar
pack.drums("Baker Brushes", "BRUSH_RIDE", {
    "SNARE":  "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "KICK":   "x............... | x...............",
    "CYMBAL": "................ | ........x.......",
})
# the cool two-feel: brushes on the ride, the foot, the kick on 1 and 3, a snare touch
# closing the second bar
pack.drums("Cool Two-Feel", "BRUSH_RIDE", {
    "CYMBAL": "x...x.x.x...x.x. | x...x.x.x...x.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "KICK":   "x.......x....... | x.......x.......",
    "SNARE":  "................ | ............x...",
})

# --- bass (degree 1 is Bb2; "-" the octave under) ----------------------------------------------
# walking the rhythm changes (I VI7 | ii7 V7 | I VI7 | ii7 V7 | I I7 | IV7 #iv°7 | iii7 VI7 |
# ii7 V7): chord tones on the beats, a chromatic step into each change, 2 and 4 leaned on
def w(a, b, c, d):
    return walk(f"{a}@100", f"{b}@106", f"{c}@100", f"{d}@106")
pack.bass("Bird Walk", "Upright", " | ".join([
    w("1", "3", "6-", "b2"), w("2", "3", "4", "5-"), w("1", "2", "3", "b3"), w("2", "1", "7-", "5-"),
    w("1", "3", "5", "b7"), w("4", "b3", "#4-", "6-"), w("3", "7-", "6-", "5-"), w("2", "4-", "5-", "7-")]))
# walking the bop blues (I7 | IV7 | I7 | v7 I7 | IV7 | #iv°7 | I7 vi7 | ii7 V7), a ghosted skip
# on the last beat of bars 4 and 8
def skip(a, b, c, d):
    return " ".join([N(f"{a}@100", 3, 1), N(f"{b}@106", 3, 1), N(f"{c}@100", 3, 1), N(f"{d}@106", 3), N(f"{d}@66", 1)])
pack.bass("Bird Blues Walk", "Upright", " | ".join([
    w("1", "3", "5", "#4"), w("4", "6-", "b7-", "7-"), w("1", "7-", "6-", "#4-"), skip("5-", "4-", "1", "3"),
    w("4", "6-", "b7-", "5-"), w("#4-", "6-", "1", "7-"), w("1", "b7-", "6-", "b2"), skip("2", "6-", "5-", "7-")]))
# walking the Countdown reharm (ii7 bII7 | bVImaj7 VII7 | IIImaj7 V7 | Imaj7): a root a half
# bar, the fifth or a chromatic step into the next
pack.bass("Countdown Walk", "Upright", " | ".join([
    w("2", "4", "b3", "b7-"), w("b6-", "b3", "7-", "#4-"), w("3", "7-", "5-", "2"), w("1", "5-", "3", "b3")]))
# the pedal under the modal vamp (Garrison's): the ii's root held on 1, its fifth on 3, a push
# on the "and" of 4; the V7sus bars on the F; the last bar walks back through A and B
pedal = lambda root, fifth: " ".join([N(f"{root}!@104", 6), R(2), N(f"{fifth}@96", 4), N(f"{root}@92", 2), R(2)])  # noqa: E731
pack.bass("Garrison Pedal", "Upright", " | ".join([
    pedal("2-", "6-"), pedal("2-", "6-"), pedal("2-", "6-"), pedal("2-", "6-"),
    pedal("5-", "2-"), pedal("5-", "2-"), pedal("2-", "6-"),
    " ".join([N("2-!@104", 4), R(4), N("6-@96", 4), N("7-@92", 2), N("b2-@96", 2)])]))
# a ballad in half notes (I vi ii V | iii VI ii V): the root, then the fifth or the third, each
# a little late, the last bar stepping up into the I
def half(a, b, c=None):
    return " ".join([N(f"{a}@92>6", 8), N(f"{b}@84>6", 8 if c is None else 4)] + ([N(f"{c}@88>6", 4)] if c else []))
pack.bass("Ballad Two", "Acoustic bass", " | ".join([
    half("1!", "5-"), half("6-", "3"), half("2", "6-"), half("5-", "7-"),
    half("3", "7-"), half("6-", "b2"), half("2", "4"), half("5-", "6-", "7-")]))
# the cool two-feel (I | ii V | iii vi | ii V | IV | iv bVII | iii VI | ii V): half notes with
# an eighth pickup into each change, the last bar walking
def two(a, b, pick=None):
    return " ".join([N(f"{a}@100", 8), N(f"{b}@92", 8 if pick is None else 6)] + ([N(f"{pick}@80", 2)] if pick else []))
pack.bass("Cool Two-Beat", "Acoustic bass", " | ".join([
    two("1!", "5-", "b2"), two("2", "5-"), two("3", "6-", "5-"), two("2", "5-", "3"),
    two("4!", "1", "b7-"), two("4", "b7-", "b3"), two("3", "6-", "5-"), w("2", "3", "5-", "7-")]))

# --- lead: the six solos (degree 1 is Bb4; "-" the octave under, "+" the one over) ------------
# Parker over the rhythm changes, fast: eighth-note lines on the chord tones, the off-beats
# louder, the chromatic approaches (B into C, Db into D, E into Eb) snapped in early, a breath
# before each phrase; the alto between Bb3 and A5
pack.lead("Bird Changes", "Alto sax", " ".join([
    ph(". 3 5 6 1+! 7 6 #1<8", 1, 100, 8),            # I VI7: up the Bb6, G7's third
    ph("2 4 6 1+ 7 5 #4<8 4", 1, 100, 8),             # ii7 V7: Cm7 up, F7's bebop scale down
    ph("3!/3 ./1 . 1 2 b3<8 2 #1<8", 1, 100, 8),      # I VI7: a jab, the blue Db, B into C
    ph("2 4 b6<8 6 5 4 3 b3<8", 1, 100, 8),           # ii7 V7: an enclosure of G, down to Db
    ph("3!/3 ./1 . 1+ 7 b7 6 5", 1, 100, 8),          # I I7: Bb7's bebop scale down
    ph("4 6 b7 1+ . #4<8 6 b3", 1, 100, 8),           # IV7 #iv°7: Eb7, then E°7's tones
    ph("3 5 7! 6 5 3 #1<8 2", 1, 100, 8),             # iii7 VI7: Dm7 up, G7's third into C
    ph("2 4 6 5 #4<8 4 . .", 1, 100, 8)]),            # ii7 V7: the turnaround, a breath
    mods={"MOTION/VIBRATO": 24})
# Parker on a bop blues, medium-up: the blue 3rd scooped into the 3rd, the b7 and the b5 as
# passing tones, a motif stated then displaced a beat later, the turnaround falling F E Eb (D)
pack.lead("Bird Blues", "Alto sax", " ".join([
    ph(". b3~ 3!/4 . 1 2 b3", 1, 98, 8),              # I7: the scoop into the 3rd
    ph("4! . 6 b7 6 4 3 b3<8", 1, 98, 8),             # IV7: Eb7's tones, Db leading down
    ph("2 1 . 1+! b7 6 5 #4<8", 1, 98, 8),            # I7: the b5 into F
    ph("5 b7 1+ b7 5 3 . .", 1, 98, 8),               # v7 I7: Fm7's shape, a breath
    ph(". . 4 6 b7 6 4 b3", 1, 98, 8),                # IV7: the bar-2 motif a beat later
    ph(". #4<8 6 1+! 6 #4 3 b3<8", 1, 98, 8),         # #iv°7: E G Bb, falling to Db
    ph("3!/3 ./1 1 3 5 b7 6 5", 1, 98, 8),            # I7 vi7: D held, Bb7 up, Gm7 down
    ph("4 2 7- 1 . 5-@92 #4-<8 4-", 1, 98, 8)]),      # ii7 V7: F E Eb into the scoop
    mods={"MOTION/VIBRATO": 24})
# Coltrane's sheets of sound through the Countdown reharm (ii7 bII7 | bVImaj7 VII7 | IIImaj7
# V7 | Imaj7): the 1-2-3-5 cell up and its mirror down on every chord, in sixteenths, each run
# swelling to its top; the tenor between F3 and Eb5; the last bar lands and breathes
def cell(up, down, top=108, low=92):
    """Eight sixteenths: four up (swelling to `top`) and four down."""
    v = [low, 96, 102, top, 104, 98, 94, low]
    return " ".join(f"{n}@{v[k]}/1" for k, n in enumerate(up + down))
pack.lead("Trane Countdown", "Tenor sax · Bright", " ".join([
    ph(cell(["2-", "3-", "4-", "6-"], ["1", "6-", "4-", "3-"]) + " " +
       cell(["b3-", "4-", "5-", "b7-"], ["b2", "b7-", "5-", "4-"]), 1),       # Cm7, Db7
    ph(cell(["b6-", "b7-", "1", "b3"], ["1", "b7-", "b6-", "5-"]) + " " +
       cell(["#4", "#2", "b2", "7-"], ["6-", "#4-", "7-", "b2"], 110), 1),     # Gbmaj7, A7 (down first)
    ph(cell(["3-", "#4-", "#5-", "7-"], ["3", "7-", "#5-", "#4-"]) + " " +
       cell(["5-", "6-", "7-", "2"], ["4", "2", "7-", "5-"], 110), 1),         # Dmaj7, F7
    ph("3-!@110/4 1-@100/4 6-~@96 5-@94/4 ./2", 1)]),                          # Bbmaj7: lands, slides, breathes
    mods={"MOTION/VIBRATO": 12})
# Coltrane modal, the soprano: a vamp on the ii7 (C Dorian) with two bars of V7sus; pentatonic
# cells up and down, fourths stacked up to the Eb6, the cell transposed, the high note cried
# four times, the phrase settling on the C
pack.lead("Trane Fourths", "Soprano sax", " ".join([
    ph("2 4 5 6 1+! 6 5 4", 1, 100, 6),               # the pentatonic cell up and down
    ph("2!/4 ./4 5 1+ 4+!@112/4", 1, 100),            # a fourths climb to the Eb6
    ph("4+ 1+ 5 2 4+! 1+ 5 2", 1, 104),               # falling fourths, twice
    ph("2+!/3 ./1 1+ 6 5 4 2/4", 1, 100, 6),          # down the pentatonic to the C
    ph(". 5 6 1+ 2+! 1+ 6 5", 1, 100, 6),             # V7sus: the cell from the F
    ph("4+!@112 4+@100 4+@112 4+@96 . 2+ 1+ 6", 1, 100),  # the cry, four times
    ph("2 4 5 . 4 5 6 .", 1, 100, 6),                 # ii7: the cell, then a step up
    ph("1+ 6 5 4 2!/4 ./4", 1, 100, 6)]),             # home on the C, a breath
    mods={"MOTION/VIBRATO": 10})
# Baker's ballad (I | vi | ii | V | iii | VI | ii | V): long tones, soft, every one behind the
# beat, the trumpet between G3 and G5, a scoop up to the G, half a bar of air before the loop
pack.lead("Baker Ballad", "Trumpet · Cool", " ".join([
    ph("./4 3@72>12/8 2@68>10/4", 1),                 # Imaj7: the D, the C
    ph("1@70>12/6 ./2 7-@66>10/4 6-@64>10/4", 1),     # vi7: Bb, A, G
    ph("./2 5-~@68>8 6-@76>10/8 ./4", 1),             # ii7: a scoop F into G, held
    ph("4@72>10/6 3@68>8 2@66>10/4 7-@62>12/4", 1),   # V7: Eb D C A
    ph("./4 3@70>14/4 5@78>10/8", 1),                 # iii7: D, the F swelling
    ph("6@80>8/4 5@74>8 #1@70>6/6 . .", 1),           # VI7: G F, G7's third, air
    ph("2@72>12/6 4@70>8 3@68>10/4 2@66>10/4", 1),    # ii7: C Eb D C
    ph("7-@68>10/6 1-@64>12 ./8", 1)]),               # V7: A, Bb, half a bar of air
    mods={"FILTER/CUTOFF": -1200, "ENVELOPE/RELEASE": 600})
# Baker's cool medium swing (I | ii V | iii vi | ii V | IV | iv bVII | iii VI | ii V): a narrow
# sung line, few notes, each phrase behind the beat, the fourth bar's long F, the iv's Gb
pack.lead("Baker Cool", "Trumpet · Cool", " ".join([
    ph("./4 3@78>8 5@82>8 6@86>8/6 5@80>8", 1),       # Imaj7: D F G, F
    ph("4@80>8/6 3@76>8 2@74>8/4 . .", 1),            # ii7 V7: Eb D C, air
    ph("./2 3@78>8 5@82>8 6@84>8/4 7@88>8/4 6@80>8", 1),  # iii7 vi7: up to the A
    ph("5@82>8/8 4@76>8 3@74>8 2@72>8/4", 1),         # ii7 V7: the long F, down
    ph("./4 4@78>8 6@84>8 5@82>8/4 4@78>8/4", 1),     # IVmaj7: Eb G F Eb
    ph("b6@80>8/4 4@78>8 b3@76>8/6 ./4", 1),          # iv7 bVII7: Gb Eb Db
    ph("./2 3@78>8 5@82>8 6@84>8/4 #1@80>8/6", 1),    # iii7 VI7: D F G, G7's B held
    ph("2@78>8/6 7-@74>8 1-@72>8/4 ./4", 1)]),        # ii7 V7: C A Bb, air
    mods={"FILTER/CUTOFF": -1200, "ENVELOPE/RELEASE": 600})

# --- chords: rootless jazz voicings, semitones from the key's root (Bb); A and B forms of a
# chord so a re-hit is struck, not merged ------------------------------------------------------
V = {
    "Imaj7": ("c", [4, 7, 11, 14]), "Imaj7B": ("c", [-1, 2, 4, 7]), "I6": ("c", [4, 7, 9, 14]),
    "I7": ("c", [4, 7, 10, 14]), "I7B": ("c", [-2, 2, 4, 7]),
    "VI7": ("c", [1, 4, 7, 10]), "VI7B": ("c", [-5, -2, 1, 4]),               # G7b9: B D F Ab
    "ii7": ("c", [5, 9, 12, 16]), "ii7B": ("c", [0, 4, 5, 9]),                 # Cm7: Eb G Bb D
    "V7": ("c", [-1, 2, 5, 9]), "V7b9": ("c", [-1, 2, 5, 8]), "V7B": ("c", [5, 9, 11, 14]),  # F7
    "IV7": ("c", [-3, 0, 3, 7]), "IVmaj7": ("c", [-3, 0, 4, 7]), "IVmaj7B": ("c", [4, 7, 9, 12]),
    "#iv°7": ("c", [-6, -3, 0, 3]),                                            # E G Bb Db
    "iii7": ("c", [2, 6, 7, 11]), "vi7": ("c", [0, 4, 7, 11]), "vi7B": ("c", [-5, -1, 0, 4]),
    "v7": ("c", [-2, 2, 5, 9]), "iv7": ("c", [-4, 0, 3, 7]), "bVII7": ("c", [2, 5, 8, 12]),
    "bII7": ("c", [-5, -2, 1, 5]), "bVImaj7": ("c", [0, 3, 7, 10]),            # Db7, Gbmaj7
    "VII7": ("c", [3, 6, 9, 13]), "IIImaj7": ("c", [-4, -1, 3, 6]),            # A7, Dmaj7
    "Q1": ("c", [2, 7, 12, 17]), "Q2": ("c", [4, 9, 14, 19]), "Q3": ("c", [-3, 2, 7, 12]),  # fourths on C Dorian
    "QS": ("c", [-5, 0, 5, 9]),                                                # F Bb Eb G: the V7sus
}
RHYTHM = [("Imaj7", "VI7"), ("ii7", "V7"), ("Imaj7B", "VI7B"), ("ii7B", "V7b9"),
          ("I6", "I7"), ("IV7", "#iv°7"), ("iii7", "VI7"), ("ii7", "V7")]
# comping the rhythm changes: each chord on its beat and the "and" after it, the even bars
# pushed to the "and" of 1 (Red Garland's way)
def charleston(a, b, pushed):
    if pushed:
        return bar(" ".join([R(2), C("@" + a, 2, 2), C("@" + a, 2), C("@" + b, 2, 4), C("@" + b, 2)]))
    return bar(" ".join([C("@" + a, 2, 4), C("@" + a, 2), C("@" + b, 2, 4), C("@" + b, 2)]))
pack.chords("Bird Changes Comp", "Grand piano", " | ".join(
    charleston(a, b, k % 2 == 1) for k, (a, b) in enumerate(RHYTHM)), V)
# comping the bop blues on the "and"s, the forms alternating
BLUES = [("I7", "I7B"), ("IV7", "IV7"), ("I7", "I7B"), ("v7", "I7"), ("IV7", "IV7"), ("#iv°7", "#iv°7"),
         ("I7", "vi7"), ("ii7", "V7b9")]
pack.chords("Bird Blues Comp", "Grand piano", " | ".join(
    bar(" ".join([R(2), C("@" + a, 2, 2), C("@" + a, 2, 2), C("@" + b, 2, 2), C("@" + b, 2)])) for a, b in BLUES), V)
# the Countdown reharm, a chord a half bar: struck on the beat, held, and again on the "and"
# of 2; the Imaj7 bar held, then its sixth
pack.chords("Countdown Comp", "Grand piano", " | ".join([
    bar(" ".join([C("@ii7", 3, 3), C("@ii7", 2), C("@bII7", 3, 3), C("@bII7", 2)])),
    bar(" ".join([C("@bVImaj7", 3, 3), C("@bVImaj7", 2), C("@VII7", 3, 3), C("@VII7", 2)])),
    bar(" ".join([C("@IIImaj7", 3, 3), C("@IIImaj7", 2), C("@V7", 3, 3), C("@V7b9", 2)])),
    bar(" ".join([C("@Imaj7", 6, 2), C("@I6", 4, 4)]))]), V)
# the quartal vamp (McCoy's): the fourths stabs on 1 (held), on the "and" of 2 and on 4, and a
# sixteenth push before the next bar (in another form than its downbeat, so it is struck, not
# merged); the voicings climbing, the V7sus bars on the F
def stabs(a, b, c, push):
    return bar(" ".join([C("@" + a, 4, 2), C("@" + b, 2, 4), C("@" + c, 2, 1), C("@" + push, 1)]))
pack.chords("Fourths Vamp", "Grand piano", " | ".join([
    stabs("Q1", "Q2", "Q1", "Q2"), stabs("Q3", "Q1", "Q2", "Q3"), stabs("Q1", "Q2", "Q3", "Q1"), stabs("Q2", "Q3", "Q1", "Q3"),
    stabs("QS", "Q1", "QS", "Q1"), stabs("QS", "Q3", "Q1", "Q3"), stabs("Q1", "Q2", "Q1", "Q2"), stabs("Q3", "Q1", "Q2", "Q3")]), V)
# the ballad's pads (I vi ii V | iii VI ii V): each chord held the bar, touched again on 3 in
# its other form where it has one
def pad(a, b=None):
    return bar(" ".join([C("@" + a, 8), C("@" + b, 7, 1)]) if b else C("@" + a, 15, 1))
pack.chords("Ballad Pads", "Upright piano", " | ".join([
    pad("Imaj7", "Imaj7B"), pad("vi7", "vi7B"), pad("ii7", "ii7B"), pad("V7", "V7b9"),
    pad("iii7"), pad("VI7", "VI7B"), pad("ii7B", "ii7"), pad("V7B", "V7")]), V)
# the cool comp on the guitar: short chords on 2 and 4, a push on the "and" of 4 into each
# change
def cool(a, b=None):
    b = b or a
    return bar(" ".join([R(4), C("@" + a, 1, 7), C("@" + b, 1, 1), C("@" + b, 2)]))
pack.chords("Cool Comp", "Jazz guitar", " | ".join([
    cool("Imaj7", "Imaj7B"), cool("ii7", "V7"), cool("iii7", "vi7"), cool("ii7B", "V7b9"),
    cool("IVmaj7", "IVmaj7B"), cool("iv7", "bVII7"), cool("iii7", "VI7"), cool("ii7", "V7")]), V)

# the templates: how a project plays these best (the projects dialog's TEMPLATES): the bop
# tempo with swung eighths, and the ballad
pack.template(160, "Bb", "Major", swing=62, swing_eighths=True, echo=0.15,
              about="Horn solos in Bb major: bebop at 160 with swung eighths, a little room.")
pack.template(64, "Bb", "Major", name="Bebop · Ballad", swing=58, swing_eighths=True, echo=0.3,
              about="The Baker-style ballad: slow, swung eighths, a trumpet in a warm room.")

if __name__ == "__main__":
    pack.done()
