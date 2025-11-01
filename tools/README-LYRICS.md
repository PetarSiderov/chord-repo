# Lyrics Generation Tools

This directory contains Python tools for scraping song lyrics and chords from [Pesmarica.rs](https://www.pesmarica.rs/) and converting them to ChordPro format for use with the Korg EK-50 keyboard.

## 📋 Overview

The lyrics generation workflow allows you to:
- Fetch song lyrics with chords from Pesmarica.rs
- Convert them to ChordPro format (`.pro` files)
- Optionally generate formatted Word documents (`.docx`)
- Process multiple songs in batch from a CSV file
- Generate files as GitHub Actions artifacts (no lyrics committed to repo)

## 🛠️ Tools

### 1. `pesmarica_to_chordpro.py`

Single-song converter that fetches and converts one song at a time.

**Features:**
- Scrapes HTML from Pesmarica.rs using `requests` and `beautifulsoup4`
- Converts lyrics with chords to ChordPro format
- Strips guitar TAB lines by default (use `--keep-tabs` to preserve them)
- Adds metadata: title, artist, key, tempo, time signature
- Includes source URL as a comment line
- Optional DOCX generation with `python-docx`
- Optional piano solo hints based on song key

**Usage:**
```bash
python tools/pesmarica_to_chordpro.py \
  --url "https://www.pesmarica.rs/akordi/350/..." \
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
- `--key`: Song key (e.g., G, Am, F#m)
- `--tempo`: Tempo in BPM
- `--meter`: Time signature (e.g., 4/4, 3/4, 7/8)
- `--docx`: Generate DOCX file in addition to .pro file
- `--keep-tabs`: Keep guitar TAB lines (default: strips them)
- `--strip-tabs`: Explicitly strip TAB lines (default behavior)
- `--piano-hints`: Add piano solo hints based on the key
- `--output-dir`: Output directory (default: lyrics-output)

### 2. `pesmarica_batch.py`

Batch processor that reads a CSV file and converts multiple songs.

**Usage:**
```bash
python tools/pesmarica_batch.py data/song-sources.csv
```

**CSV Format:**
```csv
Title,Artist,URL,Key,Tempo,Meter,GenerateDocx,PianoHints,KeepTabs
Nekako s Proleća,Crvena Jabuka,https://www.pesmarica.rs/akordi/350/...,G,74,4/4,yes,yes,no
```

**CSV Columns:**
- `Title` (required): Song title
- `Artist` (required): Artist name
- `URL` (required): Pesmarica.rs URL
- `Key` (optional): Song key
- `Tempo` (optional): BPM
- `Meter` (optional): Time signature
- `GenerateDocx` (optional): yes/no - generate DOCX file
- `PianoHints` (optional): yes/no - add piano hints
- `KeepTabs` (optional): yes/no - keep guitar tabs

## 🎵 ChordPro Format

ChordPro is a simple text format for songs with chords. Example:

```
{title: Nekako s Proleća}
{artist: Crvena Jabuka}
{key: G}
{tempo: 74}
{time: 4/4}
{comment: Source: https://www.pesmarica.rs/...}

[G]Nekako s pro[C]leća
[D]Kada sve [G]cveta
```

### ChordPro on Korg EK-50

While the Korg EK-50 doesn't natively support ChordPro files, you can:
1. Open `.pro` files in any text editor
2. Use them as reference while playing
3. Print them or view on a tablet/phone
4. Convert to PDF using ChordPro software: https://www.chordpro.org/

## 📦 Dependencies

Install required Python packages:

```bash
pip install requests beautifulsoup4 python-docx
```

- `requests`: HTTP library for fetching web pages
- `beautifulsoup4`: HTML parsing library
- `python-docx`: DOCX file generation (optional, only needed for `--docx`)

## 🚀 GitHub Actions Workflow

The repository includes `.github/workflows/lyrics-generate.yml` that:
- Triggers manually via "Actions" tab (workflow_dispatch)
- Triggers on pull requests (pull_request)
- Installs Python dependencies
- Runs the batch processor
- Uploads generated files as artifacts (available for 30 days)

**Running the workflow:**
1. Go to the "Actions" tab in GitHub
2. Select "Generate Lyrics Artifacts"
3. Click "Run workflow"
4. Download the "lyrics-output" artifact when complete

## ⚖️ Legal and Copyright Notes

**IMPORTANT:** The lyrics and chord charts on Pesmarica.rs are copyrighted materials. These tools are provided for:

- **Educational purposes only**
- **Personal use and practice**
- **Reference during live performances where you have appropriate licenses**

### Guidelines:

✅ **Acceptable Use:**
- Generating ChordPro files for personal practice with the Korg EK-50
- Using as reference during licensed live performances
- Educational purposes in music lessons
- Creating your own arrangements based on chord progressions

❌ **NOT Acceptable:**
- Redistributing generated lyrics files publicly
- Commercial use without proper licensing
- Publishing lyrics on websites or apps
- Sharing copyrighted lyrics in repositories

### This Repository's Approach:

To respect copyright:
- **No lyrics are committed to the git repository**
- Lyrics are generated as **temporary GitHub Actions artifacts** (expire after 30 days)
- `.gitignore` excludes `lyrics-output/` and `*.pro` files
- Tools are provided for **personal workflow automation** only

### Song Rights:

Songs belong to their respective:
- **Composers** (music)
- **Lyricists** (words)
- **Publishers** (rights holders)
- **Performing artists**

If you perform these songs publicly, ensure you have:
- ASCAP/BMI/SESAC licenses (USA)
- SOKOJ licenses (Serbia/Ex-Yugoslavia)
- Appropriate licenses in your jurisdiction

### Fair Use:

In many jurisdictions, using chord charts and lyrics for:
- Personal practice
- Educational purposes
- Live performance reference (with proper venue licensing)

...is considered **fair use** or covered by **venue performance licenses**. However, laws vary by country.

**When in doubt, consult with a legal professional regarding copyright law in your jurisdiction.**

## 🎹 EK-50 Context

These tools are designed to complement the Balkan repertoire in this repository:
- Generate reference materials for the songs listed in `Korg-EK50-SongBook.csv`
- Practice with accurate chord progressions
- Have lyrics available during performances
- Learn new songs from the Pesmarica.rs collection

The Korg EK-50 features:
- Built-in Balkan/Oriental styles
- 7/8 and 9/8 time signature support
- STS (Single Touch Settings) for instant sound changes
- Chord sequencer for practice

## 🔧 Customization

### Adding Your Own Songs

Edit `data/song-sources.csv` to add more songs:

```csv
Title,Artist,URL,Key,Tempo,Meter,GenerateDocx,PianoHints,KeepTabs
Your Song,Your Artist,https://www.pesmarica.rs/akordi/...,Dm,120,4/4,yes,yes,no
```

### Piano Hints

When `--piano-hints` is enabled, the tool appends scale and arpeggio suggestions:

- Major keys: Major scale and common chord arpeggios
- Minor keys: Natural minor scale and common chord arpeggios
- Helpful for improvisation and solo sections on the EK-50

### Filename Normalization

Generated files use safe, normalized filenames:
- `Crvena_Jabuka_Nekako_s_Proleca.pro`
- `Bajaga_Tisina.docx`

Special characters and spaces are converted to underscores.

## 📝 Output Files

All generated files go to `lyrics-output/` (gitignored):
- `*.pro` - ChordPro format text files
- `*.docx` - Formatted Word documents (if `--docx` is used)

## 🐛 Troubleshooting

**"Could not find lyrics content on the page"**
- The Pesmarica.rs page structure may have changed
- Try visiting the URL manually to verify it still works
- The scraper looks for `<div class="akordi">` or `<pre class="akordi">`

**"python-docx not installed"**
- DOCX generation requires `python-docx`
- Install with: `pip install python-docx`
- Or skip `--docx` flag to only generate `.pro` files

**TAB lines not stripped**
- Use `--strip-tabs` (default) to remove guitar tablature
- Use `--keep-tabs` if you want to preserve TAB notation

## 📚 Resources

- **ChordPro Format**: https://www.chordpro.org/
- **Pesmarica.rs**: https://www.pesmarica.rs/
- **Korg EK-50**: https://www.korg.com/us/products/keyboards/ek_50/
- **SOKOJ** (Serbian copyright): https://www.sokoj.rs/

## 🤝 Contributing

To add new features:
1. Fork the repository
2. Create a feature branch
3. Test your changes with the GitHub Actions workflow
4. Submit a pull request

Remember: Never commit lyrics files to the repository!

---

**Disclaimer:** These tools are provided as-is for personal educational use. Users are responsible for ensuring their use complies with applicable copyright laws and licensing requirements in their jurisdiction.
