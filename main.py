import argparse
import os

from dotenv import load_dotenv
from src.model.ngram_model import NGramModel
from pathlib import Path
from typing import Dict
from src.data_prep.normalizer import Normalizer

def main():
    parser = argparse.ArgumentParser(description="N-gram predictor CLI")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--step", type=str,  default="default", help="The step to run")

    # Load the tokenized sentences
    load_dotenv(dotenv_path="config/.env")  # Loads variables from .env
    trainTokens = os.getenv("TRAIN_TOKENS")
    unkThreshold = int(os.getenv("UNK_THRESHOLD"))
    modelFile = os.getenv("MODELF")
    vocabFile = os.getenv("VOCAB")
    ngramOrder = int(os.getenv("NGRAM_ORDER"))

    # print(type(unkThreshold))
    args = parser.parse_args()

    print("Welcome to the N-gram Predictor!")
    if args.version:
        print("ngram-predictor 0.1")
    if args.step == "default":
        print("Hello")
    if args.step == "dataprep":
        print("Running data preparation...")
        # Load and normalize the corpus
        load_dotenv(dotenv_path="config/.env")  # Loads variables from .env
        trainRawDir = os.getenv("TRAIN_RAW_DIR")
        trainTokens = os.getenv("TRAIN_TOKENS")
        # print(trainRawDir)
        normalizer = Normalizer(); # Normalizer Instance
        dataN = Normalizer.load(trainRawDir); # read library
        print(f"Loaded {len(dataN)} files.")
        trainSntns = list()
        
        for bookPath in dataN:
            bookContent=(dataN[bookPath])
            print(f"Loaded Book {bookPath} with {len(bookContent)} chars.")
            newText = Normalizer.strip_gutenberg(bookContent)
            newText = normalizer.normalize(newText, remPunc=False)
            bookTokenSntns = normalizer.sentence_tokenize(newText)
            trainSntns.extend(bookTokenSntns)

        trainSntns = trainSntns[100:201] # for testing purposes, remove this line for full dataset
        Normalizer.save(trainSntns, filepath=trainTokens)
    
    if args.step == "model":
        print("Running model training...")
        ngr = NGramModel();
        demoVocab = ngr.build_vocab(unkThreshold=unkThreshold, filename=trainTokens)
        ngr.save_vocab(vocabFile)
        demoCounts = ngr.build_counts_and_probabilities(tokenFile=trainTokens, ngramOrder=ngramOrder)
        ngr.save_model(modelFile)
        print("Model trained successfully!")
        
if __name__ == "__main__":
    main()
