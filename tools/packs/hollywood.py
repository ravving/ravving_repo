#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret "Hollywood" pack: Lana Del Rey's beats and riffs with an old-Hollywood orchestral
# sound (Born to Die, Ultraviolence, Honeymoon, Lust for Life, Norman Fucking Rockwell!): string
# pads, a cello line, tremolo violins, harp sweeps, the celesta, pizzicato, timpani, under slow
# hip-hop beats, brushes and a live room. Five pattern presets each for the drums, the bass, the
# lead and the chords (../patternkit.py). Written in scale degrees for a NATURAL MINOR key, made
# for F minor (Blue Jeans' and Honeymoon's key; the cellos' and contrabasses' low F and C under
# the strings). Her own progressions (the chord sheets, tools/genre-research/hollywood.md):
# Video Games' i III v VI, Born to Die's VI i VII VI, Blue Jeans' i VII IV (the Dorian major IV),
# Summertime Sadness' VI i VII iv, Honeymoon's i VI iv6 V7 in three, Venice Bitch's minor
# plagal (in the relative major: III III7 VI vi6); and the old-Hollywood scoring vocabulary: the
# minor line cliché (i, i(maj7), i7, i6) with the lament bass under it, the half-step sigh,
# swells. Every line, melody and rhythm is original; nothing of hers is quoted.
#
# The playing: velocity swells across each bowed phrase, long holds (_), the strings a little
# behind the beat (>6-10), a written tremolo (sixteenths swelling @40 -> @104 and back), harp
# sweeps rising in velocity to a held top note, the celesta's grace notes snapped in early (<12),
# slides (~) on the 808. MODS: slow ATTACKs on the strings, long RELEASEs (the reverb-drenched
# room), the FILTER down for the vintage tone, a little VIBRATO on the solo strings; the drum
# kits darkened (TONE) and the SP1200 tuned down.
#   python3 tools/packs/hollywood.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/hollywood/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "hollywood")
sys.path.insert(0, HERE)
import patternkit  # noqa: E402
from patternkit import MINOR, Pack, N, C, R  # noqa: E402

# kits.json presetKits "Orchestra · F": the orchestra kit with its timpani on F (TOM, key 53) and
# the C below (HAT, key 48), an F-minor tonic and dominant
patternkit.KITS.setdefault("ORCHESTRA_F", patternkit.GM + "#128:48?TOM=53&HAT=48&OPEN=81&CYMBAL=57&PERC=54")

pack = Pack("Hollywood", PACK, MINOR)


def bar(text, steps=16):
    """One bar's tokens, checked to be sixteen (a miscount is the usual slip); a 3/4 bar is 12."""
    tokens = text.split()
    if len(tokens) != steps:
        raise ValueError(f"{len(tokens)} tokens in bar: {text!r}")
    return text


def ramp(token, start, end, count):
    """`count` sixteenths of one note, their velocities going from `start` to `end`: a written
    tremolo, swelling or fading."""
    step = (end - start) / max(count - 1, 1)
    return " ".join(f"{token}@{round(start + step * i)}" for i in range(count))


# --- drums --------------------------------------------------------------------------------------
# Born to Die's slow, heavy hip-hop beat under the strings: the SP1200 tuned down two semitones
# and darkened, the kick on one, the "a" of two and the "and" of three, a fat snare on two and
# four, lazy eighth hats, the open hat lifting into the turn and a crash at the loop's top
pack.drums("Born To Die Beat", "SP1200", {
    "KICK":   "X......x..x..... | X......x..x...x.",
    "SNARE":  "....X.......X... | ....X.......X..x",
    "HAT":    "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.x...",
    "OPEN":   "................ | ..............x.",
    "CYMBAL": "X............... | ................",
}, mods={"TONE/CUTOFF": -1800, "PITCH/TUNE": -2})
# the half-time beat (Summertime Sadness, Dark Paradise: 112-120 felt at 56-60), written at the
# felt tempo: a long 808 kick, the snare on two and four with Honeymoon's stutter before the
# four, hats in eighths breaking into sixteenths
pack.drums("Summertime Halftime", "TR808", {
    "KICK":  "X..........x.... | X.......x..x....",
    "SNARE": "....X.......X... | ....X.....x.X..x",
    "HAT":   "x.x.x.x.x.xxx.x. | x.x.x.x.x.x.xxxx",
    "OPEN":  "..............x. | ................",
}, mods={"TONE/CUTOFF": -1200, "SHAPE/LENGTH": 1200})
# a brushed waltz in three (Honeymoon, Shades of Cool): four 12-step bars in three 16-step
# bars; the feathered kick on one, the brush slap on two and three, the foot with it, the ride
# on one and the "and" of three, a drag into the loop
pack.drums("Honeymoon Waltz", "BRUSH_RIDE", {
    "KICK":   "X...........X... ........X....... ....X...........",
    "SNARE":  "....x...x.......x...x.......x...x.......x...x.xx",
    "HAT":    "....x...x.......x...x.......x...x.......x...x...",
    "CYMBAL": "X.....x.x.x.X.....x.x.x.X.....x.x.x.X.....x.....",
}, mods={"TONE/CUTOFF": -1800})
# Ultraviolence's slow live band in a big room: the acoustic kit, the kick on one and the "and"
# of three, the snare cracking on two and four with a ghost before three, eighths on the hat,
# the crash at the top, a tom fill down into the loop
pack.drums("Ultraviolence Room", "BLACK_PEARL", {
    "KICK":   "X.........x..... | X.........x.x...",
    "SNARE":  "....X..x....X... | ....X..x....X...",
    "HAT":    "x.x.x.x.x.x.x.x. | x.x.x.x.x.x.....",
    "TOM":    "................ | .............xxx",
    "CYMBAL": "X............... | ................",
}, mods={"TONE/CUTOFF": -1500})
# the film score's timpani: F on one and three, the C below answering, a roll on the C up into
# the loop's top where the bass drum and the clash cymbals land; a triangle on the third beat
pack.drums("Timpani Swell", "ORCHESTRA_F", {
    "TOM":    "X.......x....... | X...............",
    "HAT":    "....x.......x... | ....x...xxxxxxxx",
    "KICK":   "X............... | X...............",
    "CYMBAL": "X............... | ................",
    "OPEN":   "........x....... | ........x.......",
}, mods={"TONE/CUTOFF": -600})

# --- bass ---------------------------------------------------------------------------------------
# Video Games' i III v VI, one chord a bar: the cellos' long bows on the roots, each swelling a
# little louder, late as a bow sits, a two-step walk into the next change
pack.bass("Video Games Bows", "Cello", " | ".join([
    bar(N("1@70>8", 14) + " " + N("2@58", 2)),
    bar(N("3@78>8", 14) + " " + N("4@60", 2)),
    bar(N("5-@84>8", 14) + " " + N("7-@62", 2)),
    bar(N("6-@92>8", 12) + " " + N("5-@70", 2) + " " + N("7-@64", 2))]),
    mods={"ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 2400, "FILTER/CUTOFF": -1800})
# Born to Die's sub under the beat: VI i VII VI, the root on one, again on the "a" of two, then
# a slide (~) down or up into the next root on the "and" of three
pack.bass("Born To Die Sub", "808 · Monosynth", " | ".join([
    bar("6-! _ _ _ _ _ . 6-@80 _ _ 6-~ _ 1 _ _ ."),
    bar("1! _ _ _ _ _ . 1@80 _ _ 1~ _ 7- _ _ ."),
    bar("7-! _ _ _ _ _ . 7-@80 _ _ 7-~ _ 6- _ _ ."),
    bar("6-! _ _ _ _ _ . 6-@80 _ _ . 5-@70 6- _ _ .")]))
# the lament bass under the line cliché: F E Eb D Db (ALTER: the E and the D outside the key),
# then the iv's Bb and the dominant C held, the leading E back to F; bowed, swelling, late
pack.bass("Lament Line", "Contrabass", " | ".join([
    bar(N("1@68>6", 8) + " " + N("#7-@72>6", 8)),
    bar(N("7-@76>6", 8) + " " + N("#6-@80>6", 8)),
    bar(N("6-@86>6", 8) + " " + N("4-@90>6", 8)),
    bar(N("5-@96>8", 12) + " " + N("#7-@70", 3, 1))]),
    mods={"ENVELOPE/ATTACK": 1800, "ENVELOPE/RELEASE": 1800, "FILTER/CUTOFF": -1200})
# Blue Jeans' i VII IV, the double bass plucked: root and fifth, the root again on three with
# a pickup, behind the beat; the D natural of the major IV (the Dorian 6th) under the Bb, and
# a walk down Bb Ab G into the loop
pack.bass("Blue Jeans Pizz", "Upright", " | ".join([
    bar("1!>8 _ . . . . 5-@70 . 1@86>8 _ . . 5-@64 . 7-@60 ."),
    bar("7-!>8 _ . . . . 4-@70 . 7-@86>8 _ . . 4-@64 . #6-@62 ."),
    bar("4-!>8 _ . . . . 1@70 . 4-@86>8 _ . . #6-@70 . 1@64 ."),
    bar("4-!>8 _ . . . . 1@70 . 4@80>8 _ . . 3@66 . 2@60 .")]),
    mods={"ENVELOPE/RELEASE": 600, "FILTER/CUTOFF": -1200})
# Honeymoon's sway in three (four 12-step bars in three 16-step bars): i VI iv6 V7, a dotted
# half on each root, late, then a quarter leading on, the V7's E natural (harmonic minor) back
# into the F
pack.bass("Honeymoon Sway", "Cello", " ".join([
    bar(N("1@72>8", 8) + " " + N("5-@60", 4), 12),
    bar(N("6-@80>8", 8) + " " + N("5-@64", 4), 12),
    bar(N("4@86>8", 8) + " " + N("6-@68", 4), 12),
    bar(N("5-@94>8", 8) + " " + N("#7-@70", 4), 12)]),
    mods={"ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 3000, "MOTION/VIBRATO": 20, "FILTER/CUTOFF": -1500})

# --- lead ---------------------------------------------------------------------------------------
# a violin line over Video Games' i III v VI: a sigh down from the 6th, a high Ab cried and
# stepping down, the 9th held over the minor v, the octave swelling over the VI; long, late,
# each phrase louder than the last
pack.lead("Video Games Violin", "Violin · Warm", " | ".join([
    bar(R(4) + " " + N("5@62>8", 6) + " " + N("6@74", 2) + " " + N("5@70", 3, 1)),
    bar(N("3+@80>8", 8) + " " + N("2+@76", 2) + " " + N("1+@72", 2) + " " + N("7@68", 3, 1)),
    bar(N("5@64", 4) + " " + N("7@72", 2) + " " + N("2+@80>8", 6) + " " + N("1+@74", 2) + " " + N("7@66", 1, 1)),
    bar(N("1+@88>10", 12) + " " + N("6@70", 2) + " " + N("5@60", 2))]),
    mods={"ENVELOPE/ATTACK": 3600, "ENVELOPE/RELEASE": 3000, "MOTION/VIBRATO": 40, "FILTER/CUTOFF": -1200})
# the cello's lament over the line cliché: up from the low C to the 3rd, then the chromatic fall
# F E Eb D Db, up to the iv's Bb, and the dominant's E natural held, swelling to @90
pack.lead("Cello Lament", "Cello", " | ".join([
    bar(N("5-@66>8", 6) + " " + N("1@72", 2) + " " + N("3@80", 6) + " " + N("2@70", 1, 1)),
    bar(N("1@74", 4) + " " + N("#7-@70", 2) + " " + N("7-@68", 2) + " " + N("#6-@72", 6) + " " + N("6-@64", 1, 1)),
    bar(N("6-@70>8", 6) + " " + N("1@78", 2) + " " + N("4@86", 4) + " " + N("3@80", 2) + " " + N("2@72", 2)),
    bar(N("#7-@90>10", 8) + " " + N("2@76", 2) + " " + N("1@70", 2) + " " + N("#7-@64", 3, 1))]),
    mods={"ENVELOPE/ATTACK": 2400, "ENVELOPE/RELEASE": 2400, "MOTION/VIBRATO": 50, "FILTER/CUTOFF": -1500})
# the celesta's music box over Born to Die's VI i VII VI: broken chords in eighths, the beats
# leaned on, a grace note snapped in early (<12) before each bar's top, a turn at the end
pack.lead("Celesta Box", "Celesta", " | ".join([
    bar("6@76 . 1+@60 . 3+@70 . 1+@58 . 6@72 . 1+@60 4+@54<12 3+@78 . 1+@60 ."),
    bar("1+@76 . 3+@60 . 5+@70 . 3+@58 . 1+@72 . 3+@60 6+@54<12 5+@78 . 3+@60 ."),
    bar("7@76 . 2+@60 . 4+@70 . 2+@58 . 7@72 . 2+@60 5+@54<12 4+@78 . 2+@60 ."),
    bar("6@76 . 1+@60 . 3+@70 . 1+@58 . 5+@80 . 3+@66 2+@60 1+@64 . 7@58 .")]),
    mods={"ENVELOPE/RELEASE": 3000, "FILTER/CUTOFF": -600})
# the harp's sweeps over i VI III VII: chord tones in sixteenths up two octaves, each louder
# than the last (@50 -> @98), the top held to ring, a few notes falling back on the VII
pack.lead("Harp Sweeps", "Harp · Concert", " | ".join([
    bar("1-@50 3-@56 5-@62 1@68 3@74 5@80 1+@86 3+@92 5+@98 _ _ _ _ _ . ."),
    bar("6-@50 1@56 3@62 6@68 1+@74 3+@80 6+@92 _ _ _ _ _ 5+@70 _ 3+@62 ."),
    bar("3-@50 5-@56 7-@62 3@68 5@74 7@80 3+@86 5+@94 _ _ _ _ _ _ . ."),
    bar("7-@50 2@56 4@62 7@68 2+@74 4+@80 7+@92 _ _ _ _ 6+@72 5+@66 4+@60 2+@56 .")]),
    mods={"ENVELOPE/RELEASE": 4000, "FILTER/CUTOFF": -900})
# the suspense tremolo (the film-noir strings): the dominant C bowed in sixteenths swelling from
# @40 to @104, the half-step sigh up to Db fading back, again, then the leading E natural
# swelling into the F
pack.lead("Tremolo Violins", "Violin", " | ".join([
    bar(ramp("5", 40, 104, 16)),
    bar(ramp("6", 104, 56, 16)),
    bar(ramp("5", 48, 100, 16)),
    bar(ramp("#7", 60, 110, 12) + " " + N("1+@110", 4))]),
    mods={"ENVELOPE/RELEASE": 600, "MOTION/VIBRATO": 30, "FILTER/CUTOFF": -1200})

# --- chords -------------------------------------------------------------------------------------
# the voicings (scale degrees from F, 0-based; or "c", semitones from the F): lush, with added
# 9ths and major 7ths, spread as a string section voices them
V = {
    "i9":     ("x", [0, 4, 8, 9, 11]),     # F C G Ab C: Fm(add9), the 9th rubbing the 3rd
    "IIImaj7": ("x", [2, 4, 6, 8]),       # Ab C Eb G
    "v7":     ("x", [4, 6, 8, 10]),        # C Eb G Bb
    "VImaj7": ("x", [5, 7, 9, 11]),       # Db F Ab C
    "VI":     ("x", [5, 7, 9]),
    "i":      ("x", [0, 2, 4, 7]),
    "VII":    ("x", [6, 8, 10]),
    "iv":     ("x", [3, 5, 7]),
    "iv6":    ("x", [3, 5, 7, 8]),         # Bb Db F G
    # the line cliché: Fm with the top voice falling F E Eb D, then the "James Bond" Fm(maj9)
    "lc1":    ("c", [0, 3, 7, 12]),
    "lc2":    ("c", [0, 3, 7, 11]),
    "lc3":    ("c", [0, 3, 7, 10]),
    "lc4":    ("c", [0, 3, 7, 9]),
    "V7":     ("c", [7, 11, 14, 17]),      # C E G Bb, the harmonic-minor dominant
    "V7b9":   ("c", [7, 11, 14, 17, 20]),  # with the Db on top
    # Venice Bitch's minor plagal, in the relative major (Ab): III, III7, VI, vi6
    "III":    ("c", [3, 7, 10, 15]),       # Ab C Eb Ab
    "III7":   ("c", [3, 7, 10, 13]),       # Ab C Eb Gb
    "VIb":    ("c", [8, 12, 15, 20]),      # Db F Ab Db
    "vi6":    ("c", [8, 11, 15, 17]),      # Db Fb Ab Bb
}

# Video Games' i III v VI, a chord a bar on long bows: the strings' slow ATTACK is the swell,
# the RELEASE the hall, the FILTER down for the old record
pack.chords("Video Games Strings", "Strings", " | ".join([
    bar(C("@i9", 15, 1)), bar(C("@IIImaj7", 15, 1)), bar(C("@v7", 15, 1)), bar(C("@VImaj7", 15, 1))]), V,
    mods={"ENVELOPE/ATTACK": 4800, "ENVELOPE/RELEASE": 3600, "FILTER/CUTOFF": -1500})
# Born to Die's VI i VII VI as the sampled strings whip it: a stab on one, another on the "and"
# of two, then the chord held from the "and" of three
def whip(name):
    return bar(C("@" + name, 3, 3) + " " + C("@" + name, 2, 2) + " " + C("@" + name, 5, 1))
pack.chords("Born To Die Stabs", "Strings · Mood", " | ".join([whip("VI"), whip("i"), whip("VII"), whip("VI")]), V,
    mods={"ENVELOPE/RELEASE": 900, "FILTER/CUTOFF": -1200})
# the minor line cliché in tremolo strings: Fm, Fm(maj7), Fm7, Fm6 two beats each, then
# Dbmaj7 and the iv6, the harmonic V7 swelling into its b9
pack.chords("Line Cliché", "Strings · Tremolo", " | ".join([
    bar(C("@lc1", 8) + " " + C("@lc2", 8)),
    bar(C("@lc3", 8) + " " + C("@lc4", 8)),
    bar(C("@VImaj7", 8) + " " + C("@iv6", 8)),
    bar(C("@V7", 8) + " " + C("@V7b9", 7, 1))]), V,
    mods={"ENVELOPE/ATTACK": 1800, "ENVELOPE/RELEASE": 2400, "FILTER/CUTOFF": -1200}, ties="all")
# Honeymoon's sway on the piano, in three (four 12-step bars in three 16-step bars): i VI iv6
# V7, each chord struck on one and let ring, touched again on three
pack.chords("Honeymoon Piano", "Grand piano", " ".join(
    bar(C("@" + name, 7, 1) + " " + C("@" + name, 3, 1), 12) for name in ["i", "VI", "iv6", "V7"]), V,
    mods={"ENVELOPE/RELEASE": 3000, "FILTER/CUTOFF": -1800})
# the minor plagal of Venice Bitch (III III7 VI vi6, the major chord turning minor) then
# Summertime Sadness' VI i VII iv, on the piano with strings under it: each chord struck, a
# second touch on the "and" of two or four
def touch(name):
    return C("@" + name, 5, 1) + " " + C("@" + name, 2)
pack.chords("Venice Plagal", "Piano + strings", " | ".join([
    bar(touch("III") + " " + touch("III7")),
    bar(touch("VIb") + " " + touch("vi6")),
    bar(touch("VI") + " " + touch("i")),
    bar(touch("VII") + " " + C("@iv", 7, 1))]), V,
    mods={"ENVELOPE/RELEASE": 2400, "FILTER/CUTOFF": -1200}, ties=[8, 24, 32])

# the templates: F minor at the pack's 72 (the middle of 56-88), a hair of lazy hip-hop swing
# under straight strings, the echo for the reverb-drenched room; and Video Games' half-time
# ballad in its own F# minor
pack.template(72, "F", "Natural Minor", swing=52, echo=0.4, heavy=0.15,
              about="Old-Hollywood sadcore at 72 in F minor: slow hip-hop beats under strings, harp and celesta, a long echo for the hall.")
pack.template(62, "F#", "Natural Minor", name="Hollywood · Video Games", echo=0.45, heavy=0.1,
              about="The half-time ballad at 62 in F# minor: long bows, harp sweeps, the drums barely there.")

if __name__ == "__main__":
    pack.done()
