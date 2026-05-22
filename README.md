# Conversational Audio Evaluation

Lightweight evaluation tools and exploratory studies
for conversational timing, pause structure,
and perceived listening in AI voice systems.

Current focus:

* conversational timing
* pause engineering
* interruption behavior
* response pacing
* conversational pressure
* perceived listening

## Project Scope

This repo explores interaction-quality problems that are difficult to capture through traditional TTS metrics alone. It is an ongoing evaluation workflow for looking at how timing choices affect whether an AI voice system feels patient, attentive, rushed, or emotionally pressuring.

The work is intentionally lightweight and operational. It combines small-sample timing analysis, reviewer notes, structured failure annotation, and exploratory calibration across versions of the same interaction.

Focus areas:

* pause appropriateness
* interruption handling
* conversational pacing
* perceived listening
* emotional pressure

This is not a general speech ML research stack. It is a practical interaction-quality toolkit for conversational audio review, especially when the important question is not only what was said, but when the system entered, waited, held silence, or pressed forward.

## Repository Contents

* `scripts/analyze_timing.py`: estimates silence ratio and pause-duration summaries from an audio file.
* `scripts/compare_versions.py`: compares raw and designed timing metrics from a CSV.
* `scripts/gemini_eval.py`: sends reviewer-style prompts to Gemini and expects structured evaluation output.
* `scripts/correlation_analysis.py`: computes Pearson correlations across selected metric columns.
* `reports/`: short exploratory writeups from current timing demos.
* `examples/`: annotation and reviewer-disagreement examples.
* `data/sample_metrics.csv`: small calibration dataset for the starter scripts.

## Example Annotation

```csv
timestamp,failure,severity,note
00:12,premature interruption,medium,AI enters before hesitation resolves
00:31,semantic pause,low,pause follows punctuation only
```

## Example Reviewer Disagreement

Reviewer A:
felt calm and patient

Reviewer B:
felt emotionally excessive

Discussion:
difference may relate to tolerance for long silence

## Current Evaluation Coverage

* 2 evaluation demos
* 9 observed failures
* 11 reviewer vocabulary terms
* 6 conversational dimensions
* 2 open questions

## Current Limitations

* small sample size
* exploratory metrics
* limited reviewer pool
* not validated through large-scale user studies
* current focus is lightweight conversational evaluation

The current experiments indicate useful directions for review, but the findings should be treated as preliminary observations. The repo is built for small-sample calibration, reviewer vocabulary development, and iterative timing checks.

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Analyze one audio file:

```bash
python scripts/analyze_timing.py path/to/audio.wav
```

Run a local timing demo without bringing your own audio:

```bash
python scripts/generate_sample_audio.py
python scripts/analyze_timing.py data/sample_audio/demo_timing.wav
```

Compare timing variants:

```bash
python scripts/compare_versions.py data/sample_metrics.csv --baseline raw --variant designed
```

Run a correlation pass:

```bash
python scripts/correlation_analysis.py data/sample_metrics.csv --target perceived_listening --output correlations.csv
```

Run a Gemini-assisted structured review:

```bash
export GEMINI_API_KEY="..."
python scripts/gemini_eval.py examples/reviewer_disagreement.md
```

`GOOGLE_API_KEY` is also accepted for local setups that already use that variable name.

## Working Vocabulary

The reviewer vocabulary is expected to evolve. Current terms include patient, rushed, clipped, attentive, hovering, over-responsive, hesitant, calm, pressuring, performative, and grounded.

## Open Questions

* How much silence feels patient before it starts to feel withholding?
* Which interruption failures come from timing alone, and which depend on semantic context?
