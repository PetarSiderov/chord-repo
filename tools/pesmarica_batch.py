#!/usr/bin/env python3
"""
Batch processor for Pesmarica to ChordPro conversion.
Reads a CSV file with song information and converts each song.
"""

import argparse
import csv
import subprocess
import sys
import os


def parse_csv(csv_file):
    """Parse CSV file and return list of song dictionaries."""
    songs = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(row)
    
    return songs


def convert_song(song, output_dir='lyrics-output'):
    """Convert a single song using pesmarica_to_chordpro.py."""
    # Build command
    script_dir = os.path.dirname(os.path.abspath(__file__))
    converter_script = os.path.join(script_dir, 'pesmarica_to_chordpro.py')
    
    cmd = [
        sys.executable,  # Use current Python interpreter
        converter_script,
        '--url', song['URL'],
        '--title', song['Title'],
        '--artist', song['Artist'],
        '--output-dir', output_dir
    ]
    
    # Add optional parameters
    if song.get('Key'):
        cmd.extend(['--key', song['Key']])
    if song.get('Tempo'):
        cmd.extend(['--tempo', song['Tempo']])
    if song.get('Meter'):
        cmd.extend(['--meter', song['Meter']])
    
    # Add boolean flags
    if song.get('GenerateDocx', '').lower() in ('yes', 'true', '1'):
        cmd.append('--docx')
    
    if song.get('PianoHints', '').lower() in ('yes', 'true', '1'):
        cmd.append('--piano-hints')
    
    if song.get('KeepTabs', '').lower() in ('yes', 'true', '1'):
        cmd.append('--keep-tabs')
    
    # Run the converter
    print(f"\n{'='*60}")
    print(f"Processing: {song['Artist']} - {song['Title']}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error processing song: {e}", file=sys.stderr)
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Batch convert songs from pesmarica.rs to ChordPro format'
    )
    parser.add_argument('csv_file', help='CSV file with song information')
    parser.add_argument('--output-dir', default='lyrics-output',
                       help='Output directory (default: lyrics-output)')
    
    args = parser.parse_args()
    
    # Check if CSV file exists
    if not os.path.exists(args.csv_file):
        print(f"Error: CSV file not found: {args.csv_file}", file=sys.stderr)
        return 1
    
    # Parse CSV
    print(f"Reading songs from: {args.csv_file}")
    songs = parse_csv(args.csv_file)
    print(f"Found {len(songs)} songs to process\n")
    
    # Process each song
    success_count = 0
    fail_count = 0
    
    for song in songs:
        if convert_song(song, args.output_dir):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Batch processing complete!")
    print(f"{'='*60}")
    print(f"Successfully processed: {success_count}/{len(songs)} songs")
    if fail_count > 0:
        print(f"Failed: {fail_count} songs")
    
    return 0 if fail_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
