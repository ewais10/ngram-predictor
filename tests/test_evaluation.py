from src.evaluation.evaluator import Evaluator


def test_evaluator_placeholder():
    ev = Evaluator()
    assert ev.evaluate(None, []) == {}
