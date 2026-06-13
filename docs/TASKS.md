# Task Board

Project task board for the **ATC Readback Verifier** (NLP Group Project, Option 1). Tasks are grouped by phase (**Early / Middle / Late**) and tagged by owner, e.g. `(Alberto)`. Items already completed by the infrastructure setup are checked `- [x]`.

> This board covers every assignment deliverable: justification of need, field review, functional system, custom evaluation + metrics, failure-mode analysis, reproducible repo, user manual, install guide, technical report (PDF), one-page executive summary, slides, code repo link, supporting artifacts (dataset + prompts), six individual reflections, the "Use of AI tools" report section, and the live hosted demo.

---

## Early — scope, setup, literature scan

- [x] Scaffold repository structure (`src/`, `app/`, `eval/`, `tests/`, `docs/`, `Makefile`, `pyproject.toml`) (Jan)
- [x] Add `requirements.txt`, `requirements-dev.txt`, editable install (`pip install -e .`) via `make setup` (Jan)
- [x] Add `.env.example` with `EXTRACTOR_BACKEND` / `MODEL_NAME` / `HF_TOKEN` / `OLLAMA_HOST` (Felipe)
- [x] Set up GitHub Actions CI (`.github/workflows/ci.yml`: ruff + pytest on Python 3.11 & 3.12) (Jan)
- [x] Define the typed 8-field schema and normalization in `src/atc_verifier/schema.py` (Vlad)
- [x] Lay down the app skeleton at `app/streamlit_app.py` (Jan)
- [ ] Write the justification-of-need narrative (safety motivation: wrong/incomplete readbacks as a documented incident contributor, e.g. NASA ASRS) (Yi)
- [ ] Field review: survey related work in NLP for aviation / ATC and readback verification; position our hybrid LLM-extraction + deterministic-comparison approach (Yi)
- [ ] Confirm scope in writing: **text input only**; live audio / speech-to-text is a future direction, not built (Yi)
- [ ] Confirm proposed role allocation with the team and adjust `docs/ROLES.md` if swapping (all)
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
- [ ] Finalize the Streamlit UI: instruction + readback text inputs, verdict rendering, discrepancy list (Jan)
- [ ] Pull the local model and verify end-to-end run with Ollama: `make pull-model` then `make run` (Felipe)
- [ ] Curate / extend test cases for label quality and balanced category coverage (Kishan)
- [ ] Run the reproducible evaluation: `make eval` → generate `metrics.md`, `metrics.json`, `predictions.csv`, `failures.md` in `eval/results/` (Alberto)
- [ ] Sanity-check reported metrics: precision, recall, F1, false-alarm rate, verdict accuracy, per-category recall, confusion matrix (Alberto)
- [ ] Deploy the hosted demo to Streamlit Community Cloud (`EXTRACTOR_BACKEND="hf"`, `HF_TOKEN` in Settings → Secrets; human does OAuth + Deploy once) (Jan)

## Late — analysis, writing, slides, rehearsal

- [ ] Failure-mode analysis: select and write up 5–10 misclassified cases from `eval/results/failures.md` (Alberto, Kishan)
- [ ] Verify the repo is reproducible end-to-end from a clean clone (`make setup` → `make test` → `make eval`) (Alberto, Jan)
- [ ] Write the **user manual** `docs/USER_MANUAL.md` (how to use the app, interpret MATCH / DISCREPANCY output) (Jan)
- [ ] Write the **install / execution guide** `docs/INSTALL.md` (Makefile targets + manual equivalents, both backends) (Jan)
- [ ] Write `docs/CONTRIBUTING.md` (dev workflow: `make lint`, `make fmt`, `make test`) (Vlad)
- [ ] Draft the **technical report** in `docs/report/` and export to **PDF** (Yi)
- [ ] Write the **one-page non-technical executive summary** (Yi)
- [ ] Write the required report section **"Use of AI tools"** (all)
- [ ] Prepare **presentation slides** (Yi)
- [ ] Assemble **supporting artifacts** for submission: dataset (`eval/data/`) + prompts (`extract_fields.txt`) (Kishan, Felipe)
- [ ] Include the **code repository link** (https://github.com/janwejchert/NLP) and the **live hosted demo link** in the report and slides (Jan)
- [ ] Each member writes their **individual reflection** at `docs/reflections/<name>.md` — 6 total (Jan, Vlad, Felipe, Alberto, Kishan, Yi)
- [ ] Final proofread pass against rubric (technical rigor, empirical depth, originality / critical thinking, communication, reproducibility) (Yi)
- [ ] Rehearse the presentation and demo (all)
