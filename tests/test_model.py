from src.model.ngram_model import NGramModel


def test_ngram_init():
    m = NGramModel(2)
    assert m.n == 2
