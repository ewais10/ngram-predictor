import pytest
from src.data_prep.normalizer import Normalizer


def test_normalizer_basic():
    n = Normalizer()
    assert n.normalize("Hello ") == "hello"
