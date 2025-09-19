# TEC_Q5EP API Spec (v0.2)

## POST /submit (multipart/form-data)

Fields:

- photo: file (optional)
- note: string (optional)
- timestamp: ISO8601 (optional; server fills if missing)
- user_id: string (optional)
- consent: boolean ("true"/"false")
- tags: string (comma-separated)
- gps: JSON string {lat, lon, accuracy?}
- device: JSON string {user_agent?, make?, model?, os?}
- context: JSON string {...}

Writes run into `data/runs/<id>/`:

- photo.jpg (if provided)
- note.txt
- metadata.json (SubmissionMeta)

## GET /runs -> RunSummary[]

Minimal overview of existing runs (id, timestamp, tags, has_photo, note_chars).

## GET /runs/{id}

Returns full `metadata.json` for the run.

## GET /pack/{id}

Returns a zip bundle of the run (also written to `data/evidence_packs/`).

## Evidence Bundle Structure

- metadata.json
- note.txt
- photo.jpg (optional)

## Data Model

- See `server/models.py` for SubmissionMeta, GPS, Device, RunSummary.
