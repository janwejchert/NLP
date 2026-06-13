# Executive Summary — ATC Readback Verifier

> One-page, **non-technical** summary for a general reader. Target ~250-350 words.
> Fill in the bracketed placeholders; remove this note before submitting.

## The Problem
In air traffic control, a controller gives an instruction (for example, a new
altitude or heading) and the pilot repeats it back to confirm they heard it
correctly. When that repeat-back is wrong, incomplete, or has digits in the
wrong order, it can go unnoticed — and such miscommunications are a known
contributor to aviation safety incidents [cite NASA ASRS / source]. Catching
these errors quickly matters.

## What We Built
We built **[ATC Readback Verifier]**, a simple web app where a user types in the
controller's instruction and the pilot's readback. The system reads both
messages, breaks each into standard pieces of information (such as the
aircraft's callsign, altitude, heading, and runway), and compares them
side by side. It then returns a clear verdict: **MATCH** when the readback is
correct, or **DISCREPANCY** with a plain-language list of exactly what is wrong
(for example, a wrong altitude or a transposed runway number).

A useful design choice: an AI language model is used only to pull the
information out of the text. All of the actual decisions about what counts as
correct are made by transparent, rule-based logic we wrote ourselves, so the
results are predictable and explainable.

## What We Found
On a hand-built test set of **50 example exchanges**, the tool [headline result:
e.g. correctly flagged X% of erroneous readbacks while raising few false alarms
— insert numbers from `eval/results/metrics.md`]. [Add one sentence on the most
common type of error it caught or struggled with.]

## Why It Matters
The tool shows that a lightweight, explainable check could help reinforce the
readback safety step, [and/or serve as a training aid]. Because every decision
is rule-based, its reasoning can be inspected and trusted.

## Limitations
This is an early proof-of-concept. It works on **typed text only** — it does not
yet process live audio — and was tested on a small, hand-written set of examples
[note any other limitation]. Live speech-to-text is a clear next step.
