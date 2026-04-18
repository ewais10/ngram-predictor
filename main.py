import argparse
import os

from dotenv import load_dotenv
from pathlib import Path
from typing import Dict
from src.data_prep.normalizer import Normalizer
from src.model.ngram_model import NGramModel
from src.inference.predictor import Predictor


def dataprep(trainRawDir: str, trainTokens: str):
    print("Running data preparation...")
    # normalize the corpus
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
    pass

def model(unkThreshold: int, modelFile: str, vocabFile: str, ngramOrder: int, trainTokens: str):
    # print("Running model training...")
    ngr = NGramModel();
    demoVocab = ngr.build_vocab(unkThreshold=unkThreshold, filename=trainTokens)
    ngr.save_vocab(vocabFile)
    demoCounts = ngr.build_counts_and_probabilities(tokenFile=trainTokens, ngramOrder=ngramOrder)
    ngr.save_model(modelFile)
    # print("Model trained successfully!")


def inference(text: str, modelFile: str, vocabFile: str, topK: int):
    # print("Running prediction...")
    # Example usage
    normalizer = Normalizer()
    model = NGramModel()
    model.load(model_path=modelFile, vocab_path=vocabFile)
    predictor = Predictor(model=model, normalizer=normalizer)
    user_choice = input("Enter a command (start/stop/exit): ").strip().lower()
    while user_choice not in ["exit", "quit"]:        
        print(f"User command: {user_choice}")
        predictions = predictor.predict_next(text=user_choice, topK=topK)
        # print(f"Predictions for '{text}': {predictions}")
        print(f"{predictions}")
        user_choice = input("Enter a command (start/stop/exit): ").strip().lower()

def main():
    parser = argparse.ArgumentParser(description="N-gram predictor CLI")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--step", type=str,  default="dataprep", help="The step to run")

    # Load the tokenized sentences
    load_dotenv(dotenv_path="config/.env")  # Loads variables from .env
    trainTokens = os.getenv("TRAIN_TOKENS")
    unkThreshold = int(os.getenv("UNK_THRESHOLD"))
    modelFile = os.getenv("MODELF")
    vocabFile = os.getenv("VOCAB")
    ngramOrder = int(os.getenv("NGRAM_ORDER"))
    topK = int(os.getenv("TOP_K"))
    
    # print(type(unkThreshold))
    args = parser.parse_args()


    print("Welcome to the N-gram Predictor!")
    if args.version:
        print("ngram-predictor 0.1")
    if args.step == "default":
        print("Hello")
    
    # Define available steps with their arguments
    trainRawDir = os.getenv("TRAIN_RAW_DIR")
    steps = {
        "dataprep": (dataprep, {"trainRawDir": trainRawDir, "trainTokens": trainTokens}),
        "model": (model, {"unkThreshold": unkThreshold, "modelFile": modelFile, "vocabFile": vocabFile, "ngramOrder": ngramOrder, "trainTokens": trainTokens}),
        "inference": (inference, {"text": "the", "modelFile": modelFile, "vocabFile": vocabFile, "topK": topK})
    }

    # Logic for "all" vs specific step
    if args.step == "all":
        print("Running ALL steps...")
        for name, (func, kwargs) in steps.items():
            func(**kwargs)
    else:
        func, kwargs = steps[args.step]
        func(**kwargs)
        
if __name__ == "__main__":
    main()
