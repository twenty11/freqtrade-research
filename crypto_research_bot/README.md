# Crypto Research Bot

基于 Freqtrade 的 OKX 策略 JSON 驱动回测研究系统（Phase 1 骨架版）。

## Quick start

```bash
cd crypto_research_bot
python -m venv .venv && source .venv/bin/activate
pip install -e '.[test]'
python -m app.cli init
python -m app.cli validate templates/trend_spot.json
python -m app.cli compile templates/trend_spot.json
```

## CLI

- `app init`
- `app validate <strategy.json>`
- `app compile <strategy.json>`
- `app backtest <strategy.json> --timerange ...`
- `app evaluate <strategy.json> --timerange ...`
- `app optimize <strategy.json> --timerange ...`
- `app report <run_id>`
- `app promote <strategy.json>`


## Frontend UI

```bash
PYTHONPATH=src python -m app.cli ui --host 127.0.0.1 --port 8088
```

浏览器打开 `http://127.0.0.1:8088`，通过页面按钮执行研究流程。详细说明见 `docs/frontend-usage.md`。
