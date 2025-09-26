# Media Companion Agent – Scope & Requirements

**Branch**: `feature/media-companion-agent`
**Author**: GitHub Copilot · TEC R&D Queen
**Status**: Draft (2025-09-26)

## Mission

Design an Azure-connected companion agent that can ingest musical and video artifacts, surface resonant insights, and maintain a conversational presence aligned with TEC canon.

## Target Use Cases

- **Music resonance explorer** – analyze stems or full tracks for mood, tempo, lyrical resonance, and lore alignment.
- **Video ritual interpreter** – summarize video evidence, extract key frames, tag symbolism, and detect emotional arcs.
- **Companion dialogue** – maintain ongoing conversations with researchers, referencing analyzed media and suggesting next experiments.

## Input Data Sources

| Medium | Expected Inputs | Notes |
| --- | --- | --- |
| Music | WAV/MP3 stems, metadata JSON, optional lyrics transcript | Lean on Azure Cognitive Services (Speech-to-Text) for lyric extraction; local spectral analysis via `librosa` if permitted |
| Video | MP4/WebM evidence captures, optional caption files | Use Azure Video Indexer or local `ffmpeg` + Whisper combo for transcripts and key frames |
| Context | Existing TEC runs (metadata, AI tags), Pantheon lore snippets | Leverage `content_hub` search + Memory store |

## Desired Outputs

- Structured JSON reports with mood taxonomy, tempo, instrumentation highlights
- Lore-aware tagging (e.g., “Kaznak harmonic”, “Lumina signal leakage”)
- Suggested companion dialogue prompts referencing analyzed assets
- Optional playlist or viewing queue scripts (Markdown + timestamp links)

## Reusable Tooling

- `tools/azure_ai_client.py` for GPT-4o mini summarization + tagging
- `content_hub/search.py` for lore grounding
- Existing memory ingestion CLI in `agents/tools/memory_client.py`
- Agent logging + run scaffolding in `agents/cli.py`

## New Capabilities Required

1. **Audio Feature Extraction** – evaluate `librosa` or Azure Audio Content Safety endpoints; consider optional dependency guard.
2. **Video Transcript & Keyframe Capture** – integrate with Azure Video Indexer API or local Whisper/FFmpeg pipeline.
3. **Companion Persona Prompting** – extend `agents/prompt_agent.py` with a companion persona (musical empath + archivist).
4. **Run Packaging** – store outputs under `data/agents/media_companion/<run_id>/` with transcript, tags, and chat-ready summaries.

## Risks & Mitigations

- **Large file sizes** → enforce size caps, stream processing where possible.
- **Dependency weight (ffmpeg/librosa)** → wrap optional installs, document prerequisites in README.
- **API rate limits** → batch requests, cache transcripts in `data/memory`.
- **Lore drift** → ensure every generation call includes `content_hub` grounding snippets.

## Milestones

1. ✅ **Baseline snapshot** (commit + branch)
2. 🚧 **Audio-first prototype** – ingest single track, output JSON + conversational summary.
3. 🚧 **Video layer** – add transcript + keyframe tagging pipeline.
4. 🚧 **Companion chat loop** – integrate persona dialogue generator referencing processed media.
5. 🚧 **Docs & dashboard update** – surface new agent outputs in README + UI.

## Regression & Documentation Strategy

- Maintain quick regression suite: `pytest -q` must stay green; add targeted tests in `server/tests/` and new tool-level tests as media features mature.
- Keep `docs/COMMANDS_CHEATSHEET.md` synced when workflows or tasks change; highlight optional dependencies (`librosa`, `ffmpeg`).
- Update README sections for new agent capabilities and link dashboards once video/companion persona views land.
- Extend `ui/dashboard.html` to display media companion outputs after feature completion.
- Document environment prerequisites for heavy media tooling (JDK zip, ffmpeg) in `docs/TEC_IT_RUNBOOK.md` or dedicated setup guide before release.

Next up: design the YAML workflow skeleton and identify tool modules per milestone.
