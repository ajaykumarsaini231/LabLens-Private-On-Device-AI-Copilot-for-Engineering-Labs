"""Capture → Ask → Ground → Act."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .backends import ASRBackend, VisionLanguageBackend
from .logbook import ObservationLog
from .retrieval import Chunk, LocalIndex
from .viva import report_outline, viva_questions


@dataclass
class Answer:
    text: str
    sources: list[Chunk]


class LabLensPipeline:
    def __init__(self, index: LocalIndex, vlm: VisionLanguageBackend, asr: ASRBackend | None = None):
        self.index = index
        self.vlm = vlm
        self.asr = asr

    def ask(self, question: str = "", image: Path | None = None, audio: Path | None = None, k: int = 3) -> Answer:
        if audio is not None:                      # ASK (voice)
            if self.asr is None:
                raise RuntimeError("No ASR backend configured for voice input.")
            question = self.asr.transcribe(audio)
        context = self.index.search(question, k=k)  # GROUND
        text = self.vlm.answer(question, image, context)
        return Answer(text=text, sources=context)

    def act(self, experiment: str, question: str, image: Path | None = None) -> dict:
        ans = self.ask(question, image)
        log = ObservationLog(experiment=experiment)
        log.add_ai_note(ans.text, [f"{c.source} › {c.section}" for c in ans.sources])
        return {
            "answer": ans,
            "log": log,
            "viva": viva_questions(experiment, ans.sources),
            "outline": report_outline(experiment),
        }
