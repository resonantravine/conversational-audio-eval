"""Generate a tiny synthetic audio clip for timing-demo smoke tests."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.io import wavfile


def tone(frequency: float, duration_sec: float, sr: int) -> np.ndarray:
    samples = int(sr * duration_sec)
    timeline = np.linspace(0, duration_sec, samples, endpoint=False)
    return 0.2 * np.sin(2 * np.pi * frequency * timeline)


def silence(duration_sec: float, sr: int) -> np.ndarray:
    return np.zeros(int(sr * duration_sec))


def generate_sample_audio(output_path: Path, sr: int = 22050) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    clip = np.concatenate(
        [
            tone(220, 0.40, sr),
            silence(0.35, sr),
            tone(330, 0.50, sr),
            silence(0.20, sr),
            tone(260, 0.35, sr),
        ]
    )
    wavfile.write(output_path, sr, clip.astype(np.float32))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/sample_audio/demo_timing.wav"),
        help="Path for the generated WAV file.",
    )
    args = parser.parse_args()

    generate_sample_audio(args.output)
    print(args.output)


if __name__ == "__main__":
    main()
