# Use of AI Tools

> Required report section. Fill in the bracketed placeholders honestly and
> specifically. Be concrete about *what* each tool did and *where* human
> judgement drove the work.

## Tools Used
List each AI/LLM tool and what it was used for. Examples to adapt:

| Tool | Used for |
|---|---|
| [e.g. ChatGPT / Claude] | [brainstorming, explaining concepts] |
| [e.g. Claude Code / Copilot] | [boilerplate, scaffolding, refactors] |
| [coding assistant] | [debugging, test ideas] |
| [writing assistant] | [drafting/proofreading report prose] |

Briefly note the two **LLMs that are part of the product itself** (not authoring
aids): the extractor backends `qwen2.5:3b` (local, via Ollama) and
`Qwen/Qwen2.5-7B-Instruct` (Hugging Face). These perform **field extraction
only**; they are a component of the system, distinct from any AI tools used to
help write the code or report.

## What the AI Did vs. What the Team Did
State this explicitly:
- AI tools assisted with **[brainstorming, boilerplate code, draft text,
  debugging suggestions]**.
- The **substantive intellectual decisions were the team's own**, including:
  - problem framing and scope (text-only readback verification);
  - the choice of the **hybrid architecture** (LLM extracts, deterministic
    Python judges);
  - the **eight-field schema** and normalization rules;
  - the **error-category definitions / labels** (`value_substitution`,
    `digit_transposition`, `omission`, `callsign_error`, `added_element`);
  - the **evaluation methodology** and metric choices (incl. false-alarm rate);
  - **interpretation** of the results and failure-mode analysis.

## Verification & Accountability
- All AI-suggested code was reviewed, run, and tested by the team
  (see `tests/test_compare.py` and the CI workflow).
- All AI-assisted text was checked for accuracy against the actual repository.

## Per-Member Note (optional)
Each member may add one line on how they used AI in their area
(see `docs/reflections/<name>.md`).

> **Q&A reminder:** every member must be able to **explain and defend** the
> design, label definitions, methodology, and results in the live Q&A,
> independent of any AI assistance used to produce them.
