"""Request structured conversational-audio evaluation notes from Gemini."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from google import genai


PROMPT_TEMPLATE = """\
You are reviewing a conversational AI voice interaction.

Return concise structured notes with these fields:
- timing_observations
- perceived_listening
- interruption_risk
- conversational_pressure
- likely_reviewer_disagreement
- limitations

Use exploratory, limitation-aware language. Do not overstate confidence.

Review material:
{review_text}
"""


def evaluate_text(review_text: str, model: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY before running Gemini evaluation.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=PROMPT_TEMPLATE.format(review_text=review_text),
    )
    return response.text or ""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--model", default="gemini-2.5-flash")
    args = parser.parse_args()

    review_text = args.input_path.read_text(encoding="utf-8")
    print(evaluate_text(review_text, args.model))


if __name__ == "__main__":
    main()
