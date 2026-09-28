from pathlib import Path

from lablens.backends import MockVisionLanguageBackend
from lablens.logbook import ObservationLog
from lablens.pipeline import LabLensPipeline
from lablens.retrieval import LocalIndex

NOTES = Path(__file__).resolve().parents[1] / "sample_data" / "notes"


def make():
    return LabLensPipeline(LocalIndex.from_folder(NOTES), MockVisionLanguageBackend())


def test_retrieval_is_grounded_in_local_notes():
    hits = LocalIndex.from_folder(NOTES).search("what should I record for the specimen")
    assert hits and "record" in hits[0].text.lower()
    assert hits[0].source == "oxidation_lab.md"


def test_answer_cites_local_source():
    ans = make().ask("How do I confirm the oxide scale mechanism?")
    assert ans.sources and "XRD" in ans.text


def test_measurements_are_kept_separate_from_ai_notes():
    log = ObservationLog("Oxidation")
    log.add_measurement("temperature", "800 C")
    log.add_ai_note("Possible diffusion-controlled growth", ["oxidation_lab.md"])
    assert log.measurements == {"temperature": "800 C"}
    assert "temperature" not in log.missing()
    assert "800 C" not in " ".join(log.ai_notes)


def test_act_returns_log_viva_and_outline():
    out = make().act("Oxidation", "What should I record?")
    assert out["viva"] and out["outline"] and out["log"].ai_notes
