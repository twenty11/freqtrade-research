from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_feature_file(path: str) -> pd.DataFrame:
    p = Path(path)
    if p.suffix == ".parquet":
        return pd.read_parquet(p)
    if p.suffix == ".csv":
        return pd.read_csv(p)
    raise ValueError(f"unsupported feature file: {path}")
