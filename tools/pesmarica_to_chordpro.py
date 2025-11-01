#!/usr/bin/env python3
"""
pesmarica_to_chordpro.py - Fetch song from Pesmarica.rs and convert to ChordPro format

This tool is for PERSONAL USE ONLY. Please respect copyright and terms of service.
DO NOT commit generated lyrics to the repository - they are automatically ignored by .gitignore.

Usage:
    python pesmarica_to_chordpro.py --url <URL> --title <TITLE> --artist <ARTIST> [OPTIONS]

Options:
    --url           URL of the song on Pesmarica.rs (required)
    --title         Song title (required)
    --artist        Artist name (required)
    --key           Musical key (optional, e.g., G, Am, F#m)
    --tempo         Tempo in BPM (optional)
    --meter         Time signature (optional, e.g., 4/4, 3/4)
    --docx          Generate .docx file in addition to .pro (flag)
    --keep-tabs     Keep ASCII guitar tabs (default: strip them)
    --strip-tabs    Strip ASCII guitar tabs (default behavior)
    --piano-hints   Add piano solo adaptation hints based on key (flag)
    --output-dir    Output directory (default: lyrics-output)
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Install with: pip install requests beautifulsoup4")
    sys.exit(1)


def normalize_filename(text):
    """Convert text to safe filename by removing/replacing special characters."""
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    # Remove non-ASCII characters or replace with underscore
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Replace spaces and special chars with underscore
    text = re.sub(r'[^\w\s-]', '_', text)
    text = re.sub(r'[-\s]+', '_', text)
    return text.strip('_')


def is_tab_line(line):
    """Detect if a line is likely an ASCII guitar tab."""
    # Tab lines typically contain patterns like e|---, B|---, |--1--2--|, etc.
    tab_patterns = [
        r'^\s*[eEbBgGdDaA]\|',  # String indicators like e|, B|, etc.
        r'^\s*\|[\d\-xXhHpPbBrR/\\~\s]+\|',  # Tab notation with frets
        r'^\s*[\-]{4,}',  # Long sequences of dashes
    ]
    for pattern in tab_patterns:
        if re.search(pattern, line):
            return True
    return False


def strip_tabs(text):
    """Remove ASCII guitar tab lines from text."""
    lines = text.split('\n')
    filtered_lines = []
    
    for line in lines:
        # Skip obvious tab lines
        if is_tab_line(line):
            continue
        # Skip lines that are mostly dashes and numbers (likely tabs)
        non_space = line.strip()
        if non_space and len(non_space) > 4:
            dash_count = non_space.count('-')
            if dash_count > len(non_space) * 0.5:
                continue
        filtered_lines.append(line)
    
    return '\n'.join(filtered_lines)


def generate_piano_hints(key):
    """Generate piano solo adaptation hints based on the song key."""
    if not key:
        return ""
    
    hints = f"""
# Piano Solo Adaptation Hints (Key: {key})
# - Practice scale runs in {key} for instrumental breaks
# - Common progression patterns: I-IV-V, I-vi-IV-V
# - Use arpeggios for smoother transitions
# - Right hand: melody + chord embellishments
# - Left hand: bass notes + chord roots (octave spacing)
# - For solo sections, expand chords to full voicing across both hands
"""
    return hints.strip()


def fetch_pesmarica_song(url):
    """Fetch song content from Pesmarica.rs."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except requests.RequestException as e:
        print(f"ERROR: Failed to fetch URL: {e}")
        sys.exit(1)


def parse_song_content(html_content):
    """Parse song lyrics and chords from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Try to find the song content in common container classes/ids
    # This is a best-effort parser and may need adjustment based on site structure
    content_div = (
        soup.find('div', {'class': 'song-content'}) or
        soup.find('div', {'class': 'akordi'}) or
        soup.find('div', {'id': 'akordi'}) or
        soup.find('pre') or
        soup.find('div', {'class': 'entry-content'})
    )
    
    if not content_div:
        # Fallback: try to find any pre or div with substantial text
        for tag in soup.find_all(['pre', 'div']):
            text = tag.get_text()
            if len(text) > 100:  # Assume song content is substantial
                content_div = tag
                break
    
    if not content_div:
        return "# ERROR: Could not parse song content from the page\n# Please check the URL"
    
    # Extract text, preserving some structure
    text = content_div.get_text(separator='\n')
    
    # Clean up excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def convert_to_chordpro(text, title, artist, key=None, tempo=None, meter=None, source_url=None, piano_hints=False, keep_tabs=False):
    """Convert parsed text to ChordPro format."""
    chordpro = []
    
    # Add directives
    chordpro.append(f"{{title: {title}}}")
    chordpro.append(f"{{artist: {artist}}}")
    
    if key:
        chordpro.append(f"{{key: {key}}}")
    if tempo:
        chordpro.append(f"{{tempo: {tempo}}}")
    if meter:
        chordpro.append(f"{{time: {meter}}}")
    
    if source_url:
        chordpro.append(f"# Source: {source_url}")
    
    chordpro.append("# ⚠️ FOR PERSONAL USE ONLY - DO NOT COMMIT TO REPOSITORY")
    chordpro.append("")
    
    # Process lyrics
    if not keep_tabs:
        text = strip_tabs(text)
    
    # Add the song content
    chordpro.append(text)
    
    # Add piano hints if requested
    if piano_hints and key:
        chordpro.append("")
        chordpro.append(generate_piano_hints(key))
    
    return '\n'.join(chordpro)


def save_as_docx(content, output_path):
    """Save content as a .docx file using python-docx."""
    try:
        from docx import Document
        from docx.shared import Pt
    except ImportError:
        print("WARNING: python-docx not installed. Skipping .docx generation.")
        print("Install with: pip install python-docx")
        return False
    
    doc = Document()
    
    # Add content line by line
    for line in content.split('\n'):
        if line.startswith('{') and line.endswith('}'):
            # ChordPro directive - make it bold
            p = doc.add_paragraph()
            run = p.add_run(line)
            run.bold = True
            run.font.size = Pt(11)
        elif line.startswith('#'):
            # Comment - make it italic
            p = doc.add_paragraph()
            run = p.add_run(line)
            run.italic = True
            run.font.size = Pt(10)
        else:
            # Regular text
            doc.add_paragraph(line)
    
    doc.save(str(output_path))
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Fetch song from Pesmarica.rs and convert to ChordPro format.\n'
                    'FOR PERSONAL USE ONLY - DO NOT COMMIT GENERATED FILES.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--url', required=True, help='URL of the song on Pesmarica.rs')
    parser.add_argument('--title', required=True, help='Song title')
    parser.add_argument('--artist', required=True, help='Artist name')
    parser.add_argument('--key', help='Musical key (e.g., G, Am, F#m)')
    parser.add_argument('--tempo', type=int, help='Tempo in BPM')
    parser.add_argument('--meter', help='Time signature (e.g., 4/4, 3/4)')
    parser.add_argument('--docx', action='store_true', help='Generate .docx file')
    
    # Mutually exclusive group for tab handling
    tab_group = parser.add_mutually_exclusive_group()
    tab_group.add_argument('--keep-tabs', action='store_true', help='Keep ASCII guitar tabs')
    tab_group.add_argument('--strip-tabs', action='store_true', default=True, 
                          help='Strip ASCII guitar tabs (default)')
    
    parser.add_argument('--piano-hints', action='store_true', help='Add piano solo adaptation hints')
    parser.add_argument('--output-dir', default='lyrics-output', help='Output directory')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Determine if we should keep tabs (default is to strip them)
    keep_tabs = args.keep_tabs
    
    print(f"Fetching: {args.title} - {args.artist}")
    print(f"URL: {args.url}")
    
    # Fetch and parse
    html_content = fetch_pesmarica_song(args.url)
    song_text = parse_song_content(html_content)
    
    # Convert to ChordPro
    chordpro_content = convert_to_chordpro(
        song_text,
        args.title,
        args.artist,
        key=args.key,
        tempo=args.tempo,
        meter=args.meter,
        source_url=args.url,
        piano_hints=args.piano_hints,
        keep_tabs=keep_tabs
    )
    
    # Generate safe filename
    safe_artist = normalize_filename(args.artist)
    safe_title = normalize_filename(args.title)
    base_filename = f"{safe_artist}_{safe_title}"
    
    # Save .pro file
    pro_path = output_dir / f"{base_filename}.pro"
    with open(pro_path, 'w', encoding='utf-8') as f:
        f.write(chordpro_content)
    print(f"✓ Saved: {pro_path}")
    
    # Save .docx if requested
    if args.docx:
        docx_path = output_dir / f"{base_filename}.docx"
        if save_as_docx(chordpro_content, docx_path):
            print(f"✓ Saved: {docx_path}")
    
    print("Done!")


if __name__ == '__main__':
    main()
