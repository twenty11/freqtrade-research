# Frontend Usage

项目提供了一个轻量本地前端页面，用于简化 CLI 操作。

## 启动

```bash
cd crypto_research_bot
PYTHONPATH=src python -m app.cli ui --host 127.0.0.1 --port 8088
```

打开浏览器访问：`http://127.0.0.1:8088`

## 页面能力

- 填写 `strategy.json` 路径
- 可选填写 `timerange`
- 可配置 `optimize` 的 `epochs`
- 一键触发：`validate / compile / backtest / evaluate / optimize / promote`
- 页面展示命令、返回码、stdout/stderr

## 注意事项

- 前端本质是本地 CLI 包装，不依赖外部服务。
- `backtest/evaluate/optimize` 仍依赖本地已安装的 Freqtrade 与数据。
- 如果策略路径无效，页面会返回结构化错误信息。
