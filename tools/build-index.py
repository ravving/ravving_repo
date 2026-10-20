#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Camilo Higuita <milo.h@aol.com>
# SPDX-License-Identifier: GPL-3.0-or-later
"""Writes the site ravving reads: index.json (every entry with its files' URLs, sizes and
SHA-256), the files beside it under <kind>/<id>/, each pack zipped as packs/<id>.zip, and
index.html, the same catalog as a page for a browser (the ravving site's look).
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
import html
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


KIND_TITLES = [("pack", "Packs", "a genre's template and twenty-odd presets for the drums, the bass, the lead and the chords"),
               ("pattern", "Patterns", "single pattern presets"), ("sound", "Sounds", "saved sounds"),
               ("template", "Templates", "project templates"), ("skin", "Skins", "sets of the instruments' colours"),
               ("soundfont", "Soundfonts", ".sf2 and .sf3 files"), ("project", "Projects", "demo projects and .ravv bundles")]
SITE = "https://ravving.github.io/"


def esc(text):
    return html.escape(str(text), quote=True)


def size_text(size):
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.0f} KB"
    return f"{size / 1024 / 1024:.1f} MB"


def page(entries, generated):
    """The catalog as a web page in the ravving site's own look (its stylesheet), for a
    browser: what GET MORE lists, with a download per entry."""
    sections = []
    for kind, title, about in KIND_TITLES:
        listed = [e for e in entries if e["type"] == kind]
        cards = []
        for e in listed:
            meta = " · ".join(part for part in [e.get("group", ""), e.get("author", ""), e.get("version", ""),
                                                size_text(sum(f["size"] for f in e["files"])), ", ".join(e.get("tags", []))] if part)
            links = " ".join(f'<a class="btn" href="{esc(f["url"])}" download>{esc(f["path"])}</a>' for f in e["files"])
            words = " ".join([e["name"], e.get("about", ""), e.get("author", ""), e.get("group", ""), e.get("version", "")] + e.get("tags", [])).lower()
            cards.append(f'<article class="card" data-words="{esc(words)}"><div class="card-head"><h3>{esc(e["name"])}</h3></div>'
                         f'<p>{esc(e.get("about", ""))}</p><p class="mono">{esc(meta)}</p><p>{links}</p></article>')
        body = "\n".join(cards) if cards else '<p class="mono">nothing here yet · be the first to contribute</p>'
        sections.append(f'<section class="wrap" id="{kind}s"><h2>{title} <span class="mono">{len(listed)}</span></h2>'
                        f'<p class="lede">{esc(about)}</p><div class="cards">{body}</div></section>')
    nav = " ".join(f'<a href="#{kind}s">{title}</a>' for kind, title, _ in KIND_TITLES)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ravving · get more</title>
<meta name="description" content="Free packs, presets, skins, soundfonts and projects for ravving: what the GET MORE dialog lists, to download or to contribute to.">
<link rel="stylesheet" href="{SITE}site.css">
<link rel="icon" type="image/png" sizes="32x32" href="{SITE}assets/favicon-32.png">
<style>
.catalog-nav {{ display: flex; flex-wrap: wrap; gap: 8px 18px; justify-content: center; margin: 24px auto 0; }}
section.wrap {{ margin-top: clamp(32px, 6vw, 64px); }}
section.wrap h2 {{ text-transform: uppercase; }}
section.wrap h2 .mono {{ margin-left: 10px; }}
.card p {{ margin: 6px 0 0; }}
.find {{ width: min(100%, 420px); margin: 22px auto 0; display: block; padding: 10px 14px; border: 1px solid var(--hair); border-radius: 8px; background: var(--panel); color: var(--ink); font-family: var(--font-mono); font-size: var(--t-label); }}
.card .btn {{ display: inline-block; margin: 8px 8px 0 0; padding: 6px 12px; border: 1px solid var(--hair); border-radius: 6px; font-family: var(--font-mono); font-size: var(--t-caps); text-decoration: none; }}
</style>
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="{SITE}" aria-label="ravving"><img class="wordmark" src="{SITE}assets/ravving.svg" alt="ravving" width="822" height="104"></a>
    <nav aria-label="Sections">
      <a href="{SITE}">ravving</a>
      <a href="https://github.com/ravving/ravving_repo">Contribute</a>
    </nav>
  </div>
</header>
<main id="top">
  <section class="landing-hero wrap">
    <p class="landing-eyebrow mono">Free and open · {len(entries)} entries · {esc(generated[:10])}</p>
    <h1>Get more</h1>
    <p class="lede">Packs, presets, skins, soundfonts and projects for ravving. On your MIKO: MENU → GET MORE lists the same, and brings one in with a tap. Here, a download each; put a file on a USB stick's <code>ravving/presets</code> folder and the USB page takes it in.</p>
    <nav class="catalog-nav mono" aria-label="Kinds">{nav}</nav>
    <p><input class="find" type="search" placeholder="FIND · a genre, a tempo, a colour…" aria-label="Find" autocomplete="off"></p>
  </section>
{"".join(sections)}
</main>
<script>
// FIND: every word typed must be in a card's words (its name, line, author, group, tags)
document.querySelector(".find").addEventListener("input", event => {{
  const words = event.target.value.toLowerCase().split(/\\s+/).filter(w => w.length > 0);
  for (const card of document.querySelectorAll(".card")) {{
    card.hidden = !words.every(w => card.dataset.words.includes(w));
  }}
}});
</script>
<footer><div class="wrap"><p>Everything here is free to download, use and remix (CC-BY-4.0 unless an entry says otherwise). Add yours: <a href="https://github.com/ravving/ravving_repo/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a>.</p></div></footer>
</body>
</html>
"""


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
    (site / "index.html").write_text(page(entries, index["generatedAt"]), encoding="utf-8")
    (site / ".nojekyll").write_text("")
    print(f"{len(entries)} entries → {site / 'index.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
