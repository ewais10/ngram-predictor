from src.ui.app import PredictorUI


def test_ui_runs(capsys):
    ui = PredictorUI()
    ui.run()
    captured = capsys.readouterr()
    assert "PredictorUI running" in captured.out
