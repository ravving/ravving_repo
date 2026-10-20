#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret folk pack: five pattern presets for each of the drums, the bass, the lead and the
# chords (see ../patternkit.py). Written in scale degrees for a MAJOR key (made for G major, as
# Dylan, Neil Young and the Pogues play), the modal songs on the scale's own degrees: degree 2 is
# the Dorian (Scarborough Fair, Drunken Sailor, Matty Groves: A Dorian in G major), degree 6 the
# Aeolian. The chords are the songs' (Ultimate Guitar's chord sheets, see the README); the lines
# are original, except the traditional tunes, which are public domain.
#
# The 6/8 jigs and the 3/4 waltzes are three 16-step bars long, which hold four 12-step bars
# (as the classical pack's waltz): their tempo counts a quarter of 4 sixteenths.
#
# The notes carry the new per-note settings: @velocity (a fiddle's bow, a banjo roll's accents)
# and <nudge (a grace note played early, a whistle's cut).
#   python3 tools/packs/folk.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/folk/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "folk")
sys.path.insert(0, HERE)
from patternkit import MAJOR, Pack, N, C, R  # noqa: E402

pack = Pack("Folk", PACK, MAJOR)


def bars12(*bars):
    """Four 12-step bars (6/8 or 3/4) as the three 16-step bars they fill."""
    tokens = " ".join(bars).split()
    if len(tokens) != 48:
        raise ValueError(f"{len(tokens)} steps, not four bars of 12")
    return " | ".join(" ".join(tokens[i:i + 16]) for i in (0, 16, 32))


def rows12(*bars):
    """A drum row of four 12-step bars."""
    row = "".join(bars).replace(" ", "")
    if len(row) != 48:
        raise ValueError(f"{len(row)} steps, not four bars of 12")
    return row


# --- drums --------------------------------------------------------------------------------------
# folk rock's train beat (Knockin' on Heaven's Door, Heart of Gold): kick on one and three, the
# snare on two and four, eighth hats, the tambourine shaking the off-beats
pack.drums("Dylan Shuffle", "FOLK", {
    "KICK":  "X.......x....... | X.......x.....x.",
    "SNARE": "....x.......x... | ....x.......x...",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "PERC":  "..x...x...x...x. | ..x...x...x.xxx.",
})
# a jig in 6/8 on the bodhrán (the low floor tom): every eighth, the strong strokes on 1 and 4
# of the six; the kick under 1, the tambourine on 4
pack.drums("Bodhran Jig", "FOLK", {
    "TOM":  rows12("X.x.x.X.x.x.", "X.x.x.X.x.x.", "X.x.x.X.x.x.", "X.x.x.X.xxx."),
    "KICK": rows12("x...........", "x...........", "x...........", "x.....x....."),
    "PERC": rows12("......x.....", "......x.....", "......x.....", "......x.x.x."),
})
# a reel's stomp (the Pogues, the Dubliners at speed): a foot on every beat, the bodhrán's
# eighths, claps on two and four, the tambourine in sixteenths
pack.drums("Reel Stomp", "FOLK", {
    "KICK": "X...x...X...x... | X...x...X...x...",
    "TOM":  "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.xxxx",
    "CLAP": "....x.......x... | ....x.......x...",
    "PERC": "xxxxxxxxxxxxxxxx | xxxxxxxxxxxxxxxx",
})
# the waltz of The Times They Are A-Changin': the kick on one, the snare's brush on two and
# three, the ride holding the bar
pack.drums("Changin' Waltz", "FOLK", {
    "KICK":   rows12("X...........", "x...........", "X...........", "x.......x..."),
    "SNARE":  rows12("....x...x...", "....x...x...", "....x...x...", "....x...x.x."),
    "CYMBAL": rows12("x...x...x...", "x...x...x...", "x...x...x...", "x...x...x..."),
})
# a drinking-song gallop (Whiskey in the Jar): driving eighths on the kick and the hats, the
# snare's backbeat, a roll on the toms into the chorus
pack.drums("Whiskey Gallop", "FOLK", {
    "KICK":  "X.x...x.X.x...x. | X.x...x.X.x.....",
    "SNARE": "....X.......X... | ....X.......X...",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.....",
    "TOM":   "................ | ............xxxx",
})

# --- bass ---------------------------------------------------------------------------------------
# Knockin' on Heaven's Door's turn (G D Am | G D C: I V ii | I V IV), root and fifth
pack.bass("Heaven's Door Roots", "Acoustic bass", " | ".join([
    " ".join([N("1!", 3, 1), N("5-", 2), N("5-", 2), N("2", 3, 1), N("6-", 2), N("2", 2)]),
    " ".join([N("1!", 3, 1), N("5-", 2), N("5-", 2), N("4", 3, 1), N("1", 2), N("4", 2)])]),
    mods={"FILTER/CUTOFF": -1800})
# a jig's bass in 6/8: the root on 1, the fifth on 4, the strong one louder (I IV V I)
pack.bass("Jig Bass", "Upright", bars12(
    N("1!@104", 6), N("5-@84", 6),
    N("4@100", 6), N("1@82", 6),
    N("5-@100", 6), N("2@82", 6),
    N("1!@104", 6), N("5-@80", 3), N("7-@76", 3)))
# The House of the Rising Sun in 6/8, eight bars: Am C D F Am E Am E (in G major: ii IV V ♭VII
# ii VI ii VI, the ♭VII and the major VI from outside the key), the bass falling by the chords
pack.bass("Rising Sun Walk", "Contrabass", " | ".join(" ".join(bar.split()) for bar in [
    " ".join([N("2!", 6), N("6-", 6), N("4", 4)]),
    " ".join([N("1", 2), N("5", 6), N("2", 6), N("b7-", 2)]),
    " ".join([N("b7-", 4), N("4", 6), N("2!", 6)]),
    " ".join([N("6-", 6), N("3", 6), N("6-", 4)]),
    " ".join([N("6-", 2), N("2!", 6), N("6-", 6), N("4", 2)]),
    " ".join([N("4", 4), N("6-", 6), N("3", 2), N("#1", 4)])]))
# the waltz of The Times They Are A-Changin' (G Em C G | G Am C D), "oom-pah-pah": the root, then
# the fifth twice
pack.bass("Changin' Oom-Pah", "Acoustic bass", bars12(
    N("1!", 4), N("5-", 4), N("5-", 4),
    N("6-!", 4), N("3", 4), N("3", 4),
    N("4!", 4), N("1", 4), N("1", 4),
    N("5-!", 4), N("2", 4), N("7-", 4)))
# a Dorian drone (Matty Groves' i–VII, Scarborough Fair's Am G): the A held, stepping to G and
# back, swelling and easing as a bowed bass does
pack.bass("Dorian Drone", "Contrabass", " ".join([
    N("2-!@90", 14), N("1-@72", 2), N("2-@96", 12), N("1-@70", 4),
    N("2-@100", 8), N("1-@78", 8), N("2-!@92", 15), R(1)]),
    mods={"ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 1800})

# --- lead ---------------------------------------------------------------------------------------
# a fiddle jig in 6/8, eighths in threes, the first of each three leaned on (the bow's push), a
# grace note snapped in early before the long notes
pack.lead("Fiddle Jig", "Fiddle", bars12(
    N("5@108", 2), N("3@80", 2), N("5@84", 2), N("1+@104", 2), N("5@80", 2), N("3@82", 2),
    N("4@108", 2), N("6@80", 2), N("4@84", 2), N("3@104", 2), N("2@80", 2), N("1@82", 2),
    N("2@108", 2), N("3@80", 2), N("4@84", 2), N("5@104", 2), N("6@80", 2), N("7@82", 2),
    N("2+@70<25", 1), N("1+!@112", 5), N("5@84", 2), N("1+@100", 4)),
    mods={"MOTION/VIBRATO": 30})
# a Scruggs-style banjo roll: sixteenths in 3 + 3 + 2 (thumb, index, middle), the roll's first
# note louder, over I and IV
ROLL = [("1", "3", "5"), ("1+", "3", "5"), ("1", "5")]
def roll(chord):
    tokens = []
    for group in ROLL:
        for i, note in enumerate(group):
            tokens.append(f"{chord.get(note, note)}@{104 if i == 0 else 78}")
    return tokens + tokens
pack.lead("Banjo Roll", "Banjo", " | ".join([
    " ".join(roll({})),
    " ".join(roll({"1": "4", "1+": "4+", "3": "6", "5": "1+"}))]))
# a slow air on the whistle (recorder): long notes, each led in by a quick cut from above,
# played early so the long note lands on the beat
pack.lead("Whistle Air", "Recorder", " | ".join([
    " ".join([N("6@64<30", 1), N("5!@96", 7), N("3@84", 4), N("2@80", 4)]),
    " ".join([N("2+@64<30", 1), N("1+@92", 7), N("6@84", 4), N("5@88", 4)]),
    " ".join([N("4@64<30", 1), N("3@90", 5), N("5@84", 2), N("6@86", 4), N("5@82", 4)]),
    " ".join([N("2@64<30", 1), N("1!@94", 13), R(2)])]),
    mods={"ENVELOPE/ATTACK": 600, "ENVELOPE/RELEASE": 1200})
# Drunken Sailor (traditional, public domain), in the Dorian of degree 2: the three rising calls
# and the "early in the morning" answer
pack.lead("Drunken Sailor", "Bagpipe", " | ".join([
    " ".join([N("6!", 2), N("6", 1), N("6", 1), N("6", 2), N("6", 1), N("6", 1), N("6", 2), N("2+", 2), N("4+", 2), N("6+", 2)]),
    " ".join([N("5!", 2), N("5", 1), N("5", 1), N("5", 2), N("5", 1), N("5", 1), N("5", 2), N("1+", 2), N("3+", 2), N("5+", 2)]),
    " ".join([N("6!", 2), N("6", 1), N("6", 1), N("6", 2), N("6", 1), N("6", 1), N("6", 2), N("7", 2), N("1+", 2), N("2+", 2)]),
    " ".join([N("1+", 2), N("6", 2), N("5", 2), N("3", 2), N("2!", 4), N("2", 3), R(1)])]))
# The House of the Rising Sun's picking, in 6/8 on the harp: each chord's root, fifth, octave,
# third, fifth and octave, eighth by eighth (Am C D F Am E Am E)
def arp(root, third, fifth):
    return " ".join([N(root + "@100", 2), N(fifth + "@78", 2), N(root.replace("-", "") + "@84", 2),
                     N(third + "@80", 2), N(fifth + "@78", 2), N(root.replace("-", "") + "@82", 2)])
pack.lead("Rising Sun Harp", "Harp", " | ".join(" ".join(" ".join(
    arp(*chord) for chord in group).split()[i:i + 16]) for group, i in [
    ([("2-", "4-", "6-"), ("4-", "6-", "1"), ("5-", "7-", "2"), ("b7-", "2", "4")], 0),
    ([("2-", "4-", "6-"), ("4-", "6-", "1"), ("5-", "7-", "2"), ("b7-", "2", "4")], 16),
    ([("2-", "4-", "6-"), ("4-", "6-", "1"), ("5-", "7-", "2"), ("b7-", "2", "4")], 32),
    ([("2-", "4-", "6-"), ("6-", "#1", "3"), ("2-", "4-", "6-"), ("6-", "#1", "3")], 0),
    ([("2-", "4-", "6-"), ("6-", "#1", "3"), ("2-", "4-", "6-"), ("6-", "#1", "3")], 16),
    ([("2-", "4-", "6-"), ("6-", "#1", "3"), ("2-", "4-", "6-"), ("6-", "#1", "3")], 32)]))

# --- chords -------------------------------------------------------------------------------------
# chromatic voicings, semitones from the key's root (G): F (♭VII) and E major (VI) in Rising Sun
FOLK = {"bVII": ("c", [-7, -3, 0, 5]), "VI": ("c", [-8, -4, -1, 4]), "ii": ("x", [1, 3, 5, 8]),
        "I": ("x", [0, 2, 4, 7]), "IV": ("x", [3, 5, 7, 10]), "V": ("x", [4, 6, 8, 11]),
        "vi": ("x", [5, 7, 9, 12]), "iiD": ("x", [1, 4, 5, 8]), "V2": ("x", [4, 6, 8, 11, 13])}
# Knockin' on Heaven's Door (G D Am | G D C), strummed in each half bar: down (held), up, down (held)
def strum(*chords):
    out = []
    for chord in chords:
        out += ["@" + chord, "=", ".", "@" + chord, ".", "@" + chord, "=", "."]
    return " ".join(out)
pack.chords("Heaven's Door Strum", "Guitar · Acoustic", " | ".join([
    strum("I", "V"), strum("ii", "ii"), strum("I", "V"), strum("IV", "IV")]), FOLK,
    mods={"MOTION/CHORUS": 200})
# The Times They Are A-Changin' in 3/4 on the 12-string: the chord on one, again on two and
# three (G Em C G | G Am C D), eight waltz bars
def waltz(chord):
    return [C("@" + chord, 3, 1), C("@" + chord, 2, 2), C("@" + chord, 2, 2)]
pack.chords("Changin' 12-String", "Guitar · 12-string", " | ".join(
    " ".join(" ".join(" ".join(waltz(c)) for c in group).split()[i:i + 16]) for group, i in [
        (["I", "vi", "IV", "I"], 0), (["I", "vi", "IV", "I"], 16), (["I", "vi", "IV", "I"], 32),
        (["I", "ii", "IV", "V"], 0), (["I", "ii", "IV", "V"], 16), (["I", "ii", "IV", "V"], 32)]), FOLK)
# The House of the Rising Sun, held a 6/8 bar each (Am C D F Am E Am E), on the accordion
pack.chords("Rising Sun Accordion", "Accordion", " | ".join(
    " ".join(" ".join(C("@" + c, 11, 1) for c in group).split()[i:i + 16]) for group, i in [
        (["ii", "IV", "V", "bVII"], 0), (["ii", "IV", "V", "bVII"], 16), (["ii", "IV", "V", "bVII"], 32),
        (["ii", "VI", "ii", "VI"], 0), (["ii", "VI", "ii", "VI"], 16), (["ii", "VI", "ii", "VI"], 32)]), FOLK)
# the Pogues' Dirty Old Town and the Dubliners' Whiskey in the Jar: G C G | D Em (I IV I | V vi),
# the accordion's off-beat "pah"
pack.chords("Dirty Old Town Pah", "Accordion", " | ".join([
    " ".join([R(2), C("@I", 1, 3), C("@I", 1, 3), C("@IV", 1, 3), C("@IV", 1, 1)]),
    " ".join([R(2), C("@I", 1, 3), C("@I", 1, 3), C("@I", 1, 3), C("@I", 1, 1)]),
    " ".join([R(2), C("@V", 1, 3), C("@V", 1, 3), C("@vi", 1, 3), C("@vi", 1, 1)]),
    " ".join([R(2), C("@IV", 1, 3), C("@V", 1, 3), C("@I", 1, 3), C("@I", 1, 1)])]), FOLK)
# Scarborough Fair's Dorian (Am G Am C | Am C D Am, all in G major: ii I ii IV | ii IV V ii) on
# the harp, each chord held, the D with its added ninth
pack.chords("Scarborough Harp", "Harp", " | ".join([
    " ".join([C("@iiD", 8), C("@I", 8)]), " ".join([C("@ii", 8), C("@IV", 8)]),
    " ".join([C("@ii", 8), C("@IV", 8)]), " ".join([C("@V2", 8), C("@iiD", 7, 1)])]), FOLK,
    mods={"ENVELOPE/RELEASE": 1800})

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(110, "G", "Major", echo=0.1,
              about="Folk in G major (the songs' key), straight, dry but for a little room.")

if __name__ == "__main__":
    pack.done()
