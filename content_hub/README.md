# Content Hub (Local RAG) — TEC

A simple, no‑GPU local RAG to ground prompts and docs:

- Ingest .md/.txt files into a TF‑IDF index
- Search by cosine similarity
- Export top snippets for agents/prompt generation

Why: keep the repo clean with a single, curated knowledge stream; upgradeable later to Azure AI Search.

## Layout

- hub.py — library: load, chunk, index, search
- ingest.py — CLI to build `content_hub/index.pkl`
- search.py — CLI to query the index

## Usage

- Build index:
  - pwsh: `python content_hub/ingest.py --roots docs data --patterns "+*.md +*.txt -data/evidence_packs/** -data/incoming/**"`
- Query:
  - pwsh: `python content_hub/search.py --query "Kaznak Machine Goddess" --topk 5`

## Upgrade path

- Swap TF‑IDF for embeddings (sentence‑transformers) when ready
- Or provision Azure AI Search; mirror the same folder mapping

## Notes

- PDF support intentionally omitted to keep deps light; export key PDFs to .md/.txt as needed.
