"""Local retrieval over the student's own lab notes (Markdown / text files).

Pure standard library: TF-IDF + cosine similarity. Nothing leaves the device.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

_TOKEN = re.compile(r"[a-z0-9]+")
_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "is", "are", "was",
    "were", "be", "with", "as", "at", "by", "it", "this", "that", "from", "what", "how",
    "should", "i", "we", "you", "my", "our", "do", "does",
}


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP]


@dataclass
class Chunk:
    source: str      # file name
    section: str     # nearest heading
    text: str
    score: float = 0.0


class LocalIndex:
    """Index of local lab notes. Each chunk keeps its source file + section so an
    answer can show exactly which local section it used (grounded answers)."""

    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self._tf: list[Counter] = []
        self._idf: dict[str, float] = {}

    # -- building ---------------------------------------------------------
    @classmethod
    def from_folder(cls, folder: str | Path) -> "LocalIndex":
        idx = cls()
        for path in sorted(Path(folder).rglob("*")):
            if path.suffix.lower() in {".md", ".txt"}:
                idx._add_file(path)
        idx._finalize()
        return idx

    def _add_file(self, path: Path) -> None:
        section = path.stem
        buf: list[str] = []

        def flush() -> None:
            body = " ".join(buf).strip()
            if body:
                self.chunks.append(Chunk(path.name, section, body))
            buf.clear()

        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                flush()
                section = line.lstrip("# ").strip() or section
            elif not line.strip():
                flush()
            else:
                buf.append(line.strip())
        flush()

    def _finalize(self) -> None:
        self._tf = [Counter(tokenize(c.section + " " + c.text)) for c in self.chunks]
        df: Counter = Counter()
        for tf in self._tf:
            df.update(tf.keys())
        n = max(len(self.chunks), 1)
        self._idf = {t: math.log((1 + n) / (1 + d)) + 1.0 for t, d in df.items()}

    # -- querying ---------------------------------------------------------
    def search(self, query: str, k: int = 3) -> list[Chunk]:
        q = Counter(tokenize(query))
        if not q or not self.chunks:
            return []
        qvec = {t: c * self._idf.get(t, 0.0) for t, c in q.items()}
        qnorm = math.sqrt(sum(v * v for v in qvec.values())) or 1.0
        scored: list[Chunk] = []
        for chunk, tf in zip(self.chunks, self._tf):
            dvec = {t: c * self._idf.get(t, 0.0) for t, c in tf.items()}
            dnorm = math.sqrt(sum(v * v for v in dvec.values())) or 1.0
            dot = sum(qvec[t] * dvec.get(t, 0.0) for t in qvec)
            score = dot / (qnorm * dnorm)
            if score > 0:
                scored.append(Chunk(chunk.source, chunk.section, chunk.text, round(score, 4)))
        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[:k]
