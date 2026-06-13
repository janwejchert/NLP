# Technical report — outline

Skeleton for the final technical report (PDF). Each section lists what to cover.
Sections map to the Option 1 required components and the grading rubric
(technical rigor, empirical depth, originality/critical thinking, communication,
reproducibility). Fill with the team's own analysis; keep claims grounded in our
own data (`eval/results/`).

---

## 1. Introduction & justification of need
- The readback loop in ATC and why correctness matters (safety stakes).
- The specific gap: existing tools transcribe ATC audio; few *verify* that a
  readback is correct. What our system adds.
- Where it would be applied (controller decision support, training, QA review).

## 2. Field review
- ATC communication and readback safety (phraseology, mandatory readback items).
- NLP / ASR in aviation: trends, major players, existing solutions and their limits.
- Academic anchors (ACL Anthology, arXiv, IEEE, Google Scholar) + NASA ASRS.
- Restate the gap this project targets. _(See `field_review.md` for the long form.)_

## 3. System design
- The **hybrid** architecture: LLM extraction → deterministic comparison → verdict.
- The eight fields and why these (`callsign, altitude, heading, speed, frequency,
  squawk, runway, qnh`).
- The comparator and **error taxonomy** (`value_substitution`,
  `digit_transposition`, `omission`, `callsign_error`, `added_element`) — define
  each and the rule that detects it.
- Normalization decisions (units, spelled-out numbers, telephony, trailing zeros)
  and the "which items are mandatory to read back" policy — these are our own
  label-design choices and must be defensible in the Q&A.
- The two extractor backends (local `ollama`, hosted `hf`) and why.

## 4. Custom evaluation
- Test-set design: 50 labelled cases, how we chose them, coverage of every error
  category, and the hard cases we deliberately included.
- Metric definitions: precision / recall / F1 (positive = error present),
  false-alarm rate, verdict accuracy, per-category detection recall.
- **Results**: the table from `eval/results/metrics.md` + the confusion matrix.
  Interpret them — what the false-alarm rate means in a safety context.

## 5. Failure-mode analysis (5–10 cases)
- Walk through cases from `eval/results/failures.md`.
- For each: what went wrong, and a hypothesis about *why* (extraction error?
  normalization gap? genuine label ambiguity?).
- Patterns across failures and what they imply about the design.

## 6. Limitations & future directions
- Text-only POC; dependence on the extraction model; small test set.
- Future: speech-to-text front end (Whisper), phonetic/accent robustness,
  multi-model comparison, confidence scoring, controller-facing alerting.

## 7. Use of AI tools
- Summarize from `use_of_ai_tools.md`: what LLM tools were used and for what,
  and the explicit statement that substantive decisions were the team's own.

## 8. Conclusion
- What we built, what we learned, and why it matters — grounded in our own
  observations (this is what the rubric rewards most).

---

### Appendices / supporting artifacts
- Link to the repository and the design spec.
- The dataset (`eval/data/atc_readback_test_set.csv`) and the extraction prompt
  (`src/atc_verifier/extract/prompts/extract_fields.txt`).
- Full `predictions.csv` audit trail.
