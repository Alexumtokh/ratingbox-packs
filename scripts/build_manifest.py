#!/usr/bin/env python3
"""Builds manifest.json for every .json / .zip pack in packs/.

A file's version goes up by one only when its sha256 changed since the
committed manifest.json. Optional packs/titles.json ({"id": "Title"}) gives
display names. Usage: build_manifest.py <packs dir> <manifest path>
"""
import hashlib
import json
import os
import re
import sys
import time

packs_dir, manifest_path = sys.argv[1], sys.argv[2]

old = {}
if os.path.exists(manifest_path):
    with open(manifest_path, encoding="utf-8") as f:
        old = {e["id"]: e for e in json.load(f).get("files", [])}

titles = {}
titles_path = os.path.join(packs_dir, "titles.json")
if os.path.exists(titles_path):
    with open(titles_path, encoding="utf-8") as f:
        titles = json.load(f)

files, bad = [], []
for name in sorted(os.listdir(packs_dir)):
    if not name.endswith((".json", ".zip")) or name in ("titles.json", "manifest.json"):
        continue
    if not re.fullmatch(r"[A-Za-z0-9._-]+", name):
        bad.append(name)
        continue
    with open(os.path.join(packs_dir, name), "rb") as f:
        data = f.read()
    file_id = re.sub(r"\.(json|zip)$", "", name)
    sha = hashlib.sha256(data).hexdigest()
    prev = old.get(file_id, {})
    prev_version = int(prev.get("version", 0))
    version = prev_version if prev.get("sha256") == sha else prev_version + 1
    entry = {"id": file_id, "version": version, "file": name,
             "sha256": sha, "size": len(data)}
    if file_id in titles:
        entry["title"] = titles[file_id]
    files.append(entry)
    print(f"{file_id}  v{version}{'  (new)' if version != prev_version else ''}")

if bad:
    sys.exit("Fayl nomida faqat lotin harflari, raqam, '.', '-', '_' bo'lsin "
             "(bo'sh joy yo'q): " + ", ".join(bad))

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump({"generated": int(time.time()), "files": files}, f,
              ensure_ascii=False, indent=2)
    f.write("\n")
print(f"{manifest_path}: {len(files)} files")
