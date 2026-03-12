from __future__ import annotations

import json
from pathlib import Path

import typer

from app.web import run_server
from compiler.strategy_compiler import compile_strategy
from domain.services.strategy_loader import load_strategy
from dsl.semantic_validator import validate_semantics
from dsl.validator import validate_schema
from evaluation.acceptance import check_acceptance
from evaluation.metrics import compute_basic_metrics
from evaluation.regime_split import run_regime_split
from evaluation.sensitivity import run_sensitivity
from evaluation.walk_forward import run_walk_forward
from freqtrade_adapter.analysis_runner import run_lookahead, run_recursive
from freqtrade_adapter.backtest_runner import run_backtest
from freqtrade_adapter.hyperopt_runner import run_hyperopt
from reporting.json_report import write_json_report
from reporting.manifest_writer import write_manifest
from reporting.markdown_report import write_summary
from utils.paths import run_dir
from utils.time import utc_now_id

app = typer.Typer(help="JSON-driven Freqtrade research CLI")


@app.command()
def init() -> None:
    for rel in ["data/reports", "data/manifests", "data/cache", "strategies"]:
        Path(rel).mkdir(parents=True, exist_ok=True)
    typer.echo("Initialized project folders.")


@app.command()
def validate(strategy_json: str) -> None:
    schema_errors = validate_schema(strategy_json, "src/dsl/schema/strategy.schema.json")
    spec = load_strategy(strategy_json)
    semantic_errors = validate_semantics(spec)
    if schema_errors or semantic_errors:
        for err in schema_errors + semantic_errors:
            typer.echo(f"ERROR: {err}")
        raise typer.Exit(code=1)
    typer.echo("Validation passed.")


@app.command()
def compile(strategy_json: str, out_dir: str = "build") -> None:
    spec = load_strategy(strategy_json)
    artifacts = compile_strategy(spec, out_dir)
    typer.echo(json.dumps(artifacts, ensure_ascii=False, indent=2))


@app.command()
def backtest(strategy_json: str, timerange: str = "") -> None:
    spec = load_strategy(strategy_json)
    artifacts = compile_strategy(spec, "build")
    result = run_backtest(artifacts["runtime"], artifacts["strategy"], timerange=timerange or None)
    typer.echo(result.stdout)
    if result.returncode != 0:
        typer.echo(result.stderr)
        raise typer.Exit(code=result.returncode)


@app.command()
def evaluate(strategy_json: str, timerange: str = "") -> None:
    spec = load_strategy(strategy_json)
    artifacts = compile_strategy(spec, "build")
    runid = utc_now_id()
    out = run_dir(runid)
    out.mkdir(parents=True, exist_ok=True)

    bt = run_backtest(artifacts["runtime"], artifacts["strategy"], timerange=timerange or None)
    look = run_lookahead(artifacts["runtime"], artifacts["strategy"])
    rec = run_recursive(artifacts["runtime"], artifacts["strategy"])

    metrics = compute_basic_metrics()
    walk = run_walk_forward(120, 30, 30)
    regime = run_regime_split()
    sensitivity = run_sensitivity()
    acceptance = check_acceptance(metrics, min_trades=spec.validation.min_trades, min_profit_factor=1.0)

    report = {
        "run_id": runid,
        "accepted": acceptance["passed"],
        "metrics": metrics,
        "lookahead_passed": look.returncode == 0,
        "recursive_passed": rec.returncode == 0,
    }
    write_summary(str(out / "summary.md"), report)
    write_json_report(str(out / "metrics.json"), metrics)
    write_json_report(str(out / "walk_forward.json"), walk)
    write_json_report(str(out / "regime_split.json"), regime)
    write_json_report(str(out / "sensitivity.json"), sensitivity)
    write_json_report(str(out / "lookahead.json"), {"returncode": look.returncode, "stdout": look.stdout, "stderr": look.stderr})
    write_json_report(str(out / "recursive.json"), {"returncode": rec.returncode, "stdout": rec.stdout, "stderr": rec.stderr})
    write_json_report(str(out / "backtest.json"), {"returncode": bt.returncode, "stdout": bt.stdout, "stderr": bt.stderr})
    write_manifest(str(out / "manifest.json"), strategy_json, artifacts["strategy"], {"runtime": artifacts["runtime"], "run_id": runid})

    typer.echo(f"evaluation finished: {out}")


@app.command()
def optimize(strategy_json: str, epochs: int = 20) -> None:
    spec = load_strategy(strategy_json)
    artifacts = compile_strategy(spec, "build")
    result = run_hyperopt(artifacts["runtime"], artifacts["strategy"], epochs)
    typer.echo(result.stdout)
    if result.returncode != 0:
        typer.echo(result.stderr)
        raise typer.Exit(code=result.returncode)


@app.command()
def report(run_id: str) -> None:
    path = Path("data/reports") / run_id / "summary.md"
    typer.echo(path.read_text(encoding="utf-8"))


@app.command()
def ui(host: str = "127.0.0.1", port: int = 8088) -> None:
    """Start local web UI for strategy research commands."""
    run_server(host=host, port=port)


@app.command()
def promote(strategy_json: str) -> None:
    spec = load_strategy(strategy_json)
    target = Path("data/manifests") / f"{spec.meta.get('strategy_id', 'unknown')}.candidate.json"
    target.write_text(json.dumps({"status": "candidate", "strategy": strategy_json}, ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"promoted: {target}")


if __name__ == "__main__":
    app()
