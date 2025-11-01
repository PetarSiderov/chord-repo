# Lyrics to ChordPro Generator Tools

**⚠️ FOR PERSONAL USE ONLY**  
These tools fetch song lyrics and chords from Pesmarica.rs for personal use. Please respect copyright laws and the website's terms of service. **DO NOT commit generated .pro or .docx files to the repository** - they are automatically ignored by `.gitignore`.

## Overview

This toolset allows you to:
1. Fetch individual songs from Pesmarica.rs and convert them to ChordPro format (.pro)
2. Optionally generate Word documents (.docx) from the ChordPro files
3. Batch process multiple songs from a CSV file
4. Run the batch process automatically via GitHub Actions (outputs as artifacts, not committed)

## Prerequisites

### Local Installation

You need Python 3.7+ and the following packages:

```bash
pip install requests beautifulsoup4 python-docx
```

### GitHub Actions

No local installation needed! The GitHub Actions workflow automatically installs dependencies and runs the batch processor. Generated files are uploaded as workflow artifacts.

## Tools

### 1. `pesmarica_to_chordpro.py` - Single Song Converter

Fetches a song from Pesmarica.rs and converts it to ChordPro format.

**Usage:**

```bash
python tools/pesmarica_to_chordpro.py \
  --url "https://www.pesmarica.rs/akordi/350/Crvena-Jabuka--Nekako-s-Prole%C4%87a" \
  --title "Nekako s Proleća" \
  --artist "Crvena Jabuka" \
  --key G \
  --tempo 74 \
  --meter "4/4" \
  --docx \
  --piano-hints
```

**Options:**

- `--url` (required): URL of the song on Pesmarica.rs
- `--title` (required): Song title
- `--artist` (required): Artist name
- `--key`: Musical key (e.g., G, Am, F#m)
- `--tempo`: Tempo in BPM
- `--meter`: Time signature (e.g., 4/4, 3/4)
- `--docx`: Generate a .docx file in addition to .pro
- `--keep-tabs`: Keep ASCII guitar tabs in the output
- `--strip-tabs`: Strip ASCII guitar tabs (default behavior)
- `--piano-hints`: Add piano solo adaptation hints based on the key
- `--output-dir`: Output directory (default: `lyrics-output`)

**Output:**

Files are saved to `lyrics-output/` (or custom directory) with safe filenames:
- `Artist_Title.pro` - ChordPro format
- `Artist_Title.docx` - Word document (if `--docx` flag used)

**Example Output Structure:**

```
lyrics-output/
├── Crvena_Jabuka_Nekako_s_Proleca.pro
├── Crvena_Jabuka_Nekako_s_Proleca.docx
├── Bajaga_Tisina.pro
└── SARS_Budav_Lebac.pro
```

### 2. `pesmarica_batch.py` - Batch Processor

Processes multiple songs from a CSV file by calling `pesmarica_to_chordpro.py` for each entry.

**Usage:**

```bash
python tools/pesmarica_batch.py data/song-sources.csv
```

**CSV Format:**

The CSV must have a header row with these columns:

```
Title,Artist,URL,Key,TempoBPM,Meter,Docx,PianoHints,KeepTabs
```

- **Title** (required): Song title
- **Artist** (required): Artist name
- **URL** (required): Full Pesmarica.rs URL (including encoded characters like `%C4%87`)
- **Key** (optional): Musical key (e.g., G, Am, F#m)
- **TempoBPM** (optional): Tempo in beats per minute
- **Meter** (optional): Time signature (e.g., 4/4, 3/4, 7/8)
- **Docx** (optional): `yes` to generate .docx, anything else to skip
- **PianoHints** (optional): `yes` to add piano adaptation hints
- **KeepTabs** (optional): `yes` to keep guitar tabs, `no` or empty to strip them

**Example CSV:**

```csv
Title,Artist,URL,Key,TempoBPM,Meter,Docx,PianoHints,KeepTabs
Nekako s Proleća,Crvena Jabuka,https://www.pesmarica.rs/akordi/350/Crvena-Jabuka--Nekako-s-Prole%C4%87a,G,74,4/4,yes,yes,no
Tišina,Bajaga,https://www.pesmarica.rs/akordi/4126/Bajaga--Tisina,F#m,106,4/4,yes,yes,no
```

## Running Locally

### Single Song

```bash
# Basic usage
python tools/pesmarica_to_chordpro.py \
  --url "https://www.pesmarica.rs/akordi/350/..." \
  --title "Song Title" \
  --artist "Artist Name"

# With all options
python tools/pesmarica_to_chordpro.py \
  --url "https://www.pesmarica.rs/akordi/350/..." \
  --title "Song Title" \
  --artist "Artist Name" \
  --key Am \
  --tempo 120 \
  --meter "4/4" \
  --docx \
  --piano-hints
```

### Batch Processing

```bash
# Process all songs in the CSV
python tools/pesmarica_batch.py data/song-sources.csv

# Custom output directory
python tools/pesmarica_batch.py data/song-sources.csv --output-dir my-lyrics
```

## GitHub Actions Workflow

The repository includes a GitHub Actions workflow (`.github/workflows/lyrics-generate.yml`) that:

1. **Triggers on:**
   - Manual workflow dispatch (Actions → "Lyrics generator" → "Run workflow")
   - Pull requests (to validate the workflow works)

2. **Process:**
   - Sets up Python 3.11
   - Installs dependencies (`requests`, `beautifulsoup4`, `python-docx`)
   - Runs `python tools/pesmarica_batch.py data/song-sources.csv`
   - Uploads all files in `lyrics-output/` as a build artifact

3. **Artifact:**
   - Name: `lyrics-output`
   - Contains all generated .pro and .docx files
   - Available for download from the workflow run page
   - Retained for 30 days

### Using the Workflow

1. Go to **Actions** tab in the repository
2. Select **"Lyrics generator"** workflow
3. Click **"Run workflow"** button
4. Select branch (usually `main`)
5. Click **"Run workflow"** to start
6. Wait for completion (~1-2 minutes)
7. Download the `lyrics-output` artifact from the workflow run summary

## Important Notes

### Copyright and Terms of Service

- ⚠️ **These tools are for personal, educational use only**
- Respect Pesmarica.rs terms of service and copyright laws
- Do not redistribute or publish fetched content
- Do not commit generated lyrics files to this repository

### .gitignore Protection

The repository's `.gitignore` automatically excludes:
- `lyrics-output/` directory
- `*.pro` files

This ensures generated lyrics are never accidentally committed to version control.

### Filename Safety

The tools automatically convert song titles and artist names to safe filenames by:
- Removing special characters
- Replacing spaces with underscores
- Handling UTF-8/Unicode properly

Example: `"Nekako s Proleća"` → `"Nekako_s_Proleca.pro"`

### Tab Stripping

By default, ASCII guitar tabs (e.g., `e|--1--2--|`) are stripped from the output because they don't translate well to ChordPro format or piano arrangements. Use `--keep-tabs` if you want to preserve them.

### Piano Hints

When you use `--piano-hints` with a `--key` specified, the tool adds helpful comments for piano players about:
- Scale runs and patterns
- Common chord progressions
- Left/right hand voicing suggestions
- Solo section expansion techniques

## Troubleshooting

### Missing Dependencies

**Error:** `ImportError: No module named 'requests'`

**Fix:**
```bash
pip install requests beautifulsoup4 python-docx
```

### Can't Parse Song Content

**Error:** `Could not parse song content from the page`

**Possible causes:**
- URL is incorrect or page structure changed
- Network/firewall blocking access
- Pesmarica.rs updated their HTML structure

**Fix:** Verify the URL works in a browser, check for typos

### Permission Denied

**Error:** `Permission denied: tools/pesmarica_to_chordpro.py`

**Fix:**
```bash
chmod +x tools/pesmarica_to_chordpro.py
chmod +x tools/pesmarica_batch.py
```

Or run with `python` explicitly:
```bash
python tools/pesmarica_to_chordpro.py ...
```

## Adding More Songs

1. Edit `data/song-sources.csv`
2. Add new rows with song information
3. Commit only the CSV file (not the generated lyrics!)
4. Run the GitHub Actions workflow or process locally

## Example Workflow

1. Find a song on Pesmarica.rs (e.g., https://www.pesmarica.rs/akordi/350/...)
2. Add a row to `data/song-sources.csv`:
   ```csv
   My Song,My Artist,https://www.pesmarica.rs/akordi/...,C,100,4/4,yes,yes,no
   ```
3. Run batch locally:
   ```bash
   python tools/pesmarica_batch.py data/song-sources.csv
   ```
4. Check `lyrics-output/My_Artist_My_Song.pro` and `.docx`
5. Or trigger GitHub Actions to generate artifacts

## License & Disclaimer

These tools are provided as-is for personal use. The repository maintainers are not responsible for misuse or copyright violations. Always respect the original content creators and website terms of service.

---

**🎶 Happy practicing! / Srećno vežbanje!**
