import json, hashlib
from pathlib import Path

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def verify_run(run_dir: Path) -> bool:
    meta = json.loads((run_dir / 'metadata.json').read_text(encoding='utf-8'))
    for fname, expected in meta['sha256_map'].items():
        got = sha256_file(run_dir / fname)
        if got != expected:
            return False
    return True

if __name__ == '__main__':
    rd = Path('data/runs')
    for d in rd.iterdir():
        if d.is_dir():
            print(d.name, 'OK' if verify_run(d) else 'MISMATCH')
