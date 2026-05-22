"""Estimate simple conversational timing metrics from an audio file."""

from __future__ import annotations

import argparse
from pathlib import Path

import librosa
import numpy as np


def analyze_timing(path: Path, top_db: float = 30.0) -> dict[str, float]:
    y, sr = librosa.load(path, sr=None, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    intervals = librosa.effects.split(y, top_db=top_db)
    voiced_duration = sum((end - start) / sr for start, end in intervals)
    silence_duration = max(duration - voiced_duration, 0.0)

    pauses = []
    for previous, current in zip(intervals, intervals[1:]):
        gap = (current[0] - previous[1]) / sr
        if gap > 0:
            pauses.append(gap)

    pause_array = np.array(pauses, dtype=float)
    return {
        "duration_sec": round(duration, 3),
        "silence_ratio": round(silence_duration / duration, 4) if duration else 0.0,
        "avg_pause_duration_sec": round(float(pause_array.mean()), 3) if pauses else 0.0,
        "max_pause_duration_sec": round(float(pause_array.max()), 3) if pauses else 0.0,
        "pause_count": float(len(pauses)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio_path", type=Path)
    parser.add_argument("--top-db", type=float, default=30.0)
    args = parser.parse_args()

    metrics = analyze_timing(args.audio_path, top_db=args.top_db)
    for key, value in metrics.items():
        print(f"{key},{value}")


if __name__ == "__main__":
    main()
