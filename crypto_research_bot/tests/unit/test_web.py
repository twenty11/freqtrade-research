from app.web import build_cli_command


def test_build_backtest_cmd_with_timerange():
    cmd = build_cli_command(
        {
            "action": "backtest",
            "strategy": "templates/trend_spot.json",
            "timerange": "20240101-20240301",
        }
    )
    assert cmd[-2:] == ["--timerange", "20240101-20240301"]


def test_build_optimize_cmd_with_epochs():
    cmd = build_cli_command(
        {
            "action": "optimize",
            "strategy": "templates/trend_spot.json",
            "epochs": 30,
        }
    )
    assert cmd[-2:] == ["--epochs", "30"]
