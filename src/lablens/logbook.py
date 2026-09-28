"""Structured observation log.

Measurement-safe by design: values typed in by the student live in `measurements`
and are never edited by the AI. Anything generated goes in `ai_notes`.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime

PROMPTS = [
    "specimen_id",
    "surface_condition",
    "exposure_time",
    "temperature",
    "visible_changes",
]


@dataclass
class ObservationLog:
    experiment: str
    created: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    measurements: dict[str, str] = field(default_factory=dict)   # user-entered only
    ai_notes: list[str] = field(default_factory=list)             # AI-generated only
    sources: list[str] = field(default_factory=list)              # local notes used

    def add_measurement(self, key: str, value: str) -> None:
        self.measurements[key] = value

    def add_ai_note(self, note: str, sources: list[str] | None = None) -> None:
        self.ai_notes.append(note)
        for s in sources or []:
            if s not in self.sources:
                self.sources.append(s)

    def missing(self) -> list[str]:
        """What the student should still record (observation assistant)."""
        return [p for p in PROMPTS if p not in self.measurements]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    def to_markdown(self) -> str:
        lines = [f"# Lab log — {self.experiment}", f"_Created {self.created}_", "", "## Measurements (user-entered)"]
        if self.measurements:
            lines += [f"- **{k.replace('_', ' ')}**: {v}" for k, v in self.measurements.items()]
        else:
            lines.append("- (none yet)")
        still = self.missing()
        if still:
            lines += ["", "## Still to record"] + [f"- {k.replace('_', ' ')}" for k in still]
        lines += ["", "## AI-generated notes"]
        lines += [f"- {n}" for n in self.ai_notes] or ["- (none)"]
        if self.sources:
            lines += ["", "## Local sources used"] + [f"- {s}" for s in self.sources]
        return "\n".join(lines) + "\n"
