import argparse
from src.model.ngram_model import NGramModel
from pathlib import Path
from typing import Dict
from src.data_prep.normalizer import Normalizer

def main():
    parser = argparse.ArgumentParser(description="N-gram predictor CLI")
    parser.add_argument("--version", action="store_true", help="Show version")
    args = parser.parse_args()
    if args.version:
        print("ngram-predictor 0.1")


if __name__ == "__main__":
    main()
    x = Normalizer.load("data/raw/train")
    print(x.keys())
    # print(Normalizer.load.__doc__)
    help(Normalizer.load)