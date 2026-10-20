#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Writes the site ravving reads: index.json (every entry with its files' URLs, sizes and
SHA-256), the files beside it under <kind>/<id>/, and each pack zipped as packs/<id>.zip.
A soundfont's file is its release asset: the URL points at the release, the size and hash
come from meta.json.

    python3 tools/build-index.py SITE_DIR [--base URL]

--base is what the file URLs start with (default the repository's GitHub Pages site); for a
local try, the site folder itself: --base file:///tmp/site/. The publish workflow runs it on
every push to main.
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import validate  # noqa: E402  (the same rules, run first)

DEFAULT_BASE = "https://ravving.github.io/ravving_repo/"
RELEASES = "https://github.com/ravving/ravving_repo/releases/download/"
SCHEMA_VERSION = 1


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def zip_pack(folder, target):
    """The pack's ravving folder as a zip, its members in a fixed order with fixed dates, so the
    same pack hashes the same on every build."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo(str(pathlib.PurePosixPath("ravving") / path.relative_to(folder)), date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                with open(path, "rb") as handle:
                    archive.writestr(info, handle.read())


def git_ref():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("site", help="the folder to write")
    parser.add_argument("--base", default=DEFAULT_BASE, help="what the file URLs start with")
    args = parser.parse_args()
    if validate.main([]) != 0:
        return 1
    base = args.base if args.base.endswith("/") else args.base + "/"
    site = pathlib.Path(args.site).resolve()
    site.mkdir(parents=True, exist_ok=True)
    entries = []
    for entry_dir in validate.entries([]):
        meta = validate.read_json(entry_dir / "meta.json")
        kind = entry_dir.parent.name
        listed = {key: meta[key] for key in ("id", "type", "name", "about", "author", "version", "license", "tags", "minAppVersion") if key in meta}
        files = []
        if meta["type"] == "soundfont":
            asset = meta["asset"]
            files.append({"path": asset["file"], "url": RELEASES + asset["release"] + "/" + asset["file"], "size": asset["size"], "sha256": asset["sha256"]})
        elif meta["type"] == "pack":
            name = meta["id"] + ".zip"
            target = site / "packs" / name
            zip_pack(entry_dir / "ravving", target)
            files.append({"path": name, "url": base + "packs/" + name, "size": target.stat().st_size, "sha256": sha256(target)})
            with zipfile.ZipFile(target) as archive:
                listed["count"] = sum(1 for member in archive.namelist() if member.endswith(".json"))
        else:
            for name in meta["files"]:
                source = entry_dir / name
                target = site / kind / meta["id"] / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                files.append({"path": name, "url": f"{base}{kind}/{meta['id']}/{name}", "size": source.stat().st_size, "sha256": sha256(source)})
                if meta["type"] == "pattern":
                    document = validate.read_json(source)
                    # the page's name for the library ("drum-presets.json" is the DRUMS' shared one)
                    group = document.get("library", "").replace("-presets.json", "")
                    listed["group"] = "DRUMS" if group == "drum" else group.upper()
                elif meta["type"] == "sound":
                    listed["group"] = validate.read_json(source).get("machine", "")
        listed["files"] = files
        entries.append(listed)
    index = {"schemaVersion": SCHEMA_VERSION,
             "generatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "ref": git_ref(),
             "entries": entries}
    with open(site / "index.json", "w", encoding="utf-8") as handle:
        json.dump(index, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    (site / ".nojekyll").write_text("")
    print(f"{len(entries)} entries → {site / 'index.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
