#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret "Body" pack: Grimes' Be a Body (Visions, 2012), its intro above all. Six pattern
# presets each for the drums, the bass, the lead and the chords (../patternkit.py), written in
# scale degrees for F DORIAN at 140 BPM: the song's F minor centre with the D natural (Hooktheory
# files it in Eb major, the same notes, its chorus ii7 V7 vi7 = Fm7 Bb7 Cm7; AcousticBrainz and
# SongBPM read 140; tools/genre-research/be-a-body.md).
#
# Its harmony (Chordu's timeline of the album audio and of the official instrumental, checked
# against Hooktheory and a chroma analysis of the store previews):
#   - the intro: i IV VII VII (Fm Bb Eb Eb), then the loop i IV v v (Fm Bb Cm Cm) three times,
#     a III IV turnaround (Ab Bb), a break;
#   - the verse: i IV v v / ii IV v v (the Gm);
#   - the middle: IV v rocking two bars each, then III IV V into the chorus (the C major);
#   - the outro: I IV V, the F major.
# The tunes sit on the 5th, the 7th, the 6th and the 4th and leave the 3rd out (the previews' notes
# use no Ab at all), so the key floats between F minor and F major.
#
# The intro is the heart of the pack: Intro Tick, Intro Sub, Intro Harp, Intro Chops, Intro
# Bells, Intro Stabs and Intro Haze, and the "Body · Intro" template. The sound is the Visions
# one: a Roland Juno-G (its "Wet Nylon", "Big Mini" and "SH101 Bs1" on this song, its harp and
# "Theramax" on the album), cheap drum machines, a multitracked high voice, a bouncing 1/8 delay
# (the templates' ECHO, and echoes written into the harp and the pluck: the note again two steps
# later, softer). Nothing is quoted: the song is copyrighted, so its progression, key, tempo and
# arrangement shape were studied and every line, melody and rhythm is new.
#   python3 tools/packs/be-a-body.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/be-a-body/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "be-a-body")
sys.path.insert(0, HERE)
from patternkit import SCALES, Pack, N, C, R  # noqa: E402

pack = Pack("Body", PACK, SCALES["Dorian"])


def bar(text, steps=16):
    """One bar's tokens, checked to be sixteen (a miscount is the usual slip)."""
    tokens = text.split()
    if len(tokens) != steps:
        raise ValueError(f"{len(tokens)} tokens in bar: {text!r}")
    return text


def bars(*texts):
    return " | ".join(bar(t) for t in texts)


def echo(token, velocity, gap=1, fade=0.55):
    """A note and its 1/8 echo: the note, `gap` steps of rest, the note again softer (the
    Visions delay written in), three steps in all with the default gap."""
    return " ".join([f"{token}@{velocity}"] + ["."] * gap + [f"{token}@{round(velocity * fade)}"])


# --- drums --------------------------------------------------------------------------------------
# the intro's cheap drum machine before the beat drops: the 606's kick on one and three, a
# ticking hat with gaps, the snare bouncing a dotted 8th apart like a delayed hit, the open
# hat breathing in at the end of the second bar
pack.drums("Intro Tick", "TR606", {
    "KICK":  "X.......x....... | X.......x.....x.",
    "SNARE": "...x..x......... | ...x..x.....x..x",
    "HAT":   "x.xxx.x.x.xxx.x. | x.xxx.x.x.xx....",
    "OPEN":  "................ | ............x...",
}, mods={"TONE/CUTOFF": -1200})
# the '90s suburban rave the reviews hear: the 909 four on the floor, the clap on two and four,
# the open hat on every off-beat, sixteenth hats around it, a clap pickup into the loop
pack.drums("Rave Pulse", "TR909", {
    "KICK":  "X...x...X...x... | X...x...X...x...",
    "CLAP":  "....x.......x... | ....x.......x..x",
    "HAT":   "xx.xxx.xxx.xxx.x | xx.xxx.xxx.xxx.x",
    "OPEN":  "..x...x...x...x. | ..x...x...x...x.",
})
# the album's syncopated electro: the 808 kick on one, the "and" of two and the "and" of three,
# the clap on two and four with its echo a 16th and an 8th later, a rim on the "a" of one
pack.drums("Visions Break", "TR808", {
    "KICK":  "X.....x...x..... | X.....x...x...x.",
    "CLAP":  "....X.x.....X... | ....X.x.....X.x.",
    "HAT":   "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.xxxx",
    "PERC":  "...x............ | ...x.......x....",
}, mods={"SHAPE/LENGTH": 800})
# the beat at half time, the snare once a bar on three, skipping sixteenth hats on the Linn,
# the kick pushed late in the second bar and a tom roll down into the loop
pack.drums("Half-Time", "LINN", {
    "KICK":   "X.........x..... | X.....x...x.....",
    "SNARE":  "........X....... | ........X.......",
    "HAT":    "x.xxx.x.x.xxx.xx | x.xxx.x.x.x.....",
    "TOM":    "................ | ............xxxx",
    "CYMBAL": "X............... | ................",
}, mods={"TONE/CUTOFF": -900})
# the build out of the intro into the beat: quarter kicks, the snare in eighths, then sixteenths
# with every beat accented, a crash at the loop's top where the drop lands
pack.drums("Drop Build", "SP1200", {
    "KICK":   "X...X...X...X... | X...X...X...X...",
    "SNARE":  "x.x.x.x.x.x.x.x. | XxxxXxxxXxxxXxxx",
    "CYMBAL": "X............... | ................",
    "OPEN":   "................ | ..............x.",
})
# the "tough, even gnarly" percussion: the HR16's kick in 3-3-2, toms answering on the off-steps,
# the clap on four, a cowbell tick
pack.drums("Gnarly Toms", "HR16", {
    "KICK":  "X..x..x.X..x..x. | X..x..x.X..x....",
    "TOM":   ".x...x....x..x.. | .x...x....x.xxxx",
    "CLAP":  "............X... | ............X...",
    "HAT":   "..x...x...x...x. | ..x...x...x...x.",
    "PERC":  "....x.......x... | ....x...........",
}, mods={"TONE/CUTOFF": -600, "PITCH/TUNE": -2})

# --- bass ---------------------------------------------------------------------------------------
# the intro's i IV VII VII (Fm Bb Eb Eb) entering low: a dotted quarter, a dotted quarter and a
# quarter on each root (a slow 3-3-2 the delay fills), the octave on the last; the Dorian D and
# the C walking up into the loop
pack.bass("Intro Sub", "Synth bass 2", bars(
    "1-@100 _ _ _ _ . 1-@72 _ _ _ _ . 1@88 _ _ .",
    "4-@100 _ _ _ _ . 4-@72 _ _ _ _ . 4@88 _ _ .",
    "7-@100 _ _ _ _ . 7-@72 _ _ _ _ . 7@88 _ _ .",
    "7-@100 _ _ _ _ . 7-@72 _ _ _ _ . 5-@84 _ 6-@88 _"),
    mods={"FILTER/CUTOFF": -1800, "ENVELOPE/RELEASE": 300})
# the loop under the beat, i IV v v, on a Minimoog-like bass: sixteenths in 3-3-2-3-3-2, the
# low root and its octave trading, the 5th in the middle, a walk down Bb Ab G into the loop
pack.bass("Mini Pulse", "Synth bass 2", bars(
    "1-! _ . 1@84 _ . 1-@90 . 5-@80 _ . 1-@92 _ . 1@84 .",
    "4-! _ . 4@84 _ . 4-@90 . 1@80 _ . 4-@92 _ . 4@84 .",
    "5-! _ . 5@84 _ . 5-@90 . 2@80 _ . 5-@92 _ . 5@84 .",
    "5-! _ . 5@84 _ . 5-@90 . 4-@82 _ . 3-@86 _ . 2-@88 ."),
    mods={"FILTER/CUTOFF": -1200, "FILTER/RESO": 60})
# the rave bass the beat drops with: the 303-style Nekobi on the off-beats, accented, the octave
# flicked on the "a" of four, i IV v v
pack.bass("Rave Offbeat", "Nekobi", bars(
    ". . 1-! _ . . 1-! _ . . 1-! _ . 1 1-! _",
    ". . 4-! _ . . 4-! _ . . 4-! _ . 4 4-! _",
    ". . 5-! _ . . 5-! _ . . 5-! _ . 5 5-! _",
    ". . 5-! _ . . 5-! _ . 7- 5-! _ . 5 1-! _"))
# the verse's ii IV v v (Gm Bb Cm Cm) plucked, each note's 1/8 echo written in two steps later,
# softer; the octaves bouncing
pack.bass("Verse Bounce", "Synth bass", bars(
    echo("2-!", 104) + " " + echo("2", 92) + " " + echo("2-", 86) + " " + echo("2", 90) + " " + echo("4-", 84) + " .",
    echo("4-!", 104) + " " + echo("4", 92) + " " + echo("4-", 86) + " " + echo("4", 90) + " " + echo("5-", 84) + " .",
    echo("5-!", 104) + " " + echo("5", 92) + " " + echo("5-", 86) + " " + echo("5", 90) + " " + echo("7-", 84) + " .",
    echo("5-!", 104) + " " + echo("5", 92) + " " + echo("7-", 86) + " " + echo("6-", 90) + " " + echo("4-", 84) + " ."),
    mods={"FILTER/CUTOFF": -900})
# the middle section on the sub: IV IV v v IV IV, then III and IV a half bar each and the C
# major V lifting into the chorus; long roots, each sliding (~) into the next
pack.bass("Bridge Sub", "808 · Monosynth", bars(
    N("4-!", 16), N("4-@80", 10) + " " + N("4-~@84", 6),
    N("5-!", 16), N("5-@80", 10) + " " + N("5-~@84", 6),
    N("4-!", 16), N("4-@80", 10) + " " + N("4-~@84", 6),
    N("3-!", 6) + " " + N("3-~@80", 2) + " " + N("4-!", 6) + " " + N("4-~@84", 2),
    N("5-!", 12) + " " + N("5@78", 2) + " " + N("5-@84", 2)))
# the outro's major I IV V V driving in straight eighths, the octave on every off-beat, a
# pickup up the scale into the loop
pack.bass("Outro Drive", "Synth bass 2", bars(
    "1-! . 1@76 . 1-@92 . 1@76 . 1-@92 . 1@76 . 1-@92 . 1@80 .",
    "4-! . 4@76 . 4-@92 . 4@76 . 4-@92 . 4@76 . 4-@92 . 4@80 .",
    "5-! . 5@76 . 5-@92 . 5@76 . 5-@92 . 5@76 . 5-@92 . 5@80 .",
    "5-! . 5@76 . 5-@92 . 5@76 . 5-@90 . 6-@84 . 7-@88 . 1@92 ."),
    mods={"FILTER/CUTOFF": -600, "FILTER/RESO": 40})

# --- lead ---------------------------------------------------------------------------------------
# the intro's plucked figure over i IV VII VII: the chord's 5th, root and 9th in dotted eighths
# (three steps apart), each echoed an 8th later and softer, so the line bounces against the
# bar; down from the Bb to the C at the end
pack.lead("Intro Harp", "Harp · Concert", bars(
    " ".join([echo("5", 96), echo("1+", 92), echo("2+", 96), echo("5", 84), echo("1+", 88)]) + " .",
    " ".join([echo("4", 96), echo("6", 92), echo("1+", 96), echo("6", 84), echo("4", 88)]) + " .",
    " ".join([echo("7", 96), echo("2+", 92), echo("4+", 100), echo("2+", 84), echo("7", 88)]) + " .",
    " ".join([echo("4+", 96), echo("2+", 90), echo("7", 86), echo("6", 82)]) + " " + N("5@90", 3, 1)),
    mods={"ENVELOPE/RELEASE": 1500, "FILTER/CUTOFF": -600})
# the multitracked voice chopped into syllables over the intro: stuttered sixteenths, short
# high notes that leave the 3rd out (the 5th, the 7th, the 6th, the 9th), gaps between them
pack.lead("Intro Chops", "Synth voice", bars(
    "1+@100 1+@60 . 7@90 . . 5@96 5@58 5@80 . 7@92 . 6@84 . . .",
    "4@88 . 5@96 . . 5@62 7@100 _ . . 6@86 . 5@92 . 4@76 .",
    "7@100 7@62 . 2+@96 . . 1+@92 1+@56 7@88 . 1+@96 . 2+@90 _ . .",
    "4+@84 . 2+@92 . 1+@96 _ _ . 7@88 . 6@80 . 5@100 _ _ ."),
    mods={"ENVELOPE/RELEASE": -1200, "FILTER/CUTOFF": -300})
# the turnaround's sparkle (III IV i IV: Ab Bb Fm Bb): short high flicks, a grace note snapped
# in early before the first of each bar, the honey-sweet tics the reviews hear
pack.lead("Intro Bells", "Celesta", bars(
    "3+@70<12 5+@96 . . . . 4+@80 . 3+@88 . . . 1+@84 . . .",
    "6@60<12 1+@92 . . 2+@84 . . . 4+@96 _ . . 2+@80 . 1+@72 .",
    "5+@100 . . 4+@70 . 2+@88 . . 1+@92 _ _ . 7@76 . 5@70 .",
    "6@84 . 1+@76 . 2+@88 . 4+@96 _ _ _ . . 2+@70 . 1+@64 ."),
    mods={"ENVELOPE/RELEASE": 2400})
# a sung hook over i IV v v: long high notes, a scoop up into the 7th, a sigh down to the 5th,
# the 9th held over the minor v; laid a touch behind the beat
pack.lead("Voice Hook", "Voice oohs", bars(
    ". . 6@58<14 7@96>6 _ _ _ _ _ 6@82 _ 5@88 _ _ _ _",
    "4@80>6 _ _ _ . . 5@60<14 6@92 _ _ _ 5@84 _ 4@78 _ .",
    "5@90>6 _ _ _ _ _ _ _ 2+@96>6 _ _ _ 1+@88 _ 7@80 _",
    "5@86 _ _ _ _ _ _ _ _ _ _ _ . . 4@64 5@72"),
    mods={"ENVELOPE/ATTACK": 300, "ENVELOPE/RELEASE": 1500, "MOTION/VIBRATO": 30})
# an SH-101 bass-lead riff over i IV v v: sequenced sixteenths, the root, 5th and octave with
# the accent on the "and" of two, a run at each bar's end
pack.lead("Square Riff", "Lead · Square", bars(
    "1 . 5 1+ . 5 7 . 1+! . 5 . 2+ 1+ 7 5",
    "4- . 1 4 . 1 6 . 4! . 1 . 6 4 1 6-",
    "5- . 2 5 . 2 4 . 5! . 2 . 6 5 4 2",
    "5- . 2 5 . 2 4 . 5! . 7 . 1+ 7 6 4"),
    mods={"FILTER/CUTOFF": -2400, "FILTER/RESO": 60, "ENVELOPE/RELEASE": -1200})
# the album's theremin lead (its "Theramax"): long notes gliding (~) into each other over i IV
# v v, on the lead's own Monosynth
pack.lead("Theremin Glide", "Calf Monosynth", bars(
    "5~ _ _ _ _ _ _ 1+ _ _ _ _ _ _ _ .",
    "6~ _ _ _ _ _ 4 _ _ _ _ _ _ _ . .",
    "2+~ _ _ _ 1+~ _ _ _ 7 _ _ _ _ _ _ .",
    "5 _ _ _ _ _ _ _ _ _ _ _ 4~ _ 5 _"))

# --- chords -------------------------------------------------------------------------------------
# the voicings (scale degrees from F, 0-based: 0 F3, 4 C4, 7 F4; or "c", semitones from the F)
V = {
    "i9":      ("x", [0, 4, 6, 8, 9]),     # F C Eb G Ab: Fm9, the 9th under the 3rd
    "i7":      ("x", [0, 2, 4, 6]),        # F Ab C Eb
    "IV9":     ("x", [3, 5, 7, 9, 11]),    # Bb D F Ab C: the Dorian major IV
    "IV7":     ("x", [3, 5, 7, 9]),        # Bb D F Ab
    "v9":      ("x", [4, 6, 8, 10, 12]),   # C Eb G Bb D
    "v7":      ("x", [4, 6, 8, 10]),       # C Eb G Bb
    "ii7":     ("x", [1, 3, 5, 7]),        # G Bb D F
    "VIImaj7": ("x", [6, 8, 10, 12]),      # Eb G Bb D
    "III":     ("x", [2, 4, 6, 9]),        # Ab C Eb Ab
    "IV":      ("x", [3, 5, 7, 10]),       # Bb D F Bb
    # the intro's stabs leave the 3rd out, as the tunes do: sus chords over the F
    "isus2":   ("x", [0, 1, 4, 7]),        # F G C F
    "isus4":   ("x", [0, 3, 4, 7]),        # F Bb C F
    "IV/I":    ("x", [0, 3, 5, 7]),        # F Bb D F
    "IV/I9":   ("x", [0, 3, 5, 8]),        # F Bb D G
    "VII/I":   ("x", [0, 6, 8, 10]),       # F Eb G Bb: F11
    "VII":     ("x", [6, 8, 10, 13]),      # Eb G Bb Eb
    # the outro's major chords and the middle's major V (A and E natural: chromatic)
    "I":       ("c", [0, 4, 7, 12]),       # F A C F
    "V":       ("c", [7, 11, 14, 19]),     # C E G C
}


def stabs(a, b):
    """The intro's rocker stabs, one bar: two-step hits on 1, the "a" of one, the "and" of two,
    the "and" of three and the "a" of four, swapping between two voicings."""
    return " ".join([C("@" + a, 2, 1), C("@" + b, 2, 1), C("@" + a, 2, 2), C("@" + b, 2, 2), C("@" + a, 1, 1)])


# the intro's opening motif, an 80s radio-rocker riff on synth brass (the Arts Desk: "could hail
# from a mainstream radio rocker"): i IV VII VII as syncopated stabs over the F, sus chords with
# the top voice rocking
pack.chords("Intro Stabs", "Synth brass", bars(
    stabs("isus2", "isus4"), stabs("IV/I", "IV/I9"), stabs("VII/I", "VII"), stabs("VII", "VII/I")), V,
    mods={"ENVELOPE/RELEASE": -600, "FILTER/CUTOFF": -1200})
# the whole intro as a Juno haze: i IV VII VII then the loop i IV v v, a chord a bar, chorused
# and slow in, the VII and the v held over two bars
pack.chords("Intro Haze", "Pad · Polysynth", bars(
    C("@i9", 15, 1), C("@IV9", 15, 1), C("@VIImaj7", 16), C("=", 15, 1),
    C("@i9", 15, 1), C("@IV9", 15, 1), C("@v9", 16), C("=", 15, 1)), V,
    mods={"ENVELOPE/ATTACK": 600, "ENVELOPE/RELEASE": 2400, "MOTION/CHORUS": 600})
# the loop under the beat on the chords machine's own Juno-style synth: i7 IV7 v7 v9 stabbed on
# every off-beat 8th, the rave's pump
pack.chords("Juno Offbeats", "TAL NoiseMaker", bars(
    *[" ".join([R(2) + " " + C("@" + name, 1, 1)] * 4) for name in ("i7", "IV7", "v7", "v9")]), V)
# the verse, i IV v v then ii IV v v, as the hissing cloud of voices: held a bar each (the v two),
# breathing in
pack.chords("Verse Choir", "Pad · Choir", bars(
    C("@i7", 15, 1), C("@IV7", 15, 1), C("@v7", 16), C("=", 15, 1),
    C("@ii7", 15, 1), C("@IV7", 15, 1), C("@v9", 16), C("=", 15, 1)), V,
    mods={"ENVELOPE/ATTACK": 1200, "ENVELOPE/RELEASE": 3000})
# the middle section in 3-3-2 (a dotted quarter, a dotted quarter, a quarter): IV IV v v IV IV,
# III and IV a half bar each, the C major V lifting into the chorus
def lilt(name):
    return C("@" + name, 5, 1) + " " + C("@" + name, 5, 1) + " " + C("@" + name, 3, 1)
pack.chords("Bridge Lift", "Strings · Digital", bars(
    lilt("IV7"), lilt("IV7"), lilt("v7"), lilt("v7"), lilt("IV7"), lilt("IV7"),
    C("@III", 7, 1) + " " + C("@IV", 7, 1), C("@V", 15, 1)), V,
    mods={"ENVELOPE/RELEASE": 900})
# the outro's I IV V V in F major, struck long-short-long on the polysynth
def outro(name):
    return C("@" + name, 5, 1) + " " + C("@" + name, 2, 1) + " " + C("@" + name, 6, 1)
pack.chords("Major Ending", "Pad · Polysynth", bars(outro("I"), outro("IV"), outro("V"), outro("V")), V,
    mods={"ENVELOPE/RELEASE": 1200, "MOTION/CHORUS": 400})

# the templates: the song's 140 in F Dorian, straight, the 1/8 delay on everything (ECHO); and
# the intro's own, more echo and the phaser's slow swirl, the compressor eased off
pack.template(140, "F", "Dorian", echo=0.35, phaser=0.1, heavy=0.25,
              about="Grimes' Be a Body at 140 in F Dorian: Juno pads, a Minimoog bass, cheap drum machines, the bouncing delay.")
pack.template(140, "F", "Dorian", name="Body · Intro", echo=0.5, phaser=0.2, heavy=0.1,
              about="The intro at 140 in F Dorian: harp and chopped voices over sus stabs, the drums ticking, a long echo.")

if __name__ == "__main__":
    pack.done()
