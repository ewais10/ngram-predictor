import argparse
from src.model.ngram_model import NGramModel


def main():
    parser = argparse.ArgumentParser(description="N-gram predictor CLI")
    parser.add_argument("--version", action="store_true", help="Show version")
    args = parser.parse_args()
    if args.version:
        print("ngram-predictor 0.1")


if __name__ == "__main__":
    main()
