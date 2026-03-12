# Strategy JSON Spec

本文件定义 Phase 1 支持的 DSL：version/meta/market/data/features/indicators/signals/risk/protections/optimization/validation/reporting。

- Rule 支持: `> >= < <= == != crosses_above crosses_below`。
- spot 下禁止 `can_short=true` 与 leverage。
- 外部特征必须包含 `candle_close_time` join key。
