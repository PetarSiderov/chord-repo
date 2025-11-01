#!/usr/bin/env python3
# Purpose: For personal/educational use. Converts a Pesmarica.rs song page to ChordPro (.pro).
# NOTE: Do not commit generated .pro files to a public repo without rights.
# Usage (single):
#   python tools/pesmarica_to_chordpro.py --url "https://www.pesmarica.rs/akordi/350/Crvena-Jabuka--Nekako-s-Prole%C4%87a" --title "Nekako s Proleća" --artist "Crvena Jabuka" --key "G" --tempo 74 --meter "4/4" --docx --piano-hints --strip-tabs
#
# Limitations:
# - Site structure may change; adjust selectors accordingly.
# - This script is for local/offline personal use; respect site TOS and copyright.

import argparse
import os
import re
import sys
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except Exception:
    print("Please install dependencies: pip install requests beautifulsoup4 python-docx (optional)")
    sys.exit(1)

def extract_text_blocks(html):
    soup = BeautifulSoup(html, "html.parser")
    # Prefer <pre>
    pre = soup.find("pre")
    if pre and pre.get_text(strip=False):
        return pre.get_text(strip=False)
    # Try known containers
    for sel in ["div.song", "div#song", "div.content", "article", "div.post-entry"]:
        node = soup.select_one(sel)
        if node and node.get_text(strip=False):
            return node.get_text(strip=False)
    body = soup.find("body")
    return body.get_text("\n", strip=False) if body else ""

CHORD_TOKEN = re.compile(r"\b([A-G](?:#|b)?m?(?:maj7|m7|7|sus2|sus4|dim|aug)?)(/[A-G](?:#|b)?)?\b")
TAB_LINE = re.compile(r"^\s*([eE]|B|G|D|A)\s*\|.*")  # crude ASCII TAB detector

def piano_hint_block(key: str):
    scale = {
        "G": "G major (G A B C D E F#) / Em pentatonic (E G A B D)",
        "F#m": "F# natural minor / A major",
        "Am": "A natural minor (A B C D E F G) / A minor pentatonic (A C D E G)",
        "Em": "E natural minor (E F# G A B C D) / E minor pentatonic (E G A B D)",
        "Dm": "D natural minor / D minor pentatonic",
        "Fm": "F natural minor",
        "Cm": "C natural minor",
        "F": "F major (F G A Bb C D E)",
        "D": "D major (D E F# G A B C#)"
    }.get(key, f"{key} scale (relative major/minor) + minor pentatonic")
    lines = [
        "{comment: Piano solo adaptation hints}",
        f"{{comment: Key center: {key}; Use scale: {scale}}}",
        "{comment: Patch: Grand Piano or EP; optional slight delay.}",
        "{comment: Approach: right-hand plays main guitar lick; left-hand holds chord tones (1-5 or 1-5-8).}",
        "{comment: Phrase on chord tones; use neighbor notes and slides between scale tones.}"
    ]
    return "\n".join(lines)

def to_chordpro(raw_text, title, artist, key=None, tempo=None, meter=None, keep_tabs=False, piano_hints=False, source_url=None):
    lines = raw_text.splitlines()
    out = []
    out.append(f"{{title: {title}}}")
    if artist:
        out.append(f"{{artist: {artist}}}")
    if source_url:
        out.append(f"{{comment: Source: {source_url}}}")
    if key:
        out.append(f"{{key: {key}}}")
    if tempo:
        out.append(f"{{tempo: {tempo}}}")
    if meter:
        out.append(f"{{time: {meter}}}")
    out.append("")

    for line in lines:
        line = line.replace("\t", "    ")
        if not keep_tabs and TAB_LINE.match(line):
            # Skip ASCII TAB lines if we don't keep them
            continue
        tokens = CHORD_TOKEN.findall(line)
        text_only = CHORD_TOKEN.sub("", line).strip()
        if tokens and not text_only:
            def wrap(m): return f"[{m.group(0)}]"
            out.append(CHORD_TOKEN.sub(wrap, line))
        else:
            out.append(line)

    out.append("")
    if piano_hints and key:
        out.append(piano_hint_block(key))
        out.append("")
    out.append(f"{{comment: Generated locally on {datetime.now().strftime('%Y-%m-%d %H:%M')}}}")
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Pesmarica.rs song URL")
    ap.add_argument("--title", required=True, help="Song title")
    ap.add_argument("--artist", required=True, help="Artist")
    ap.add_argument("--key", default=None)
    ap.add_argument("--tempo", default=None)
    ap.add_argument("--meter", default=None)
    ap.add_argument("--outdir", default="lyrics-output", help="Output directory for .pro/.docx")
    ap.add_argument("--docx", action="store_true", help="Also export a basic .docx (requires python-docx)")
    ap.add_argument("--keep-tabs", action="store_true", help="Keep ASCII TAB lines")
    ap.add_argument("--strip-tabs", action="store_true", help="Force strip guitar TAB lines")
    ap.add_argument("--piano-hints", action="store_true", help="Append piano solo adaptation hints block")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    resp = requests.get(args.url, timeout=25)
    resp.raise_for_status()

    raw = extract_text_blocks(resp.text)
    keep_tabs = True if args.keep_tabs else False
    if args.strip_tabs:
        keep_tabs = False

    chordpro = to_chordpro(raw, args.title, args.artist, args.key, args.tempo, args.meter,
                           keep_tabs=keep_tabs, piano_hints=args.piano_hints, source_url=args.url)

    safe_title = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{args.artist}-{args.title}")
    pro_path = os.path.join(args.outdir, f"{safe_title}.pro")
    with open(pro_path, "w", encoding="utf-8") as f:
        f.write(chordpro)
    print(f"Wrote {pro_path}")

    if args.docx:
        try:
            from docx import Document
        except Exception:
            print("Install python-docx for DOCX export: pip install python-docx")
            return
        doc = Document()
        doc.add_heading(f"{args.title} — {args.artist}", 1)
        doc.add_paragraph(chordpro)
        docx_path = os.path.join(args.outdir, f"{safe_title}.docx")
        doc.save(docx_path)
        print(f"Wrote {docx_path}")

if __name__ == "__main__":
    main()