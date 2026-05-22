"""Compute Pearson correlations for exploratory timing metrics."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import pearsonr


DEFAULT_METRICS = [
    "silence_ratio",
    "avg_pause_duration_sec",
    "max_pause_duration_sec",
    "interruption_count",
    "conversational_pressure",
]


def correlation_analysis(csv_path: Path, target: str, metrics: list[str]) -> pd.DataFrame:
    data = pd.read_csv(csv_path)
    rows = []

    for metric in metrics:
        pair = data[[metric, target]].dropna()
        if len(pair) < 2:
            rows.append({"metric": metric, "target": target, "pearson_r": None, "p_value": None})
            continue

        r_value, p_value = pearsonr(pair[metric], pair[target])
        rows.append(
            {
                "metric": metric,
                "target": target,
                "pearson_r": round(float(r_value), 4),
                "p_value": round(float(p_value), 4),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--target", default="perceived_listening")
    parser.add_argument("--metrics", nargs="*", default=DEFAULT_METRICS)
    parser.add_argument("--output", type=Path, default=Path("correlations.csv"))
    args = parser.parse_args()

    results = correlation_analysis(args.csv_path, args.target, args.metrics)
    results.to_csv(args.output, index=False)
    print(results.to_csv(index=False))


if __name__ == "__main__":
    main()
