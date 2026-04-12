from src.inference.predictor import Predictor


def test_predictor_init():
    p = Predictor(model=None)
    assert p.predict([]) == []
