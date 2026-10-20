#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret "R&B" pack: contemporary R&B after Jorja Smith (Be Honest, Teenage Fantasy, Blue
# Lights, Don't Watch Me Cry) and Snoh Aalegra (Fool For You, Situationship, Whoa, Lost You,
# I Want You Around), five pattern presets each for the drums, the bass, the lead and the
# chords, laid out as a USB stick holds them (../patternkit.py). Written in scale degrees for a
# NATURAL MINOR key, made for E minor (Be Honest's, Teenage Fantasy's and Fool For You's key);
# the songs in other keys are moved onto its degrees (tools/genre-research/rnb.md).
#
# The songs' progressions (their chord sheets, Ultimate Guitar) as reference; every line,
# melody and rhythm here is original. The playing: laid-back pockets with ghost notes (a
# drum chart has no per-hit velocity or nudge, so the backbeats are the accented steps, the
# ghosts the plain ones, and the drag comes from the hits placed a 16th behind and the
# template's swing), basses and leads played behind the beat (>6–14), vocal-like leads with
# melismatic runs, grace notes snapped in early (<4–12) and scoops (~), extended voicings
# (maj9, min9, 11, 13, 7#9, 7b9) on Rhodes, a warm grand, a Wurlitzer, strings and a pad.
#   python3 tools/packs/rnb.py

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/rnb/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "rnb")
sys.path.insert(0, HERE)
import patternkit  # noqa: E402
from patternkit import MINOR, Pack, N, C, R  # noqa: E402

pack = Pack("R&B", PACK, MINOR)


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


# --- voicings: note names, kept as semitones from the chord base (degree I at octave 0: E3 in
# E minor), the ("c", […]) form of patternkit; they follow the session's key --------------------
NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
BASE = 52  # E3: ChordMachine's base C3 (48) plus the root E (4)


def v(notes):
    """("c", semitones from E3) for a voicing written "G3 B3 D4 F#4"."""
    out = []
    for note in notes.split():
        letter, accidental, octave = re.fullmatch(r"([A-G])([b#]?)(\d)", note).groups()
        midi = 12 * (int(octave) + 1) + NAMES[letter] + {"b": -1, "#": 1, "": 0}[accidental]
        if midi < BASE:
            raise ValueError(f"{note} is under the chord base")
        out.append(midi - BASE)
    return ("c", out)


V = {
    # E minor's own chords, extended: i9, i11, iv9, VImaj9, VImaj7, VIImaj9 (rootless), VII6/9
    "i9": v("E3 B3 D4 F#4 G4"), "i11": v("E3 A3 B3 D4 G4"), "i7": v("G3 B3 D4 E4"),
    "iv9": v("A3 C4 E4 G4 B4"), "VImaj9": v("E3 B3 C4 D4 G4"), "VImaj7": v("C4 E4 G4 B4"),
    "VIImaj9": v("F#3 A3 C#4 E4"), "VII69": v("F#3 B3 D4 E4 A4"), "v7": v("F#3 A3 B3 D4"),
    # from outside the key: the major V with its altered tones (harmonic minor), the Dorian IV13
    # (Fool For You's F#m(b9)/A shape), the Dorian ii11 (Situationship's), Whoa's minor ♭vii9
    "V7#9": v("B3 D#4 A4 D5"), "V7b9": v("A3 C4 D#4 F#4"), "V7": v("A3 B3 D#4 F#4"),
    "IV13": v("A3 C#4 F#4 G4 B4"), "ii11": v("F#3 B3 E4 A4 C#5"), "bvii9": v("F3 A3 C4 E4"),
}


def comp(*bars):
    """Chord bars, each a list of (voicing, steps), "." a rest, "=" the chord before going on;
    checked to sixteen steps a bar."""
    out = []
    for chords in bars:
        if sum(steps for _, steps in chords) != 16:
            raise ValueError(f"a chord bar of {sum(s for _, s in chords)} steps: {chords}")
        out.append(" ".join(R(steps) if name == "." else " ".join(["="] * steps) if name == "="
                            else C("@" + name, steps) for name, steps in chords))
    return " | ".join(out)


# =========================================================================================
# DRUMS. Every backbeat is an accented step (X), the ghosts and the hats around it plain (x).
# Be Honest's pocket: a soft acoustic kit, the kick on one and pushed to the "a" of two, the
# snare ghosting a 16th before and after each backbeat, 8th hats with a 16th lift
pack.drums("Honest Pocket", "BLACK_PEARL", {
    "KICK":  "X... .... ..x. ...x | X... ..x. ..x. ....",
    "SNARE": "...x X..x ..x. X..x | .... X... .x.x X...",
    "HAT":   "x.x. x.x. x.x. x.xx | x.x. x.x. x.x. x...",
    "OPEN":  ".... .... .... .... | .... .... .... ..x.",
}, mods={"TONE/CUTOFF": -1500})
# the contemporary 808 groove (H.E.R., Snoh's uptempo cuts): a long 808 kick, snare and clap
# stacked on two and four, hats in 8ths with a 16th roll into the turn, rim clicks off the beat
pack.drums("Lazy 808", "TR808", {
    "KICK":  "X... .... x.x. .... | X..x .... ..x. ....",
    "SNARE": ".... X... .... X... | .... X... .... X...",
    "CLAP":  ".... X... .... X... | .... X... .... X...",
    "HAT":   "x.x. x.x. x.x. xxx. | x.x. x.x. x.xx x.x.",
    "PERC":  "...x .... ..x. .... | ...x .... .... .x..",
}, mods={"SHAPE/LENGTH": 1200})
# Teenage Fantasy's neo-soul lean on the SP-1200: the kick late on the "a", the snare dragged
# by a ghost a 16th after it, a clap thickening the four; play it with the template's swing
pack.drums("Teenage Swing", "SP1200", {
    "KICK":  "X... ...x ..x. .... | X... .... x..x ....",
    "SNARE": ".... X..x .... X... | .... X... ...x X..x",
    "CLAP":  ".... .... .... X... | .... .... .... X...",
    "HAT":   "x.x. x.x. x.x. x... | x.x. x.x. x.x. x.x.",
    "OPEN":  ".... .... .... ..x. | .... .... .... ....",
})
# a slow-jam ballad (Fool For You, Lost You): half time, the rimshot on three, the kick on one
# and the "a" of two, soft 16th hats, a ghost snare or two, the room kit darkened
pack.drums("Rimshot Ballad", "ROOM", {
    "KICK":  "X... ...x .... ..x. | X... .... .x.. ....",
    "PERC":  ".... .... X... .... | .... .... X... ..x.",
    "SNARE": ".... ..x. .... x... | .... .... ...x ....",
    "HAT":   "xxxx xxxx xxxx xxxx | xxxx xxxx xxxx xxxx",
}, mods={"TONE/CUTOFF": -2400})
# Blue Lights' late-90s clap: the Linn's clap over its snare on two and four, a pickup clap at
# the end of the loop, hats skipping in 16ths, an open hat before the top
pack.drums("Nineties Clap", "LINN", {
    "KICK":  "X... ..x. ..x. .... | X... ..x. .x.. ..x.",
    "SNARE": ".... X... .... X... | .... X... .... X...",
    "CLAP":  ".... X... .... X... | .... X... .... X..x",
    "HAT":   "x.xx x.x. x.xx x.x. | x.xx x.x. x.xx x...",
    "OPEN":  ".... .... .... .... | .... .... .... ..x.",
    "PERC":  ".... .... .... .... | .x.. .... .... ....",
})

# =========================================================================================
# BASS (degree 1 is E2)
# Be Honest's VI – V – i: the 808 holding each root behind the beat, an octave dropped onto
# the tonic, the V's leading tone (D#) sliding up into it; the Monosynth glides the slides
pack.bass("Honest Sub", "808 · Monosynth", ph(
    "6-@100>6/12 ./2 6-~@84/2 "                 # C, held; slid into the B
    "5-@100>6/8 ./2 5-@80/2 ./2 #7-~@84/2 "     # B major: B, the D# sliding into the E
    "1@104>6/12 ./2 1+~@80/2 "                  # E, the octave dropping onto it
    "1@96>6/8 ./2 3-@84/2 5-@80/2 7-~@78/2", 4))  # E G B, D sliding home to the C
# Teenage Fantasy's iv – V7 – i – VII on a finger bass: a muted 16th after each root (@44),
# fills walking into the next chord, a chromatic G# back into the A
pack.bass("Fantasy Walk", "Finger bass", ph(
    "4-@96>8/3 4-@44/1 ./2 4@70/1 3@64/1 5-@94>8/3 5-@44/1 ./1 #7-@76/1 ./2 "
    "1@98>8/3 1@44/1 ./2 1+@70/1 7@64/1 7-@94>8/3 7-@44/1 ./1 6-@72/1 5-@70/1 #3-@74/1", 2),
    mods={"FILTER/CUTOFF": -1500})
# Fool For You's i9 – IV13 – VIImaj7 – v7 V7 on a fretless: long roots behind the beat, the
# Dorian C# in the IV, a melodic walk between the chords
pack.bass("Fool Fretless", "Fretless", ph(
    "1@96>10/6 5-@80>8 7-@84>8/4 1@78>6 2@74 "
    "4-@96>10/6 1@80>8 3@84>8/4 2@74 #6-@76 "
    "7-@96>10/6 4-@80>8 6-@84>8/4 7-@74 1@72 "
    "5-@94>10/6 2@80>8 #7-@84>8/4 5-@76>6 6-~@74", 4),
    mods={"ENVELOPE/RELEASE": 600, "FILTER/CUTOFF": -900})
# Don't Watch Me Cry's VII – i – VI – III: a synth bass bouncing root, ghost, octave pop, the
# downbeats leaning late
pack.bass("Cry Synth", "Synth bass", ph(
    "7-@100>6 ./1 7-@60/1 7@84/1 ./1 7-@70 1@100>6 ./1 1@60/1 1+@84/1 ./1 1@70 "
    "6-@100>6 ./1 6-@60/1 6@84/1 ./1 6-@70 3-@100>6 ./1 3-@60/1 3@84/1 ./1 5-@70", 2),
    mods={"FILTER/CUTOFF": -2400, "FILTER/RESO": 60})
# Situationship's i9 – ii11 vamp: a sine sub, a bar a root, each sliding up or down into the next
pack.bass("Situation Sub", "Sine sub", ph(
    "1@110>8/13 ./1 1~@84/2 "                   # E, slid up into the F#
    "2@110>8/13 ./1 2~@84/2", 2))               # F#, slid back to the E

# =========================================================================================
# LEAD (degree 1 is E4): vocal lines, every long note behind the beat
# Be Honest's hum over VI – V – i: a sigh from the B, the V's D# reached by a scoop, a melisma
# climbing the pentatonic to the D and falling home
pack.lead("Honest Hum", "Voice oohs", ph(
    "./4 5@70>12/4 6@76>10 5@72>8 3@68>10/4 "
    "4@72>8 3@70>8 2~@66>10 #7-@64>12/6 ./4 "
    "./2 1@70<6/1 3@74<4/1 5@80 7@88>6/6 5@76>8 6@72>8 "
    "5@74>10 3@70>8/1 2@66>8/1 1@72>12/8 ./4", 4),
    mods={"ENVELOPE/ATTACK": 1200, "ENVELOPE/RELEASE": 1200, "MOTION/VIBRATO": 24})
# Snoh Aalegra's strings over Fool For You's changes: a long line swelling up (@64 → 88), the
# Dorian C# on the IV13, the B7's D# at the end
pack.lead("Aalegra Strings", "Strings", ph(
    "5-@64>8/8 1@72>8/4 2@78>6/4 "
    "3@82>6/6 #6@88>6/6 5@80>8/4 "
    "5@84>6/8 4@76>8/4 3@72>8/4 "
    "2@74>8/8 #7-@80>6/6 ./2", 4),
    mods={"ENVELOPE/ATTACK": 3600, "ENVELOPE/RELEASE": 2400, "MOTION/VIBRATO": 10})
# a gliding synth line over Teenage Fantasy's iv – V7 | i – VII, slurred like a voice bending
# between notes (the lead's own Monosynth glides; it takes no MODS in a pack)
pack.lead("Fantasy Glide", "Calf Monosynth", ph(
    "6@86>6/4 5~@80 4@76 ./2 4~@78 #7-@72>8/4 "
    "1@82>8/4 3~@84 5@90/4 ./2 4@78/1 3@74/1 2@70>8", 2))
# Blue Lights' VI – VII – i – VII: a breathy flute singing short calls, a repeated note, a
# scoop down to the tonic
pack.lead("Blue Light Flute", "Flute", ph(
    "./2 3@70>10 3@66>10/1 5@78>8/3 6@74>8 5@70>10/6 "
    "./4 7-@68>10 1@74>8 3@80>6/4 2~@72 1@70>10", 2),
    mods={"MOTION/VIBRATO": 30, "ENVELOPE/ATTACK": 600})
# Don't Watch Me Cry's VII – i – VI – III: a Rhodes answering the voice in the gaps, each fill
# flicked in with two grace notes
pack.lead("Cry Answer", "Rhodes · Suitcase", ph(
    "./8 6@66<10/1 7@74/1 2+@84>6/4 1+@76 "
    "7@74>8 5@70>8/4 ./10 "
    "./8 3@64<10/1 4@70/1 5@80>6 3@72 1@68>8 "
    "2@70>8 7-@66>8 1@74>10/4 ./8", 4),
    mods={"ENVELOPE/RELEASE": 600})

# =========================================================================================
# CHORDS
# Be Honest's VImaj9 – V7#9/b9 – i9 on a Rhodes: a long chord, then re-struck on the "a" of two
# and on the "and" of three, the dominant turned from #9 to b9, a push into the top
pack.chords("Honest Rhodes", "Rhodes · Suitcase", comp(
    [("VImaj9", 6), (".", 1), ("VImaj9", 3), (".", 1), ("VImaj9", 4), (".", 1)],
    [("V7#9", 7), (".", 1), ("V7b9", 7), (".", 1)],
    [("i9", 10), (".", 1), ("i9", 4), (".", 1)],
    [(".", 2), ("i11", 4), (".", 2), ("i11", 3), (".", 1), ("V7b9", 3), (".", 1)]), V,
    mods={"ENVELOPE/RELEASE": 600, "MOTION/CHORUS": 400})
# Fool For You's i9 – IV13 – VIImaj9 – v7 V7b9 held by the strings, a bar each, bowed in slowly
pack.chords("Fool Strings", "Strings · Ensemble", comp(
    [("i9", 15), (".", 1)], [("IV13", 15), (".", 1)], [("VIImaj9", 15), (".", 1)],
    [("v7", 8), ("V7b9", 7), (".", 1)]), V,
    mods={"ENVELOPE/ATTACK": 1800, "ENVELOPE/RELEASE": 1800})
# Teenage Fantasy's iv9 – V7#9 | i9 – VII6/9 on a warm grand: hit, a stab on the "a" of two
# that anticipates the next chord, a second touch before the bar line
pack.chords("Fantasy Keys", "Grand · Warm", comp(
    [("iv9", 3), (".", 3), ("iv9", 1), ("V7#9", 5), (".", 1), ("V7#9", 2), (".", 1)],
    [("i9", 3), (".", 3), ("i9", 1), ("VII69", 5), (".", 2), ("VII69", 1), (".", 1)]), V,
    mods={"ENVELOPE/RELEASE": 900})
# Situationship's i9 – ii11 (the Dorian ii: stacked fourths over the F#) on a Wurlitzer, comped
# in a lazy long-short-short figure
pack.chords("Situation Wurli", "Wurlitzer", comp(
    [("i9", 6), (".", 2), ("i9", 2), (".", 1), ("i9", 4), (".", 1)],
    [("ii11", 6), (".", 2), ("ii11", 2), (".", 1), ("ii11", 3), (".", 2)]), V,
    mods={"FILTER/CUTOFF": -1200})
# Whoa's VImaj7 – V7 – ♭vii9 – i7, a bar each, on a warm pad that breathes in
pack.chords("Whoa Pads", "Pad · Warm", comp(
    [("VImaj7", 15), (".", 1)], [("V7", 15), (".", 1)], [("bvii9", 15), (".", 1)],
    [("i7", 15), (".", 1)]), V,
    mods={"ENVELOPE/ATTACK": 1200, "ENVELOPE/RELEASE": 2400})

# the templates: the pack's pocket at 86 in E minor with a lazy 16th swing, and the slow jam at
# Fool For You's 75 (the projects dialog's TEMPLATES)
pack.template(86, "E", "Natural Minor", swing=56, echo=0.25, heavy=0.25,
              about="Contemporary R&B at 86 in E minor (Jorja Smith's Be Honest key): a lazy 16th swing, a soft room.")
pack.template(75, "E", "Natural Minor", name="R&B · Slow Jam", swing=58, echo=0.35, heavy=0.15,
              about="Snoh Aalegra's slow jams (Fool For You) at 75 in E minor: deeper swing, a longer room for the strings.")

if __name__ == "__main__":
    pack.done()
