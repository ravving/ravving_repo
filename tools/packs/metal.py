#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret heavy metal pack: five pattern presets for each of the drums, the bass, the lead
# and the chords (see ../patternkit.py). Written in scale degrees for a NATURAL MINOR key, made
# for E minor (the open low string most of these riffs ride on). The progressions are the
# bands' (Ultimate Guitar's tabs and chord sheets, see the README): Paranoid's i VII III VII,
# The Trooper's and Fear of the Dark's i VI VII, Iron Man's riff, Master of Puppets' chromatic
# fall; the lines are original takes on them. Out of the key: the ♭2 (Phrygian), the ♭5, the
# raised 7th (harmonic minor), through ALTER and chromatic voicings.
#
# Velocity does the palm-muting: a chug at @70–84 under accented hits; the tremolo and the
# gallop lean on their first stroke.
#   python3 tools/packs/metal.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/metal/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "metal")
sys.path.insert(0, HERE)
from patternkit import MINOR, Pack, N, C, R, cpower  # noqa: E402

pack = Pack("Metal", PACK, MINOR)

# --- drums --------------------------------------------------------------------------------------
# Paranoid's drive: eighth hats, the snare on two and four, the kick pushing the "and"s
pack.drums("Paranoid Drive", "BLACK_PEARL", {
    "KICK":   "X.x...x.X.x...x. | X.x...x.X.x.x.x.",
    "SNARE":  "....X.......X... | ....X.......X...",
    "HAT":    "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "CYMBAL": "x............... | ................",
})
# the Iron Maiden gallop (Run to the Hills, The Trooper): the kick in eighth-sixteenth-sixteenth,
# sixteenth hats as Clive Burr kept them, the snare on the backbeat
pack.drums("Maiden Gallop", "BLACK_PEARL", {
    "KICK":   "X.xxx.xxx.xxx.xx | X.xxx.xxx.xxx.xx",
    "SNARE":  "....X.......X... | ....X.......X...",
    "HAT":    "xxxxxxxxxxxxxxxx | xxxxxxxxxxxx....",
    "TOM":    "................ | ............xxxx",
    "CYMBAL": "X............... | ................",
})
# Sabbath's doom: half time, the snare on three, the ride's quarters and a crash to open the
# riff, the toms rolling the turn
pack.drums("Doom Half-Time", "BLACK_PEARL", {
    "KICK":   "X.......x.x..... | X.......x.....x.",
    "SNARE":  "........X....... | ........X.......",
    "CYMBAL": "X...x...x...x... | x...x...x...x...",
    "TOM":    "................ | ..........x.xxxx",
})
# double bass (Priest, Metallica): the kicks in sixteenths, the snare on two and four, crashes
# on the bar
pack.drums("Double Kick", "BLACK_PEARL", {
    "KICK":   "xxxxxxxxxxxxxxxx | xxxxxxxxxxxxxxxx",
    "SNARE":  "....X.......X... | ....X.......X...",
    "CYMBAL": "X.......x....... | X.......x.......",
    "HAT":    "..x...x...x...x. | ..x...x...x...x.",
})
# Motörhead's speed rock (Ace of Spades): the kick on every eighth, the snare's backbeat, the ride
# driving eighths
pack.drums("Speed Rock", "RED_ZEPPELIN", {
    "KICK":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x.x.",
    "SNARE":  "....X.......X... | ....X.......X.XX",
    "CYMBAL": "X.x.x.x.x.x.x.x. | x.x.x.x.x.x.x...",
})

# --- bass ---------------------------------------------------------------------------------------
# Paranoid's eighths (Em D G D Em: i VII III VII i), pick-hard on the beats
def picked(note, n):
    """Eighths on one note, picked harder on the beat."""
    return " ".join(f"{note}@{112 if k % 2 == 0 else 92}" for k in range(n))
pack.bass("Paranoid Eighths", "Picked bass", " | ".join([
    " ".join([picked("1", 8), picked("7-", 4), picked("3", 4)]),
    " ".join([picked("7-", 8), picked("1", 8)])]),
    mods={"FILTER/CUTOFF": -1200})
# Steve Harris's gallop under i VI VII i (The Trooper, Fear of the Dark), the eighth louder than
# its two sixteenths
def gallop(note, beats):
    return " ".join(f"{note}@112 _ {note}@86 {note}@90" for _ in range(beats))
pack.bass("Harris Gallop", "Picked bass", " | ".join([
    gallop("1", 4), " ".join([gallop("6-", 2), gallop("7-", 2)]),
    gallop("1", 4), " ".join([gallop("6-", 2), gallop("7-", 1), gallop("#7-", 1)])]))
# after Iron Man's riff (B D D E E | G F♯ G F♯ G F♯ D D E E: degrees 5 7 7 1 1 | 3 2 3 2 3 2 7 7 1
# 1), slow and heavy, the first note sliding up into place
pack.bass("Iron Riff", "Guitar · Heavy muted", " | ".join([
    " ".join([N("5-!~@118", 7), N("5-@110", 1), N("7-", 4), N("7-", 4)]),
    " ".join([N("1", 4), N("1", 4), N("3@104", 2), N("2@98", 2), N("3@104", 2), N("2@98", 2)]),
    " ".join([N("3@104", 2), N("2@98", 2), N("7-", 4), N("7-", 4), N("1", 4)]),
    " ".join([N("1!", 12), R(4)])]))
# Master of Puppets' kind: a palm-muted E chugging in sixteenths, the power notes falling
# chromatically from it (E D♯ D C♯), each accented
def chug(note, n=3):
    return " ".join([f"{note}!@122"] + [f"1-@{72 + 6 * (k % 2)}" for k in range(n)])
pack.bass("Thrash Chromatic", "Guitar · Heavy muted", " | ".join([
    " ".join([chug("1"), chug("#7-"), chug("7-"), chug("#6-")]),
    " ".join([chug("1"), chug("1"), chug("b2"), chug("1")])]))
# i VI VII in octaves (Fear of the Dark's Dm B♭ C, here Em C D): eighths jumping root and octave
def octaves(note, n):
    """Eighths jumping between a note an octave down and the note."""
    return " ".join(f"{note + '-' if k % 2 == 0 else note}@{110 if k % 2 == 0 else 96}" for k in range(n))
pack.bass("Anthem Octaves", "Picked bass", " | ".join([
    octaves("1", 16), " ".join([octaves("6", 8), octaves("7", 8)])]))

# --- lead ---------------------------------------------------------------------------------------
# a twin-guitar gallop melody (The Trooper's kind), in the gallop's rhythm, climbing the minor
# and falling home
def gal(*notes):
    return " ".join(f"{n}@110 _ {n}@88 {n}@92" for n in notes)
pack.lead("Trooper Twin Lead", "Guitar · Heavy lead", " | ".join([
    gal("5", "6", "7", "1+"), gal("7", "6", "5", "3"),
    gal("4", "5", "6", "7"), " ".join([gal("6", "5"), N("5!", 4), N("#7-", 2), N("1", 2)])]))
# Iron Man's riff an octave up, for the lead
pack.lead("Iron Theme", "Guitar · Heavy lead", " | ".join([
    " ".join([N("5!~@118", 7), N("5@110", 1), N("7", 4), N("7", 4)]),
    " ".join([N("1+", 4), N("1+", 4), N("3+@104", 2), N("2+@98", 2), N("3+@104", 2), N("2+@98", 2)]),
    " ".join([N("3+@104", 2), N("2+@98", 2), N("7", 4), N("7", 4), N("1+", 4)]),
    " ".join([N("1+!", 12), R(4)])]))
# a Sabbath blues lick in the minor pentatonic, a slide up into the bend note, the last note
# left ringing
pack.lead("Pentatonic Lick", "Guitar · Valve OD", " | ".join([
    " ".join([N("3~@96", 1), N("4!", 3), N("3@92", 2), N("1", 2), N("3@96", 2), N("1@90", 2), N("7-", 2), N("5-", 2)]),
    " ".join([N("7-~@92", 1), N("1!", 7), N("#4-@84", 2), N("4-@88", 2), N("5-", 4)])]),
    mods={"MOTION/VIBRATO": 40})
# a neoclassical run (Priest, Malmsteen): sixteenth arpeggios of i and the major V (the raised
# seventh), louder on each beat
def run(notes, first=118, rest=92):
    return " ".join(f"{n}@{first if k % 4 == 0 else rest}" for k, n in enumerate(notes))
pack.lead("Harmonic Run", "Guitar · Heavy lead", " | ".join([
    run(["1", "3", "5", "1+", "3+", "1+", "5", "3", "1", "3", "5", "1+", "3+", "5+", "3+", "1+"]),
    run(["5", "#7", "2+", "5+", "2+", "#7", "5", "#7", "2+", "#7", "5", "#7-"]) + " 1!@118 _ _ _"]))
# a Fear of the Dark-style lead over i VI VII: long notes, a pickup into each change
pack.lead("Dark Anthem", "Guitar · Heavy lead", " | ".join([
    " ".join([N("5!", 12), N("4@92", 2), N("3@96", 2)]),
    " ".join([N("3", 6), N("4@96", 2), N("5", 6), N("6@96", 2)]),
    " ".join([N("7!", 12), N("6@92", 2), N("5@96", 2)]),
    " ".join([N("5", 8), N("#7-@100", 4), N("1", 4)])]))

# --- chords -------------------------------------------------------------------------------------
# power chords, semitones from the key's root (E): root, fifth, octave; a second voicing of the
# same chord (root and fifth only) lets two hits sit side by side without merging into one
P = {"E": cpower(0), "D": cpower(-2), "G": cpower(3), "C": cpower(-4), "B": cpower(-5),
     "F#": cpower(2), "Ds": cpower(-1), "Cs": cpower(-3), "F": cpower(1), "A": cpower(5),
     "E2": ("c", [0, 7]), "C2": ("c", [-4, 3]), "D2": ("c", [-2, 5]), "Ds2": ("c", [-1, 6]),
     "Cs2": ("c", [-3, 4]), "B2": ("c", [-5, 2])}
def eighths(chord, n):
    """Palm-muted eighths: a hit, a gap, n times."""
    return " ".join(C("@" + chord, 1, 1) for _ in range(n))
# Paranoid (Em D G D Em): driving eighths
pack.chords("Paranoid Power", "Guitar · Heavy rhythm", " | ".join([
    " ".join([eighths("E", 4), eighths("D", 2), eighths("G", 2)]),
    " ".join([eighths("D", 4), eighths("E", 4)])]), P)
# The Trooper's gallop (E5 D G D | C5 D E5): the eighth, then two sixteenths on the second
# voicing, so each is struck
def gallop_chords(chord, beats, start=0):
    """The gallop on a chord for `beats` beats: the two voicings alternate beat by beat, so no
    hit merges with the one before it."""
    out = []
    for k in range(start, start + beats):
        a, b = (chord, chord + "2") if k % 2 == 0 else (chord + "2", chord)
        out.append(f"@{a} . @{b} @{a}")
    return " ".join(out)
pack.chords("Trooper Gallop", "Guitar · Heavy rhythm", " | ".join([
    " ".join([gallop_chords("E", 2), gallop_chords("D", 1), gallop_chords("C", 1)]),
    " ".join([gallop_chords("D", 1), gallop_chords("C", 1, 1), gallop_chords("D", 1), C("@E", 3, 1)])]), P)
# Iron Man's chords, held and heavy: B5 D5 E5, then G5 F♯5
pack.chords("Iron Doom", "Guitar · Heavy rhythm", " | ".join([
    " ".join([C("@B", 8), C("@D", 4), C("@D2", 4)]),
    " ".join([C("@E", 8), C("@G", 2), C("@F#", 2), C("@G", 2), C("@F#", 2)])]), P)
# i VI VII i (Fear of the Dark, The Trooper's chorus): each held two beats, struck again
pack.chords("Anthem i-VI-VII", "Guitar · Heavy rhythm", " | ".join([
    " ".join([C("@E", 7, 1), C("@E", 7, 1)]), " ".join([C("@C", 7, 1), C("@D", 7, 1)]),
    " ".join([C("@E", 7, 1), C("@E", 7, 1)]), " ".join([C("@C", 7, 1), C("@D", 3, 1), C("@Ds", 4)])]), P)
# Master of Puppets' chromatic fall: E5 D♯5 D5 C♯5, each struck on the beat and its "and"
pack.chords("Chromatic Fall", "Guitar · Heavy rhythm", " | ".join([
    " ".join([C("@E", 2), C("@E2", 2), C("@Ds", 2), C("@Ds2", 2), C("@D", 2), C("@D2", 2), C("@Cs", 2), C("@Cs2", 2)]),
    " ".join([C("@E", 6), C("@F", 2), C("@E", 6), R(2)])]), P)

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(150, "E", "Natural Minor", echo=0.05, heavy=0.6,
              about="Heavy metal in E minor (the guitar's low string) at 150, compressed hard.")

if __name__ == "__main__":
    pack.done()
