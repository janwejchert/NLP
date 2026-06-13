# Field Review — ATC Communication, Readback Safety, and NLP (Outline)

> Stub for the report's field-review section. Replace bullets with prose and
> fill in the **References** section. Anchor every claim to a citation.

## 1. ATC Communication & Readback Safety
- Explain the readback/hear-back loop: controller issues an instruction, pilot reads it back, controller confirms — the readback is the safety check.
- Establish the risk: wrong, incomplete, or transposed readbacks (wrong altitude, transposed digits, omitted items) are a documented contributor to incidents. Cite NASA ASRS and any official incident/communication-error studies.

## 2. The Role of NLP / ASR in ATC
- Summarize how NLP and automatic speech recognition (ASR) are applied to ATC voice (transcription, command extraction, controller workload tools).
- Distinguish **transcription** (speech -> text) from **verification** (is the readback correct?) — the latter is this project's focus.

## 3. Existing Tools & Solutions
- Survey existing/representative systems and datasets (e.g. ATC speech corpora and transcription pipelines).
- Make the key observation explicit: existing tools mostly **transcribe** rather than **verify** readback correctness against the instruction.

## 4. Academic Anchors to Find
*Locate and cite concrete sources from each venue; replace this list with the actual citations in References.*
- ACL Anthology — NLP for speech/aviation, information extraction.
- arXiv — recent ASR/NLP for ATC, LLM extraction.
- Google Scholar — readback error / communication error studies.
- IEEE Xplore — ATC speech recognition, safety systems.
- NASA ASRS — incident reports on readback/hear-back errors.

## 5. The Gap This Project Fills
- State the gap: no lightweight, deterministic, field-by-field readback **verifier** with an explicit, defensible error taxonomy (value substitution, digit transposition, omission, callsign error, added element).
- Connect the gap to our design: an LLM extracts fields; deterministic Python makes every judgement, so results are auditable and reproducible.

## References
<!-- Populate with full citations (author, year, title, venue, URL/DOI). Use a consistent style. -->
- TODO
