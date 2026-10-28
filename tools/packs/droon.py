#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret "Droon" pack: after Sonder, the R&B trio of Brent Faiyaz and the producers Dpat
# and Atu (the EP *Into*, 2017: Feel, Lovely, Sirens, Too Fast, Baldwin Park, Searchin', Care;
# the single What You Heard, 2018), five pattern presets each for the drums, the bass, the lead
# and the chords, laid out as a USB stick holds them (../patternkit.py). Written in scale
# degrees for a NATURAL MINOR key: every Into song is in a minor key. Made for E minor at 74,
# Too Fast's key and tempo; Care and Searchin' are in Bb minor (the second template). The
# songs' progressions (Too Fast's and What You Heard's chord sheets, Care's tab, Ultimate
# Guitar) as reference; every line, riff and rhythm here is original
# (tools/genre-research/droon.md).
#
# The feel: slow, spacious and moody: sparse kicks, rimshots and snares left alone in the
# room, the 808's tail lengthened, quarter- and dotted-8th hats instead of busy 16ths (the
# template's ECHO is the reverb); subs that slide, a finger bass in Care's 3-3-2 lilt; clean
# chorused guitar with hammer-on grace notes (<12), a Rhodes, a falsetto line laid back
# (>10–14), ghostly vocal pads.
#   python3 tools/packs/droon.py

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/droon/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "droon")
sys.path.insert(0, HERE)
from patternkit import MINOR, Pack, N, C, R  # noqa: E402

pack = Pack("Droon", PACK, MINOR)


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
    # the key's own chords as a guitarist on Into voices them: open, with added 9ths
    "i9": v("E3 B3 D4 F#4 G4"), "iadd9": v("E3 B3 E4 F#4 G4"), "i7": v("E3 G3 B3 D4"),
    "VIIadd9": v("F#3 A3 D4 E4"), "VII6": v("F#3 A3 B3 D4 F#4"), "v7": v("B3 D4 F#4 A4"),
    "VImaj7": v("E3 G3 B3 C4"), "VImaj9": v("E3 B3 C4 D4 G4"), "IIImaj7": v("F#3 B3 D4 G4"),
    "III": v("G3 B3 D4 G4"), "iv7": v("E3 G3 A3 C4"), "iv9": v("A3 C4 E4 G4 B4"),
    "ivadd9": v("E3 A3 B3 C4 E4"), "v": v("F#3 B3 D4 F#4"),
    # from outside the key: Too Fast's intro F#m (the Dorian ii), What You Heard's major V7b9
    "ii7": v("F#3 A3 C#4 E4"), "V7b9": v("A3 C4 D#4 F#4"),
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
# DRUMS: the backbeats are the accented steps; the ECHO of the template is the room
# Too Fast's drift: the 808 with its tail long and its top dulled, a kick and a half a bar,
# snare on two and four with a clap only on the first, hats in quarters with a pickup
pack.drums("Too Fast Drift", "TR808", {
    "KICK":  "X... .... .x.. .... | X... ..x. .... ....",
    "SNARE": ".... X... .... X... | .... X... .... X...",
    "CLAP":  ".... X... .... .... | .... X... .... ....",
    "HAT":   "x... x... x... x..x | x... x... x... x.xx",
    "OPEN":  ".... .... .... .... | .... .... ..x. ....",
}, mods={"SHAPE/LENGTH": 2000, "TONE/CUTOFF": -1200})
# Care's lilt: hats in dotted 8ths (3 + 3 + 2), the slow pulse leaning toward a triplet feel,
# a rim before the turn, the SP-1200 darkened
pack.drums("Care Lilt", "SP1200", {
    "KICK":  "X... .... ..x. .... | X... .... .... ..x.",
    "SNARE": ".... X... .... X... | .... X... .... X...",
    "HAT":   "x..x ..x. x..x ..x. | x..x ..x. x..x ..x.",
    "PERC":  ".... .... .... ...x | .... .... ...x ....",
}, mods={"TONE/CUTOFF": -1800})
# Sirens, kept minimal: a kick, a rimshot on three alone in the room, hats on the off-beats,
# a low tom answering at the end; the acoustic kit dark and ringing
pack.drums("Sirens Space", "BLACK_PEARL", {
    "KICK":  "X... .... .... .... | X... .... ..x. ....",
    "PERC":  ".... .... X... .... | .... .... X... ....",
    "HAT":   "..x. ..x. ..x. ..x. | ..x. ..x. ..x. ....",
    "TOM":   ".... .... .... .... | .... .... .... ..x.",
}, mods={"TONE/CUTOFF": -3000, "SHAPE/LENGTH": 1200})
# Searchin's knock: snare and clap together, the kick skipping around them, off-beat 16th
# hats like a shaker (the downbeats left empty)
pack.drums("Searchin Knock", "ROOM", {
    "KICK":  "X... ...x ..x. .... | X... .... .xx. ....",
    "SNARE": ".... X... .... X... | .... X... .... X...",
    "CLAP":  ".... X... .... X... | .... X... .... X...",
    "HAT":   ".xxx .xxx .xxx .xxx | .xxx .xxx .xxx .xxx",
}, mods={"TONE/CUTOFF": -1800})
# Lovely's half time: the snare once a bar on three, the kick on one and a late "a", 8th hats
# doubling the pace over it, a ghost snare into the loop
pack.drums("Lovely Halftime", "RED_ZEPPELIN", {
    "KICK":  "X... .... .... ..x. | X..x .... .... ....",
    "SNARE": ".... .... X... .... | .... .... X... ...x",
    "HAT":   "x.x. x.x. x.x. x.xx | x.x. x.x. x.x. x.x.",
}, mods={"TONE/CUTOFF": -2400})

# =========================================================================================
# BASS (degree 1 is E2)
# Too Fast's i – VII | i – v | i – VII | i – VI on the 808: each root held, the octave above
# struck and slid down into the next chord
pack.bass("Too Fast Sub", "808 · Monosynth", ph(
    "1@104>8/6 ./1 1+~@72/1 7-@96>8/6 ./2 "
    "1@104>8/6 ./1 1+~@72/1 5-@96>8/6 ./1 7-~@70/1 "
    "1@104>8/6 ./1 1+~@72/1 7-@96>8/6 ./2 "
    "1@104>8/6 ./1 1+~@72/1 6-@96>8/8", 4))
# Care's iv – v – i – i in its 3-3-2 lilt on a finger bass, a soft second stroke, the octave,
# a hammered grace note into the tonic, a run up into the top
pack.bass("Care Line", "Finger bass", ph(
    "4-@96>8/3 4-@50>8/3 4@72 4-@88>8/3 3@60/3 2@64 "
    "5-@96>8/3 5-@50>8/3 5@72 5-@88>8/3 4@60/3 7-@64 "
    "1@96>8/3 1@50>8/3 1+@72 1@88>8/3 7-@62<10/1 1@74 3-@60 "
    "1@96>8/3 ./3 5-@72 7-@84>8/3 1@64/1 2@68 3@70", 4),
    mods={"FILTER/CUTOFF": -1800})
# What You Heard's VImaj7 – IIImaj7 – VImaj7 – iv V7 on a fretless: roots behind the beat,
# fifths and passing tones gliding between them, the V7's D#
pack.bass("Heard Walk", "Fretless", ph(
    "6-@94>10/6 ./2 3@76>8 5@72 6-@84>8/4 "
    "3-@94>10/6 ./2 7-@76>8 2@72 3-@84>8 5-@76 "
    "6-@94>10/8 5-@80>8 6-@78 7-@82/4 "
    "4-@94>10/6 ./2 5-@96>8/4 #7-@80 5-@74", 4),
    mods={"ENVELOPE/RELEASE": 900})
# Searchin's i – VI pulse: a dark synth bass in late 8ths, the octave flicked, a pickup into
# the next bar
pack.bass("Searchin Pulse", "Synth bass", ph(
    "1@100>10 ./2 1@70>10/1 ./1 1@84>10 ./2 1+@74/1 ./1 1@90>10 3-@70/1 5-@74/1 "
    "6-@100>10 ./2 6-@70>10/1 ./1 6-@84>10 ./2 6@74/1 ./1 6-@90>10 5-@70/1 7-@74/1", 2),
    mods={"FILTER/CUTOFF": -3000, "FILTER/RESO": 30})
# Sirens' drone: a sine sub, two bars on the tonic and two on the VI, sliding between them
pack.bass("Sirens Drone", "Sine sub", ph(
    "1@110>10/16 1@96>10/12 ./2 1~@80 "
    "6-@110>10/16 6-@96>10/12 ./2 7-~@80", 4))

# =========================================================================================
# LEAD (degree 1 is E4)
# a Too Fast-style clean guitar over i – VII | i – v: chorused, each phrase flicked in with a
# hammered grace note (<12), a breath at the end of each bar
pack.lead("Too Fast Guitar", "Guitar · Chorus", ph(
    "5@80>6 1+@74<12/1 2+@84/3 1+@70 7@74 5@78>6/4 ./2 "
    "3@76>6 4@70<12/1 5@84/3 3@72 2@70 7-@74>8/4 ./2", 2),
    mods={"MOTION/CHORUS": 600, "ENVELOPE/RELEASE": 900})
# a lick in Care's manner: minor pentatonic hammer-ons (the grace note <12 before each target),
# a slide into the 3rd, a held note with vibrato
pack.lead("Care Lick", "Guitar · Clean", ph(
    "4-@70<12/1 5-@82 7-@72<12/1 1@84 3@70<12/1 4@86/3 3@72/1 2~@70/1 3@74/4 "
    "./2 5@78<12/1 6@86 5@74/1 3~@72/1 4@80>6/5 3@70 1@68>8", 2),
    mods={"MOTION/VIBRATO": 40, "MOTION/CHORUS": 300})
# a falsetto line in Feel's mood: long notes laid well behind the beat (>10–14), a slide down
# into the 5th, half a bar of air
pack.lead("Feel Falsetto", "Voice oohs", ph(
    "./4 5@64>14/6 6@70>10 5@66>12/4 "
    "3@68>12/8 2@62>14/4 ./4 "
    "./2 1+@72>10/6 7@68>12 5@66>12 6~@64 5@70>10 "
    "3@66>12/10 ./6", 4),
    mods={"ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 2400, "MOTION/VIBRATO": 18})
# Into's keys: a Rhodes line rising through the i9's tones and falling over the VI, soft
# and chorused
pack.lead("Into Keys", "Rhodes · Suitcase", ph(
    "1@74 3@70 5@76 7@82>6/4 5@70 ./4 "
    "6@78 5@72 3@70 2@74>6/4 7-@66 ./4", 2),
    mods={"ENVELOPE/RELEASE": 1200, "MOTION/CHORUS": 500})
# Lovely's synth: slow glides between long notes (the lead's own Monosynth; no MODS in a pack)
pack.lead("Lovely Glide", "Calf Monosynth", ph(
    "1+@90/4 7~@80/4 5@84/6 ./2 "
    "3~@78/4 4@84/4 2~@74/4 1@82/4", 2))

# =========================================================================================
# CHORDS
# Too Fast's refrain (i – VII, i – v, i – VII, i – VI) on the chorused guitar: a chord a half
# bar, struck, held and caught again on the "a" of two
def half(name):
    return [(name, 6), (".", 1), (name, 1)]


pack.chords("Too Fast Strum", "Guitar · Chorus", comp(
    half("iadd9") + half("VIIadd9"), half("iadd9") + half("v"),
    half("iadd9") + half("VII6"), half("iadd9") + half("VImaj7")), V,
    mods={"MOTION/CHORUS": 700, "ENVELOPE/RELEASE": 1200})
# Care's chorus (iv add9 – v – i7 – i7) in its 3-3-2 strum on a clean guitar
def lilt(name):
    return [(name, 2), (".", 1), (name, 2), (".", 1), (name, 1), (".", 1)] * 2


pack.chords("Care Chorus", "Guitar · Clean", comp(
    lilt("ivadd9"), lilt("v"), lilt("i7"), lilt("i9")), V,
    mods={"MOTION/CHORUS": 400})
# What You Heard's VImaj9 – IIImaj7 – VImaj9 – iv9 V7b9 on a Rhodes: each chord pushed in a
# 16th early and held across the bar line
pack.chords("Heard Rhodes", "Rhodes · Suitcase", comp(
    [("VImaj9", 14), (".", 1), ("IIImaj7", 1)], [("=", 13), (".", 2), ("VImaj9", 1)],
    [("=", 13), (".", 2), ("iv9", 1)], [("=", 7), ("V7b9", 7), (".", 2)]), V,
    mods={"ENVELOPE/RELEASE": 900, "MOTION/CHORUS": 500}, ties="all")
# Too Fast's intro (iv – i | VI – ii | i – v | i) as ghostly backing vocals: a vocal pad,
# a chord a half bar, slow in and slow out
pack.chords("Intro Ghosts", "Pad · Vocal", comp(
    [("iv7", 8), ("i7", 8)], [("VImaj7", 8), ("ii7", 8)], [("i9", 8), ("v7", 8)],
    [("iadd9", 15), (".", 1)]), V,
    mods={"ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 3000}, ties="all")
# Too Fast's interlude (i – VI – iv – VI | III – iv – III – i) on a warm grand, a chord a half
# bar: struck on one, again on the "and" of two
def piano(name):
    return [(name, 4), (".", 2), (name, 2)]


pack.chords("Interlude Keys", "Grand · Warm", comp(
    piano("i9") + piano("VImaj9"), piano("iv9") + piano("VImaj7"),
    piano("III") + piano("iv7"), piano("IIImaj7") + piano("i7")), V,
    mods={"ENVELOPE/RELEASE": 1500})

# the templates: Too Fast's key and tempo, and Care's and Searchin's Bb minor at a slower
# pulse with the eighths swung toward the triplet (the projects dialog's TEMPLATES)
pack.template(74, "E", "Natural Minor", swing=58, phaser=0.1, echo=0.35, heavy=0.2,
              about="Sonder's moody R&B at 74 in E minor (Too Fast): spacious drums in a long room, a lazy 16th swing.")
pack.template(64, "Bb", "Natural Minor", name="Droon · Care", swing=62, swing_eighths=True, echo=0.4, heavy=0.15,
              about="Care's and Searchin's Bb minor, slower, the eighths swung toward a triplet lilt, a deep room.")

if __name__ == "__main__":
    pack.done()
