#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret "Meller" pack: jazz-pop after Petite Meller, from her records measured
# (tools/genre-research/fukui-meller.md, style.py and drum-grid.py on the audio):
#   Baby Love (2015): D♭ major, 129 BPM, straight; the verse vi IVmaj7, the "ta da da" V … ii,
#     the chorus ii I V; four on the floor, hats on every eighth, the kick and bass pulsing the
#     eighths, claps on 2 and 4, toms rolling in the intro; a soaring 90s-house alto sax.
#   Backpack (2016): E♭ major, 103 BPM, swung hard (the off-beat eighth at 0.77); the loop
#     I iii7 ii7 IVmaj7; an alto solo at the start in sixteenth runs and half steps.
#   Fela: an Afrobeat vamp on the ii, after the records she names behind Baby Love.
# Five sets of drums, bass, lead and chords (../patternkit.py), in scale degrees for D♭ MAJOR
# (Backpack's set plays in any major key: its template sets E♭). The lead's degree 1 is D♭4, the
# bass's D♭2, the chords' voicings are semitones from D♭3.
#
# Nothing is quoted: the songs are copyrighted. Their progressions, tempo and grooves were
# measured; every hook, solo line and rhythm here is new. The sets:
#   Verse       vi IVmaj7: the stomp, the octave pump, a piano on the eighths, a trumpet hook;
#   Ta Da       V V ii ii: the toms galloping, brass stabs, the sax's repeated notes;
#   Chorus      ii I V V: four on the floor, the piano on the beats, the house sax soaring;
#   Backpack    Imaj7 iii7 ii7 IVmaj7, shuffled: a walk, the Rhodes, the alto's runs;
#   Fela        a ii vamp, Afrobeat's sixteenth hats and the horn riff.
#   python3 tools/packs/meller.py

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/meller/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "meller")
sys.path.insert(0, HERE)
from patternkit import MAJOR, Pack, N, C, R  # noqa: E402

pack = Pack("Meller", PACK, MAJOR)


def bar(text):
    """One bar's tokens, checked to be sixteen (a miscount is the usual slip)."""
    tokens = text.split()
    if len(tokens) != 16:
        raise ValueError(f"{len(tokens)} tokens in bar: {text!r}")
    return text


def ph(text, bars, base=None, lean=0):
    """A phrase: tokens `note[/steps]` or `.[/steps]`, an eighth (2 steps) unless `/steps`
    says; a note without its own @velocity gets `base`, plus `lean` when it starts on an
    off-beat eighth. Checked to fill `bars` bars."""
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


# --- drums --------------------------------------------------------------------------------------
# Baby Love's grid, measured (tools/genre-research/drum-grid.py --percussive, 129 BPM): hats on
# every eighth, the kick and the bass pulsing the eighths, claps on 2 and 4, the intro's toms
# rolling in sixteenths; straight, no Latin hand percussion.
# the verse's gospel stomp: four on the floor, snare and clap on 2 and 4, the hats in eighths,
# a tom gallop opening each bar and a run into the loop
pack.drums("Gospel Stomp", "STANDARD", {
    "KICK":  "x...x...x...x... | x...x...x...x...",
    "SNARE": "....x.......x... | ....x.......x...",
    "CLAP":  "....x.......x... | ....x.......x..x",
    "TOM":   "x.xx..x......... | x.xx..x.....xxxx",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
})
# the "ta da da": the toms rolling sixteenths through the first half bar (the intro's hand
# drums), the kick on the beats, the clap on 2 and 4
pack.drums("Tom Gallop", "STANDARD", {
    "KICK": "x...x...x...x... | x...x...x...x...",
    "TOM":  "xxxxxxxxx.x.x.x. | xxxxxxxxx.x.xxxx",
    "CLAP": "....x.......x... | ....x.......x...",
    "HAT":  "x...x...x...x... | x...x...x...x...",
})
# the chorus drive: four on the floor, snare and clap on 2 and 4, the hats on every eighth,
# an open hat lifting each bar's end, the crash on the downbeat
pack.drums("Disco Drive", "STANDARD", {
    "KICK":   "x...x...x...x...",
    "SNARE":  "....x.......x...",
    "CLAP":   "....x.......x.x.",
    "HAT":    "x.x.x.x.x.x.x...",
    "OPEN":   "..............x.",
    "CYMBAL": "x...............",
})
# Backpack's shuffle (play it swung hard, its template): the kick on 1 and the "and" of 3, the
# snare on 2 and 4 with a ghost, the hats in eighths
pack.drums("Backpack Shuffle", "STANDARD", {
    "KICK":  "x.......x.x..... | x.......x.......",
    "SNARE": "....x.x.....x... | ....x.......x.xx",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "OPEN":  "..............x. | ................",
})
# Fela's Afrobeat: sixteenth hats opening at each half, the kick syncopated, the snare ghosting
# around 2 and 4
pack.drums("Afrobeat Fela", "STANDARD", {
    "KICK":  "x.....x...x..x.. | x.....x...x.....",
    "SNARE": "....x..x....x... | .x..x..x....x..x",
    "HAT":   "xxxxxxx.xxxxxxx. | xxxxxxx.xxxxxxx.",
    "OPEN":  ".......x.......x | .......x.......x",
})

# --- bass (degree 1 is D♭2; "-" the octave under) ----------------------------------------------
# the verse (vi IVmaj7, twice): the root and its octave trading eighths, the pulse the record's
# low end keeps
def octaves(low, high):
    return bar(" ".join([N(f"{low}!@108", 1, 1), N(f"{high}@94", 1, 1), N(f"{low}@102", 1, 1), N(f"{high}@94", 1, 1)] * 2))


pack.bass("Verse Pump", "Finger bass", " | ".join([octaves("6-", "6"), octaves("4-", "4"), octaves("6-", "6"), octaves("4-", "4")]))
# the "ta da da" (V V ii ii): the root struck, again, its octave, a run up to the next
V = "5-!@110 _ . 5-@96 5@100 . 5-@96 . 7-@100 _ . 1@96 2@100 . 5-@96 ."
II = "2!@110 _ . 2@96 2+@100 . 2@96 . 4@100 _ . 5@96 6@100 . 1@96 ."
pack.bass("Ta Da Bass", "Finger bass", " | ".join([bar(V), bar(V.replace("7-@100", "6-@100")), bar(II), bar(II)]))
# the chorus pumping (ii I V V): eighths on the root with octave pops, the last bar walking
# A♭ B♭ C into the ii
def pump(low, high):
    return bar(" ".join([N(f"{low}!@110", 1, 1), N(f"{low}@96", 1, 1), N(f"{high}@104", 1, 1), N(f"{low}@96", 1, 1)] * 2))


pack.bass("Chorus Pump", "Slap bass", " | ".join([
    pump("2", "2+"), pump("1", "1+"), pump("5-", "5"),
    bar(" ".join([N("5-!@110", 1, 1), N("5-@96", 1, 1), N("5@104", 1, 1), N("5-@96", 1, 1),
                  N("5-@100", 2), N("6-@100", 2), N("7-@104", 2), N("1@106", 2)]))]))
# Backpack's walk under the shuffle (Imaj7 iii7 ii7 IVmaj7): quarters on the chord tones, a
# chromatic step into each next root
def walk(*beats):
    return bar(" ".join(N(b, 3, 1) for b in beats))


pack.bass("Backpack Walk", "Finger bass", " | ".join([
    walk("1!@104", "3@94", "5@100", "b3@94"), walk("3@104", "5@94", "7@100", "#1@94"),
    walk("2@104", "4@94", "6@100", "3@94"), walk("4@104", "6@94", "1+@100", "7@94")]))
# the Afrobeat vamp on the ii: a syncopated figure up to the octave and back, the second bar
# walking down to the root
pack.bass("Fela Vamp", "Finger bass", " | ".join([
    bar("2!@110 . . 2@96 . 6@100 . 1+@96 2+@104 . 1+@96 . 6@100 . 4@96 ."),
    bar("2!@110 . . 2@96 . 6@100 . 1+@96 . 6@98 5@96 . 4@100 3@96 1@100 .")]))

# --- lead (degree 1 is D♭4; "-" the octave under, "+" the one over) ----------------------------
# the verse's trumpet hook over vi IVmaj7: a short bright call, a held answer, then again,
# landing high (Dizzy's horn among her heroes)
pack.lead("Verse Trumpet", "Trumpet", " ".join([
    ph(". 3+ 1+ 6 5 6/4 .", 1, 104, 6),                 # vi: F D♭ B♭ A♭, the B♭
    ph("6/3 ./1 1+ 6 4/4 . .", 1, 104, 6),              # IV: B♭, D♭ B♭, the G♭
    ph(". 3+ 1+ 6 5 3 5 6", 1, 104, 6),                 # vi: the call, then up
    ph("1+!/6 6 4/4 . .", 1, 108, 6)]))                 # IV: the high D♭ held
# the "ta da da" on the alto: repeated sixteenths and a fall, each bar's tail different, over
# V V ii ii
pack.lead("Ta Da Sax", "Alto sax", " ".join([
    ph("5/1 5/1 5 3 5/1 6/1 5 3 2/4", 1, 100, 8),       # V: A♭ A♭ A♭ F, A♭ B♭ A♭ F E♭
    ph("5/1 5/1 5 3 5/1 6/1 7 6 5/4", 1, 100, 8),       # V: up to the C, the A♭
    ph("4/1 4/1 4 2 4/1 5/1 4 2 1/4", 1, 100, 8),       # ii: on the G♭
    ph("6/1 5/1 4 2 1 7- 6-/4 .", 1, 100, 8)]),         # ii: falling to the B♭
    mods={"MOTION/VIBRATO": 18})
# the 90s house sax over the chorus (ii I V V): high held notes, a scoop, a turn and a slide up,
# the alto soaring
pack.lead("House Sax", "Alto sax", " ".join([
    ph("2+!/6 1+ 6/4 4 .", 1, 108, 6),                  # ii: the high E♭, D♭, B♭, G♭
    ph("1+/6 6 5/4 3 .", 1, 104, 6),                    # I: D♭ B♭ A♭ F
    ph("7/3 ./1 1+ 2+ 1+/4 7 5", 1, 106, 6),            # V: C, a turn on the D♭
    ph("5/8 ./4 2+~ 3+", 1, 110)]),                     # V: the long A♭, a slide up to F
    mods={"MOTION/VIBRATO": 22})
# the alto over Backpack's shuffle (Imaj7 iii7 ii7 IVmaj7), in the style of its intro solo: runs
# of sixteenths in the low-middle register, half-step approaches, short notes, a breath at each
# bar's end, the last bar climbing (nothing of the record's solo is copied)
pack.lead("Backpack Sax", "Alto sax", " ".join([
    ph("./2 5-/1 #5-/1 6-/1 7-/1 1/1 2/1 3 2/1 1/1 7- .", 1, 84, 8),          # Imaj7: up from the A♭
    ph("3/1 #3/1 4/1 5/1 . 4/1 3/1 b3/1 2/1 1 3 .", 1, 88, 8),              # iii7: around the F
    ph("2/1 #2/1 3/1 4/1 6 5/1 #4/1 4 2/1 1/1 7- .", 1, 92, 8),             # ii7: the E♭ chromatic
    ph("4/1 6/1 1+/1 3+/1 2+ 1+/1 7/1 6 4 ./4", 1, 100, 8)]),               # IVmaj7: up to the F
    mods={"MOTION/VIBRATO": 18})
# Fela's horn riff on the ii: punched, short, the answer falling to the B♭ (a muted horn line)
pack.lead("Fela Horns", "Muted trumpet", " ".join([
    ph("2!/3 ./1 2 4 . 5/1 4/1 2 1", 1, 108, 6),
    ph("6-/3 ./1 1 2/4 . 4 2", 1, 104, 6)]))

# --- chords: semitones from D♭3; A and B forms so a re-hit is struck ---------------------------
V_ = {
    "vi7": ("c", [-3, 0, 4, 7]), "vi7B": ("c", [4, 7, 9, 12]),                  # B♭m7
    "IVmaj7": ("c", [5, 9, 12, 16]), "IVmaj7B": ("c", [-3, 0, 4, 5]),          # G♭maj7
    "V": ("c", [7, 11, 14]), "VB": ("c", [2, 7, 11]),                           # A♭
    "ii": ("c", [2, 5, 9]), "iiB": ("c", [5, 9, 14]),                           # E♭m
    "ii9": ("c", [5, 9, 12, 16]), "ii9B": ("c", [2, 5, 9, 12]),                 # E♭m9
    "Imaj7": ("c", [4, 7, 11, 14]), "iii7": ("c", [7, 11, 14, 16]),            # D♭maj9, Fm7
    "ii7": ("c", [5, 9, 12, 14]),                                              # E♭m7
}
# the verse's piano pumping eighths (vi7 | IVmaj7, twice), the forms trading on each
def pump8(a, b):
    return bar(" ".join([C("@" + a, 1, 1), C("@" + b, 1, 1)] * 4))


pack.chords("Verse Piano", "Grand piano", " | ".join([
    pump8("vi7", "vi7B"), pump8("IVmaj7", "IVmaj7B"), pump8("vi7", "vi7B"), pump8("IVmaj7", "IVmaj7B")]), V_)
# the brass's "ta da da" stabs (V V ii ii): struck, again, a longer one, a gap, two more
def tada(a, b):
    return bar(" ".join([C("@" + a, 1, 1), C("@" + b, 1, 1), C("@" + a, 2, 2), R(2), C("@" + b, 1, 1), C("@" + a, 1, 1), R(2)]))


pack.chords("Ta Da Brass", "Brass section", " | ".join([
    tada("V", "VB"), tada("VB", "V"), tada("ii", "iiB"), tada("iiB", "ii")]), V_)
# the chorus piano (ii I V V): the chord on the beats with an off-beat push, house-piano style
def beats(degree):
    return bar(" ".join([C(degree, 2, 2), C(degree, 1, 1), C(degree, 2, 2), C(degree, 1, 1), C(degree, 3, 1)]))


pack.chords("Chorus Piano", "Grand piano", " | ".join([beats("2"), beats("1"), beats("5"), beats("5")]))
# Backpack's Rhodes (Imaj7 iii7 ii7 IVmaj7): a chord a bar, struck and touched again on 3
pack.chords("Backpack Rhodes", "Rhodes", " | ".join(
    bar(" ".join([C("@" + chord, 6, 2), C("@" + chord, 4, 4)])) for chord in ("Imaj7", "iii7", "ii7", "IVmaj7")), V_)
# Fela's organ on the ii9: syncopated stabs, the forms trading, a different second bar
pack.chords("Fela Organ", "Jazz organ", " | ".join([
    bar(" ".join([R(1), C("@ii9", 1, 1), R(1), C("@ii9B", 1, 2), C("@ii9", 2, 2), R(2), C("@ii9B", 1, 2)])),
    bar(" ".join([C("@ii9", 1, 1), R(2), C("@ii9B", 1, 1), C("@ii9", 1, 3), C("@ii9B", 2, 2), C("@ii9", 1, 1)]))]), V_)

# the templates: Baby Love's drive, Backpack's shuffle in its own key, the Afrobeat vamp
BAND = {"drums1": "STANDARD", "drums2": "ROOM", "bass": "Finger bass", "chords": "Grand piano", "lead": "Alto sax"}
pack.template(129, "Db", "Major", echo=0.15, heavy=0.2, sounds=BAND,
              sections=[("VERSE", 4), ("TA DA", 4), ("CHORUS", 4), ("SAX SOLO", 4), ("CHORUS", 4)],
              about="Jazz-pop after Petite Meller's Baby Love in D♭ major: 129, straight, the horns on top.")
pack.template(103, "Eb", "Major", name="Meller · Backpack", swing=66, swing_eighths=True, echo=0.2,
              sounds=dict(BAND, chords="Rhodes"),
              sections=[("SAX INTRO", 4), ("VERSE", 4), ("CHORUS", 4)],
              about="After Backpack: E♭ major at 103, the eighths swung hard, the alto first.")
pack.template(108, "Db", "Major", name="Meller · Fela", phaser=0.1, echo=0.2, heavy=0.25,
              sounds=dict(BAND, chords="Jazz organ", lead="Muted trumpet"),
              sections=[("GROOVE", 2), ("HORNS", 2), ("BREAK", 2)],
              about="The Afrobeat vamp: slower, warmer, room for the horn riff.")

if __name__ == "__main__":
    pack.done()
