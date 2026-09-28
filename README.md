# LabLens

**Private, on-device AI copilot for engineering labs.**
*See it. Understand it. Record it. Learn from it.*

Built for the **Snapdragon® AI Lab Build & Present Challenge**. LabLens is a Windows app concept that uses local vision + language + speech AI to turn lab photos, notes and questions into structured assistance, designed for Snapdragon-powered HP PCs.

> **Project status: proposal + working prototype scaffold.**
> The local-first workflow (retrieval over your own notes, structured lab log, viva questions, report outline, CLI, tests) runs today using only the Python standard library.
> The on-device vision-language and speech models are **not wired in yet** — `MockVisionLanguageBackend` stands in, and the Snapdragon backends in `src/lablens/backends.py` are marked TODO. See the [roadmap](docs/roadmap.md).

## The problem

Engineering students lose context between the lab bench and the laptop. Photos, handwritten observations, instrument readings and PDFs become disconnected.

- **Visual context gets lost** — a setup/sample photo is rarely linked to the final lab record.
- **Notes are fragmented** — information lives across notebooks, screenshots, PDFs and messages.
- **Cloud upload is not always desirable** — private lab material should not need to leave the device just to get AI help.
- **Students need "why?"** — they need explanation + observation guidance, not just generated text.

## What LabLens does

| Step | What happens |
|---|---|
| **Capture** | Photo of setup, specimen, graph or instrument. |
| **Ask** | Type or speak a question. |
| **Ground** | Retrieve relevant local lab notes/PDFs. |
| **Act** | Explanation + lab log + viva + report structure. |

Features: Visual Lab Understanding · Local Lab Knowledge · Voice Mode · Observation Assistant · Viva Mode · Report Builder.

## Architecture

```
Input ──► Perception ──► Context ──► Reasoning ──► Action
Image/PDF   Vision-language  Local      Grounded     Log / Quiz /
Voice/Text  + ASR            retrieval  response     Draft
```

Images, notes and lab documents remain on-device unless the user explicitly exports/shares them. Proposed stack: Windows ARM app • Qualcomm AI Hub models • GenieX • local retrieval/storage. Details in [docs/architecture.md](docs/architecture.md).

## Quick start

Requires Python 3.10+. No third-party packages are needed for the scaffold.

```bash
git clone <your-repo-url>
cd lablens
pip install -e .          # or: export PYTHONPATH=src

# Ask a question grounded in the sample local notes
lablens ask --question "What should I record from this setup?" --image setup.jpg

# Generate a structured observation log / viva questions + report outline
lablens log  --question "What should I record?" --experiment "High-temperature oxidation"
lablens viva --question "diffusion"             --experiment "High-temperature oxidation"

# Run the tests
pip install pytest && pytest
```

Point `--notes` at your own folder of `.md` / `.txt` lab notes to ground answers in your material.

## Design principles

- **Local-first** — no cloud upload required for the core workflow.
- **Grounded** — answers carry the local source file and section they used.
- **Measurement-safe** — user-entered measurements (`ObservationLog.measurements`) are kept separate from AI-generated text (`ai_notes`) and are never modified by the AI.
- **Action-oriented** — outputs become logs, quizzes and report structures.

## Mapping to the evaluation criteria

- **Technical implementation** — multimodal pipeline + local retrieval + Qualcomm AI Hub / GenieX + Snapdragon optimization.
- **Application use case & innovation** — engineering-lab workflow combining visual understanding, grounded notes, viva and reporting.
- **Deployment & accessibility** — Windows ARM; local-first; camera, keyboard and voice inputs.
- **Presentation & documentation** — clear user journey, architecture, prototype UI, metrics and roadmap.

## Success metrics

Latency • memory • grounded-answer rate • vision accuracy • task completion time.

## Repository layout

```
src/lablens/      retrieval, backends, logbook, viva, pipeline, cli
sample_data/      sample local lab notes
tests/            pytest suite
docs/             architecture + roadmap
```

## Sources & caveat

Qualcomm AI Hub (models, Apps, Workbench, GenieX; Qwen3-VL-4B-Instruct and Whisper model cards) and HP Support (OmniBook X 14 specifications). Technical claims should be rechecked against the exact HP Snapdragon configuration used for the final demo.

## License

MIT — see [LICENSE](LICENSE).
