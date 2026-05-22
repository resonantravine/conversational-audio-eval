"""Request structured conversational-audio evaluation notes from Gemini."""

from __future__ import annotations

import argparse
import json
import mimetypes
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

AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac"}


def api_key_from_env() -> str:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY or GOOGLE_API_KEY before running Gemini evaluation.")
    return api_key


def format_json_response(text: str) -> str:
    return json.dumps(json.loads(text or "{}"), indent=2)


def evaluate_text(review_text: str, model: str) -> str:
    client = genai.Client(api_key=api_key_from_env())
    response = client.models.generate_content(
        model=model,
        contents=PROMPT_TEMPLATE.format(review_text=review_text),
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return format_json_response(response.text or "{}")


def evaluate_audio(audio_path: Path, model: str, notes: str = "") -> str:
    mime_type = mimetypes.guess_type(audio_path.name)[0] or "audio/wav"
    client = genai.Client(api_key=api_key_from_env())
    prompt = PROMPT_TEMPLATE.format(
        review_text=(
            "Audio file attached. Focus on timing, pause structure, interruption risk, "
            "conversational pressure, and perceived listening. "
            f"Additional notes: {notes or 'none'}"
        )
    )
    response = client.models.generate_content(
        model=model,
        contents=[
            prompt,
            types.Part.from_bytes(data=audio_path.read_bytes(), mime_type=mime_type),
        ],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return format_json_response(response.text or "{}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--model", default="gemini-2.5-flash")
    parser.add_argument("--notes", default="", help="Optional context to include with an audio review.")
    args = parser.parse_args()

    if args.input_path.suffix.lower() in AUDIO_EXTENSIONS:
        print(evaluate_audio(args.input_path, args.model, notes=args.notes))
    else:
        review_text = args.input_path.read_text(encoding="utf-8")
        print(evaluate_text(review_text, args.model))


if __name__ == "__main__":
    main()
