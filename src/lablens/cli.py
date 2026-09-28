"""Command-line demo: `lablens ask|log|viva ...`"""
from __future__ import annotations

import argparse
from pathlib import Path

from .backends import MockVisionLanguageBackend
from .pipeline import LabLensPipeline
from .retrieval import LocalIndex


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="lablens", description="Private, on-device AI copilot for engineering labs (scaffold)")
    p.add_argument("command", choices=["ask", "log", "viva"])
    p.add_argument("--notes", default="sample_data/notes", help="folder of local lab notes (.md/.txt)")
    p.add_argument("--question", required=True)
    p.add_argument("--image", type=Path)
    p.add_argument("--experiment", default="Untitled experiment")
    a = p.parse_args(argv)

    pipe = LabLensPipeline(LocalIndex.from_folder(a.notes), MockVisionLanguageBackend())
    out = pipe.act(a.experiment, a.question, a.image)
    if a.command == "ask":
        print(out["answer"].text)
        for c in out["answer"].sources:
            print(f"  · {c.source} › {c.section} (score {c.score})")
    elif a.command == "log":
        print(out["log"].to_markdown())
    else:
        print("\n".join(f"{i}. {q}" for i, q in enumerate(out["viva"], 1)))
        print("\nReport outline:\n" + "\n".join(f"- {s}" for s in out["outline"]))


if __name__ == "__main__":
    main()
