#!/usr/bin/env python3
"""
TEC Copilot Ingester
--------------------
A command-line tool to capture summaries and notes from web browsing
and save them as permanent memories in the local TEC Memory API.

This agent acts as a bridge between external information (like summaries
from an Edge Copilot) and the sovereign, local-first knowledge base
of The Elidoras Codex.

Usage:
  python tools/copilot_ingester.py \
    --summary "Astronomers found a black hole growing at 2.4x the theoretical Eddington limit..." \
    --source-url "https://www.example.com/article" \
    --tags "astrophysics,blackhole,super-eddington" \
    --notes "This is a key piece of evidence for the Kaznak entity's hunger."
"""

import argparse
from pathlib import Path
import sys

# Ensure the project root is in the Python path to allow for module imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from agents.tools.memory_client import make_memory_client
except ImportError:
    print("ERROR: Could not import memory_client. Make sure you are running this from the repo root.", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    """Main function to parse arguments and save the memory."""
    parser = argparse.ArgumentParser(
        description="Ingest a summary into the TEC Local Memory API.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--summary",
        required=True,
        help="The summary text to be saved. (e.g., copied from Edge Copilot)"
    )
    parser.add_argument(
        "--source-url",
        required=True,
        help="The original URL of the content that was summarized."
    )
    parser.add_argument(
        "--tags",
        default="",
        help="Comma-separated tags for the memory (e.g., 'research,ai,cosmology')."
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Personal notes or context to add to the memory."
    )
    parser.add_argument(
        "--user-id",
        default="kaznakalpha",
        help="The user ID to associate with the memory."
    )
    parser.add_argument(
        "--api-base-url",
        default="http://127.0.0.1:8000",
        help="The base URL for the running TEC_Q5EP API server."
    )
    args = parser.parse_args()

    print("Attempting to connect to TEC Memory API...")

    try:
        # Instantiate the client to interact with your FastAPI server
        memory_client = make_memory_client(args.api_base_url)

        # Format the content of the memory for clarity
        content_parts = []
        if args.notes:
            content_parts.append(f"## Architect's Notes\n\n{args.notes}")
        content_parts.append(f"## Summary\n\n{args.summary}")
        full_content = "\n\n---\n\n".join(content_parts)

        # Prepare the metadata
        tags_list = [tag.strip() for tag in args.tags.split(',') if tag.strip()]
        metadata = {
            "source_url": args.source_url,
            "ingest_method": "copilot_ingester_v1"
        }

        # Construct the payload for the Memory API
        payload = {
            "user_id": args.user_id,
            "tags": tags_list,
            "content": full_content,
            "metadata": metadata,
        }

        print(f"Submitting memory for source: {args.source_url}")
        new_memory = memory_client["add"](payload)

        print("\n✅ Success! Memory saved to the Elidoras Codex.")
        print(f"   ID: {new_memory.get('id')}")
        print(f"   Timestamp: {new_memory.get('timestamp')}")
        print(f"   Tags: {', '.join(new_memory.get('tags', []))}")

    except Exception as e:
        print("\n❌ ERROR: Could not save memory to the API.", file=sys.stderr)
        print("   Please ensure the TEC_Q5EP FastAPI server is running.", file=sys.stderr)
        print("   (Run task: 'server:run' in VS Code or `uvicorn server.app:app --reload`)", file=sys.stderr)
        print(f"   Details: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
