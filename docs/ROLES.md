# Roles

Proposed role allocation for the **ATC Readback Verifier** project (NLP Group Project, Option 1 — Application Development).

> **Note:** This is a **starting allocation**, not a contract. The team can swap, split, or share ownership freely as the work evolves — these assignments exist to give every area a clear point of contact, not to lock anyone in.
>
> Everyone writes their own reflection at `docs/reflections/<name>.md`.

| Member | Role | Owned modules / paths | Key responsibilities | Main graded deliverables driven |
| --- | --- | --- | --- | --- |
| **Jan** *(repo owner)* | App / UI & hosting | `app/streamlit_app.py`, Streamlit Cloud deploy | Build and maintain the Streamlit web UI (instruction + readback text input, verdict display); manage the GitHub repo; deploy the hosted demo on Streamlit Community Cloud (`EXTRACTOR_BACKEND="hf"` + `HF_TOKEN` in Settings → Secrets) | Functional system, live hosted demo link, code repository link |
| **Vlad** | Comparator core IP | `src/atc_verifier/compare.py`, `src/atc_verifier/verdict.py`, `src/atc_verifier/schema.py` | Own the deterministic field-by-field comparator (the core original IP) and the verdict/result types; maintain the typed 8-field schema and normalization; keep the error categories (`value_substitution`, `digit_transposition`, `omission`, `callsign_error`, `added_element`) correct and well-justified | Functional system (core logic), originality / critical-thinking content for the report |
| **Felipe** | Extraction & prompts | `src/atc_verifier/extract/` (`base.py`, `ollama_backend.py`, `hf_backend.py`, `prompts/extract_fields.txt`) | Own the LLM extractor interface/factory and both backends (Ollama local, Hugging Face API); maintain and iterate the few-shot extraction prompt; document backend selection via `EXTRACTOR_BACKEND` / `MODEL_NAME` | Supporting artifacts (prompts), functional system (extraction layer) |
| **Alberto** | Evaluation & metrics | `eval/` (`run_eval.py`, `metrics.py`, `results/`) | Own the evaluation harness and metric computation (precision, recall, F1, false-alarm rate, verdict accuracy, per-category recall, confusion matrix); produce the reproducible `make eval` run and the outputs in `eval/results/` | Custom evaluation + metrics, reproducibility |
| **Kishan** | Test set & data quality | `eval/data/` (`atc_readback_test_set.csv`) | Own, extend, and curate the labelled test cases (TC01–TC50); ensure coverage of MATCH plus every error category; safeguard label quality and the failure-mode case selection | Supporting artifacts (dataset), input to the failure-mode analysis |
| **Yi** | Report, field review & coordination | `docs/report/`, slides, project management | Own the technical report and slides; lead the domain/field review and justification-of-need narrative; coordinate tasks and deadlines across the team | Technical report (PDF), executive summary, presentation slides, project coordination |

## Cross-cutting responsibilities

- **Everyone** writes their own individual reflection at `docs/reflections/<name>.md`.
- **Everyone** contributes to the required report section titled **"Use of AI tools."**
- **Everyone** keeps tests (`tests/test_compare.py`) and CI (`.github/workflows/ci.yml`, ruff + pytest on Python 3.11/3.12) green for changes they own.

## Rubric coverage

The allocation is designed so each rubric dimension has a clear owner: **technical rigor** (Vlad, Felipe), **empirical depth** (Alberto, Kishan), **originality / critical thinking** (Vlad), **communication** (Yi), **reproducibility** (Alberto, Jan). These are shared goals — owners coordinate, they do not work in isolation.
