from __future__ import annotations

import pandas as pd


def merge_feature(base: pd.DataFrame, feat: pd.DataFrame, on: list[str], fill_value: float | int | None = None) -> pd.DataFrame:
    out = base.merge(feat, on=on, how="left")
    if fill_value is not None:
        return out.fillna(fill_value)
    return out
