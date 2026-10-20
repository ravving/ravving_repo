#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The secret post-punk pack: five pattern presets for each of the drums, the bass, the lead and
# the chords (see ../patternkit.py). Written in scale degrees for a NATURAL MINOR key, made for
# A minor. The progressions are the bands' (Ultimate Guitar's chord sheets, see the README),
# each set on its minor key's degrees:
#   The Cure, A Forest            Am C F D        i III VI IV (the Dorian major IV)
#   Joy Division, Love Will Tear Us Apart   D A Bm Em (in B minor)   III VII i iv
#   The Cure, Boys Don't Cry      A Bm C#m D (in F# minor)           III iv v VI
#   Siouxsie, Spellbound          Dm7 C G (D Dorian)                 i7 VII IV
#   The Sisters of Mercy, Temple of Love  E G A                      i III IV
#   The Sisters of Mercy, Lucretia My Reflection  Am C Dm            i III iv
#   The Cure, Lullaby             C#m A                              i VI
# The lines are original: a high, melodic bass leading (Peter Hook), chorused guitar arpeggios,
# machine drums (the Sisters' Doktor Avalanche was a drum machine) and Joy Division's room kit.
# The bass leans on velocity and sits a little late on the off-beats (a NUDGE).
#   python3 tools/packs/postpunk.py

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the pack is written into the catalog: packs/postpunk/ravving/presets/…
PACK = os.path.join(os.path.dirname(os.path.dirname(HERE)), "packs", "postpunk")
sys.path.insert(0, HERE)
from patternkit import MINOR, Pack, N, C, R  # noqa: E402

pack = Pack("Post-Punk", PACK, MINOR)

# --- drums --------------------------------------------------------------------------------------
# She's Lost Control's kind: sixteenth hats, the snare cracking on two and four, the kick
# syncopated against it (Stephen Morris's machine-like playing), on a room kit
pack.drums("Lost Control", "ROOM", {
    "HAT":   "xxxxxxxxxxxxxxxx | xxxxxxxxxxxxxxxx",
    "SNARE": "....X.......X... | ....X.......X...",
    "KICK":  "X.....x.x....... | X.....x.x.....x.",
})
# the toms' post-punk (Joy Division's Atrocity Exhibition, Siouxsie's Budgie): a floor-tom figure
# instead of the backbeat, the kick on one, a rim on four
pack.drums("Tribal Toms", "ROOM", {
    "TOM":  "x.xx..x.xx..x.x. | x.xx..x.xx..xxxx",
    "KICK": "X.......x....... | X.......x.......",
    "PERC": "............x... | ............x...",
})
# Doktor Avalanche (the Sisters of Mercy's drum machine): a rigid four on the floor, the snare
# on two and four, the closed hat on the beat and the open one on its "and", a snare flam
# turning the phrase, on the Boss DR-55
pack.drums("Doktor Avalanche", "DR55", {
    "KICK":  "X...X...X...X... | X...X...X...X...",
    "SNARE": "....X.......X... | ....X.......X.xx",
    "HAT":   "x...x...x...x... | x...x...x...x...",
    "OPEN":  "..x...x...x...x. | ..x...x...x...x.",
})
# A Forest's run: kick on one and three, the snare on two and four, eighth hats with an open
# hat on the "and" of four, on the Roland CR-78
pack.drums("Forest Run", "CR78", {
    "KICK":  "X.......X.x..... | X.......X.......",
    "SNARE": "....X.......X... | ....X.......X...",
    "HAT":   "x.x.x.x.x.x.x... | x.x.x.x.x.x.x...",
    "OPEN":  "..............x. | ..............x.",
})
# Bela Lugosi's Dead's dub: the rim clicking a clave-like figure, soft sixteenth hats, the toms
# answering at the end of the phrase
pack.drums("Undead Dub", "ROOM", {
    "PERC": "x..x..x...x..x.. | x..x..x...x..x..",
    "HAT":  "..x...x...x...x. | ..x...x...x...x.",
    "KICK": "X............... | X.........x.....",
    "TOM":  "................ | ............x.xx",
})

# --- bass ---------------------------------------------------------------------------------------
# Peter Hook's lead bass over III VII i iv (Love Will Tear Us Apart's, here C G Am Dm): high
# on the neck, the melody carrying the song, the off-beats a hair late
pack.bass("Hook Melody", "Squier bass", " | ".join([
    " ".join([N("3+!@112", 4), N("2+@96>8", 2), N("1+@100", 2), N("7@96", 4), N("5@92>8", 2), N("7@96", 2)]),
    " ".join([N("1+!@112", 4), N("7@96>8", 2), N("5@100", 2), N("4@98", 6), N("3@90>8", 2)]),
    " ".join([N("3+!@112", 4), N("2+@96>8", 2), N("1+@100", 2), N("7@96", 4), N("1+@92>8", 2), N("2+@96", 2)]),
    " ".join([N("1+!@112", 6), N("7@96", 2), N("6@100", 4), N("5@94", 4)])]))
# A Forest's pulse: the root in eighths (Am C F D: i III VI and the Dorian IV), picked harder
# on the beat
def pulse(note, n):
    return " ".join(f"{note}@{110 if k % 2 == 0 else 90}" for k in range(n))
pack.bass("Forest Pulse", "Squier bass", " | ".join([
    pulse("1", 8), pulse("3", 8), pulse("6-", 8), pulse("4", 8)]),
    mods={"FILTER/CUTOFF": -1200})
# Bela Lugosi's Dead's dub bass: a falling figure, gaps between, everything a little behind the
# beat
pack.bass("Undead Dub Bass", "Squier bass", " | ".join([
    " ".join([N("1!@108>10", 3), R(1), N("7-@92>10", 2), N("6-@96>10", 4), R(2), N("5-@100>10", 4)]),
    " ".join([N("1!@108>10", 3), R(1), N("7-@92>10", 2), N("b7-@96>10", 2), N("6-@100>10", 6), R(2)])]))
# Disorder's run: busy eighths climbing the minor, the bass doubling the guitar's role
pack.bass("Disorder Run", "Squier bass", " | ".join([
    " ".join(f"{n}@{112 if k % 4 == 0 else 94}" for k, n in enumerate(["1", "1", "3", "1", "4", "3", "1", "7-", "1", "1", "3", "1", "5", "4", "3", "4"])),
    " ".join(f"{n}@{112 if k % 4 == 0 else 94}" for k, n in enumerate(["6-", "6-", "1", "6-", "3", "1", "6-", "5-", "7-", "7-", "2", "7-", "4", "3", "2", "7-"]))]))
# Boys Don't Cry's walk (A Bm C#m D, here C Dm Em F: III iv v VI), roots in eighths, up the scale
pack.bass("Boys Walk", "Squier bass", " | ".join([
    " ".join([pulse("3", 8), pulse("4", 8)]), " ".join([pulse("5", 8), pulse("6", 8)])]))

# --- lead ---------------------------------------------------------------------------------------
# A Forest's guitar: a chorused arpeggio in eighths over i III VI IV, the major IV's sixth raised
def arp(*notes):
    return " ".join(f"{n}@{104 if k % 2 == 0 else 86} _" for k, n in enumerate(notes))
pack.lead("Forest Arpeggio", "Guitar · Chorus", " | ".join([
    arp("1", "5", "1+", "3+", "5", "1+", "3+", "5"), arp("3", "7", "3+", "5+", "7", "3+", "5+", "7"),
    arp("6-", "3", "6", "1+", "3", "6", "1+", "3"), arp("4", "1+", "4+", "#6", "1+", "4+", "#6", "1+")]))
# Love Will Tear Us Apart's synth line kind: a falling, singing figure on the lead's own synth
pack.lead("Tear Apart Synth", "Calf Monosynth", " | ".join([
    " ".join([N("5+!", 4), N("4+", 2), N("3+", 2), N("2+", 4), N("1+", 4)]),
    " ".join([N("2+", 4), N("1+", 2), N("7", 2), N("5", 8)]),
    " ".join([N("5+!", 4), N("4+", 2), N("3+", 2), N("2+", 4), N("3+", 4)]),
    " ".join([N("4+", 4), N("3+", 2), N("2+", 2), N("1+", 7), R(1)])]))
# Spellbound's sixteenth arpeggios (Dorian: i VII IV), picked fast on the chorus guitar
def sixteenths(*notes):
    return " ".join(f"{n}@{108 if k % 4 == 0 else 84}" for k, n in enumerate(notes))
pack.lead("Spellbound Sixteenths", "Guitar · Chorus", " | ".join([
    sixteenths(*["1", "5", "1+", "5"] * 4), sixteenths(*["7-", "5", "7", "5"] * 4),
    sixteenths(*["4", "1+", "#6", "1+"] * 4), sixteenths(*["1", "5", "1+", "3+"] * 2 + ["5+", "3+", "1+", "5"] * 2)]))
# Temple of Love's chime (i III IV): high eighths ringing over the drum machine
pack.lead("Temple Chime", "Guitar · Valve OD", " | ".join([
    " ".join([N("5+@104", 2), N("3+@88", 2), N("5+@96", 2), N("1+@90", 2), N("5+@104", 2), N("3+@88", 2), N("5+@96", 2), N("3+@90", 2)]),
    " ".join([N("5+@104", 2), N("3+@88", 2), N("5+@96", 2), N("1+@90", 2), N("4+@104", 2), N("#6@88", 2), N("4+@96", 2), N("#6@90", 2)])]),
    mods={"MOTION/CHORUS": 500})
# Lullaby's creeping line (i VI): plucked notes tiptoeing, some a touch early
pack.lead("Lullaby Creep", "Guitar · Clean", " | ".join([
    " ".join([N("1+@96", 2), N("7@80<8", 2), N("1+@92", 2), N("3+@100", 4), N("2+@84<8", 2), N("1+@90", 4)]),
    " ".join([N("1+@96", 2), N("7@80<8", 2), N("6@92", 4), N("5@84<8", 2), N("6@96", 6)])]),
    mods={"MOTION/CHORUS": 400})

# --- chords -------------------------------------------------------------------------------------
# chromatic voicings, semitones from the key's root (A): the Dorian major IV, the triads
PP = {"i": ("c", [0, 3, 7, 12]), "III": ("c", [3, 7, 10, 15]), "VI": ("c", [-4, 0, 3, 8]),
      "IV": ("c", [5, 9, 12, 17]), "VII": ("c", [-2, 2, 5, 10]), "iv": ("c", [5, 8, 12, 17]),
      "v": ("c", [7, 10, 14, 19]), "i7": ("c", [0, 3, 7, 10]), "IVadd9": ("c", [5, 9, 12, 19]),
      "Dmaj": ("c", [5, 9, 12])}
# A Forest (Am C F D), a bar each, struck on one and pushed on the "and" of two
pack.chords("Forest Chords", "Guitar · Chorus", " | ".join(
    " ".join([C("@" + c, 5, 1), C("@" + c, 9, 1)]) for c in ["i", "III", "VI", "IVadd9"]), PP)
# Love Will Tear Us Apart (D A Bm Em, here C G Am Dm: III VII i iv), the string synth held
pack.chords("Tear Apart Strings", "Strings · Fat", " | ".join(
    C("@" + c, 15, 1) for c in ["III", "VII", "i", "iv"]), PP,
    mods={"ENVELOPE/ATTACK": 1200, "ENVELOPE/RELEASE": 1800})
# Boys Don't Cry (here C Dm Em F), strummed in eighths, two chords a bar
def eighth_strums(chord, n):
    return " ".join(C("@" + chord, 1, 1) for _ in range(n))
pack.chords("Boys Strum", "Guitar · Clean", " | ".join([
    " ".join([eighth_strums("III", 4), eighth_strums("iv", 4)]),
    " ".join([eighth_strums("v", 4), eighth_strums("VI", 4)])]), PP)
# Spellbound's Dorian (Dm7 C G, here Am7 G D), the 12-string held, its last chord pushed
pack.chords("Spellbound Dorian", "Guitar · 12-string", " | ".join([
    C("@i7", 15, 1), C("@VII", 15, 1), C("@IV", 15, 1), " ".join([C("@i7", 7, 1), C("@VII", 7, 1)])]), PP)
# Lucretia My Reflection's gloom (Am C Dm), on the organ's vox humana
pack.chords("Lucretia Gloom", "Organ · Vox humana", " | ".join([
    C("@i", 16), " ".join([C("@III", 8), C("@iv", 8)]), C("@i", 16), " ".join([C("@iv", 8), C("@III", 7, 1)])]), PP,
    mods={"ENVELOPE/RELEASE": 1800})

# the template: how a project plays these best (the projects dialog's TEMPLATES)
pack.template(142, "A", "Natural Minor", phaser=0.3, echo=0.3, heavy=0.3,
              about="Post-punk in A minor at 142: the chorus-drenched guitars as phaser, the echo of a cold room.")

if __name__ == "__main__":
    pack.done()
