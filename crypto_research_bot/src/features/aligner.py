from __future__ import annotations

import pandas as pd


def align_with_lag(df: pd.DataFrame, lag_minutes: int) -> pd.DataFrame:
    out = df.copy()
    out["candle_close_time"] = pd.to_datetime(out["candle_close_time"]) + pd.Timedelta(minutes=lag_minutes)
    return out
