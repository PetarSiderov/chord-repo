#!/usr/bin/env python3
# Batch runner for Pesmarica → ChordPro
# CSV format (header required):
# Title,Artist,URL,Key,TempoBPM,Meter,Docx,PianoHints,KeepTabs
# Example row:
# Nekako s Proleća,Crvena Jabuka,https://www.pesmarica.rs/akordi/350/Crvena-Jabuka--Nekako-s-Prole%C4%87a,G,74,4/4,yes,yes,no

import csv
import subprocess
import sys
from pathlib import Path

def booly(x: str) -> bool:
    return str(x).strip().lower() in ("y","yes","1","true","t")

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/pesmarica_batch.py data/song-sources.csv")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}")
        sys.exit(1)

    for row in csv.DictReader(csv_path.open(encoding="utf-8")):
        title = row.get("Title"," ").strip()
        artist = row.get("Artist"," ").strip()
        url = row.get("URL"," ").strip()
        key = row.get("Key"," ").strip() or None
        tempo = row.get("TempoBPM"," ").strip() or None
        meter = row.get("Meter"," ").strip() or None
        docx = booly(row.get("Docx","no"))
        piano = booly(row.get("PianoHints","no"))
        keeptabs = booly(row.get("KeepTabs","no"))

        cmd = [
            sys.executable, "tools/pesmarica_to_chordpro.py",
            "--url", url, "--title", title, "--artist", artist,
            "--outdir", "lyrics-output"
        ]
        if key:   cmd += ["--key", key]
        if tempo: cmd += ["--tempo", tempo]
        if meter: cmd += ["--meter", meter]
        if docx:  cmd += ["--docx"]
        if piano: cmd += ["--piano-hints"]
        if keeptabs: cmd += ["--keep-tabs"]
        else: cmd += ["--strip-tabs"]

        print("Running:", " ".join(cmd))
        subprocess.check_call(cmd)

if __name__ == "__main__":
    main()