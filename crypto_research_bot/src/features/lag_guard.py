from __future__ import annotations

import pandas as pd


def assert_no_future_feature(df: pd.DataFrame, ts_col: str = "candle_close_time", feat_ts_col: str = "feature_time") -> None:
    if feat_ts_col not in df.columns:
        return
    base_t = pd.to_datetime(df[ts_col])
    feat_t = pd.to_datetime(df[feat_ts_col])
    if (feat_t > base_t).any():
        raise ValueError("future feature timestamp detected")
