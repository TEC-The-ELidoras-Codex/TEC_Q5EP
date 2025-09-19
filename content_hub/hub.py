from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import pickle
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


CHUNK_SEP = "\n\n"


def _iter_files(roots: List[Path], include_ext=(".md", ".txt")) -> List[Path]:
    files: List[Path] = []
    for root in roots:
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in include_ext:
                files.append(p)
    return files


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _split_chunks(text: str, max_chars: int = 1200, overlap: int = 150) -> List[str]:
    # crude splitter on headings and paragraphs, then window by chars
    parts = re.split(r"\n\s*#+\s|\n\n+", text)
    chunks: List[str] = []
    buf = ""
    for part in parts:
        if not part.strip():
            continue
        if len(buf) + len(part) + 2 <= max_chars:
            buf = f"{buf}\n\n{part}" if buf else part
        else:
            if buf:
                chunks.append(buf.strip())
            # slide window
            if len(part) > max_chars:
                start = 0
                while start < len(part):
                    end = min(len(part), start + max_chars)
                    chunks.append(part[start:end])
                    start = max(0, end - overlap)
                buf = ""
            else:
                buf = part
    if buf:
        chunks.append(buf.strip())
    return chunks


@dataclass
class DocChunk:
    source: str
    chunk_id: int
    text: str


@dataclass
class HubIndex:
    vectorizer: TfidfVectorizer
    matrix: any
    chunks: List[DocChunk]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: Path) -> "HubIndex":
        with path.open("rb") as f:
            return pickle.load(f)

    def search(self, query: str, topk: int = 5) -> List[Tuple[DocChunk, float]]:
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.matrix).ravel()
        idx = sims.argsort()[::-1][:topk]
        return [(self.chunks[i], float(sims[i])) for i in idx]


def build_index(roots: List[str]) -> HubIndex:
    root_paths = [Path(r).resolve() for r in roots]
    files = _iter_files(root_paths)
    chunks: List[DocChunk] = []
    for fp in files:
        text = _read_text(fp)
        for i, ch in enumerate(_split_chunks(text)):
            chunks.append(DocChunk(source=str(fp.relative_to(Path.cwd())), chunk_id=i, text=ch))

    corpus = [c.text for c in chunks]
    vec = TfidfVectorizer(max_features=50000, ngram_range=(1, 2))
    mat = vec.fit_transform(corpus)
    return HubIndex(vectorizer=vec, matrix=mat, chunks=chunks)
