#!/usr/bin/env python3
# Purpose: For personal/educational use. Converts a Pesmarica.rs song page to ChordPro (.pro).
# NOTE: Do not commit generated .pro files to a public repo without rights.
# Usage:
#   python tools/pesmarica_to_chordpro.py --url "https://www.pesmarica.rs/akordi/2866/Divlje-Jagode--Marija" --title "Marija" --artist "Divlje Jagode"
# Optional:
#   --docx will also render a simple .docx (requires python-docx)
#
# Limitations:
# - Site structure may change; adjust CSS selectors accordingly.
# - This script is for local use only; respect website TOS and copyright.

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
    """
    Heuristic extraction: Pesmarica often renders lyrics+chords in <pre> or a content div.
    We try common containers. Adjust if site layout changes.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Try <pre> first
    pre = soup.find("pre")
    if pre and pre.get_text(strip=False):
        return pre.get_text(strip=False)

    # Try main content divs
    for sel in ["div.song", "div#song", "div.content", "article"]:
        node = soup.select_one(sel)
        if node and node.get_text(strip=False):
            return node.get_text(strip=False)

    # Fallback: body text
    body = soup.find("body")
    return body.get_text("\n", strip=False) if body else ""

CHORD_TOKEN = re.compile(r"\b([A-G](?:#|b)?m?(?:maj7|m7|7|sus2|sus4|dim|aug)?)(/[A-G](?:#|b)?)?\b")

def to_chordpro(raw_text, title, artist, key=None, tempo=None, meter=None):
    """
    Convert mixed text to a simple ChordPro:
    - Lines with many chord tokens are preserved; lyrics lines kept as-is.
    - Wrap chords inline like [Am] in front of the following lyric chunk (very heuristic).
    """
    lines = raw_text.splitlines()
    out = []
    out.append(f"{title: {title}}")
    if artist:
        out.append(f"{artist: {artist}}")
    if key:
        out.append(f"{key: {key}}")
    if tempo:
        out.append(f"{tempo: {tempo}}")
    if meter:
        out.append(f"{time: {meter}}")
    out.append("")

    for line in lines:
        # Normalize tabs
        line = line.replace("\t", "    ")
        # If it's a pure chord line (mostly chords and spaces), keep as-is
        tokens = CHORD_TOKEN.findall(line)
        text_only = CHORD_TOKEN.sub("", line).strip()
        if tokens and not text_only:
            # Convert chord tokens to [Chord]
            def wrap_chord(m):
                return f"[{m.group(0)}]"
            out.append(CHORD_TOKEN.sub(wrap_chord, line))
        else:
            # Leave lyrics or mixed lines as-is; optional: try to inline chords
            out.append(line)
    out.append("")
    out.append(f"{comment: Generated locally on {datetime.now().strftime('%Y-%m-%d %H:%M')}}")
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Pesmarica.rs song URL")
    ap.add_argument("--title", required=True, help="Song title")
    ap.add_argument("--artist", required=True, help="Artist")
    ap.add_argument("--key", default=None)
    ap.add_argument("--tempo", default=None)
    ap.add_argument("--meter", default=None)
    ap.add_argument("--outdir", default="lyrics-output", help="Output directory for .pro")
    ap.add_argument("--docx", action="store_true", help="Also export a basic .docx (requires python-docx)")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    resp = requests.get(args.url, timeout=20)
    resp.raise_for_status()

    raw = extract_text_blocks(resp.text)
    chordpro = to_chordpro(raw, args.title, args.artist, args.key, args.tempo, args.meter)

    safe_title = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{args.artist}-{args.title}")
    pro_path = os.path.join(args.outdir, f"{safe_title}.pro")
    with open(pro_path, "w", encoding="utf-8") as f:
        f.write(chordpro)
    print(f"Wrote {pro_path}")

    if args.docx:
        try:
            from docx import Document
            from docx.shared import Pt
        except Exception:
            print("Install python-docx for DOCX export: pip install python-docx")
            return
        doc = Document()
        doc.add_heading(f"{args.title} — {args.artist}", 1)
        p = doc.add_paragraph(chordpro)
        # Using default style; monospace style varies by template
        docx_path = os.path.join(args.outdir, f"{safe_title}.docx")
        doc.save(docx_path)
        print(f"Wrote {docx_path}")

if __name__ == "__main__":
    main()