"""Request structured conversational-audio evaluation notes from Gemini."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from google import genai
from google.genai import types


PROMPT_TEMPLATE = """\
You are reviewing a conversational AI voice interaction.

Return valid JSON with this shape:
{{
  "timing_observations": ["..."],
  "perceived_listening": "...",
  "interruption_risk": "...",
  "conversational_pressure": "...",
  "likely_reviewer_disagreement": "...",
  "limitations": ["..."]
}}

Use exploratory, limitation-aware language. Do not overstate confidence.

Review material:
{review_text}
"""


def evaluate_text(review_text: str, model: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY or GOOGLE_API_KEY before running Gemini evaluation.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=PROMPT_TEMPLATE.format(review_text=review_text),
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    text = response.text or "{}"
    return json.dumps(json.loads(text), indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--model", default="gemini-2.5-flash")
    args = parser.parse_args()

    review_text = args.input_path.read_text(encoding="utf-8")
    print(evaluate_text(review_text, args.model))


if __name__ == "__main__":
    main()
