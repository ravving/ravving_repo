#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret "Fukui" pack: piano trio jazz after Ryo Fukui's Scenery (1976), its energy above all:
# the crescendos that climb to a crash, the McCoy Tyner-style fourths and runs, the progressions
# that slip a half step out and back. Six sets of drums, bass, lead (the right hand) and chords
# (the left hand), see ../patternkit.py, written in scale degrees for D NATURAL MINOR, the key of
# "Scenery" (tools/genre-research/fukui-meller.md): its intro Dm | B♭maj7 | E♭maj7 | Edim A7, its
# A theme Dm | Edim A7 | B♭maj7 | Dm | Edim | A7 | Dm | Edim A7, its B theme Fmaj7 | Gm7 | Am7 |
# D7 | Gm7 | C7 | Fmaj7 | Edim A7. The lead's degree 1 is D4, the bass's D2, the chords' voicings
# are semitones from D3.
#
# Nothing is quoted: the tune and the recorded solos are copyrighted. The progressions are the
# song's; every line, voicing and rhythm is new. The sets:
#   Scenery     the A theme as a ballad (about 70): long tones behind the beat, the left hand
#               pumping the chord on every beat, the bass in halves with pickups;
#   Part B      the B theme up-tempo and swung: bop eighths, a walk, Red Garland-style comping;
#   Cascade     a D minor vamp in four bars of crescendo: pentatonic sixteenths climbing and
#               getting louder, a pedal of root and fifth, fourths filling in, the ride building;
#   Slip        the intro's changes (E♭maj7 a half step over the D) with runs side-stepping into
#               E♭ (the pentatonic's degrees raised a semitone), a 3-3-2 Latin vamp;
#   Waltz       a modal 6/8 (four 12-step bars in three 16-step ones): pentatonic triplet cells;
#   Climax      the finale: an octave tremolo, the fourths planing, the toms rolling, the crash.
# Velocity carries the crescendos (the lead and bass @ ramps; chords and drums thicken instead).
#   python3 tools/packs/fukui.py

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/fukui/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "fukui")
sys.path.insert(0, HERE)
from patternkit import MINOR, Pack, N, C, R  # noqa: E402

pack = Pack("Fukui", PACK, MINOR)


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


def ramp(text, start, end):
    """Sixteen one-step tokens (notes, "." or "_"), the notes without their own velocity swelling
    from `start` to `end` across the bar: the crescendo, written note by note."""
    tokens = bar(text).split()
    out = []
    for k, token in enumerate(tokens):
        if token in (".", "_") or "@" in token:
            out.append(token)
        else:
            out.append(f"{token}@{round(start + (end - start) * k / 15)}")
    return " ".join(out)


def walk(*beats):
    """A walking bar: four quarters (a token each, `note@velocity`), each held three steps."""
    if len(beats) != 4:
        raise ValueError(f"{len(beats)} beats in a walking bar")
    return " ".join(N(b, 3, 1) for b in beats)


def w(a, b, c, d):
    """A walking bar with 2 and 4 leaned on."""
    return walk(f"{a}@100", f"{b}@106", f"{c}@100", f"{d}@106")


# --- drums --------------------------------------------------------------------------------------
# Scenery's ballad: brushes circling the snare, the foot on 2 and 4, the kick feathered on 1 and
# 3, the ride touched before the turn
pack.drums("Scenery Brushes", "BRUSH_RIDE", {
    "SNARE":  "x..xx..xx..xx..x | x..xx..xx..xx.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "KICK":   "x.......x....... | x...............",
    "CYMBAL": "................ | ............x...",
})
# the B theme up-tempo: the ride's "ding, ding-a" with 2 and 4 leaned on, the foot, the snare
# comping between, a kick bomb on the "and" of 4 into the second bar
pack.drums("Early Swing", "JAZZ", {
    "CYMBAL": "x...X.x.x...X.x. | x...X.x.x...X.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "SNARE":  "......x.....x..x | ..x.......x...x.",
    "KICK":   "..............x. | ........x.......",
})
# the crescendo in four bars: the ride and the foot alone, then the snare talking, then kick
# bombs and accents, then the fill and the crash on its downbeats
pack.drums("Crescendo Ride", "JAZZ_CRASH", {
    "CYMBAL": "................ | ................ | ................ | X.......X.......",
    "OPEN":   "x...x.x.x...x.x. | x...x.x.x...x.x. | x...X.x.x...X.x. | ....x.x.....x.x.",
    "HAT":    "....x.......x... | ....x.......x... | ....x.......x... | ....x.......x...",
    "SNARE":  "................ | ......x.......x. | ..x...x..x..x.x. | x.x.xxx.x.xxxxxx",
    "KICK":   "................ | ..............x. | ......x.....x... | x.......x.....x.",
    "TOM":    "................ | ................ | ................ | ..x.......x.....",
})
# the Latin vamp under the slips (Tyner's straight-eighth modal grooves): the ride in eighths,
# the toms in a 3-3-2 figure, the kick on 1 and the "and" of 2, the snare answering
pack.drums("Latin Vamp", "JAZZ", {
    "CYMBAL": "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "HAT":    "....x.......x... | ....x.......x...",
    "TOM":    "...x..x.....x... | ...x..x...x..x..",
    "KICK":   "x.....x.x....... | x.....x.x.......",
    "SNARE":  "..........x..... | ..x.......x....x",
})
# the modal waltz in 6/8 (four 12-step bars): the ride in eighths, accented every other bar, the
# foot on the second dotted quarter, the snare cross-talking, a tom turning the third bar
pack.drums("Modal Six", "JAZZ", {
    "CYMBAL": "X.x.x.x.x.x. x.x.x.x.x.x. X.x.x.x.x.x. x.x.x.x.x.x.",
    "HAT":    "......x..... ......x..... ......x..... ......x.....",
    "KICK":   "x........... ......x..... x........x.. ......x.....",
    "SNARE":  "....x.....x. ..x.....x... ....x.....x. ..x..x..x.xx",
    "TOM":    "............ ............ ........x... ..........x.",
})
# the climax (Elvin's rolling toms): the crash on every beat, the toms in running pairs, the
# snare and the kick cutting across, the second bar all toms into the loop
pack.drums("Climax Toms", "JAZZ_CRASH", {
    "CYMBAL": "X...X...X...X... | X...X...X...X...",
    "TOM":    "..xx..xx..xx..xx | xx.xx.xx.xx.xxxx",
    "SNARE":  ".x...x...x...x.. | ..x..x..x..x....",
    "KICK":   "x.....x.....x... | x.....x.....x.x.",
    "HAT":    "....x.......x... | ....x.......x...",
})

# --- bass (degree 1 is D2; "-" the octave under) -----------------------------------------------
# Scenery's A theme (Dm | Edim A7 | B♭maj7 | Dm | Edim | A7 | Dm | Edim A7): half notes a little
# late, a dotted quarter with two sixteenths running into the next chord
def halves(a, b):
    return " ".join([N(f"{a}@92>6", 8), N(f"{b}@84>6", 8)])


def pickup(a, b, c):
    return " ".join([N(f"{a}@94>6", 12), N(f"{b}@78", 2), N(f"{c}@82", 2)])


pack.bass("Scenery Halves", "Upright", " | ".join([
    pickup("1!", "3", "#1"), halves("2", "5-"), pickup("6-", "7-", "#7-"), halves("1", "5-"),
    pickup("2", "4", "#4"), halves("5-", "#7-"), pickup("1", "2", "3"), halves("2", "5-")]))
# walking the B theme (Fmaj7 | Gm7 | Am7 | D7 | Gm7 | C7 | Fmaj7 | Edim A7): chord tones on the
# beats, a chromatic step into each change
pack.bass("Part B Walk", "Upright", " | ".join([
    w("3", "5", "7", "#3"), w("4", "6", "1", "#4"), w("5", "3", "2", "#1"), w("1", "#3", "5", "#4"),
    w("4", "6-", "5-", "#6-"), w("7-", "2", "6-", "2"), w("3", "2", "1", "#1"), w("2", "4", "5-", "2")]))
# the pedal under the cascade: the D held on 1, its A on 3, the D again on the "and" of 4, each
# bar louder; the last bar four bombs and a C♯ into the loop
def pedal(v):
    return " ".join([N(f"1!@{v}", 6), R(2), N(f"5-@{v - 6}", 4), N(f"1@{v - 10}", 2), R(2)])


pack.bass("Pedal Fifths", "Upright", " | ".join([
    pedal(80), pedal(92), pedal(106),
    " ".join([N("1!@122", 3, 1), N("5-@116", 3, 1), N("1@120", 3, 1), N("5-@110", 2), N("#7-@114", 2)])]))
# the intro's changes in a 3-3-2 Latin figure (Dm | B♭maj7 | E♭maj7 | Edim A7): root and fifth,
# the E♭ a half step over the home D, a step into each next root
pack.bass("Slip Tumbao", "Upright", " | ".join([
    " ".join([N("1!@108", 3), N("5-@96", 3), N("1@100", 2), N("5-@96", 3), N("1@98", 3), N("7-@96", 2)]),
    " ".join([N("6-!@108", 3), N("3@96", 3), N("6-@100", 2), N("3@96", 3), N("6-@98", 3), N("1@96", 2)]),
    " ".join([N("#1!@110", 3), N("6-@98", 3), N("#1@102", 2), N("6-@98", 3), N("#1@100", 3), N("2@98", 2)]),
    " ".join([N("2!@108", 3), N("6-@96", 3), N("2@100", 2), N("5-!@108", 3), N("2@98", 3), N("#7-@100", 2)])]))
# the waltz's drone in 6/8 (four 12-step bars): the D held a dotted quarter, the fifth and the
# root after; the C, the G and F, and a climb back C♯… into the D, louder each bar
pack.bass("Waltz Drone", "Upright", " ".join([
    N("1!@100", 6), N("5-@92", 4), N("1@88", 2),
    N("1!@104", 6), N("7-@94", 4), N("5-@90", 2),
    N("4!@108", 6), N("3@96", 4), N("2@94", 2),
    N("1!@112", 6), N("5-@100", 2), N("6-@102", 2), N("#7-@106", 2)]))
# the climax's drive: the D in eighths with the fifth and a C♯ kicking, swelling across four
# bars from soft to full, the last bar bombs
def drive(start, end):
    return ramp("1! . 1 . 5- . 1 . 1 . 5- . 1 . #7- .", start, end)


pack.bass("Climax Pedal", "Upright", " | ".join([
    drive(74, 88), drive(90, 104), drive(106, 118),
    " ".join([N("1!@124", 4), N("5-@118", 2, 2), N("1@122", 2, 2), N("#7-@116", 2), N("1@124", 2)])]))

# --- lead: the right hand (degree 1 is D4; "-" the octave under, "+" the one over) -------------
# Scenery's ballad over the A theme: few notes, soft, each behind the beat, room before the loop
pack.lead("Scenery Ballad", "Grand piano", " ".join([
    ph("./4 5@74>10/6 4@70>8/2 3@68>8/4", 1),            # Dm: A G F
    ph("2@72>10/6 ./2 #7-@70>8/4 2@72>8/4", 1),           # Edim A7: E, the C♯, E
    ph("3@76>10/8 5@80>8/4 7@74>8/4", 1),                 # B♭maj7: F, A, the ninth C
    ph("1+@82>10/10 ./6", 1),                             # Dm: the high D, held
    ph("./2 6@78>8/4 4@74>8/4 2@70>10/6", 1),             # Edim: B♭ G E
    ph("#7-@72>8/4 2@74>8/4 5@78>8/4 4@76>8/4", 1),       # A7: C♯ E A G
    ph("3@74>10/6 2@70>8/2 1@68>10/8", 1),                # Dm: F E D
    ph("./4 #7-@66>10/4 6-@64>8/4 5-@62>10/4", 1)]))      # Edim A7: C♯ B♭ A, into the loop
# bop eighths over the B theme, up-tempo: chord tones, chromatic notes snapped in early, the
# off-beats leaned on, a breath before the turnaround
pack.lead("Early Lines", "Grand piano", " ".join([
    ph(". 3 5 7 2+ 1+ 7 5", 1, 100, 8),                   # Fmaj7: up the chord
    ph("4 6 1+ 3+ 2+ 1+ 6 #4<8", 1, 100, 8),              # Gm7: G♯ into the A
    ph("5 7 2+ 4+ 3+ 2+ 1+ #7<8", 1, 100, 8),             # Am7: C♯ into the D
    ph("1+ #3+ 5+ 1+ 7 5 #3 1", 1, 100, 8),               # D7: the F♯s
    ph("4!/3 ./1 . 6 1+ 3+ 2+ 1+", 1, 100, 8),            # Gm7: a jab, then up
    ph("7 6 4 2 7- 2 4 6", 1, 100, 8),                    # C7: down and up its tones
    ph("5!/3 ./1 3 5 7 2+ 1+ 7", 1, 100, 8),              # Fmaj7
    ph("6 4 2 #7- 2 4 5 .", 1, 100, 8)]))                 # Edim A7: the turnaround, a breath
# the cascade: the D minor pentatonic in sixteenths, each bar climbing higher and louder, the last
# falling from the A5 to a low D bomb
pack.lead("Pentatonic Cascade", "Grand piano", " ".join([
    ramp("5 7 1+ 3+ 1+ 7 5 4 3 4 5 7 5 4 3 1", 66, 80),
    ramp("7 1+ 3+ 4+ 3+ 1+ 7 5 4 5 7 1+ 7 5 4 3", 82, 96),
    ramp("1+ 3+ 4+ 5+ 4+ 3+ 1+ 7 1+ 3+ 4+ 5+ 7+ 5+ 4+ 3+", 98, 112),
    ramp("5+! _ 4+ 3+ 1+ 7 5 4 3 1 7- 5- 1-! _ _ .", 114, 124)]))
# the slips over the intro's changes: D minor's pentatonic, B♭maj7 up its tones, then E♭maj7's
# arpeggio a half step over home (the degrees raised), Edim and A7 climbing to the A
pack.lead("Side-Slip Run", "Grand piano", " ".join([
    ramp("1 3 4 5 7 5 4 3 1 3 4 5 7 1+ 7 5", 84, 96),
    ramp("3 5 7 2+ 3+ 2+ 7 5 3 5 7 1+ 2+ 1+ 7 5", 92, 102),
    ramp("#1 4 6 1+ 3+ 1+ 6 4 #1 4 6 1+ 3+ 4+ 3+ 1+", 100, 110),
    ramp("2 4 6 #7 2+ #7 6 4 #7 2+ 4+ 5+!@120 _ _ . .", 104, 116)]))
# the waltz's cells in 6/8 (four 12-step bars): pentatonic triplets up and down, a bar higher
# each time and louder, the last a long A and the D
pack.lead("Waltz Cells", "Grand piano", ph(
    "1@80 3@80 4@82 5@84 4@82 3@80 "                     # D F G A G F
    "5@90 7@92 1+@94 3+@96 1+@94 7@92 "                  # A C D F D C
    "4+@104 3+@104 1+@106 7@108 5@106 4@104 "            # G F D C A G, from the top
    "5!@118/4 3@110 1@114/4 .", 3))                      # the long A, F, the D
# the climax: the A tremolo in octaves swelling, the B♭ a half step over, the A again at full,
# then falling fourths G5 D5 A4 E4 B♭3 F3 to the low D
pack.lead("Tremolo Climax", "Grand piano", " ".join([
    ramp("5 5+ 5 5+ 5 5+ 5 5+ 5 5+ 5 5+ 5 5+ 5 5+", 70, 90),
    ramp("6 6+ 6 6+ 6 6+ 6 6+ 6 6+ 6 6+ 6 6+ 6 6+", 92, 106),
    ramp("5 5+ 5 5+ 5 5+ 5 5+ 5 5+ 5 5+ 5 5+ 5 5+", 108, 122),
    ramp("4+ 1+ 5 2 6- 3- . 1-!@124 _ _ _ _ _ _ . .", 124, 120)]))

# --- chords: the left hand, semitones from D3; A and B forms of a chord so a re-hit is struck ---
V = {
    "Dm9": ("c", [3, 7, 10, 14]), "Dm9B": ("c", [-2, 2, 3, 7]), "Dm6": ("c", [3, 7, 9, 12]),
    "Edim": ("c", [2, 5, 8, 11]), "EdimB": ("c", [-1, 2, 5, 8]),               # E G B♭ D♭
    "A7": ("c", [-5, -1, 5, 7]), "A7b9": ("c", [-5, -1, 5, 8]),                # A C♯ G (A / B♭)
    "Bbmaj7": ("c", [-4, 0, 3, 7]), "Bbmaj7B": ("c", [7, 12, 15, 20]),
    "Ebmaj7": ("c", [1, 5, 8, 12]), "Ebmaj7B": ("c", [5, 8, 12, 13]),          # E♭ G B♭ D
    "Fmaj7": ("c", [3, 7, 10, 14]), "Fmaj7B": ("c", [-2, 2, 3, 7]),
    "Gm7": ("c", [-4, 0, 3, 7]), "Gm7B": ("c", [3, 7, 8, 12]),
    "Am7": ("c", [-2, 2, 5, 7]), "Am7B": ("c", [5, 7, 10, 14]),
    "D7": ("c", [-2, 2, 4, 7]), "D7B": ("c", [4, 7, 10, 14]),                 # C E F♯ A
    "C7": ("c", [-4, 0, 2, 7]), "C7B": ("c", [2, 8, 12, 17]),
    # the fourths (Tyner's): "So What" on D, stacks on E, G and A, the same a half step up and
    # down for the slips, and the low root-fifth bomb
    "SW": ("c", [0, 5, 10, 15, 19]), "Qa": ("c", [2, 7, 12, 17]), "Qc": ("c", [5, 10, 15, 20]),
    "Qd": ("c", [7, 12, 17, 22]), "SWup": ("c", [1, 6, 11, 16, 20]), "QaUp": ("c", [3, 8, 13, 18]),
    "QdUp": ("c", [8, 13, 18, 23]), "SWdn": ("c", [-1, 4, 9, 14, 18]), "P": ("c", [-12, -5, 0]),
}
# Scenery's left hand: the chord struck on every beat, soft and short, the bar of two chords
# split at 3
def quarters(a, b=None):
    b = b or a
    return bar(" ".join([C("@" + a, 3, 1), C("@" + a, 3, 1), C("@" + b, 3, 1), C("@" + b, 3, 1)]))


pack.chords("Scenery Quarters", "Grand piano", " | ".join([
    quarters("Dm9"), quarters("Edim", "A7b9"), quarters("Bbmaj7"), quarters("Dm6"),
    quarters("Edim"), quarters("A7b9"), quarters("Dm9B"), quarters("EdimB", "A7")]), V)
# comping the B theme on the beat and the "and", the even bars pushed to the "and" of 1
def charleston(a, b, pushed):
    if pushed:
        return bar(" ".join([R(2), C("@" + a, 2, 2), C("@" + a, 2), C("@" + b, 2, 4), C("@" + b, 2)]))
    return bar(" ".join([C("@" + a, 2, 4), C("@" + a, 2), C("@" + b, 2, 4), C("@" + b, 2)]))


PART_B = [("Fmaj7", "Fmaj7B"), ("Gm7", "Gm7B"), ("Am7", "Am7B"), ("D7", "D7B"),
          ("Gm7B", "Gm7"), ("C7", "C7B"), ("Fmaj7B", "Fmaj7"), ("Edim", "A7b9")]
pack.chords("Part B Comp", "Grand piano", " | ".join(
    charleston(a, b, k % 2 == 1) for k, (a, b) in enumerate(PART_B)), V)
# the cascade's fourths: a bar of two held, a bar of stabs, a bar of eighths climbing, then the
# bomb and the half-step slips at full
pack.chords("Fourths Climb", "Grand piano", " | ".join([
    bar(" ".join([C("@SW", 6, 2), C("@Qa", 6, 2)])),
    bar(" ".join([C("@SW", 4, 2), C("@Qc", 2, 2), C("@Qa", 3, 3)])),
    bar(" ".join([C("@Qa", 1, 1), C("@Qc", 1, 1), C("@Qd", 1, 1), C("@SW", 1, 1),
                  C("@Qa", 1, 1), C("@Qc", 1, 1), C("@Qd", 1, 1), C("@SW", 1, 1)])),
    bar(" ".join([C("@P", 2), C("@SWup", 2), C("@SW", 2), C("@SWup", 2), C("@SW", 4), C("@P", 3, 1)]))]), V)
# the intro's changes in 3-3-2 (Dm | B♭maj7 | E♭maj7 | Edim A7), each chord's forms alternating
def tresillo(a, b, c=None, d=None):
    c, d = c or a, d or b
    return bar(" ".join([C("@" + a, 3), C("@" + b, 3), C("@" + a, 2), C("@" + d, 3), C("@" + c, 3), C("@" + d, 2)]))


pack.chords("Slip Fourths", "Grand piano", " | ".join([
    tresillo("Dm9", "Dm9B"), tresillo("Bbmaj7", "Bbmaj7B"), tresillo("Ebmaj7", "Ebmaj7B"),
    tresillo("Edim", "EdimB", "A7b9", "A7")]), V)
# the waltz in 6/8 (four 12-step bars): a held chord on 1 and a stab on the second dotted
# quarter, the fourths shifting, the last bar slipping up and back
pack.chords("Waltz Fourths", "Grand piano", " ".join([
    C("@SW", 5, 1), C("@Qd", 4, 2), C("@Qa", 5, 1), C("@Qc", 4, 2),
    C("@SW", 5, 1), C("@Qd", 4, 2), C("@SWup", 3, 1), C("@SW", 6, 2)]), V)
# the climax: the fourths in sixteenth tremolos, the slip a half step up, then planing down
# through the half steps to the bomb
def tremolo(a, b):
    return bar(" ".join([C("@" + a, 1), C("@" + b, 1)] * 8))


pack.chords("Planing Climax", "Grand piano", " | ".join([
    tremolo("SW", "Qa"), tremolo("SWup", "QaUp"), tremolo("Qd", "SW"),
    bar(" ".join([C("@SWup", 2), C("@SW", 2), C("@SWdn", 2), C("@SW", 2), C("@P", 6, 2)]))]), V)

# the templates: the trio's medium-up swing, and Scenery's ballad
# the trio's band: the jazz kit, the upright, the grand piano for both hands
TRIO = {"drums1": "JAZZ", "drums2": "JAZZ_CRASH", "drums3": "BRUSH_RIDE",
        "bass": "Upright", "chords": "Grand piano", "lead": "Grand piano"}
pack.template(180, "D", "Natural Minor", swing=60, swing_eighths=True, echo=0.1, sounds=TRIO,
              sections=[("HEAD", 8), ("CASCADE", 4), ("SLIP", 4), ("CLIMAX", 4), ("HEAD OUT", 8)],
              about="Piano trio after Ryo Fukui in D minor: medium-up, swung eighths, a small room.")
pack.template(70, "D", "Natural Minor", name="Fukui · Scenery", swing=56, swing_eighths=True, echo=0.3,
              sounds=dict(TRIO, drums1="BRUSH_RIDE"),
              sections=[("INTRO", 4), ("THEME A", 8), ("THEME B", 8), ("SOLO", 8), ("THEME A", 8)],
              about="Scenery's ballad: slow, a lilt on the eighths, the piano in a warm hall.")

if __name__ == "__main__":
    pack.done()
