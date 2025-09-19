from pathlib import Path
import argparse
from hub import build_index


def main():
    ap = argparse.ArgumentParser(description="Build local TF-IDF index for Content Hub")
    ap.add_argument("--roots", nargs="+", default=["docs"], help="Root folders to index")
    ap.add_argument("--out", default="content_hub/index.pkl", help="Output index path")
    args = ap.parse_args()

    idx = build_index(args.roots)
    out = Path(args.out)
    idx.save(out)
    print(f"Indexed {len(idx.chunks)} chunks from {args.roots} -> {out}")


if __name__ == "__main__":
    main()
