# Contributing

Collaboration guide for the 6-person team building the **ATC Readback Verifier**
(NLP Group Project, Option 1). This is a university proof-of-concept, not
production software — but we still keep `main` clean and reviewable.

Members: Jan, Vlad, Felipe, Alberto, Kishan, Yi.

## Branching model

- **Never commit straight to `main`.** `main` is always green and deployable.
- Create a feature branch off the latest `main`:

  ```bash
  git checkout main
  git pull --rebase origin main
  git checkout -b feature/<area>-<short-desc>
  ```

- Name branches `feature/<area>-<short-desc>` (e.g. `feature/compare-digit-transposition`)
  or `fix/<area>-<short-desc>` for bug fixes.
- Open a **Pull Request** into `main` when ready.
- **At least one teammate reviews** before merge.
- **CI (ruff + pytest) must pass** before a PR can be merged.

## Module ownership

To avoid editing the same files in parallel, each area has a primary owner.
Coordinate with the owner before touching their files. This is a starting
point — the team can swap freely; see [ROLES.md](ROLES.md) for the full mapping.

| Area                       | Path(s)                                              | Owner   |
| -------------------------- | ---------------------------------------------------- | ------- |
| App / UI & hosting         | `app/`                                               | Jan     |
| Comparator (core IP)       | `src/atc_verifier/compare.py`, `verdict.py`, `schema.py` | Vlad    |
| Extraction & prompts       | `src/atc_verifier/extract/`                          | Felipe  |
| Evaluation & metrics       | `eval/`                                              | Alberto |
| Test set & data quality    | `eval/data/`                                         | Kishan  |
| Report & coordination      | `docs/report/`, slides                               | Yi      |

Everyone writes their own `docs/reflections/<name>.md`.

## Where things live

- **Library code** → `src/atc_verifier/` (importable package).
- **Web app** → `app/streamlit_app.py`.
- **Evaluation** → `eval/` (harness, test data, results).
- **Unit tests** → `tests/`.
- **Docs** → `docs/`.

## Local checks before pushing

Run these from the repo root before you push. Fix anything that fails.

```bash
make lint    # ruff check src tests eval app
make test    # pytest (comparator unit tests, no LLM/token needed)
```

If you touched **extraction, the comparator, or the eval harness**, also
regenerate metrics and sanity-check them:

```bash
make eval    # python eval/run_eval.py -> writes eval/results/
```

Manual equivalents (inside the activated `.venv`) if you prefer not to use Make:

```bash
ruff check src tests eval app
pytest
python eval/run_eval.py
```

## Keeping `main` green

- **CI** runs on every push and pull request via
  `.github/workflows/ci.yml`. It installs `ruff` + `pytest` and runs
  `ruff check src tests eval app` then `pytest` on **Python 3.11 and 3.12**.
  The comparator tests need no LLM and no API token, so CI is fast and offline.
- Keep your branch current with `main` to avoid surprise conflicts:

  ```bash
  git pull --rebase origin main
  ```

- If CI fails on your PR, fix it on the branch and push again — do not merge red.

## Commit messages

- Short, **imperative** summary line (~50 chars): "Add digit-transposition rule".
- Reference the area when useful: "compare: handle missing callsign".
- Keep one logical change per commit where practical.

## Adding test cases

The labelled test set is `eval/data/atc_readback_test_set.csv` (50 cases,
ids `TC01`..`TC50`). To add a case, append a row following the existing column
schema exactly:

```
id,instruction,readback,expected_verdict,error_category,affected_field,expected_detail,design_note
```

- `expected_verdict` is `MATCH` or `DISCREPANCY`.
- `error_category` is one of: `correct`, `value_substitution`,
  `digit_transposition`, `omission`, `callsign_error`, `added_element`.
- `affected_field` is one of the eight fields (`callsign`, `altitude`,
  `heading`, `speed`, `frequency`, `squawk`, `runway`, `qnh`) or `none`.
- Quote fields that contain commas. Use a fresh, sequential `id`.

After adding cases, run `make eval` and review `eval/results/metrics.md`.

## Adding unit tests

Unit tests for the deterministic comparator live in `tests/test_compare.py`.
They run without any LLM or token. Add focused tests there for new comparator
behaviour (new error category, normalization edge case, etc.) and confirm
`make test` passes locally before opening a PR.

## A note on our own thinking

Substantive intellectual decisions — label definitions, how we interpret each
error category, and our evaluation methodology — must be **the team's own work
and defensible in the Q&A**, per the assignment. Tools may help us draft and
implement, but the design choices and their justification are ours. Document
non-obvious decisions in the relevant PR or in `docs/report/`.
