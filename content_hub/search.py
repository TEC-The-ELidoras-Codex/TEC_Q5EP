from pathlib import Path
import argparse
from hub import HubIndex


def main():
    ap = argparse.ArgumentParser(description="Query Content Hub index")
    ap.add_argument("--index", default="content_hub/index.pkl", help="Index path")
    ap.add_argument("--query", required=True, help="Search query")
    ap.add_argument("--topk", type=int, default=5, help="Top results")
    args = ap.parse_args()

    idx = HubIndex.load(Path(args.index))
    results = idx.search(args.query, topk=args.topk)
    for (chunk, score) in results:
        print(f"\n# {chunk.source} [chunk {chunk.chunk_id}] — score={score:.3f}\n")
        print(chunk.text[:1200])


if __name__ == "__main__":
    main()
