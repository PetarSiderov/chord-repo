# Lyrics/Chords generation (local use)

Важно: Не комитирај лирики во јавниот репо освен ако имаш право. Ова е алат за локална (лична) употреба.

## Инсталација
pip install requests beautifulsoup4 python-docx

## Single пример (со piano hints и без TAB)
python tools/pesmarica_to_chordpro.py --url "https://www.pesmarica.rs/akordi/350/Crvena-Jabuka--Nekako-s-Prole%C4%87a" --title "Nekako s Proleća" --artist "Crvena Jabuka" --key "G" --tempo 74 --meter "4/4" --docx --piano-hints --strip-tabs

## Batch (со твоите линкови)
python tools/pesmarica_batch.py data/song-sources.csv

Излезот е во:
- lyrics-output/<Artist>-<Title>.pro (ChordPro)
- lyrics-output/<Artist>-<Title>.docx (ако е селектирано Docx)

## Напомени
- Ако Pesmarica има ASCII TAB за гитара, со `--strip-tabs` ќе ги прескокнеме. Додај `--piano-hints` за да добиеш блок со насоки како да се отсвири солото на пијано (скали, пристап, фразирање).
- За модели на URL /akordi/gitara/... користи точни „slug“-ови (внимавај на дијакритика, на пр. Proleћа vs. Proleca). Ако slug не се совпаќа, отвори ја страната рачно и копирај го полниот URL во CSV.
- Генерираните .pro/.docx се игнорираат со .gitignore и не се качуваат на GitHub.
