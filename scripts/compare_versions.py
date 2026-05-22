"""Compare raw and designed conversational timing variants."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


METRICS = [
    "silence_ratio",
    "avg_pause_duration_sec",
    "max_pause_duration_sec",
    "interruption_count",
    "perceived_listening",
    "conversational_pressure",
]


def compare_versions(csv_path: Path, baseline: str, variant: str) -> pd.DataFrame:
    data = pd.read_csv(csv_path)
    grouped = data.groupby("version")[METRICS].mean(numeric_only=True)

    missing = {baseline, variant} - set(grouped.index)
    if missing:
        raise ValueError(f"Missing version(s): {', '.join(sorted(missing))}")

    comparison = pd.DataFrame(
        {
            "baseline": grouped.loc[baseline],
            "variant": grouped.loc[variant],
        }
    )
    comparison["delta"] = comparison["variant"] - comparison["baseline"]
    return comparison.reset_index(names="metric")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--baseline", default="raw")
    parser.add_argument("--variant", default="designed")
    args = parser.parse_args()

    comparison = compare_versions(args.csv_path, args.baseline, args.variant)
    print(comparison.to_csv(index=False))


if __name__ == "__main__":
    main()
