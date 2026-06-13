# ATC Readback Verifier — Infrastructure & System Design

**Course:** NLP Group Project — Option 1 (Application Development)
**Team size:** 6
**Status:** Approved in brainstorming (2026-06-13); pending spec review before implementation
**Repository:** https://github.com/janwejchert/NLP

---

## 1. Overview

We are building the **ATC Readback Verifier**: an NLP application that checks whether a
pilot's spoken-then-typed *readback* correctly matches the air-traffic-control (ATC)
*instruction* it responds to, and flags any discrepancy.

In aviation a controller issues an instruction (e.g. "Speedbird 245, climb flight level
280") and the pilot reads it back so the controller can confirm it was heard correctly.
Wrong values, transposed digits, omitted items, and similar readback errors are a
well-documented contributor to safety incidents (e.g. NASA ASRS reports). Existing tooling
focuses on *transcribing* ATC audio, not on *verifying that a readback is correct*. This
proof of concept (POC) targets that gap, on **text input** (audio is a future direction).

This document specifies the **infrastructure and system design** so all six team members can
work in parallel and every graded deliverable has a home.

## 2. Goals and non-goals

### Goals
- A working **Streamlit** web app: user types the instruction and the readback → gets a
  verdict (`MATCH`, or a list of specific discrepancies).
- A **hybrid pipeline**: an LLM extracts structured fields; our **own deterministic Python
  code** compares them field-by-field and decides the verdict. The comparison logic is our
  original work and is fully defensible in Q&A.
- **$0 running cost.** Two interchangeable free LLM backends (see §4).
- A **reproducible evaluation harness** over our 50-case labelled test set reporting
  precision, recall, F1, false-alarm rate, per-category breakdown, and a confusion matrix.
- An automatic **failure-case dump** (5–10 cases) for the failure-mode analysis.
- A **clean, reproducible repository**: README, install guide, user manual, requirements,
  pinned model, CI.
- **Team coordination**: 6 roles mapped to non-colliding modules + a markdown task board.

### Non-goals (POC scope — documented as future directions)
- No speech-to-text / live radio audio. Input is text.
- Not production-grade: no auth, no database, no multi-user state.
- No fine-tuning. We use off-the-shelf instruction models with prompting.
- The hosted demo is best-effort; **graded metrics come from the reproducible local run**,
  not the hosted free-tier endpoint.

## 3. Assignment requirement → deliverable mapping

| Required component (Option 1) | Where it lives |
|---|---|
| Justification of need | `docs/report/` (field review + intro) |
| Field review | `docs/report/field_review.md` |
| Functional system (POC) | `app/streamlit_app.py` + `src/atc_verifier/` |
| Custom evaluation (≥30–50 examples, metrics) | `eval/` + `eval/data/atc_readback_test_set.csv` (50 cases) |
| Failure-mode analysis (5–10 cases) | `eval/results/failures.md` (auto-seeded) |
| Reproducible repository | whole repo: README, `INSTALL.md`, requirements, CI |
| User manual (Option 1) | `docs/USER_MANUAL.md` |
| Install/execution guide (Option 1) | `docs/INSTALL.md` |
| Live link (bonus) | Streamlit Community Cloud |
| Use-of-AI-tools section | `docs/report/use_of_ai_tools.md` |
| Individual reflections (×6) | `docs/reflections/<name>.md` |
| Exec summary (1 page, non-technical) | `docs/report/executive_summary.md` |
| Slides | `docs/report/slides/` (link or file) |

## 4. Architecture

### 4.1 Hybrid pipeline (data flow)

```
            instruction (text)            readback (text)
                  │                             │
                  ▼                             ▼
        ┌───────────────────┐         ┌───────────────────┐
        │  Extractor (LLM)  │         │  Extractor (LLM)  │   ← swappable backend
        │  text → fields    │         │  text → fields    │
        └─────────┬─────────┘         └─────────┬─────────┘
                  │  ReadbackFields              │  ReadbackFields
                  └───────────────┬──────────────┘
                                  ▼
                   ┌──────────────────────────────┐
                   │  Comparator (deterministic)   │  ★ our core IP
                   │  field-by-field, normalized   │
                   └───────────────┬───────────────┘
                                   ▼
                   ┌──────────────────────────────┐
                   │  Verdict assembler            │
                   │  MATCH | [Discrepancy, ...]   │
                   └──────────────────────────────┘
```

The LLM does **only** structured extraction (the easy, well-bounded part that a small free
model handles well). All judgement — what counts as a match, how values are normalized, which
error category applies — is **deterministic Python we wrote**. This maximizes originality,
reproducibility, and defensibility, and is what lets a small free model suffice.

### 4.2 Pluggable extractor — two free backends

A single `Extractor` interface with two implementations, selected by the
`EXTRACTOR_BACKEND` env var:

| Backend (`EXTRACTOR_BACKEND`) | Implementation | Used for | Cost |
|---|---|---|---|
| `ollama` | Local Ollama server, default model `qwen2.5:3b-instruct` (`7b` optional) | Development + the **reproducible evaluation run** | $0, offline |
| `hf` | Hugging Face Inference API (free token) | The **live Streamlit Cloud demo** (1 GB tier can't host a local model) | $0 within free tier |

Both return the same `ReadbackFields` object, so the comparator and the entire downstream
are backend-agnostic. Swapping backends is a one-line env change. This resolves the
"free local model" vs "Streamlit Cloud hosting" tension: the cloud free tier (~1 GB RAM,
CPU) cannot run a 3B/7B model, so the hosted app uses `hf`; the graded eval uses `ollama`.

**Model rationale:** Qwen2.5-3B-Instruct is small (~2 GB Q4), fast on an Intel CPU, Apache-2.0
licensed, and strong at constrained JSON extraction. The local model is **pinned by name+tag**
for reproducibility. The `hf` backend's model is configurable (`MODEL_NAME`) since free-tier
availability shifts; the default is chosen at build time among models confirmed live.

**Robustness:** extraction prompts are few-shot and request strict JSON; the backend layer
validates/repairs the JSON (retry + lenient parse) before handing typed fields downstream.

## 5. Data model and field schema

Eight fields, matching the proposal and the test set:

| Field | Type | Normalization notes |
|---|---|---|
| `callsign` | str | airline+number or registration (e.g. "Speedbird 245", "G-ABCD"); telephony spelling normalized |
| `altitude` | struct | flight level (FL280) vs altitude in feet (3000 ft); spelled-out numbers ("three thousand") → digits |
| `heading` | int (deg) | 3-digit heading; "left/right" direction captured |
| `speed` | int (kt) | speed restriction in knots |
| `frequency` | str/decimal | e.g. 118.7, 121.35; trailing-zero normalization |
| `squawk` | str (4 digits) | transponder code, leading zeros preserved |
| `runway` | str | e.g. "24", "32 left"; designator + side |
| `qnh` | int | pressure setting (e.g. 1013, 998) |

Each field is `None` when absent. Spelled-out numbers, telephony ("one zero one three"), and
unit variants are normalized before comparison so semantically-equal readbacks match
(e.g. TC10: "climb three thousand feet, QNH 1013" ≡ "climb altitude 3000 feet, QNH 1013").

## 6. Comparator and error taxonomy (the core IP)

The comparator compares each instruction field against the corresponding readback field and
emits zero or more `Discrepancy` records. Categories are derived directly from our test set:

| Error category | Detection rule (sketch) |
|---|---|
| `correct` / MATCH | every required field present and equal after normalization |
| `value_substitution` | field present in both, normalized values differ |
| `digit_transposition` | values differ **and** are digit-permutations of each other (special-cased, higher-risk flag) |
| `omission` | required field in instruction absent from readback |
| `callsign_error` | callsign present but differs (or missing entirely) |
| `added_element` | field in readback that was not in the instruction |

Design decisions encoded (and documented for Q&A):
- **Which items are mandatory to read back** vs. informational (e.g. wind is informational —
  TC07 is a MATCH despite the readback omitting wind). This "required-item" policy is an
  explicit, defensible label-design choice.
- **Transposition vs. substitution** precedence (a transposition is a more specific
  classification of a value error).
- Normalization rules (units, spelled-out numbers, telephony, trailing zeros).

The verdict is `MATCH` iff no discrepancies; otherwise the ordered discrepancy list with
human-readable detail strings (mirroring the test set's `expected_detail`).

## 7. Evaluation harness

`eval/run_eval.py`:
1. Loads `eval/data/atc_readback_test_set.csv` (50 labelled cases).
2. Runs the full pipeline (configurable backend) per case.
3. Compares predicted verdict + affected field(s) to the gold labels.
4. Writes to `eval/results/`:
   - `metrics.md` / `metrics.json`: **precision, recall, F1** for error detection (DISCREPANCY
     vs MATCH as the positive/negative framing), **false-alarm rate** on correct readbacks,
     **per-error-category** recall, and a **confusion matrix**.
   - `predictions.csv`: per-case predicted vs expected (full audit trail).
   - `failures.md`: the misclassified / lowest-confidence cases, with the model's extracted
     JSON, seeding the required failure-mode analysis.

Metrics framing (documented): a readback with ≥1 discrepancy is a positive ("error present").
Precision/recall/F1 measure error **detection**; false-alarm rate = fraction of truly-correct
readbacks wrongly flagged (critical in a safety setting — false alarms erode trust).

## 8. Testing strategy

- `tests/test_compare.py`: **unit tests for the comparator and normalization** on synthetic
  pre-extracted fields — **no LLM, no token, deterministic**. This is the part that is "our own
  work," so it is the part we prove correct on every push.
- CI (`.github/workflows/ci.yml`): on every push/PR, set up Python, install, run `pytest` +
  `ruff` lint. CI does **not** call any LLM (no secrets needed there).
- The LLM-dependent eval is a documented script run locally; its committed `eval/results/`
  output is the reproducible record.

## 9. Repository structure

```
NLP/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
├── Makefile
├── app/
│   └── streamlit_app.py
├── src/atc_verifier/
│   ├── __init__.py
│   ├── schema.py
│   ├── extract/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── ollama_backend.py
│   │   ├── hf_backend.py
│   │   └── prompts/extract_fields.txt
│   ├── compare.py
│   └── verdict.py
├── eval/
│   ├── data/atc_readback_test_set.csv
│   ├── run_eval.py
│   ├── metrics.py
│   └── results/            (committed outputs)
├── tests/
│   └── test_compare.py
├── docs/
│   ├── USER_MANUAL.md
│   ├── INSTALL.md
│   ├── CONTRIBUTING.md
│   ├── ROLES.md
│   ├── TASKS.md
│   ├── report/
│   ├── reflections/
│   └── superpowers/specs/
└── .github/workflows/ci.yml
```

## 10. Tooling and reproducibility

- **Python 3.13** (local has 3.13.5), `venv` virtual environment.
- `requirements.txt` (pinned) + `pyproject.toml` for metadata.
- `Makefile` targets: `setup`, `run` (Streamlit), `eval`, `test`, `lint`, `fmt`.
- `.env` (gitignored) holds `HF_TOKEN`, `EXTRACTOR_BACKEND`, `MODEL_NAME`; `.env.example`
  documents them.
- Pinned local model (`qwen2.5:3b-instruct`) for reproducible eval.
- All prompts versioned under `src/atc_verifier/extract/prompts/`.

## 11. Hosting

- **Streamlit Community Cloud**, deployed from this GitHub repo (auto-redeploys on push).
- Hosted app runs `EXTRACTOR_BACKEND=hf`; `HF_TOKEN` stored as a Streamlit **secret**.
- One-time human step: a team member signs in at share.streamlit.io with GitHub and clicks
  Deploy (OAuth — cannot be automated). Repo is prepared so this is one click + one secret.

## 12. Team: 6 roles → non-colliding modules

| # | Role | Owns | Primary deliverables |
|---|---|---|---|
| 1 | Extraction & prompts | `src/extract/` | extractor backends, few-shot prompts |
| 2 | Comparator (core IP) | `src/compare.py`, `verdict.py`, `schema.py` | normalization + error-detection logic |
| 3 | Evaluation & metrics | `eval/` | harness, metrics, failure dump |
| 4 | App / UI & hosting | `app/`, Streamlit Cloud | UI, deploy, live link |
| 5 | Test set & data | `eval/data/` | extend/curate cases, label review |
| 6 | Report & coordination | `docs/report/`, slides | field review, report, PM, task board |

Everyone writes their own `docs/reflections/<name>.md`. Workflow: feature branches → PR →
review → merge to `main` (documented in `CONTRIBUTING.md`). Task board: `docs/TASKS.md`
(markdown checklist covering every graded deliverable).

## 13. What the user/team must provide (cannot be automated)

1. **Hugging Face free token** (Read scope) → for the `hf` backend / live demo. Stored in
   gitignored `.env` and as a Streamlit secret. Free.
2. **Streamlit Community Cloud authorization** → OAuth sign-in + Deploy click. Free.
3. **Team members' names** (+ GitHub usernames to add as collaborators) → for `ROLES.md`,
   `CONTRIBUTING.md`, `TASKS.md`, and reflection stubs.

Everything else (all code, both backends, comparator, eval harness, UI, packaging, CI, docs)
is built by the assistant. The local Ollama model is pulled by the assistant.

## 14. Risks and mitigations

| Risk | Mitigation |
|---|---|
| HF free-tier rate limits / model availability shifts | Graded metrics come from local `ollama` run; `MODEL_NAME` configurable; hosted demo is best-effort |
| Small model emits malformed JSON | Strict-JSON prompt + validate/repair + retry in backend layer |
| Local model slow on Intel CPU | Default to 3B (fast); 7B optional; eval is a one-time batch, not interactive |
| 6 people editing same files → conflicts | Module-per-role ownership + PR workflow |
| LLM non-determinism affects eval reproducibility | Temperature 0, pinned model+tag, committed `eval/results/` snapshot |
| Label-design disputes (what must be read back) | Required-item policy documented explicitly in §6 and the report |

## 15. Future directions (for the report)

- Speech-to-text front end (Whisper) for live radio audio.
- Phonetic / NATO-alphabet robustness, accent and noise handling.
- Comparison of multiple extractor models (local vs hosted) as an ablation.
- Confidence scoring and controller-facing alerting UX.
