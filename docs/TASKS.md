# Task Board

Project task board for the **ATC Readback Verifier** (NLP Group Project, Option 1). Tasks are grouped by phase (**Early / Middle / Late**) and tagged by owner, e.g. `(Alberto)`. Completed items are checked `- [x]`.

> This board covers every assignment deliverable: justification of need, field review, functional system, custom evaluation + metrics, failure-mode analysis, reproducible repo, user manual, install guide, technical report (PDF), one-page executive summary, slides, code repo link, supporting artifacts (dataset + prompts), six individual reflections, the "Use of AI tools" report section, and the live hosted demo.

> **Status:** all artifact deliverables are complete and submission-ready. The only open items are inherently human actions (each member runs the app once locally, and the team rehearses the talk).

---

## Early — scope, setup, literature scan

- [x] Scaffold repository structure (`src/`, `app/`, `eval/`, `tests/`, `docs/`, `Makefile`, `pyproject.toml`) (Jan)
- [x] Add `requirements.txt`, `requirements-dev.txt`, editable install (`pip install -e .`) via `make setup` (Jan)
- [x] Add `.env.example` with `EXTRACTOR_BACKEND` / `MODEL_NAME` / `HF_TOKEN` / `OLLAMA_HOST` (Felipe)
- [x] Set up GitHub Actions CI (`.github/workflows/ci.yml`: ruff + pytest on Python 3.11 & 3.12) (Jan)
- [x] Define the typed 8-field schema and normalization in `src/atc_verifier/schema.py` (Vlad)
- [x] Lay down the app skeleton at `app/streamlit_app.py` (Jan)
- [x] Write the justification-of-need narrative (safety motivation: wrong/incomplete readbacks as a documented incident contributor, e.g. NASA ASRS) (Yi)
- [x] Field review: survey related work in NLP for aviation / ATC and readback verification; position our hybrid LLM-extraction + deterministic-comparison approach (Yi)
- [x] Confirm scope in writing: **text input only**; live audio / speech-to-text is a future direction, not built (Yi)
- [x] Confirm proposed role allocation with the team and adjust `docs/ROLES.md` if swapping (all)
- [ ] Each member set up their local environment (`make setup`, `make pull-model`) and run the app once (`make run`) (all)

## Middle — core build & evaluation

- [x] Implement the deterministic field-by-field comparator in `src/atc_verifier/compare.py` (core IP) (Vlad)
- [x] Implement verdict / result types in `src/atc_verifier/verdict.py` (MATCH vs. list of discrepancies) (Vlad)
- [x] Implement the error categories: `value_substitution`, `digit_transposition`, `omission`, `callsign_error`, `added_element` (Vlad)
- [x] Implement the extractor interface + factory in `src/atc_verifier/extract/base.py` (Felipe)
- [x] Implement the Ollama local backend `ollama_backend.py` (default `qwen2.5:3b`) (Felipe)
- [x] Implement the Hugging Face backend `hf_backend.py` (default `Qwen/Qwen2.5-7B-Instruct`) (Felipe)
- [x] Author the few-shot extraction prompt `src/atc_verifier/extract/prompts/extract_fields.txt` (Felipe)
- [x] Wire the public API `from atc_verifier import verify` → `result.status` / `result.verdict.summary()` (Vlad)
- [x] Build the labelled test set `eval/data/atc_readback_test_set.csv` (50 cases, TC01–TC50, all categories) (Kishan)
- [x] Build the evaluation harness `eval/run_eval.py` + `eval/metrics.py` (Alberto)
- [x] Write unit tests for the comparator `tests/test_compare.py` (no LLM, no token) (Vlad)
- [x] Finalize the Streamlit UI: instruction + readback text inputs, verdict rendering, discrepancy list (Jan)
- [x] Pull the local model and verify end-to-end run with Ollama: `make pull-model` then `make run` (Felipe)
- [x] Curate / extend test cases for label quality and balanced category coverage (Kishan)
- [x] Run the reproducible evaluation: `make eval` → generate `metrics.md`, `metrics.json`, `predictions.csv`, `failures.md` in `eval/results/` (Alberto)
- [x] Sanity-check reported metrics: precision, recall, F1, false-alarm rate, verdict accuracy, per-category recall, confusion matrix (Alberto)
- [x] Prompt-iteration study (baseline → hardened regression → principled fix) and 3B-vs-7B run archived under `eval/results/runs/` (Alberto, Felipe)
- [x] Deploy the hosted demo to Streamlit Community Cloud (`EXTRACTOR_BACKEND="hf"`, `HF_TOKEN` in Settings → Secrets; human does OAuth + Deploy once) (Jan)

## Late — analysis, writing, slides, rehearsal

- [x] Author the reproducible analysis notebook `notebooks/analysis.ipynb` (via `notebooks/build_notebook.py`): tests, comparator demo, live pipeline, metrics, prompt-iteration, 3B-vs-7B figures, failure analysis (Jan)
- [x] Failure-mode analysis: select and write up 5–10 misclassified cases from `eval/results/` → `docs/report/failure_analysis.md` (Alberto, Kishan)
- [x] Verify the repo is reproducible end-to-end from a clean clone (`make setup` → `make test` → `make eval`) (Alberto, Jan)
- [x] Write the **user manual** `docs/USER_MANUAL.md` (how to use the app, interpret MATCH / DISCREPANCY output) (Jan)
- [x] Write the **install / execution guide** `docs/INSTALL.md` (Makefile targets + manual equivalents, both backends) (Jan)
- [x] Write `docs/CONTRIBUTING.md` (dev workflow: `make lint`, `make fmt`, `make test`) (Vlad)
- [x] Draft the **technical report** in `docs/report/` and export to **PDF** (`make pdfs`) (Yi)
- [x] Write the **one-page non-technical executive summary** and export to **PDF** (Yi)
- [x] Write the required report section **"Use of AI tools"** (`docs/report/use_of_ai_tools.md`) (all)
- [x] Prepare **presentation slides** (`docs/report/slides.md`) and export to **PDF** (`make slides`) (Yi)
- [x] Assemble **supporting artifacts** for submission: dataset (`eval/data/`) + prompts (`extract_fields.txt`) (Kishan, Felipe)
- [x] Include the **code repository link** (https://github.com/janwejchert/NLP) and the **live hosted demo link** in the report and slides (Jan)
- [x] Each member writes their **individual reflection** at `docs/reflections/<name>.md` — 6 total (Jan, Vlad, Felipe, Alberto, Kishan, Yi)
- [x] Build the submission PDFs into `docs/report/pdf/` (technical report, executive summary, reflections, slides) (Jan, Yi)
- [x] Final proofread pass against rubric (technical rigor, empirical depth, originality / critical thinking, communication, reproducibility) (Yi)
- [ ] Rehearse the presentation and demo (all)

## Submission checklist (Option 1 deliverables)

- [x] Technical report (PDF) — `docs/report/pdf/ATC_Readback_Verifier_Technical_Report.pdf`
- [x] One-page executive summary (PDF) — `docs/report/pdf/ATC_Readback_Verifier_Executive_Summary.pdf`
- [x] Slides (PDF) — `docs/report/pdf/ATC_Readback_Verifier_Slides.pdf`
- [x] Code repository (link) — https://github.com/janwejchert/NLP
- [x] Supporting artifacts — dataset (`eval/data/`), prompt (`extract_fields.txt`), full predictions (`eval/results/`)
- [x] Six individual reflections — `docs/reflections/` (and combined PDF)
- [x] User manual — `docs/USER_MANUAL.md`
- [x] Installation / execution guide — `docs/INSTALL.md`
- [ ] Live hosted demo link pasted into the README/report once deployed (Jan)
