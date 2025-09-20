# Local Memory API

A tiny, local-first memory store backed by JSON files. Designed for fast iteration and zero external dependencies.

## Storage layout

- Base dir: `data/memory/`
- Files are sharded by the first two characters of the id: `data/memory/<shard>/<id>.json`
- Each file contains a single `MemoryItem` JSON document.

Example:

- `data/memory/17/1758090841.json`

## Models

- MemoryItem: `{ id, timestamp, user_id?, tags[], content, metadata{} }`
- MemoryUpsert: `{ user_id?, tags[], content, metadata{} }`
- MemoryQuery: `{ q, tags[], limit }`
- MemorySummary: `{ id, timestamp, tags[], content_chars }`

## Endpoints

- POST `/memory` → MemoryItem
  - Body: MemoryUpsert
  - Creates a new item with a simple epoch-second id and current UTC timestamp
- GET `/memory` → MemorySummary[]
  - Lists all items as summaries (id, timestamp, tags, content length)
- GET `/memory/{id}` → MemoryItem
  - Fetch full item by id
- POST `/memory/search` → MemoryItem[]
  - Body: MemoryQuery. Simple substring match on `content`, optional tag intersection, default limit 10
- DELETE `/memory/{id}` → `OK`
  - Removes the file if it exists

## Notes

- IDs are generated from epoch seconds. If you upsert multiple items in the same second you could collide. If this becomes an issue, switch to `time.time_ns()` or append a short random suffix.
- Search is naive and deterministic: no external vector DB, no network calls.
- This API is meant to be MCP-friendly: a simple local surface for agents to read/write/search.

## Future ideas

- Add `q` search across tags/metadata
- Implement optional TF‑IDF index over `content` for better ranking
- Bulk import/export via JSONL
