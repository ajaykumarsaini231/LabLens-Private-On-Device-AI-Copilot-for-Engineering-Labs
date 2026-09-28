"""Model backends.

LabLens talks to models only through these two small interfaces, so the on-device
runtime can be swapped without touching the rest of the app.

* MockVisionLanguageBackend — deterministic, dependency-free stand-in used for the
  scaffold, demos and tests. It does NOT look at pixels.
* QualcommAIHubBackend — placeholder where a real vision-language model running on the
  Snapdragon NPU (e.g. via Qualcomm AI Hub / GenieX) is meant to be wired in.
  Not implemented yet.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence

from .retrieval import Chunk


class VisionLanguageBackend(ABC):
    @abstractmethod
    def answer(self, question: str, image: Path | None, context: Sequence[Chunk]) -> str:
        """Return an explanation for `question`, optionally about `image`, grounded in `context`."""


class ASRBackend(ABC):
    @abstractmethod
    def transcribe(self, audio: Path) -> str:
        """Turn spoken audio into text."""


class MockVisionLanguageBackend(VisionLanguageBackend):
    """Placeholder model: builds an answer from the retrieved local notes only."""

    def answer(self, question: str, image: Path | None, context: Sequence[Chunk]) -> str:
        parts = []
        if image is not None:
            parts.append(f"[mock] Image received ({Path(image).name}); pixels are not analysed by the mock backend.")
        if context:
            top = context[0]
            parts.append(f"From your notes ({top.source} › {top.section}): {top.text}")
        else:
            parts.append("No matching local notes were found for this question.")
        return "\n".join(parts)


class QualcommAIHubBackend(VisionLanguageBackend):
    """TODO: integrate a local multimodal model on Snapdragon (Windows ARM)."""

    def answer(self, question: str, image: Path | None, context: Sequence[Chunk]) -> str:
        raise NotImplementedError(
            "Wire a Snapdragon-optimised vision-language model here "
            "(see docs/roadmap.md, stage 2 'Multimodal')."
        )


class QualcommWhisperBackend(ASRBackend):
    """TODO: integrate a local speech-to-text model (see docs/roadmap.md, stage 3)."""

    def transcribe(self, audio: Path) -> str:
        raise NotImplementedError("Wire a local Whisper-class model here.")
