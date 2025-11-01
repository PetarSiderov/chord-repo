# Lyrics/Chords generation (local use)

Важно: Не комитирај лирики во јавниот репо освен ако имаш право.

## Локална конверзија (Pesmarica.rs → ChordPro/.docx)
1) Инсталирај зависимости:
```
pip install requests beautifulsoup4 python-docx
```

2) Пример:
```
python tools/pesmarica_to_chordpro.py --url "https://www.pesmarica.rs/akordi/2866/Divlje-Jagode--Marija" --title "Marija" --artist "Divlje Jagode" --key "Am" --tempo 116 --meter "4/4" --docx
```

3) Излез:
- lyrics-output/Divlje_Jagode-Marija.pro
- lyrics-output/Divlje_Jagode-Marija.docx (ако додадеш --docx)

Овие фајлови се игнорираат со .gitignore за да не се објавуваат.
