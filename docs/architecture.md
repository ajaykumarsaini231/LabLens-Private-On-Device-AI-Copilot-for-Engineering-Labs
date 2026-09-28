# Architecture

Multimodal + retrieval-grounded + local inference.

| Stage | Component | In this repo |
|---|---|---|
| Input | Image / PDF / Voice / Text | image path + question text; audio via `ASRBackend` |
| Perception | Vision-language + ASR | `VisionLanguageBackend`, `ASRBackend` (mock + TODO Snapdragon backends) |
| Context | Local retrieval | `retrieval.LocalIndex` (TF-IDF over local `.md`/`.txt`) |
| Reasoning | Grounded response | `pipeline.LabLensPipeline.ask` |
| Action | Log / Quiz / Draft | `logbook.ObservationLog`, `viva.viva_questions`, `viva.report_outline` |

## Local-first boundary

Images, notes and lab documents remain on-device unless the user explicitly exports/shares them. The scaffold makes no network calls.

## Swapping in real models

`pipeline.LabLensPipeline` depends only on the two interfaces in `backends.py`. To run on Snapdragon, implement `VisionLanguageBackend` (and `ASRBackend`) against the local runtime and pass them to the pipeline — retrieval, logging and viva code stay unchanged.

Proposed stack: Windows ARM app • Qualcomm AI Hub models • GenieX • local retrieval/storage.
