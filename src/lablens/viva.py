"""Viva mode + report outline (template-based scaffold; a real model can replace it)."""
from __future__ import annotations

from typing import Sequence

from .retrieval import Chunk


def viva_questions(topic: str, context: Sequence[Chunk], n: int = 4) -> list[str]:
    qs = [
        f"Explain the mechanism behind {topic} in your own words.",
        f"Which measurements did you record for {topic}, and why do they matter?",
        f"How would you confirm your explanation for {topic} with a characterisation technique?",
        f"What could go wrong or bias the result in this experiment on {topic}?",
    ]
    for c in context[:2]:
        qs.append(f"Your notes discuss '{c.section}'. How does that apply to this experiment?")
    return qs[:n] if n < len(qs) else qs


def report_outline(experiment: str) -> list[str]:
    return [
        f"Title — {experiment}",
        "Aim and background",
        "Apparatus and procedure",
        "Observations (your recorded measurements, unchanged)",
        "Analysis and mechanism",
        "Conclusion",
        "References",
    ]
