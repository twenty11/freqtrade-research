# CLI Usage

- `python -m app.cli init`
- `python -m app.cli validate <strategy.json>`
- `python -m app.cli compile <strategy.json> --out-dir build`
- `python -m app.cli backtest <strategy.json> --timerange 20240101-20240301`
- `python -m app.cli evaluate <strategy.json> --timerange ...`
- `python -m app.cli optimize <strategy.json> --epochs 20`
- `python -m app.cli report <run_id>`
- `python -m app.cli promote <strategy.json>`

- `python -m app.cli ui --host 127.0.0.1 --port 8088`
