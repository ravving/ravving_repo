#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret "Solos" pack: six ballad solos for the LEAD machine, moody, prolonged and
# passionate, after the John Coltrane Quartet's *Ballads* (Impulse!, 1962/63: Coltrane, McCoy
# Tyner, Jimmy Garrison, Elvin Jones) and Chet Baker's slow ballad trumpet. Four for the
# saxophone in Coltrane's ballad voice (three tenor, one soprano), two for the trumpet in
# Baker's; each with the drums (brushes), the bass and the chords (Tyner-style voicings) it is
# heard over (six of each, see ../patternkit.py). Written in scale degrees for a MAJOR key, made
# for Eb major (a ballad key of the tenor; the minor moods sit on degree 6, C minor): the lead's
# degree 1 is Eb4, so the tenor sings "5-".."1+" (Bb3–Eb5) and cries up to "2+" (F5), the
# soprano floats "5".."3+", the trumpet stays "7-".."6" (D4–C5).
#
# Nothing is quoted (the album's standards and the recorded solos are copyrighted): the style
# was studied (tools/genre-research/solos.md) and every line, progression and rhythm here is
# original. The playing: slow (56–70), long held notes (_), each phrase swelling and fading by
# its velocities (@60–110), every long note behind the beat (>8–16, the rubato lean), the short
# flurries only as ornaments (three or four sixteenths, pushed early <2–6, climbing in
# velocity) into a long note, space between the phrases, a scoop (~) into a long tone. The
# sounds' MODS soften the attack (a swell into each note), lengthen the release (the room) and
# add a little vibrato on the sax, none on the trumpet.
#   python3 tools/packs/solos.py

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/solos/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "solos")
sys.path.insert(0, HERE)
import patternkit  # noqa: E402
from patternkit import MAJOR, Pack, N, C, R  # noqa: E402

# kits.json presetKits "Brush · crash": the brush kit with its crash (key 49) on CYMBAL, for the
# rolled cymbal swells (patternkit.KITS has the ride one, BRUSH_RIDE)
patternkit.KITS.setdefault("BRUSH_CRASH", patternkit.GM + "#128:40")

pack = Pack("Solos", PACK, MAJOR)


def ph(text, bars):
    """A phrase: tokens `note[@velocity][<|>nudge][/steps]` or `.[/steps]`, two steps unless
    `/steps` says; checked to fill `bars` bars."""
    out, at = [], 0
    for token in text.split():
        head, _, steps = token.partition("/")
        steps = int(steps) if steps else 2
        if head == ".":
            out.append(R(steps))
        else:
            if not re.fullmatch(r"[#b]?[1-7][+-]?[!~]*(@\d+)?([<>]\d+)?", head):
                raise ValueError(f"bad token {token!r}")
            out.append(N(head, steps))
        at += steps
    if at != bars * 16:
        raise ValueError(f"{at} steps, not {bars} bars: {text[:50]!r}")
    return " ".join(out)


# --- voicings: note names, kept as semitones from the chord base (degree I at octave 0: Eb3
# in Eb), the ("c", […]) form of patternkit -----------------------------------------------------
NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
BASE = 51  # Eb3: ChordMachine's base C3 (48) plus the root Eb (3)


def v(notes):
    """("c", semitones from Eb3) for a voicing written "G3 Bb3 D4 F4"."""
    out = []
    for note in notes.split():
        m = re.fullmatch(r"([A-G])([b#]?)(\d)", note)
        letter, accidental, octave = m.groups()
        midi = 12 * (int(octave) + 1) + NAMES[letter] + {"b": -1, "#": 1, "": 0}[accidental]
        out.append(midi - BASE)
    return ("c", out)


V = {
    # Eb major's own chords, rootless (the bass has the root) or in fourths (Tyner)
    "Ebmaj9": v("G3 Bb3 D4 F4"), "Eb69": v("G3 C4 F4 Bb4"), "Ebmaj9q": v("D4 G4 C5 F5"),
    "Cm9": v("Eb3 G3 Bb3 D4"), "Cm11": v("F3 Bb3 Eb4 G4"),
    "Fm9": v("Ab3 C4 Eb4 G4"), "Fm11": v("Bb3 Eb4 Ab4 C5"),                 # Fm11: the So What shape
    "Gm7": v("F3 Bb3 D4 G4"), "Gm11": v("F3 Bb3 C4 D4"),
    "Abmaj9": v("C4 Eb4 G4 Bb4"), "Abmaj7#11": v("G3 C4 D4 Eb4"), "Abmaj9#11": v("C4 D4 G4 Bb4"),
    "Bb13sus": v("Ab3 Eb4 G4 C5"), "Bb13": v("Ab3 C4 D4 G4"), "Bb7b9": v("Ab3 B3 D4 G4"),
    # from outside the key: the minor iv (Abm6), the backdoor Db9, the secondary dominants
    "Abm6": v("F3 B3 Eb4 Ab4"), "Db9": v("B3 Eb4 F4 Ab4"),
    "C7b9": v("Bb3 Db4 E4 A4"), "C7alt": v("Bb3 E4 Ab4 Db5"), "C7#9": v("E3 Bb3 Eb4 Ab4"),
    "Eo7": v("G3 Bb3 Db4 E4"),
    # C minor (degree 6): the line cliché C B Bb A under a held D, the ii–V
    "Cm": v("C4 Eb4 G4 D5"), "CmMaj": v("B3 Eb4 G4 D5"), "Cm7": v("Bb3 Eb4 G4 D5"),
    "Cm6": v("A3 Eb4 G4 D5"), "CmMaj9": v("Eb3 G3 B3 D4"),
    "Dø": v("C4 F4 Ab4 D5"), "G7alt": v("B3 F4 Ab4 Eb5"), "G7b9": v("B3 F4 Ab4 D5"),
    # fourths planed over the F pedal (F Dorian, degree 2): Tyner's vamp
    "QF": v("Bb3 Eb4 Ab4 C5"), "QG": v("C4 F4 Bb4 D5"), "QEb": v("G3 C4 F4 Bb4"),
    "QAb": v("D4 G4 C5 F5"),
}


def comp(*bars):
    """Chord bars, each a list of (voicing, steps) with "." a rest; checked to sixteen steps."""
    out = []
    for chords in bars:
        if sum(steps for _, steps in chords) != 16:
            raise ValueError(f"a chord bar of {sum(s for _, s in chords)} steps: {chords}")
        out.append(" ".join(R(steps) if name == "." else C("@" + name, steps) for name, steps in chords))
    return " | ".join(out)


# the brushes: the kit's darker for the ballads (engines.json kitSound TONE/CUTOFF, in cents)
SOFT = {"TONE/CUTOFF": -1800}
# the tenor (Coltrane's Ballads tone): each note swells in (ATTACK, timecents: +2400 is four
# times the font's own attack), rings into the room (RELEASE), a little vibrato, the top
# darkened; the trumpet (Baker): breathier and slower in, darker, no vibrato
TENOR = {"FILTER/CUTOFF": -600, "ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 1200, "MOTION/VIBRATO": 14}
SOPRANO = {"FILTER/CUTOFF": -900, "ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 1800, "MOTION/VIBRATO": 18}
TRUMPET = {"FILTER/CUTOFF": -1800, "ENVELOPE/ATTACK": 3600, "ENVELOPE/RELEASE": 1200}
PIANO = {"ENVELOPE/RELEASE": 1200}  # the sustain pedal's ring

# =========================================================================================
# 1. VOW (66): a warm major ballad (I vi ii V | iii VI7 ii iv | I VI7alt ii V), the theme
# paraphrased in long tones, a chromatic flurry climbing into the high Eb; the minor iv's Cb
# --- drums: brushes swept in eighths, the slap and the foot on 2 and 4, the kick feathered on
# one, the ride coming in at the end of the second bar
pack.drums("Vow Brushes", "BRUSH_RIDE", {
    "SNARE":  "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "CLAP":   "....x.......x... | ....x.......x...",
    "HAT":    "....x.......x... | ....x.......x...",
    "KICK":   "x............... | ................",
    "CYMBAL": "................ | ..........x.x.x.",
}, mods=SOFT)
# --- bass (degree 1 is Eb2): Garrison's two-feel, half notes behind the beat, a chromatic
# eighth into the next chord
pack.bass("Vow Two", "Upright", ph(
    "1@92>8/8 5-@84>8/6 #5-@74>6/2 "      # Eb, Bb, B into C
    "6-@92>8/8 3@84>8/8 "                 # Cm: C, G
    "2@92>8/8 6-@84>8/6 #4-@74>6/2 "      # Fm: F, C, A into Bb
    "5-@94>8/12 4-@78>6/4 "               # Bb: held, Ab into G
    "3-@92>8/8 6-@88>8/8 "                # Gm C7
    "2@90>8/8 4-@86>8/8 "                 # Fm Abm6
    "1@90>8/8 6-@86>8/8 "                 # Eb C7alt
    "2@90>8/8 5-@88>8/6 7-@74>6/2", 8))   # Fm Bb7, D into Eb
# --- lead: the tenor
pack.lead("Trane Vow", "Tenor sax", ph(
    "./2 5-@62>14 3@72>10/10 2~@70>8 "                 # Ebmaj9: Bb, the G held, slurred from F
    "3@78>8/4 5@84>6/8 4@74>8 3@70>10 "                # Cm11: G, Bb swelling, Ab G
    "4@76>12/12 ./4 "                                  # Fm9: the Ab held, air
    "6-@66<4/1 7-@72<4/1 1@78<2/1 2@84/1 6@92>6/8 b6@80>8 5@72>8 "  # Bb7: a flurry up to the C, its b9
    "./2 3@72>12/6 #4@78>6 3@74>8/6 "                  # Gm7 C7: G, C7's A, G
    "4@80>8/8 b6~@84>6/8 "                             # Fm9 Abm6: Ab, the minor iv's Cb, sliding down
    "5@74>10/10 ./2 5@68<6/1 6@72<6/1 b7@78<4/1 7@84<2/1 "  # Ebmaj9 C7alt: Bb, a chromatic climb
    "1+@100>6/10 7@80>8 6@74>10 ./2", 8),              # Fm11 Bb7: the high Eb cried, falling
    mods=TENOR)
# --- chords: Tyner's ballad comp, lush and held, re-voiced on three
pack.chords("Vow Voicings", "Grand piano", comp(
    [("Ebmaj9", 9), (".", 1), ("Eb69", 6)], [("Cm11", 7), (".", 1), ("Cm9", 8)],
    [("Fm9", 7), (".", 1), ("Fm11", 8)], [("Bb13sus", 8), ("Bb7b9", 7), (".", 1)],
    [("Gm7", 8), ("C7b9", 7), (".", 1)], [("Fm9", 8), ("Abm6", 7), (".", 1)],
    [("Ebmaj9", 8), ("C7alt", 7), (".", 1)], [("Fm11", 8), ("Bb7b9", 6), (".", 2)]), V, mods=PIANO)

# =========================================================================================
# 2. LAMENT (56): C minor (degree 6), the darkest: the line cliché C B Bb A under a held D, the
# minor ii–V; the tenor waits a beat, sighs, a flurry up G7's b9 arpeggio into a long Eb cry
# --- drums: slow brushes, the slap on 2 and 4, a crash rolled up through the last two beats
# into the downbeat (the cymbal swell)
pack.drums("Lament Swells", "BRUSH_CRASH", {
    "SNARE":  "x.....x.x.....x. | x.....x.x.....x.",
    "CLAP":   "....x.......x... | ....x.......x...",
    "HAT":    "....x.......x... | ....x.......x...",
    "KICK":   "X............... | ................",
    "CYMBAL": "X............... | ........xxxxxxxx",
}, mods={"TONE/CUTOFF": -2400})
# --- bass: whole and half notes, the C held under the cliché, a pickup G back into it
pack.bass("Lament Pedal", "Upright", ph(
    "6-@94>8/16 "                         # Cm: C, the bar
    "6-@86>8/8 3-@82>8/8 "                # Cm7 Cm6: C, G
    "7-@90>8/8 3-@88>8/8 "                # Dø G7alt
    "6-@92>8/8 4-@88>8/8 "                # Cm9 Abmaj7#11
    "2@90>8/8 5-@86>8/8 "                 # Fm9 Bb13
    "1@88>8/8 4-@84>8/8 "                 # Ebmaj9 Abmaj9
    "7-@88>8/8 3-@90>8/8 "                # Dø G7alt
    "6-@92>8/12 3-@74>8/4", 8))           # Cm(maj9), G into the C
pack.lead("Trane Lament", "Tenor sax", ph(
    "./4 3@66>14/12 "                                  # Cm: a beat of air, the G held
    "2@70>10/6 1@74>8 7-~@70>10/8 "                    # Cm7 Cm6: F Eb, D sliding
    "2@76>10/8 #5-@70<6/1 7-@76<4/1 2@82<2/1 4@88/1 "  # Dø G7alt: F, a flurry up the b9 arpeggio
    "1+@98>4/12 7@84>8/4 6@74>10/4 "                   # Cm9 Abmaj7#11: the Eb cried, D, C
    "./2 4@72>12/6 3@76>10 2~@72>8/6 "                 # Fm9 Bb13: Ab, G, F sliding
    "3@78>8/8 6@82>6/8 "                               # Ebmaj9 Abmaj9: G, C
    "4@80>8/6 2@74>10 4@78<4/1 2@74<4/1 7-@70<2/1 #5-@66>8/5 "  # Dø G7alt: Ab F, down to the B
    "7-~@70>12 6-@66>14/10 ./4", 8),                   # Cm(maj9): D sighing to the C, air
    mods=TENOR)
pack.chords("Lament Line", "Grand piano", comp(
    [("Cm", 8), ("CmMaj", 8)], [("Cm7", 8), ("Cm6", 7), (".", 1)],
    [("Dø", 8), ("G7alt", 7), (".", 1)], [("Cm9", 8), ("Abmaj7#11", 7), (".", 1)],
    [("Fm9", 8), ("Bb13", 7), (".", 1)], [("Ebmaj9", 8), ("Abmaj9", 7), (".", 1)],
    [("Dø", 8), ("G7alt", 8)], [("CmMaj9", 15), (".", 1)]), V, mods=PIANO)

# =========================================================================================
# 3. DEVOTION (70): the passionate one, on an F pedal (F Dorian, degree 2) with Tyner's fourths
# planed over it, then the Lydian IV, Gm and C7alt home: the tenor starts low and quiet and
# climbs for eight bars to F5, cried three times
# --- drums: Elvin with soft sticks, the ride skipping, the toms rolling around the pedal, a
# brush slap closing the loop
pack.drums("Devotion Mallets", "BRUSH_RIDE", {
    "CYMBAL": "x...x.x.x...x.x. | x...x.x.x...x.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "TOM":    "......x.......x. | ....x.....x.x.xx",
    "KICK":   "x.........x..... | x.....x.........",
    "SNARE":  "...x.......x.... | ...x.......x....",
    "CLAP":   "................ | ............x...",
}, mods=SOFT)
# --- bass: the F pedal with its fifth and a push; the IV, the iii, the V7 alt held
def pedal():
    return "2-@96>6/6 ./2 6-@84>6/6 2-@78>6/2 "
pack.bass("Devotion Pedal", "Upright", ph(
    pedal() + pedal() + pedal() + pedal() +
    "4-@92>6/8 1@84>6/8 "                 # Abmaj9#11: Ab, Eb
    "3-@92>6/8 7-@84>6/8 "                # Gm11: G, D
    "2-@94>6/8 6-@84>6/8 "                # Fm11: F, C
    "6-@96>6/12 #1-@80>6/4", 8))          # C7alt: C held, E into the F
pack.lead("Trane Devotion", "Tenor sax · Bright", ph(
    "./6 2-@60>14/10 "                                 # the low F, soft, late
    "4-@64>10/4 5-@68>8/4 6-@72>8/8 "                  # Ab Bb, the C held
    "./2 1@74>8 2@78>6/12 "                            # Eb into the F, held
    "3@74<6/1 4@78<4/1 5@82<4/1 6@86<2/1 1+@92>6/8 6@80>8/4 "  # a flurry up to the high Eb, C
    "7@88>6/8 6@82>8/4 3@76>10/4 "                     # Abmaj9#11: D (the #11), C, G
    "5@80>8/6 6@84<4/1 1+@90<2/1 2+@104>4/8 "          # Gm11: Bb, then up to the F, cried
    "2+@108>2/4 1+@96>4/2 2+@110>2/4 1+@94>6/2 6@86>8/4 "  # Fm11: the cry again, twice, falling
    "b7@84>6/6 4@78>8 #1@74>10/6 ./2", 8),             # C7alt: Db, Ab, E, a breath
    mods={**TENOR, "ENVELOPE/ATTACK": 1200, "MOTION/VIBRATO": 22})
pack.chords("Devotion Fourths", "Grand piano", comp(
    [("QF", 6), ("QG", 2), ("QF", 8)], [("QEb", 6), ("QF", 2), ("QG", 8)],
    [("QF", 6), ("QG", 2), ("QF", 8)], [("QG", 6), ("QAb", 2), ("QG", 7), (".", 1)],
    [("Abmaj7#11", 8), ("Abmaj9#11", 7), (".", 1)], [("Gm11", 8), ("Gm7", 7), (".", 1)],
    [("QF", 8), ("QEb", 7), (".", 1)], [("C7alt", 8), ("C7#9", 8)]), V, mods=PIANO)

# =========================================================================================
# 4. NOCTURNE (60): the soprano floating high over IV iii ii I (the Lydian IV first), the minor
# iv and a ii–V to close: one chord a bar, the line held across them
# --- drums: hardly there: the ride on one and three, the foot, two brush taps, one click
pack.drums("Nocturne Whisper", "BRUSH_RIDE", {
    "CYMBAL": "x.......x....... | x.......x.....x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "SNARE":  "......x.......x. | ......x.....x.x.",
    "KICK":   "x............... | ................",
    "PERC":   "................ | ..........x.....",
}, mods={"TONE/CUTOFF": -2400})
# --- bass: a note a bar, the roots under the floating line
pack.bass("Nocturne Roots", "Upright", ph(
    "4-@86>8/16 "                         # Abmaj9#11
    "3-@84>8/16 "                         # Gm11
    "2@84>8/16 "                          # Fm11
    "1@86>8/12 5-@74>8/4 "                # Eb6/9, Bb
    "4-@86>8/16 "                         # Abmaj9#11 Abm6
    "3-@84>8/8 6-@82>8/8 "                # Gm7 C7b9
    "2@84>8/16 "                          # Fm11
    "5-@88>8/12 #4-@72>8/4", 8))          # Bb7sus, A into the Ab
pack.lead("Soprano Nocturne", "Soprano sax", ph(
    "./2 6@66>12 1+@74>10/12 "                         # Abmaj9#11: C, the Eb held
    "7@76>8/6 6@72>8 5@70>10/8 "                       # Gm11: D C Bb
    "./4 4@68>12/4 6@74>10/8 "                         # Fm11: Ab, C
    "5@76>8/4 6@72<4/1 7@76<4/1 1+@80<2/1 2+@84/1 3+@90>6/8 "  # Eb6/9: Bb, a turn up to the G
    "7@80>8/8 b6@78>6/8 "                              # Abmaj9#11 Abm6: D (the #11), the Cb
    "5@72>10/8 ./2 #4@70>8 3@68>10/4 "                 # Gm7 C7b9: Bb, A, G
    "4@72>10/12 5@70<4/1 6@74<4/1 1+@80<2/1 2+@86/1 "  # Fm11: Ab held, climbing
    "1+@88>6/8 7@76>8/4 ./4", 8),                      # Bb7sus: the Eb, its D, air
    mods=SOPRANO)
pack.chords("Nocturne Floating", "Grand piano", comp(
    [("Abmaj9#11", 15), (".", 1)], [("Gm11", 15), (".", 1)], [("QF", 15), (".", 1)],
    [("Eb69", 15), (".", 1)], [("Abmaj9#11", 8), ("Abm6", 7), (".", 1)],
    [("Gm7", 8), ("C7b9", 7), (".", 1)], [("QF", 7), (".", 1), ("Fm9", 8)],
    [("Bb13sus", 8), ("Bb7b9", 7), (".", 1)]), V, mods=PIANO)

# =========================================================================================
# 5. TWILIGHT (62): Baker's ballad, the major: I #i°7 ii V | iii VI7 ii V | I vi ii V; few
# notes, low and soft, every one behind the beat, a scoop into the G
# --- drums: the brushes swirled (soft sixteenth taps), the slap on 2 and 4, the two-feel kick
pack.drums("Twilight Swirl", "BRUSH_RIDE", {
    "SNARE":  "xxxxxxxxxxxxxxxx | xxxxxxxxxxxxxxxx",
    "CLAP":   "....x.......x... | ....x.......x...",
    "HAT":    "....x.......x... | ....x.......x...",
    "KICK":   "x.......x....... | x.......x.......",
    "CYMBAL": "................ | ...............x",
}, mods={"TONE/CUTOFF": -2400})
# --- bass: the two-feel, root and fifth or third, a step into the turnaround
pack.bass("Twilight Two", "Acoustic bass", ph(
    "1@90>8/8 5-@82>8/8 "                 # Ebmaj7
    "#1@88>8/8 3@80>8/8 "                 # E°7: E, G
    "2@90>8/8 6-@82>8/8 "                 # Fm9
    "5-@90>8/8 4-@80>8/8 "                # Bb13, Ab into G
    "3-@88>8/8 6-@86>8/8 "                # Gm7 C7b9
    "2@88>8/8 5-@84>8/8 "                 # Fm9 Bb13
    "1@88>8/8 6-@84>8/8 "                 # Ebmaj7 Cm9
    "2@88>8/8 5-@86>8/6 7-@72>8/2", 8))   # Fm9 Bb7b9, D into the Eb
pack.lead("Baker Twilight", "Trumpet · Cool", ph(
    "./6 3@64>14/6 2@60>12/4 "                         # Ebmaj7: G, F
    "3@66>14/12 ./4 "                                  # E°7: the G held
    "4@68>12/8 6@72>10/4 5@66>12/4 "                   # Fm9: Ab, C, Bb
    "b3~@60>12/1 3@70>10/11 ./4 "                      # Bb13: a scoop into the G
    "./2 5@68>12/6 #4@64>12/6 ./2 "                    # Gm7 C7b9: Bb, C7's A
    "4@70>12/4 3@64>10/4 2@62>12/8 "                   # Fm9 Bb13: Ab G F
    "./4 7-@64>14/4 1@68>12/4 3@72>10/4 "              # Ebmaj7 Cm9: D Eb G
    "6@76>10/6 5@68>12 4@62>14/4 ./4", 8),             # Fm9 Bb7b9: C Bb, the Ab, air
    mods=TRUMPET)
pack.chords("Twilight Piano", "Upright piano", comp(
    [("Ebmaj9", 8), ("Ebmaj9q", 7), (".", 1)], [("Eo7", 15), (".", 1)],
    [("Fm9", 8), ("Fm11", 7), (".", 1)], [("Bb13", 15), (".", 1)],
    [("Gm7", 8), ("C7b9", 7), (".", 1)], [("Fm9", 8), ("Bb13", 7), (".", 1)],
    [("Ebmaj9", 8), ("Cm9", 7), (".", 1)], [("Fm9", 8), ("Bb7b9", 7), (".", 1)]), V, mods=PIANO)

# =========================================================================================
# 6. RAIN (58): Baker in the minor: i VI ii V | I, the backdoor iv–bVII7, I vi, the minor
# ii–V back to the C; half a bar of silence before the first note, the Cb, a scoop
# --- drums: brushes in 3 + 3 + 2, the slap only on four, a soft crash touching the loop's top
pack.drums("Rain Brushes", "BRUSH_CRASH", {
    "SNARE":  "x..x..x.x..x..x. | x..x..x.x..x..x.",
    "CLAP":   "............x... | ............x...",
    "HAT":    "....x.......x... | ....x.......x...",
    "KICK":   "x............... | x...............",
    "CYMBAL": "x............... | ................",
}, mods={"TONE/CUTOFF": -3000})
pack.bass("Rain Long Tones", "Acoustic bass", ph(
    "6-@90>10/16 "                        # Cm9
    "4-@86>10/16 "                        # Abmaj9
    "2@88>10/12 #4-@70>10/4 "             # Fm9, A into Bb
    "5-@88>10/16 "                        # Bb7sus Bb13
    "1@88>10/12 5-@74>10/4 "              # Ebmaj9
    "4-@86>10/8 b7-@84>10/8 "             # Abm6 Db9
    "1@86>10/8 6-@84>10/8 "               # Ebmaj9 Cm7
    "7-@86>10/8 3-@84>10/8", 8))          # Dø G7b9
pack.lead("Baker Rain", "Trumpet · Cool", ph(
    "./8 1@62>16/8 "                                   # Cm9: half a bar of air, the Eb
    "3@66>14/10 2@60>12/6 "                            # Abmaj9: G, F
    "4@68>12/12 ./4 "                                  # Fm9: the Ab held
    "6@70>10/6 5@66>12 7-@62>14/8 "                    # Bb7sus Bb13: C Bb, the D
    "./2 2@64>14/6 3@70>12/8 "                         # Ebmaj9: F, G
    "b6-@64>14/8 4@66>12/4 2@60>14/4 "                 # Abm6 Db9: the Cb, Ab, F
    "b3~@58>12/1 3@68>10/7 1@62>12/8 "                 # Ebmaj9 Cm7: a scoop into the G, Eb
    "2@66>12/6 4@62>12 #5-@60>14/6 ./2", 8),           # Dø G7b9: F, Ab, the B
    mods=TRUMPET)
pack.chords("Rain Rhodes", "Rhodes", comp(
    [("Cm9", 15), (".", 1)], [("Abmaj9", 15), (".", 1)],
    [("Fm9", 8), ("Fm11", 7), (".", 1)], [("Bb13sus", 8), ("Bb13", 7), (".", 1)],
    [("Ebmaj9", 15), (".", 1)], [("Abm6", 8), ("Db9", 7), (".", 1)],
    [("Ebmaj9", 8), ("Cm7", 7), (".", 1)], [("Dø", 8), ("G7b9", 7), (".", 1)]), V)

# the templates: how a project plays these best (the projects dialog's TEMPLATES): the ballad
# tempo with the eighths barely swung and a warm room, and a slower late-night one
pack.template(64, "Eb", "Major", swing=56, swing_eighths=True, echo=0.35,
              about="Ballads in Eb major after Coltrane's Ballads: slow, long tones, brushes, a warm room.")
pack.template(58, "Eb", "Major", name="Solos · Late Night", swing=54, swing_eighths=True, echo=0.45,
              about="The slowest ballads (Lament, Rain): rubato, nearly straight eighths, a deeper room.")

if __name__ == "__main__":
    pack.done()
