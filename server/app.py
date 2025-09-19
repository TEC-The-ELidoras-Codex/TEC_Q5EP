from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, FileResponse
from pathlib import Path
import hashlib, json, time, io, zipfile
from typing import List
from .models import SubmissionMeta, RunSummary, GPS, Device

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / 'data' / 'runs'
RUNS.mkdir(parents=True, exist_ok=True)

app = FastAPI(title='TEC_Q5EP Evidence API', version='0.2.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

@app.post('/submit', response_class=PlainTextResponse)
async def submit(photo: UploadFile | None = File(default=None),
                 note: str = Form(default=''),
                 timestamp: str = Form(default=''),
                 user_id: str = Form(default=''),
                 consent: bool = Form(default=False),
                 tags: str = Form(default=''),  # comma-separated
                 gps: str = Form(default=''),  # JSON string {lat,lon,accuracy}
                 device: str = Form(default=''),  # JSON string
                 context: str = Form(default='')):  # JSON string
    run_id = f"{int(time.time())}"
    run_dir = RUNS / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    sha_map = {}
    if photo:
        b = await photo.read()
        (run_dir / 'photo.jpg').write_bytes(b)
        sha_map['photo.jpg'] = sha256_bytes(b)

    (run_dir / 'note.txt').write_text(note, encoding='utf-8')
    sha_map['note.txt'] = sha256_bytes(note.encode('utf-8'))

    def loads_or_none_obj(s: str):
        try:
            v = json.loads(s) if s else None
            return v if isinstance(v, dict) else None
        except Exception:
            return None

    tags_list = [t.strip() for t in tags.split(',') if t.strip()]
    gps_obj = loads_or_none_obj(gps)
    device_obj = loads_or_none_obj(device)
    ctx_obj = loads_or_none_obj(context) or {}

    meta_model = SubmissionMeta(
        id=run_id,
        timestamp=timestamp or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        user_id=user_id or None,
        consent=bool(consent),
        tags=tags_list,
        gps=GPS(**gps_obj) if gps_obj else None,
        device=Device(**device_obj) if device_obj else None,
        context=ctx_obj,
        sha256_map=sha_map,
    )

    (run_dir / 'metadata.json').write_text(meta_model.model_dump_json(indent=2), encoding='utf-8')
    return f"OK {run_id}"


@app.get('/runs', response_model=List[RunSummary])
def list_runs():
    items: List[RunSummary] = []
    if not RUNS.exists():
        return items
    for d in sorted(RUNS.iterdir()):
        if d.is_dir() and (d / 'metadata.json').exists():
            meta = SubmissionMeta.model_validate_json((d / 'metadata.json').read_text(encoding='utf-8'))
            has_photo = (d / 'photo.jpg').exists()
            note_chars = len((d / 'note.txt').read_text(encoding='utf-8')) if (d / 'note.txt').exists() else 0
            items.append(RunSummary(id=meta.id, timestamp=meta.timestamp, tags=meta.tags, has_photo=has_photo, note_chars=note_chars))
    return items


@app.get('/runs/{run_id}')
def get_run(run_id: str):
    run_dir = RUNS / run_id
    if not (run_dir / 'metadata.json').exists():
        raise HTTPException(status_code=404, detail='Run not found')
    return json.loads((run_dir / 'metadata.json').read_text(encoding='utf-8'))


@app.get('/pack/{run_id}')
def pack_run(run_id: str):
    run_dir = RUNS / run_id
    if not (run_dir / 'metadata.json').exists():
        raise HTTPException(status_code=404, detail='Run not found')

    mem = io.BytesIO()
    with zipfile.ZipFile(mem, 'w', zipfile.ZIP_DEFLATED) as zf:
        for p in run_dir.iterdir():
            if p.is_file():
                zf.write(p, arcname=p.name)
    mem.seek(0)

    out_dir = ROOT / 'data' / 'evidence_packs'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f'{run_id}_bundle.zip'
    out_path.write_bytes(mem.getvalue())
    return FileResponse(path=out_path, media_type='application/zip', filename=out_path.name)
