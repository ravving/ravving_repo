#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# What every secret genre pack's build.py writes its presets with: the same files as the jazz
# pack (jazz-presets/build.py), one per preset, laid out as a USB stick holds them
# (PresetExchange):
#
#     <pack>/ravving/presets/<drums|bass|lead|chords>/patterns/<Genre> · <Name>.json
#     {"ravving": "preset", "type": "pattern", "library": "<x>-presets.json",
#      "preset": {"name", "genre", "chart", "sound"}}
#
# "sound" is the sound the pattern is meant for, a subset of Machine::soundState():
# {"soundSource": "<a source of the machine>"} for the bass, lead and chords (kits.json's
# machines[].sourceName or sources[].name), {"kit": "<kit path>"} for the drums
# (DrumMachine::kitPath()). validate.py checks the names against kits.json.
#
# A bass, lead or chords preset may bring MODS for its source too (mods={"CARD/KNOB": value}),
# written in the engine's own units as data/engines.json gives each knob's min and max (the
# soundfonts' FILTER/CUTOFF in cents, -8400 to 0), or a choice knob by its label: they go in as
# the knob positions the machine keeps (0-1), under "sourceSound" for a soundfont source (one
# set for all of a machine's soundfonts) or "sourceSounds"/<source> for a synth source (the
# 808 · Monosynth). A drums preset's MODS are its kit's (engines.json's kitSound: TONE, SHAPE,
# PITCH on the whole kit), under "sound". Loading the preset WITH ITS SOUND + MODS puts that
# set back whole (its other knobs at rest); a preset without MODS leaves the machine's alone.
#
# The patterns are written as step grids that read like a tracker, one token or character a
# 16th, "|" and spaces only for the eye:
#
#   drums   one string per role (KICK SNARE CLAP TOM HAT OPEN CYMBAL PERC): x a hit, X an
#           accented one. An accent is the whole step's (DrumMachine::setAccent), so every
#           hit on an accented step is written X, as the machine's own chart() writes it.
#   mono    (bass, lead) tokens: "." a rest, "_" the note before still sounding (HOLD), or a
#           note: [b|#]<degree 1-7>[+|-][!][~][@velocity][<|>nudge]: b/# a semitone down/up
#           (written as the degree below plus ALTER, as MonoMachine::chart() does), +/- an
#           octave, ! an accent, ~ a slide into the next note (which must start where this one
#           ends), @64 the note's own velocity (1-127, SELECT's knob 2), <10 / >10 the note
#           played that % of a step early / late (SELECT's NUDGE, at most 50): the chart's
#           VELOCITY and NUDGE lanes, by step.
#   chords  tokens: "." nothing, "=" the chord before goes on, "1"-"7" the chord on that
#           degree (stacked in thirds, as the CHORD SET says), "@name" a voicing of the
#           pack's own: ("x", scale degrees from degree I, 0-based) or ("c", semitones from
#           the chord base). Two hits of the same chord need a "." between them, or they
#           are one held chord (ChordMachine::writePattern).

import json
import math
import os
import re

STEPS = 16
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]  # the "Natural Minor" of Rave.qml's scales
# Rave.qml's scales by name (a template names its scale; Templates::scaleNames())
SCALES = {"Natural Minor": MINOR, "Major": MAJOR, "Dorian": [0, 2, 3, 5, 7, 9, 10],
          "Phrygian": [0, 1, 3, 5, 7, 8, 10], "Lydian": [0, 2, 4, 6, 7, 9, 11],
          "Mixolydian": [0, 2, 4, 5, 7, 9, 10], "Harmonic Minor": [0, 2, 3, 5, 7, 8, 11]}
ROOTS = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6,
         "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
ROLES = ["KICK", "SNARE", "CLAP", "TOM", "HAT", "OPEN", "CYMBAL", "PERC"]

# the sounds, by their names in data/kits.json (the drum kits by their paths, as kitPath()
# gives them: the machines' default soundfonts, a demo's, and kits.json's presetKits)
DRUM_MACHINES = "/zynthian/zynthian-data/soundfonts/SFZ Drum Machines/"
GM = "/zynthian/zynthian-data/soundfonts/SF2 Instruments/FluidR3Mono_GM.sf3"
KITS = {
    "TR909": DRUM_MACHINES + "Roland TR909.sf3",
    "TR808": DRUM_MACHINES + "Roland TR808.sf3",
    "LINN": DRUM_MACHINES + "LINN9000 1.sf3",
    "SP1200": DRUM_MACHINES + "SP1200 1.sf3",
    "STANDARD": GM + "#128:0",
    "ROOM": GM + "#128:8",
    "JAZZ": GM + "#128:32?CYMBAL=51&HAT=44",
    "JAZZ_CRASH": GM + "#128:32",  # kits.json presetKits "Jazz · crash": the climaxes' crash
    "BRUSH": GM + "#128:40",
    "BRUSH_RIDE": GM + "#128:40?CYMBAL=51&HAT=44",  # kits.json presetKits "Brush · ride"
    "POWER": GM + "#128:16",      # kits.json presetKits, added with these packs
    # the orchestra kit: KICK concert bass drum, SNARE concert snare, TOM timpani C, HAT timpani
    # G (the dominant below), OPEN triangle, CYMBAL concert crash, PERC tambourine, CLAP castanets
    "ORCHESTRA": GM + "#128:48?TOM=48&HAT=43&OPEN=81&CYMBAL=57&PERC=54",
    # cumbia: PERC güiro, TOM timbale, CYMBAL cowbell (the campana), CLAP conga (the llamador)
    "CUMBIA": GM + "#128:0?PERC=73&TOM=65&CYMBAL=56&CLAP=63",
    "CUMBIA_ROOM": GM + "#128:8?PERC=74&TOM=66&CYMBAL=56&CLAP=63",
    # salsa / son: SNARE open conga, CLAP conga slap, TOM tumba, HAT claves, OPEN maracas,
    # CYMBAL cowbell (campana), PERC güiro; KICK the kit's kick
    "CONGAS": GM + "#128:0?SNARE=63&CLAP=62&TOM=64&HAT=75&OPEN=70&CYMBAL=56&PERC=73",
    # merengue / bachata: SNARE high bongo, TOM low bongo, CLAP conga slap, OPEN tumba (the
    # tambora's low stroke), HAT maracas, CYMBAL cowbell, PERC cabasa (the metal güira)
    "GUIRA": GM + "#128:0?SNARE=60&TOM=61&CLAP=62&OPEN=64&HAT=70&CYMBAL=56&PERC=69",
    # the kit folder's machines (the kit picker lists them all): post-punk's and the 80s'
    "DR55": DRUM_MACHINES + "Boss DR55.sf3",
    "CR78": DRUM_MACHINES + "Roland CR78.sf3",
    "HR16": DRUM_MACHINES + "Alesis HR16.sf3",
    "SIMMONS": DRUM_MACHINES + "Simmons.sf3",
    "TR606": DRUM_MACHINES + "Roland TR606.sf3",
    # kits.json presetKits, added with the folk / metal / post-punk / gothic packs: the AVL
    # acoustic kits (their LV2s' soundfonts) and the folk room kit (TOM a low floor tom for the
    # bodhrán, PERC the tambourine, CYMBAL the ride)
    "BLACK_PEARL": "/zynthian/zynthian-plugins/lv2/Black_Pearl_5.lv2/FluidPlug.sf2",
    "RED_ZEPPELIN": "/zynthian/zynthian-plugins/lv2/Red_Zeppelin_5.lv2/FluidPlug.sf2",
    "FOLK": GM + "#128:8?TOM=41&PERC=54&CYMBAL=51",
    # the orchestra kit with its timpani on D (TOM) and A below (HAT): a D-minor or D-Dorian
    # tonic and dominant, for the Gregorian pack
    "ORCHESTRA_D": GM + "#128:48?TOM=50&HAT=45&OPEN=81&CYMBAL=57&PERC=54",
}

LIBRARY = {"drums": "drum-presets.json", "bass": "bass-presets.json",
           "lead": "lead-presets.json", "chords": "chord-presets.json"}

# ravving's data folder (kits.json, engines.json): RAVVING_DATA, else the ravving checkout
# beside this repository (~/Coding/ravving next to ~/Coding/ravving_repo)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.environ.get("RAVVING_DATA") or os.path.join(os.path.dirname(REPO), "ravving", "data")


def _load(name):
    with open(os.path.join(DATA, name)) as f:
        return json.load(f)


def source_mods(machine, source):
    """Where a source's MODS go in a sound ("sourceSound", or "sourceSounds" for a synth
    source; "sound" for a drum kit) and its knobs as engines.json gives them, as
    EngineProfiles::profileFor finds the profile: by the engine's type, a jalv by its URI (a
    kit: the soundfont profile's kitSound, EngineProfiles::resolveKit)."""
    if machine == "drums":
        profile = next(p for p in _load("engines.json")["engines"] if p["type"] == "fluidsynth")
        return "sound", profile["kitSound"]
    for entry in _load("kits.json")["machines"]:
        if entry["key"] != machine:
            continue
        for candidate in entry.get("sources", []):
            if candidate["name"] != source:
                continue
            engine = candidate["engine"]
            for profile in _load("engines.json")["engines"]:
                if profile["type"] == engine["type"] and (engine["type"] != "jalv" or profile.get("uri") == engine.get("uri")):
                    return ("sourceSound" if engine["type"] == "fluidsynth" else "sourceSounds"), profile["sound"]
            raise ValueError(f"{source}: no engine profile in engines.json")
    raise ValueError(f"{machine} has no source {source!r} with MODS")


def knob_position(knob, value):
    """A knob's position (0-1) for a value in the engine's units, or a choice by its label."""
    choices = knob.get("choices")
    if choices:
        labels = [c["label"] for c in choices]
        return labels.index(value) / (len(labels) - 1)
    low, high = knob.get("min", 0.0), knob.get("max", 1.0)
    if not min(low, high) <= value <= max(low, high):
        raise ValueError(f"{knob['name']}: {value} is outside {low}..{high}")
    if knob.get("curve") == "log" and low > 0:
        return round(math.log(value / low) / math.log(high / low), 4)
    return round((value - low) / (high - low), 4)


def mods_state(machine, source, mods):
    """The sound's MODS part for `mods` ({"CARD/KNOB": value}): {"sourceSound": {...}} or
    {"sourceSounds": {source: {...}}}."""
    where, cards = source_mods(machine, source)
    positions = {}
    for key, value in mods.items():
        card_title, knob_name = key.split("/", 1)
        knob = next((k for c in cards if c["title"] == card_title for k in c["knobs"] if k["name"] == knob_name), None)
        if knob is None:
            raise ValueError(f"{source}: no MODS knob {key}")
        positions[key] = knob_position(knob, value)
    return {where: {source: positions}} if where == "sourceSounds" else {where: positions}


def _grid(text):
    return re.sub(r"[\s|]", "", text)


def _tokens(text):
    return [t for t in re.split(r"[\s|]+", text) if t]


class Pack:
    def __init__(self, genre, here, scale):
        self.genre = genre
        self.out = os.path.join(here, "ravving", "presets")
        self.scale = scale
        self.names = set()

    def _write(self, group, name, chart, sound):
        full = f"{self.genre} · {name}"
        if full in self.names:
            raise ValueError(f"{full}: written twice")
        self.names.add(full)
        if re.search(r'[/\\:*?"<>|]', full):
            raise ValueError(f"{full}: not a FAT file name (PresetExchange fileNameOf)")
        folder = os.path.join(self.out, group, "patterns")
        os.makedirs(folder, exist_ok=True)
        document = {"ravving": "preset", "type": "pattern", "library": LIBRARY[group],
                    "preset": {"name": full, "genre": self.genre, "chart": chart, "sound": sound}}
        with open(os.path.join(folder, full + ".json"), "w") as f:
            json.dump(document, f, indent=4, ensure_ascii=False)
            f.write("\n")

    @staticmethod
    def _length(name, length):
        if length % STEPS or not 1 <= length // STEPS <= 8:
            raise ValueError(f"{name}: {length} steps is not 1-8 bars of {STEPS}")

    # --- drums ------------------------------------------------------------------------------
    def drums(self, name, kit, rows, mods=None):
        rows = {role: _grid(line) for role, line in rows.items()}
        lengths = {len(line) for line in rows.values()}
        if len(lengths) != 1:
            raise ValueError(f"{name}: rows of different lengths {lengths}")
        length = lengths.pop()
        self._length(name, length)
        for role, line in rows.items():
            if role not in ROLES or set(line) - set(".xX"):
                raise ValueError(f"{name}: bad role or characters in {role}")
        accented = {i for line in rows.values() for i, c in enumerate(line) if c == "X"}
        chart = {}
        for role in ROLES:  # in the kit's order
            if role in rows:
                chart[role] = "".join("." if c == "." else ("X" if i in accented else "x")
                                      for i, c in enumerate(rows[role]))
        sound = {"kit": KITS[kit]}
        if mods:
            sound.update(mods_state("drums", KITS[kit], mods))
        self._write("drums", name, chart, sound)

    # --- bass and lead ----------------------------------------------------------------------
    def _note(self, token):
        m = re.fullmatch(r"([#b]?)([1-7])([+-]?)([!~]*)(?:@(\d{1,3}))?(?:([<>])(\d{1,2}))?", token)
        if not m:
            raise ValueError(f"bad note token {token!r}")
        shift, degree, octave, flags, velocity, way, nudge = m.groups()
        self._extra = (int(velocity) if velocity else None,
                       (-1 if way == "<" else 1) * int(nudge) if nudge else 0)
        if self._extra[0] is not None and not 1 <= self._extra[0] <= 127:
            raise ValueError(f"{token!r}: velocity out of 1-127")
        if abs(self._extra[1]) > 50:
            raise ValueError(f"{token!r}: nudge past half a step")
        semitones = self.scale[int(degree) - 1] + {"+": 12, "-": -12, "": 0}[octave] + {"#": 1, "b": -1, "": 0}[shift]
        octave = semitones // 12
        pc = semitones - 12 * octave
        if octave not in (-1, 0, 1):
            raise ValueError(f"{token!r} is out of the chart's three octaves")
        d = max(i for i, s in enumerate(self.scale) if s <= pc)
        return d + 1, octave, pc - self.scale[d], "!" in flags, "~" in flags

    def _sound(self, group, source, mods):
        sound = {"soundSource": source}
        if mods:
            sound.update(mods_state(group, source, mods))  # the groups are the machines' keys
        return sound

    def _mono(self, group, name, source, text, mods=None):
        tokens = _tokens(text)
        length = len(tokens)
        self._length(name, length)
        lanes = {lane: ["."] * length for lane in ("NOTES", "OCTAVE", "ACCENT", "SLIDE", "HOLD", "ALTER")}
        sounding = False
        starts = []
        velocities, nudges = {}, {}
        for i, token in enumerate(tokens):
            if token == ".":
                sounding = False
            elif token == "_":
                if not sounding:
                    raise ValueError(f"{name}: a hold at step {i} with no note before it")
                lanes["HOLD"][i] = "x"
            else:
                degree, octave, alter, accent, slide = self._note(token)
                lanes["NOTES"][i] = str(degree)
                lanes["OCTAVE"][i] = "+" if octave > 0 else "-" if octave < 0 else "."
                if alter:
                    lanes["ALTER"][i] = str(alter)
                lanes["ACCENT"][i] = "x" if accent else "."
                lanes["SLIDE"][i] = "x" if slide else "."
                velocity, nudge = self._extra
                if velocity is not None:
                    velocities[str(i)] = velocity
                if nudge:
                    nudges[str(i)] = nudge
                sounding = True
                starts.append(i)
        # a slide glides into the note that starts where it ends
        for i in starts:
            if lanes["SLIDE"][i] == "x":
                end = i + 1
                while end < length and lanes["HOLD"][end] == "x":
                    end += 1
                if lanes["NOTES"][end % length] == ".":  # past the end: the loop's first step
                    raise ValueError(f"{name}: the slide at step {i} glides into nothing")
        chart = {lane: "".join(chars) for lane, chars in lanes.items()}
        # the shipped charts leave out lanes with nothing in them (MonoMachine::chart())
        for lane in ("HOLD", "ALTER"):
            if set(chart[lane]) == {"."}:
                del chart[lane]
        # the notes' own velocity and nudge (MonoMachine::applyChart), by step
        if velocities:
            chart["VELOCITY"] = velocities
        if nudges:
            chart["NUDGE"] = nudges
        self._write(group, name, chart, self._sound(group, source, mods))

    def bass(self, name, source, text, mods=None):
        self._mono("bass", name, source, text, mods)

    def lead(self, name, source, text, mods=None):
        self._mono("lead", name, source, text, mods)

    # --- chords -----------------------------------------------------------------------------
    def chords(self, name, source, text, voicings=None, mods=None, ties=None):
        """`ties`: where the notes a voicing change keeps are held on instead of struck again
        (chord_ties()): "all", or a list of the steps; none (the default) strikes every chord."""
        voicings = voicings or {}
        tokens = _tokens(text)
        length = len(tokens)
        self._length(name, length)
        line, chart_voicings = [], {}
        current = None  # the voicing sounding at the step before
        for i, token in enumerate(tokens):
            if token == ".":
                line.append(".")
                current = None
                continue
            if token == "=":
                if current is None:
                    raise ValueError(f"{name}: '=' at step {i} with no chord before it")
                voicing = current
            elif re.fullmatch(r"[1-7]", token):
                voicing = ("d", token)
                if voicing == current:
                    raise ValueError(f"{name}: chord {token} at step {i} would merge with the one before")
            elif token.startswith("@"):
                kind, notes = voicings[token[1:]]
                voicing = (kind, tuple(notes))
                if voicing == current:
                    raise ValueError(f"{name}: {token} at step {i} would merge with the one before")
            else:
                raise ValueError(f"{name}: bad chord token {token!r}")
            if voicing[0] == "d":
                line.append(voicing[1])
            else:
                line.append(voicing[0])
                chart_voicings[str(i)] = list(voicing[1])
            current = voicing
        chart = {"CHORDS": "".join(line)}
        if chart_voicings:
            chart["VOICINGS"] = chart_voicings
        if ties:
            chart["TIES"] = chord_ties(chart, self.scale, ties, name)
        self._write("chords", name, chart, self._sound("chords", source, mods))

    def template(self, bpm, root, scale, name=None, **settings):
        """A template of the pack (write_template()); its scale must be the pack's own. A pack
        has one at least, named after it; more take a `name` of their own ("Vuelo · Crave")."""
        if SCALES.get(scale) != self.scale:
            raise ValueError(f"{self.genre}: the template's {scale} is not the scale the pack is written in")
        write_template(self.out, name or self.genre, bpm, root, scale, genre=self.genre, **settings)
        self.has_template = True

    def done(self):
        if not getattr(self, "has_template", False):
            raise ValueError(f"{self.genre}: no template (pack.template(…) before pack.done())")
        count = sum(len(files) for _, _, files in os.walk(self.out))
        print(f"{count} presets under {self.out}")


def template_sounds(sounds):
    """A template's sounds (Templates' "sounds") from `sounds`: a drum machine's kit by its KITS
    key ({"drums1": "JAZZ"}), the bass's, lead's or chords' source by its kits.json name
    ({"lead": "Grand piano"}), each checked."""
    out = {}
    for machine, sound in sounds.items():
        if machine.startswith("drums"):
            if sound not in KITS:
                raise ValueError(f"{machine}: no kit {sound!r} in KITS")
            out[machine] = {"kit": KITS[sound]}
            continue
        entry = next((m for m in _load("kits.json")["machines"] if m["key"] == machine), None)
        names = [entry.get("sourceName")] + [c["name"] for c in entry.get("sources", [])] if entry else []
        if sound not in names:
            raise ValueError(f"{machine}: no source {sound!r} in kits.json")
        out[machine] = {"soundSource": sound}
    return out


def template_sections(sections):
    """A template's sections (Templates' "sections" and "song") from `sections`: (name, bars)
    pairs in order, bars 0 for AUTO, each played once in the song, the colours in turn."""
    listed = [{"name": name, "colour": index % 8, "bars": bars} for index, (name, bars) in enumerate(sections)]
    # Sections' limits: 16 sections, names of 12 characters, 8 bars at most (0 is AUTO)
    if not 1 <= len(listed) <= 16:
        raise ValueError(f"{len(listed)} sections, not 1-16")
    for section in listed:
        if not section["name"] or len(section["name"]) > 12 or not 0 <= section["bars"] <= 8:
            raise ValueError(f"section {section['name']!r}: a name of 1-12 characters, 0-8 bars")
    return listed, [{"section": index, "repeats": 1} for index in range(len(listed))]


def write_template(out, name, bpm, root, scale, swing=50, phaser=0.0, echo=0.0, heavy=0.0,
                   about="", swing_eighths=False, genre=None, sounds=None, sections=None):
    """A pack's project template (src/backend/templates.h): the tempo, swing, key and LIVE
    FX its presets are best played with, at <out>/templates/<name>.json (`out` the pack's
    ravving/presets; `name` the pack's, or a template's own, with `genre` the pack's). `root`
    a note name ("E", "F#"), `scale` a name of SCALES, `swing` as the header shows it
    (50–75 %), the LIVE FX knobs 0..1; `sounds` the machines' sounds (template_sounds()) and
    `sections` the song's sections (template_sections()), both optional."""
    genre = genre or name
    if scale not in SCALES:
        raise ValueError(f"{name}: no scale {scale!r} (one of {', '.join(SCALES)})")
    if root not in ROOTS:
        raise ValueError(f"{name}: no root {root!r}")
    if not 30 <= bpm <= 300 or not 50 <= swing <= 75:
        raise ValueError(f"{name}: {bpm} BPM, SWING {swing} out of range")
    for knob, value in (("phaser", phaser), ("echo", echo), ("heavy", heavy)):
        if not 0 <= value <= 1:
            raise ValueError(f"{name}: {knob} {value} is not 0..1")
    folder = os.path.join(out, "templates")
    os.makedirs(folder, exist_ok=True)
    template = {"name": name, "genre": genre, "about": about, "bpm": bpm, "swing": swing,
                "swingEighths": swing_eighths, "root": ROOTS[root], "scale": scale,
                "phaser": phaser, "echo": echo, "heavy": heavy}
    if sounds:
        template["sounds"] = template_sounds(sounds)
    if sections:
        template["sections"], template["song"] = template_sections(sections)
    with open(os.path.join(folder, name + ".json"), "w") as f:
        json.dump({"ravving": "preset", "type": "template", "template": template}, f, indent=4, ensure_ascii=False)
        f.write("\n")


# ChordMachine's Classic chord set: the notes of each degree's chord (I to VII)
CLASSIC_SIZES = [4, 4, 3, 4, 4, 4, 3]


def _degree_semitones(scale, degree):
    octave = degree // len(scale)
    return scale[degree - octave * len(scale)] + 12 * octave


def chord_pitches(scale, char, notes):
    """The pitches (semitones from degree I) a chart step plays, in the order ChordMachine lists
    them (a tie names a note by its place in that order): a degree's chord stacked in thirds
    (the Classic set), "x" scale degrees, "c" semitones."""
    if char in "1234567":
        degree = int(char) - 1
        return [_degree_semitones(scale, degree + 2 * third) for third in range(CLASSIC_SIZES[degree])]
    if char == "x":
        return [_degree_semitones(scale, n) for n in notes]
    return list(notes)


def chord_ties(chart, scale, steps="all", name=""):
    """A chords chart's TIES: on each voicing change (no rest between, `steps` "all" or the
    listed ones), the places in the new voicing of the notes the one before also plays, held on
    instead of struck again. A listed step that keeps no note is an error."""
    line, voicings = chart["CHORDS"], chart.get("VOICINGS", {})
    ties = {}
    for i in range(1, len(line)):
        before, after = line[i - 1], line[i]
        if "." in (before, after) or (before, voicings.get(str(i - 1))) == (after, voicings.get(str(i))):
            continue  # a rest, or the same voicing going on
        held = chord_pitches(scale, before, voicings.get(str(i - 1), []))
        places = [k for k, pitch in enumerate(chord_pitches(scale, after, voicings.get(str(i), []))) if pitch in held]
        if places and (steps == "all" or i in steps):
            ties[str(i)] = places
    if steps != "all" and set(steps) - {int(step) for step in ties}:
        raise ValueError(f"{name}: ties on steps {sorted(set(steps) - {int(step) for step in ties})} that keep no note")
    return ties


def N(token, length=1, gap=0):
    """A note held `length` steps, then `gap` steps of rest: N("5-", 3, 1) → "5- _ _ ."."""
    return " ".join([token] + ["_"] * (length - 1) + ["."] * gap)


def C(token, length=1, gap=0):
    """A chord held `length` steps, then `gap` steps of nothing: C("@I", 3, 1) → "@I = = ."."""
    return " ".join([token] + ["="] * (length - 1) + ["."] * gap)


def R(steps):
    """`steps` steps of rest."""
    return " ".join(["."] * steps)


def power(degree):
    """A power chord on a scale degree (0-based): root, fifth, octave, in scale degrees."""
    return ("x", [degree, degree + 4, degree + 7])


def cpower(semitones):
    """A power chord on a chromatic root (semitones from the key's root): a ♭VII in major."""
    return ("c", [semitones, semitones + 7, semitones + 12])
