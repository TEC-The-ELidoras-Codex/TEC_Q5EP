# TEC Memory Scribe (Edge/Chrome Extension)

A minimal MV3 extension that lets you:

- Capture selected text as a Memory via your local TEC API
- Add tags and an optional note
- Use quick Prompt Helper pills to prefill common prompt skeletons
- Configure base URL and default tags in Options

## Install (Load Unpacked)

- Edge: edge://extensions → Enable Developer mode → Load unpacked → select `ui/extension`
- Chrome: chrome://extensions → Enable Developer mode → Load unpacked → select `ui/extension`

Grant permissions when prompted. Open Options to set your API base URL if not default.

## Use

- Select text on any page → right-click → "Save selection to TEC Memory"
- Or click the toolbar icon to open the popup, edit tags/content, and Save
- Prompt Helper pills will prepend a skeleton to the textarea for faster drafting

Memory items are stored by your FastAPI server under `data/memory/`.

## Troubleshooting

- Ensure the API is running (VS Code task "server:run" or "dev:all")
- Check Options for the correct Base URL
- Inspect the Service Worker logs from the extension page for errors
