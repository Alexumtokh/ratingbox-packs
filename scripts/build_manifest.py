#!/usr/bin/env python3
"""Builds manifest.json for every .json / .zip pack in packs/.

The folder gives the file's kind (the app imports each kind into its own
data): packs/questions/ -> "questions", packs/books/ -> "book",
packs/dicts/ -> "dict". Files right
in packs/ are "questions" (the old layout). Hosts keep files flat, so a
file name must be unique across all folders.

A file's version goes up by one only when its sha256 changed since the
committed manifest.json. Optional packs/titles.json ({"id": "Title"}) gives
display names. With <out dir>, every pack file is also copied there.
Usage: build_manifest.py <packs dir> <manifest path> [<out dir>]
"""
import hashlib
import json
import os
import re
import shutil
import sys
import time

packs_dir, manifest_path = sys.argv[1], sys.argv[2]
out_dir = sys.argv[3] if len(sys.argv) > 3 else None

# Folder (relative to packs/) -> kind written to the manifest.
KINDS = {"": "questions", "questions": "questions", "books": "book",
         "dicts": "dict"}

old = {}
if os.path.exists(manifest_path):
    with open(manifest_path, encoding="utf-8") as f:
        old = {e["id"]: e for e in json.load(f).get("files", [])}

titles = {}
titles_path = os.path.join(packs_dir, "titles.json")
if os.path.exists(titles_path):
    with open(titles_path, encoding="utf-8") as f:
        titles = json.load(f)

files, bad, seen = [], [], {}
for folder, kind in KINDS.items():
    folder_path = os.path.join(packs_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    for name in sorted(os.listdir(folder_path)):
        path = os.path.join(folder_path, name)
        if (not os.path.isfile(path) or not name.endswith((".json", ".zip"))
                or name in ("titles.json", "manifest.json")):
            continue
        if not re.fullmatch(r"[A-Za-z0-9._-]+", name):
            bad.append(os.path.join(folder, name))
            continue
        if name in seen:
            sys.exit(f"Bir xil fayl nomi ikki papkada: {seen[name]} va "
                     f"{os.path.join(folder, name)}")
        seen[name] = os.path.join(folder, name)
        with open(path, "rb") as f:
            data = f.read()
        file_id = re.sub(r"\.(json|zip)$", "", name)
        sha = hashlib.sha256(data).hexdigest()
        prev = old.get(file_id, {})
        prev_version = int(prev.get("version", 0))
        version = prev_version if prev.get("sha256") == sha else prev_version + 1
        entry = {"id": file_id, "version": version, "file": name,
                 "sha256": sha, "size": len(data), "kind": kind}
        if file_id in titles:
            entry["title"] = titles[file_id]
        files.append(entry)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            shutil.copyfile(path, os.path.join(out_dir, name))
        print(f"{kind:9} {file_id}  v{version}"
              f"{'  (new)' if version != prev_version else ''}")

if bad:
    sys.exit("Fayl nomida faqat lotin harflari, raqam, '.', '-', '_' bo'lsin "
             "(bo'sh joy yo'q): " + ", ".join(bad))

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump({"generated": int(time.time()), "files": files}, f,
              ensure_ascii=False, indent=2)
    f.write("\n")
print(f"{manifest_path}: {len(files)} files")
