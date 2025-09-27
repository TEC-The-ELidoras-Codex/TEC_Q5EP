"""Package the TEC Research & Development Queen agent manifest into a deployable zip.

Usage:
    python tools/package_agent_manifest.py --output dist/tec_rd_queen_agent.zip

The generated archive bundles the chat mode markdown and toolset definition
required by the Microsoft 365 admin center "Upload custom Agent" flow.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "tec_rd_queen_agent.zip"

CHATMODE_FILE = REPO_ROOT / ".github" / "chatmodes" / "Agent_of_Research&Dev_Queen.chatmode.md"
TOOLSET_FILE = REPO_ROOT / ".github" / "TEC_Tools_Azure_Copilot.toolsets.jsonc"


def build_archive(output_path: Path) -> Path:
    """Create the agent manifest archive at *output_path*.

    Returns
    -------
    Path
        Absolute path to the generated archive.
    """
    missing = [p for p in (CHATMODE_FILE, TOOLSET_FILE) if not p.exists()]
    if missing:
        missing_list = "\n".join(str(p.relative_to(REPO_ROOT)) for p in missing)
        raise FileNotFoundError(
            "Required manifest component(s) missing:\n" f"{missing_list}"
        )

    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(output_path, mode="w", compression=ZIP_DEFLATED) as archive:
        archive.write(CHATMODE_FILE, arcname=CHATMODE_FILE.name)
        archive.write(TOOLSET_FILE, arcname=TOOLSET_FILE.name)

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Where to write the packaged zip (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    archive_path = build_archive(args.output)
    print(f"Agent manifest packaged to: {archive_path}")


if __name__ == "__main__":
    main()
