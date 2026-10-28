#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Checks every secret pack's preset files (jazz included) against what ravving's parsers
# accept, so a pack copied to a stick loads as written:
#
#   PresetExchange::stickPatterns / loadStickPattern: {"ravving": "preset", "type": "pattern",
#       "library": the group's library file, "preset": {"name", "genre", "chart"}}, the file at
#       <group>/patterns/<fileNameOf(name)>
#   PresetLibrary::barsOf: the longest row / 16, rounded up; Machine::MaxBars = 8
#   DrumMachine::applyChart: a row per role, "x" a hit, "X" an accented one (the step's)
#   MonoMachine::applyChart: NOTES 1-7, OCTAVE + -, ACCENT SLIDE HOLD x, ALTER a digit;
#       HOLD runs after a note, at most MaxLength (64) steps a note
#   ChordMachine::applyChart: CHORDS 1-7 x c, VOICINGS by step for the x and c steps; STRIKES,
#       VELOCITY, NUDGE, STRUM, HOMES by a chord's step; TIES by step: the places of the notes
#       held on through a change of voicing (none: every note struck with its chord)
#   Machine::applySoundParts / DrumMachine::applySoundParts: "sound" {"soundSource": a
#       source's name in kits.json} or {"kit": a kit path}; a source's MODS with it,
#       "sourceSound" (a soundfont source) or "sourceSounds" {source: …} (a synth source),
#       knob positions 0-1 by "CARD/KNOB" as engines.json names them (patternkit.mods_state);
#       a drums preset's kit MODS under "sound" (engines.json kitSound)
#
# Errors are what the parsers would drop or misread; warnings are what plays but is probably
# not what was meant. Also checks that no two presets of a genre and instrument are the same
# or nearly so.
#   python3 validate.py         # exit status 1 on any error

import glob
import json
import os
import re
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from patternkit import SCALES, source_mods  # noqa: E402  (where a source's MODS go, its knobs; the scales)
from patternkit import DATA, REPO  # noqa: E402  (ravving's data folder, this repository)
STEPS, MAX_BARS, MAX_LENGTH = 16, 8, 64
ROLES = {"KICK", "SNARE", "CLAP", "TOM", "HAT", "OPEN", "CYMBAL", "PERC"}
MONO = {"NOTES", "OCTAVE", "ACCENT", "SLIDE", "HOLD", "ALTER"}
LIBRARY = {"drums": "drum-presets.json", "bass": "bass-presets.json",
           "lead": "lead-presets.json", "chords": "chord-presets.json"}
NEAR = 0.8  # Jaccard similarity of two presets' notes at which they count as near-identical

errors, warnings = [], []
# milo's SFZ Drum Machines folder (kits.json kitFolder), listed 2026-10-10
KIT_FOLDER = {f + ".sf3" for f in (
    "Acetone Rhythm Ace", "Akai XE8", "Akai XR10", "Alesis HR16", "Boss DR220", "Boss DR55", "DrumFire",
    "DrumTraks", "Drumula 1", "Drumula 2", "E Ave", "Electro Puff", "Fricke MSB512", "Kawai R50", "Korg DDD1",
    "Korg DDM110", "Lab", "LINN9000 1", "LINN9000 2", "Mattel Synsonic", "MXR 185", "Retrobox", "Roland CR78",
    "Roland TR606", "Roland TR727", "Roland TR808", "Roland TR909", "SCI Tom", "Simmons", "SP1200 1",
    "SP1200 2", "SP 12", "Sween", "Tama Tech Star 1", "Tama Tech Star 2", "Tama Tech Star 3", "Tyson 1",
    "Tyson 2", "Tyson 3", "Yamaha RX11")}


def known_sounds():
    """The source names each machine offers and the drum kits, from kits.json (and the kit
    paths the shipped demos use, which name soundfonts of the kit folder)."""
    kits = json.load(open(os.path.join(DATA, "kits.json")))
    sources = {}
    for machine in kits["machines"]:
        names = [machine.get("sourceName", "SYNTH")] + [s["name"] for s in machine.get("sources", [])]
        sources[machine["key"]] = set(names)
        # the machine's own presets file is the library its stick presets must name
        if machine["key"] in LIBRARY and machine.get("presets") != LIBRARY[machine["key"]]:
            errors.append(f"kits.json: {machine['key']} reads {machine.get('presets')}, not {LIBRARY[machine['key']]}")
    paths = {m["engine"]["soundfont"] for m in kits["drumMachines"]} | {k["path"] for k in kits["presetKits"]}
    # the kit folder's machines (the kit picker lists the folder): as on milo, 2026-10-10
    paths |= {kits["kitFolder"].rstrip("/") + "/" + name for name in KIT_FOLDER}
    for demo in glob.glob(os.path.join(DATA, "demos", "*.json")):
        paths |= set(re.findall(r'"kit": "([^"]+)"', open(demo).read()))
    return sources, paths


SOURCES, KITS = known_sounds()

# The device's FluidR3Mono_GM.sf3 is MuseScore 2.3.2's (its sha256 is zynthbox-qml's
# config/soundfonts.json SF_00022). With a copy of it here, every bank:program kits.json takes
# from it is checked to exist (a missing preset would leave the source silent).
GM_FONT = "/zynthian/zynthian-data/soundfonts/SF2 Instruments/FluidR3Mono_GM.sf3"
GM_SHA256 = "cfcd66d89e8386823400eca64934b14fbea7bf48ba1f00d21189af1262794ec2"
GM_COPY = os.environ.get("FLUIDR3MONO", os.path.expanduser("~/Downloads/ravving-soundfonts/fluidr3mono/FluidR3Mono_GM.sf3"))


def check_gm_presets():
    import hashlib
    import struct
    if not os.path.exists(GM_COPY):
        return f"skipped (no copy of the device's FluidR3Mono_GM.sf3 at {GM_COPY})"
    data = open(GM_COPY, "rb").read()
    if hashlib.sha256(data).hexdigest() != GM_SHA256:
        return f"skipped ({GM_COPY} is not the device's FluidR3Mono_GM.sf3)"
    at = data.find(b"phdr")
    size = struct.unpack("<I", data[at + 4:at + 8])[0]
    phdr = data[at + 8:at + 8 + size]
    have = {struct.unpack_from("<HH", phdr, i + 20)[::-1] for i in range(0, len(phdr) - 38, 38)}
    kits = json.load(open(os.path.join(DATA, "kits.json")))
    wanted = []
    for machine in kits["machines"]:
        for source in machine.get("sources", []):
            engine = source["engine"]
            if engine.get("soundfont") == GM_FONT:
                wanted.append((f"{machine['key']} source {source['name']!r}", (engine.get("bank", 0), engine.get("program", 0))))
    for kit in kits["presetKits"]:
        if kit["path"].startswith(GM_FONT + "#"):
            bank, program = kit["path"][len(GM_FONT) + 1:].split("?")[0].split(":")
            wanted.append((f"kit {kit['name']!r}", (int(bank), int(program))))
    for what, preset in wanted:
        if preset not in have:
            errors.append(f"kits.json: {what} wants FluidR3Mono_GM {preset[0]}:{preset[1]}, which the font does not have")
    return f"{len(wanted)} FluidR3Mono_GM presets kits.json uses, checked against the device's font"


# lv2info dumps of the engines kits.json's jalv sources play (taken on the device for the
# engine mods): every control a source sets is checked to be a port within its range
LV2INFO = {"http://calf.sourceforge.net/plugins/Monosynth":
           os.path.expanduser("~/Coding/engine-mods/calf_monosynth_mod/docs/engine-symbols.txt")}


def lv2_ports(path):
    ports, symbol = {}, None
    low = high = None
    for line in open(path):
        line = line.strip()
        if line.startswith("Port ") or line.startswith("Symbol:"):
            if line.startswith("Symbol:"):
                symbol = line.split()[1]
        if line.startswith("Minimum:"):
            low = float(line.split()[1])
        if line.startswith("Maximum:"):
            high = float(line.split()[1])
            if symbol:
                ports[symbol] = (low, high)
    return ports


def check_jalv_sources():
    kits = json.load(open(os.path.join(DATA, "kits.json")))
    checked = 0
    for machine in kits["machines"]:
        for source in machine.get("sources", []):
            engine = source["engine"]
            dump = LV2INFO.get(engine.get("uri", ""))
            if engine.get("type") != "jalv" or not dump:
                continue
            if not os.path.exists(dump):
                return f"skipped (no lv2info dump at {dump})"
            ports = lv2_ports(dump)
            for symbol, value in engine.get("controls", {}).items():
                checked += 1
                if symbol not in ports:
                    errors.append(f"kits.json: {machine['key']} source {source['name']!r} sets {symbol!r}, no port of {engine['uri']}")
                elif not ports[symbol][0] <= value <= ports[symbol][1]:
                    errors.append(f"kits.json: {machine['key']} source {source['name']!r} sets {symbol} {value} outside {ports[symbol]}")
    return f"{checked} jalv source controls checked against the engines' lv2info ports"


def file_name_of(name):
    return re.sub(r'[/\\:*?"<>|]', "_", name).strip() + ".json"


def rows_of(where, chart, keys):
    """The chart's string rows, checked for keys, length and bars."""
    unknown = set(chart) - keys
    if unknown:
        errors.append(f"{where}: unknown chart keys {sorted(unknown)}")
    rows = {k: v for k, v in chart.items() if k in keys}
    for key, row in rows.items():
        if not isinstance(row, str):
            errors.append(f"{where}: {key} is not a string")
            return None
    lengths = {len(r) for r in rows.values()}
    if len(lengths) != 1:
        errors.append(f"{where}: rows of different lengths {sorted(lengths)}")
    length = max(lengths)
    if length % STEPS:
        errors.append(f"{where}: {length} steps is not a whole number of {STEPS}-step bars")
    if not 1 <= -(-length // STEPS) <= MAX_BARS:
        errors.append(f"{where}: {length} steps is more than {MAX_BARS} bars")
    return rows, length


def chars(where, key, row, allowed):
    bad = set(row) - set(allowed)
    if bad:
        errors.append(f"{where}: {key} has characters {sorted(bad)} (allowed: {allowed})")


def check_drums(where, chart):
    rows, length = rows_of(where, chart, ROLES)
    for role, row in rows.items():
        chars(where, role, row, ".xX")
    if not any(c in "xX" for row in rows.values() for c in row):
        errors.append(f"{where}: no hits")
    accented = {i for row in rows.values() for i, c in enumerate(row) if c == "X"}
    mixed = sorted(i for i in accented if any(row[i] == "x" for row in rows.values()))
    if mixed:
        warnings.append(f"{where}: steps {mixed} accented on one row, not on another (an accent is the whole step's)")
    return {(role, i % length) for role, row in rows.items() for i, c in enumerate(row) if c in "xX"}, length


def check_mono(where, chart):
    if "NOTES" not in chart:
        errors.append(f"{where}: no NOTES")
        return set(), 16
    # the notes' own velocity and nudge, by step (MonoMachine::applyChart): checked below
    by_step = {k: chart[k] for k in ("VELOCITY", "NUDGE") if k in chart}
    chart = {k: v for k, v in chart.items() if k not in by_step}
    rows, length = rows_of(where, chart, MONO)
    lane = lambda key: rows.get(key, "." * length)  # noqa: E731
    notes, octave, accent, slide, hold, alter = (lane(k) for k in ("NOTES", "OCTAVE", "ACCENT", "SLIDE", "HOLD", "ALTER"))
    chars(where, "NOTES", notes, ".1234567")
    chars(where, "OCTAVE", octave, ".+-")
    for key in ("ACCENT", "SLIDE", "HOLD"):
        chars(where, key, lane(key), ".x")
    chars(where, "ALTER", alter, ".123456789")
    for key, values in by_step.items():
        if not isinstance(values, dict):
            errors.append(f"{where}: {key} is not a map of steps")
            continue
        for step, value in values.items():
            if not step.isdigit() or int(step) >= length or notes[int(step)] not in "1234567":
                errors.append(f"{where}: {key} at step {step}, where no note starts")
            elif key == "VELOCITY" and not (isinstance(value, int) and 1 <= value <= 127):
                errors.append(f"{where}: VELOCITY {value!r} at step {step} (1-127)")
            elif key == "NUDGE" and not (isinstance(value, (int, float)) and -50 <= value <= 50 and value != 0):
                errors.append(f"{where}: NUDGE {value!r} at step {step} (-50..50 %, not 0)")
    if not any(c in "1234567" for c in notes):
        errors.append(f"{where}: no notes")
    signature = set()
    for i in range(length):
        is_note = notes[i] in "1234567"
        for key, row in (("OCTAVE", octave), ("ACCENT", accent), ("SLIDE", slide), ("ALTER", alter)):
            if row[i] != "." and not is_note:
                errors.append(f"{where}: {key} at step {i}, where no note starts")
        if hold[i] == "x" and is_note:
            errors.append(f"{where}: HOLD at step {i}, where a note starts (the note before would sound over it)")
        if hold[i] == "x" and i > 0 and notes[i - 1] not in "1234567" and hold[i - 1] != "x":
            errors.append(f"{where}: HOLD at step {i} after a rest")
        if is_note:
            end = i + 1
            while end < length and hold[end] == "x":
                end += 1
            if end - i > MAX_LENGTH:
                errors.append(f"{where}: the note at step {i} is longer than {MAX_LENGTH} steps")
            if slide[i] == "x" and notes[end % length] not in "1234567":
                warnings.append(f"{where}: the slide at step {i} ends on a rest (no note to glide into)")
            signature.add((i, notes[i], octave[i], alter[i]))
    return signature, length


def check_chords(where, chart):
    if "CHORDS" not in chart:
        errors.append(f"{where}: no CHORDS")
        return set(), 16
    unknown = set(chart) - {"CHORDS", "VOICINGS", "STRIKES", "VELOCITY", "NUDGE", "STRUM", "HOMES", "TIES"}
    if unknown:
        errors.append(f"{where}: unknown chart keys {sorted(unknown)}")
    rows, length = rows_of(where, {"CHORDS": chart["CHORDS"]}, {"CHORDS"})
    line = rows["CHORDS"]
    chars(where, "CHORDS", line, ".1234567xc")
    voicings = chart.get("VOICINGS", {})
    if not isinstance(voicings, dict):
        errors.append(f"{where}: VOICINGS is not a map")
        voicings = {}
    custom = {str(i) for i, c in enumerate(line) if c in "xc"}
    if set(voicings) - custom:
        errors.append(f"{where}: VOICINGS for steps {sorted(set(voicings) - custom, key=int)} that are no x or c step")
    if custom - set(voicings):
        errors.append(f"{where}: x/c steps {sorted(custom - set(voicings), key=int)} with no VOICINGS (they play nothing)")
    signature = set()
    for i, c in enumerate(line):
        if c == ".":
            continue
        if c in "xc":
            notes = voicings.get(str(i), [])
            if not notes or not all(isinstance(n, int) for n in notes):
                errors.append(f"{where}: step {i}'s voicing is not a list of whole numbers")
                continue
            low, high = (-14, 20) if c == "x" else (-24, 36)
            if not all(low <= n <= high for n in notes):
                errors.append(f"{where}: step {i}'s voicing {notes} is outside {low}..{high}")
            if len(set(notes)) != len(notes):
                warnings.append(f"{where}: step {i}'s voicing {notes} doubles a note")
            signature.add((i, c, tuple(notes)))
        else:
            signature.add((i, c))
    # TIES: by step, the places (from the lowest note, 0) of the notes held on from the step
    # before through a change of voicing; both steps must play, and the place must exist
    ties = chart.get("TIES", {})
    if not isinstance(ties, dict):
        errors.append(f"{where}: TIES is not a map")
        ties = {}
    for step, places in ties.items():
        i = int(step) if step.isdigit() else -1
        if i < 1 or i >= len(line) or line[i] == "." or line[i - 1] == ".":
            errors.append(f"{where}: TIES on step {step}, which has no chord on it and the step before")
            continue
        size = len(voicings.get(step, [])) if line[i] in "xc" else 4
        if not isinstance(places, list) or not all(isinstance(n, int) and 0 <= n < size for n in places):
            errors.append(f"{where}: TIES on step {step} is not a list of places 0..{size - 1}")
    if not signature:
        errors.append(f"{where}: no chords")
    return signature, length


def check_sound(where, group, sound, required):
    if sound is None:
        if required:
            errors.append(f"{where}: no sound")
        return "-"
    if not isinstance(sound, dict):
        errors.append(f"{where}: sound is not a map")
        return "?"
    key = "kit" if group == "drums" else "soundSource"
    mods = {k: sound[k] for k in (("sound",) if group == "drums" else ("sourceSound", "sourceSounds")) if k in sound}
    if set(sound) - set(mods) != {key}:
        errors.append(f"{where}: sound {sorted(sound)} must hold {key!r} (and its MODS) only")
    value = sound.get(key, "")
    if mods:
        check_mods(where, group, value, mods)
    known = KITS if group == "drums" else SOURCES[group if group != "chords" else "chords"]
    if value not in known:
        errors.append(f"{where}: {key} {value!r} is not one kits.json (or a demo) knows")
    return value


def check_mods(where, group, source, mods):
    """A preset's MODS: under the key its source's kind takes, every knob one of its engine
    profile's, every position 0-1 (a choice knob's on one of its choices)."""
    try:
        where_key, cards = source_mods(group, source)
    except ValueError as e:
        errors.append(f"{where}: MODS: {e}")
        return
    if set(mods) != {where_key}:
        errors.append(f"{where}: {source}'s MODS go under {where_key!r}, not {sorted(mods)}")
        return
    positions = mods[where_key]
    if where_key == "sourceSounds":
        if set(positions) != {source}:
            errors.append(f"{where}: sourceSounds names {sorted(positions)}, not the preset's source {source!r}")
            return
        positions = positions[source]
    knobs = {f"{c['title']}/{k['name']}": k for c in cards for k in c["knobs"]}
    for name, position in positions.items():
        knob = knobs.get(name)
        if knob is None:
            errors.append(f"{where}: no MODS knob {name} on {source}")
        elif not isinstance(position, (int, float)) or not 0 <= position <= 1:
            errors.append(f"{where}: {name} at {position!r}, not a position 0-1")
        elif knob.get("choices") and abs(position * (len(knob["choices"]) - 1) - round(position * (len(knob["choices"]) - 1))) > 1e-6:
            errors.append(f"{where}: {name} at {position}, between two of its choices")


CHECKS = {"drums": check_drums, "bass": check_mono, "lead": check_mono, "chords": check_chords}


def tiled(signature, length, to):
    """A preset's notes repeated to `to` steps, to compare a 1-bar with a 2-bar one."""
    return {(s[0] + k * length,) + s[1:] if isinstance(s[0], int) else (s[0], s[1] + k * length)
            for s in signature for k in range(to // length)}


def main():
    names = {}
    packs = sorted(p for p in glob.glob(os.path.join(REPO, "packs", "*")) if os.path.isdir(os.path.join(p, "ravving")))
    for pack in packs:
        pack_name = os.path.basename(pack)
        required = pack_name != "jazz"  # the jazz pack came before sounds
        counts, presets = {}, {}
        for group in LIBRARY:
            folder = os.path.join(pack, "ravving", "presets", group, "patterns")
            files = sorted(glob.glob(os.path.join(folder, "*.json")))
            counts[group] = len(files)
            for path in files:
                where = f"{pack_name}/{group}/{os.path.basename(path)}"
                try:
                    document = json.load(open(path))
                except ValueError as e:
                    errors.append(f"{where}: not JSON ({e})")
                    continue
                if set(document) != {"ravving", "type", "library", "preset"}:
                    errors.append(f"{where}: document keys {sorted(document)}")
                if document.get("ravving") != "preset" or document.get("type") != "pattern":
                    errors.append(f"{where}: not a ravving pattern preset")
                if document.get("library") != LIBRARY[group]:
                    errors.append(f"{where}: library {document.get('library')!r} is not {LIBRARY[group]!r}")
                preset = document.get("preset", {})
                if set(preset) - {"name", "genre", "chart", "sound"} or not {"name", "genre", "chart"} <= set(preset):
                    errors.append(f"{where}: preset keys {sorted(preset)}")
                name, genre = preset.get("name", ""), preset.get("genre", "")
                if os.path.basename(path) != file_name_of(name):
                    errors.append(f"{where}: the file is not named after {name!r}")
                if not name.startswith(genre + " · "):
                    errors.append(f"{where}: {name!r} is not '<genre> · <name>'")
                if name in names:
                    errors.append(f"{where}: {name!r} is also {names[name]}")
                names[name] = where
                chart = preset.get("chart", {})
                if not isinstance(chart, dict) or not chart:
                    errors.append(f"{where}: an empty chart (loadStickPattern refuses it)")
                    continue
                signature, length = CHECKS[group](where, chart)
                sound = check_sound(where, group, preset.get("sound"), required)
                presets[(group, name)] = (signature, length, sound)
        # a template at least (more for a pack with several grooves), the pack's tempo, swing,
        # key and LIVE FX (patternkit.write_template)
        templates = sorted(glob.glob(os.path.join(pack, "ravving", "presets", "templates", "*.json")))
        if not templates:
            errors.append(f"{pack_name}: no template")
        for path in templates:
            where = f"{pack_name}/templates/{os.path.basename(path)}"
            document = json.load(open(path))
            template = document.get("template", {})
            if document.get("ravving") != "preset" or document.get("type") != "template":
                errors.append(f"{where}: not a ravving template")
            if template.get("scale") not in SCALES or not 0 <= template.get("root", -1) <= 11:
                errors.append(f"{where}: key {template.get('root')} {template.get('scale')!r}")
            if not 30 <= template.get("bpm", 0) <= 300 or not 50 <= template.get("swing", 50) <= 75:
                errors.append(f"{where}: {template.get('bpm')} BPM, SWING {template.get('swing')}")
            genres = {preset_genre for (_, n) in presets for preset_genre in [n.split(" · ")[0]]}
            if genres and template.get("genre") not in genres:
                errors.append(f"{where}: genre {template.get('genre')!r} is not the presets' {sorted(genres)}")
        # five of each instrument, three in the smaller packs (piig) or six (solos), the same for all four
        if len(set(counts.values())) != 1 or set(counts.values()) - {3, 5, 6}:
            errors.append(f"{pack_name}: {dict(counts)} presets, not 5 (or 3, or 6) of each instrument")
        # no two of a genre and instrument the same, or nearly
        closest = {}
        for group in LIBRARY:
            items = [(n, s, l) for (g, n), (s, l, _) in presets.items() if g == group]
            best = 0.0
            for (a, sa, la), (b, sb, lb) in combinations(items, 2):
                to = max(la, lb)
                ta, tb = tiled(sa, la, to), tiled(sb, lb, to)
                similarity = len(ta & tb) / max(1, len(ta | tb))
                best = max(best, similarity)
                if similarity >= NEAR:
                    errors.append(f"{pack_name}: {a!r} and {b!r} are {similarity:.0%} the same")
            closest[group] = best
        print(f"{pack_name:22} " + "  ".join(f"{g} {counts[g]}" for g in LIBRARY)
              + "   most alike: " + " ".join(f"{g} {closest[g]:.0%}" for g in LIBRARY))
    print("soundfont:", check_gm_presets())
    print("engines:", check_jalv_sources())
    for warning in warnings:
        print("warning:", warning)
    for error in errors:
        print("ERROR:", error)
    print(f"{len(names)} presets in {len(packs)} packs: {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
