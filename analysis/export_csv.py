import json, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / 'data' / 'runs'
OUT = ROOT / 'analysis' / 'runs.csv'

fields = [
    'id', 'timestamp', 'user_id', 'consent', 'tags', 'lat', 'lon', 'accuracy', 'has_photo', 'note_chars'
]

rows = []
for d in RUNS.iterdir():
    if d.is_dir() and (d / 'metadata.json').exists():
        meta = json.loads((d / 'metadata.json').read_text(encoding='utf-8'))
        has_photo = (d / 'photo.jpg').exists()
        note_chars = len((d / 'note.txt').read_text(encoding='utf-8')) if (d / 'note.txt').exists() else 0
        gps = meta.get('gps') or {}
        rows.append({
            'id': meta.get('id'),
            'timestamp': meta.get('timestamp'),
            'user_id': meta.get('user_id'),
            'consent': meta.get('consent'),
            'tags': ','.join(meta.get('tags') or []),
            'lat': gps.get('lat'),
            'lon': gps.get('lon'),
            'accuracy': gps.get('accuracy'),
            'has_photo': has_photo,
            'note_chars': note_chars,
        })

with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUT}")
