#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Checks every entry of the repository: its meta.json against schemas/meta.schema.json (the
same rules, without a jsonschema dependency), its files, their sizes, and that each file is
what its type says (a ravving preset document of that type, a stick layout for a pack, a
project for a project). Ids must be unique across the repository.

    python3 tools/validate.py [ENTRY_DIR ...]     # every entry by default; exit 1 on an error

The pull request check runs it; run it before opening one.
"""
import json
import os
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
KINDS = {"packs": "pack", "patterns": "pattern", "sounds": "sound", "templates": "template",
         "skins": "skin", "icons": "icons", "soundfonts": "soundfont", "projects": "project"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
VERSION_RE = re.compile(r"^[0-9]+(\.[0-9]+){0,2}$")
FILE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._·-]{0,127}$")
ASSET_FILE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._-]{0,127}\.(sf2|sf3)$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
STRING_LIMITS = {"name": 64, "about": 240, "author": 64, "license": 64}
PRESET_LIMIT = 256 * 1024
PACK_LIMIT = 8 * 1024 * 1024
PACK_FILES = 400
PROJECT_LIMIT = 64 * 1024 * 1024
PRESET_GROUPS = {"drums", "bass", "lead", "chords", "sampler", "pads"}
# an icon pack's icons: filled paths in straight lines on a 4-16 cell grid (ravving's IconPacks)
STRAIGHT_LINES = re.compile(r"^[MmLlHhVvZz0-9 .,\-]+$")


def fail(errors, entry, text):
    errors.append(f"{entry}: {text}")


def read_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def check_meta(meta, entry_dir, errors):
    """The schema's rules."""
    entry = entry_dir.relative_to(ROOT)
    if not isinstance(meta, dict):
        return fail(errors, entry, "meta.json is not an object")
    for key in ("id", "type", "name", "version"):
        if key not in meta:
            fail(errors, entry, f"meta.json lacks {key}")
    allowed = {"id", "type", "name", "about", "author", "version", "license", "tags", "minAppVersion", "files", "asset"}
    for key in meta:
        if key not in allowed:
            fail(errors, entry, f"meta.json has an unknown key: {key}")
    if not ID_RE.match(str(meta.get("id", ""))):
        fail(errors, entry, "id must be lower-case letters, digits and dashes (64 at most)")
    if meta.get("id") != entry_dir.name:
        fail(errors, entry, f"id {meta.get('id')!r} is not the folder's name")
    if meta.get("type") != KINDS.get(entry_dir.parent.name):
        fail(errors, entry, f"type {meta.get('type')!r} does not match the folder {entry_dir.parent.name}/")
    for key, limit in STRING_LIMITS.items():
        value = meta.get(key)
        if value is not None and (not isinstance(value, str) or not value.strip() or len(value) > limit):
            fail(errors, entry, f"{key} must be a non-empty string of at most {limit} characters")
    for key in ("version", "minAppVersion"):
        if key in meta and not VERSION_RE.match(str(meta[key])):
            fail(errors, entry, f"{key} must look like 1.2.3")
    tags = meta.get("tags", [])
    if not isinstance(tags, list) or len(tags) > 12 or any(not isinstance(t, str) or len(t) > 32 for t in tags):
        fail(errors, entry, "tags must be a list of at most 12 short strings")
    files = meta.get("files", [])
    if not isinstance(files, list) or len(files) > 8 or any(not isinstance(f, str) or not FILE_RE.match(f) for f in files):
        fail(errors, entry, "files must be a list of at most 8 plain file names")
    if "asset" in meta:
        asset = meta["asset"]
        if not isinstance(asset, dict) or set(asset) != {"release", "file", "size", "sha256"}:
            fail(errors, entry, "asset must hold release, file, size and sha256")
        else:
            if not re.match(r"^[A-Za-z0-9._-]{1,64}$", str(asset["release"])):
                fail(errors, entry, "asset.release must be a release tag")
            if not ASSET_FILE_RE.match(str(asset["file"])):
                fail(errors, entry, "asset.file must be an .sf2 or .sf3 name")
            if not isinstance(asset["size"], int) or asset["size"] < 1:
                fail(errors, entry, "asset.size must be the file's bytes")
            if not SHA_RE.match(str(asset["sha256"])):
                fail(errors, entry, "asset.sha256 must be 64 hex digits")


def preset_document(path, wanted, errors, entry):
    """A ravving preset file of the type wanted."""
    try:
        document = read_json(path)
    except (OSError, ValueError) as error:
        return fail(errors, entry, f"{path.name}: not JSON ({error})")
    if not isinstance(document, dict) or document.get("ravving") != "preset":
        return fail(errors, entry, f"{path.name}: not a ravving preset file")
    if document.get("type") != wanted:
        return fail(errors, entry, f"{path.name}: a {document.get('type')} file, not a {wanted}")
    body = document.get({"pattern": "preset", "sound": "sound", "template": "template", "skin": "skin", "icons": "pack"}[wanted])
    if not isinstance(body, dict) or not body.get("name"):
        fail(errors, entry, f"{path.name}: the {wanted} has no name")
    if wanted == "pattern" and (not isinstance(document.get("library"), str) or not document["library"].endswith("-presets.json")):
        fail(errors, entry, f"{path.name}: a pattern names its library (bass-presets.json)")
    if wanted == "pattern" and not isinstance(body.get("chart"), dict):
        fail(errors, entry, f"{path.name}: a pattern holds a chart")
    if wanted == "sound" and not isinstance(document.get("machine"), str):
        fail(errors, entry, f"{path.name}: a sound names its machine")
    if wanted == "skin" and not isinstance(body.get("machines"), dict):
        fail(errors, entry, f"{path.name}: a skin holds its machines' colours")
    if wanted == "icons" and isinstance(body, dict):
        grid, icons = body.get("grid"), body.get("icons")
        if not isinstance(grid, int) or not 4 <= grid <= 16:
            fail(errors, entry, f"{path.name}: an icon pack's grid is a whole number from 4 to 16")
        if not isinstance(icons, dict) or not icons:
            fail(errors, entry, f"{path.name}: an icon pack holds its icons")
        else:
            for name, d in icons.items():
                if not isinstance(d, str) or not STRAIGHT_LINES.match(d.strip()):
                    fail(errors, entry, f"{path.name}: {name} must be a path in straight lines (M L H V Z)")


def check_pack(folder, errors, entry):
    """A stick's layout: ravving/presets/<group>/patterns/*.json and templates/*.json."""
    presets = folder / "presets"
    if not presets.is_dir():
        return fail(errors, entry, "a pack's ravving folder holds presets/")
    count, total = 0, 0
    for path in folder.rglob("*"):
        if path.is_symlink():
            fail(errors, entry, f"{path.relative_to(folder)}: no symlinks")
        if not path.is_file():
            continue
        count += 1
        total += path.stat().st_size
        rel = path.relative_to(presets).parts if presets in path.parents else ()
        if path.suffix != ".json" or not rel:
            fail(errors, entry, f"{path.relative_to(folder)}: only preset .json files under presets/")
            continue
        if rel[0] == "templates" and len(rel) == 2:
            preset_document(path, "template", errors, entry)
        elif rel[0] == "skins" and len(rel) == 2:
            preset_document(path, "skin", errors, entry)
        elif rel[0] == "icons" and len(rel) == 2:
            preset_document(path, "icons", errors, entry)
        elif len(rel) == 3 and rel[1] == "patterns" and rel[0] in PRESET_GROUPS:
            preset_document(path, "pattern", errors, entry)
        elif len(rel) == 3 and rel[1] == "sounds":
            preset_document(path, "sound", errors, entry)
        else:
            fail(errors, entry, f"{path.relative_to(folder)}: not where a stick keeps it (<group>/patterns, <machine>/sounds, templates, skins, icons)")
    if count == 0:
        fail(errors, entry, "the pack is empty")
    if count > PACK_FILES:
        fail(errors, entry, f"the pack holds {count} files; {PACK_FILES} at most")
    if total > PACK_LIMIT:
        fail(errors, entry, f"the pack is {total // 1024} KB; {PACK_LIMIT // 1024 // 1024} MB at most")


def check_files(meta, entry_dir, errors):
    entry = entry_dir.relative_to(ROOT)
    kind = meta.get("type")
    files = meta.get("files", [])
    present = sorted(p.name for p in entry_dir.iterdir() if p.name != "meta.json")
    if kind == "soundfont":
        if "asset" not in meta:
            fail(errors, entry, "a soundfont names its release asset")
        if files or present:
            fail(errors, entry, "a soundfont's file is attached to a release, not committed")
        return
    if "asset" in meta:
        fail(errors, entry, "only a soundfont has an asset")
    if not files:
        return fail(errors, entry, "files names what the entry ships")
    for name in files:
        path = entry_dir / name
        if path.is_symlink() or not path.exists():
            fail(errors, entry, f"{name}: missing (or a symlink)")
            continue
        if kind == "pack":
            if name != "ravving" or not path.is_dir():
                fail(errors, entry, "a pack's files is [\"ravving\"], the folder a stick holds")
            else:
                check_pack(path, errors, entry)
        elif kind in ("pattern", "sound", "template", "skin", "icons"):
            if not path.is_file() or path.suffix != ".json":
                fail(errors, entry, f"{name}: a {kind} is one .json file")
            elif path.stat().st_size > PRESET_LIMIT:
                fail(errors, entry, f"{name}: over {PRESET_LIMIT // 1024} KB")
            else:
                preset_document(path, kind, errors, entry)
        elif kind == "project":
            if not path.is_file() or path.suffix not in (".ravv", ".json"):
                fail(errors, entry, f"{name}: a project is a .ravv bundle or a .json file")
            elif path.stat().st_size > PROJECT_LIMIT:
                fail(errors, entry, f"{name}: over {PROJECT_LIMIT // 1024 // 1024} MB")
            elif path.suffix == ".ravv" and not zipfile.is_zipfile(path):
                fail(errors, entry, f"{name}: not a bundle")
    stray = [name for name in present if name not in files]
    if stray:
        fail(errors, entry, f"files not named in meta.json: {', '.join(stray)}")


def entries(paths):
    if paths:
        return [pathlib.Path(p).resolve() for p in paths]
    found = []
    for kind in KINDS:
        folder = ROOT / kind
        if folder.is_dir():
            found.extend(sorted(p for p in folder.iterdir() if p.is_dir()))
    return found


def main(argv):
    errors = []
    ids = {}
    checked = 0
    for entry_dir in entries(argv):
        entry = entry_dir.relative_to(ROOT) if ROOT in entry_dir.parents else entry_dir
        meta_path = entry_dir / "meta.json"
        if not meta_path.is_file():
            fail(errors, entry, "no meta.json")
            continue
        try:
            meta = read_json(meta_path)
        except (OSError, ValueError) as error:
            fail(errors, entry, f"meta.json is not JSON ({error})")
            continue
        check_meta(meta, entry_dir, errors)
        check_files(meta, entry_dir, errors)
        if isinstance(meta, dict) and meta.get("id") in ids:
            fail(errors, entry, f"id {meta['id']!r} is also {ids[meta['id']]}")
        elif isinstance(meta, dict):
            ids[meta.get("id")] = entry
        checked += 1
    for line in errors:
        print(line)
    print(f"{checked} entries, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
