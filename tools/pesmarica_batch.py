#!/usr/bin/env python3
"""
pesmarica_batch.py - Batch process songs from CSV using pesmarica_to_chordpro.py

This tool is for PERSONAL USE ONLY. Please respect copyright and terms of service.
DO NOT commit generated lyrics to the repository - they are automatically ignored by .gitignore.

Usage:
    python pesmarica_batch.py <csv_file> [--output-dir <dir>]

CSV Format:
    Title,Artist,URL,Key,TempoBPM,Meter,Docx,PianoHints,KeepTabs
    
    - Title: Song title (required)
    - Artist: Artist name (required)
    - URL: Pesmarica.rs URL (required)
    - Key: Musical key (optional, e.g., G, Am)
    - TempoBPM: Tempo in BPM (optional)
    - Meter: Time signature (optional, e.g., 4/4)
    - Docx: 'yes' to generate .docx, anything else to skip (optional)
    - PianoHints: 'yes' to add piano hints (optional)
    - KeepTabs: 'yes' to keep tabs, 'no' or empty to strip (optional)
"""

import argparse
import csv
import subprocess
import sys
from pathlib import Path


def process_csv(csv_path, output_dir='lyrics-output'):
    """Process all songs in the CSV file."""
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        print(f"ERROR: CSV file not found: {csv_path}")
        sys.exit(1)
    
    print(f"Processing songs from: {csv_path}")
    print(f"Output directory: {output_dir}")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Validate required columns
        required_cols = {'Title', 'Artist', 'URL'}
        if not required_cols.issubset(reader.fieldnames):
            print(f"ERROR: CSV must have columns: {', '.join(required_cols)}")
            print(f"Found columns: {', '.join(reader.fieldnames)}")
            sys.exit(1)
        
        for row_num, row in enumerate(reader, start=2):
            title = row.get('Title', '').strip()
            artist = row.get('Artist', '').strip()
            url = row.get('URL', '').strip()
            
            if not title or not artist or not url:
                print(f"Row {row_num}: Skipping - missing required fields")
                error_count += 1
                continue
            
            print(f"\n[{row_num}] Processing: {artist} - {title}")
            
            # Build command
            script_path = Path(__file__).parent / 'pesmarica_to_chordpro.py'
            cmd = [
                sys.executable,
                str(script_path),
                '--url', url,
                '--title', title,
                '--artist', artist,
                '--output-dir', output_dir
            ]
            
            # Add optional parameters
            key = row.get('Key', '').strip()
            if key:
                cmd.extend(['--key', key])
            
            tempo = row.get('TempoBPM', '').strip()
            if tempo:
                cmd.extend(['--tempo', tempo])
            
            meter = row.get('Meter', '').strip()
            if meter:
                cmd.extend(['--meter', meter])
            
            # Boolean flags
            if row.get('Docx', '').strip().lower() == 'yes':
                cmd.append('--docx')
            
            if row.get('PianoHints', '').strip().lower() == 'yes':
                cmd.append('--piano-hints')
            
            if row.get('KeepTabs', '').strip().lower() == 'yes':
                cmd.append('--keep-tabs')
            else:
                cmd.append('--strip-tabs')
            
            # Execute
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(result.stdout)
                success_count += 1
            except subprocess.CalledProcessError as e:
                print(f"ERROR processing song:")
                print(e.stderr)
                error_count += 1
            except Exception as e:
                print(f"ERROR: {e}")
                error_count += 1
    
    print("\n" + "=" * 60)
    print(f"Batch processing complete!")
    print(f"Success: {success_count} | Errors: {error_count}")
    print("=" * 60)
    
    if error_count > 0:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Batch process songs from CSV.\n'
                    'FOR PERSONAL USE ONLY - DO NOT COMMIT GENERATED FILES.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('csv_file', help='Path to CSV file with song data')
    parser.add_argument('--output-dir', default='lyrics-output', 
                       help='Output directory (default: lyrics-output)')
    
    args = parser.parse_args()
    
    process_csv(args.csv_file, args.output_dir)


if __name__ == '__main__':
    main()
