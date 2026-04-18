from collections import defaultdict
from typing import List
from dotenv import load_dotenv
import os
import re
# import Normalizer

class NGramModel:
    """building, storing, and exposing n-gram probability tables and backoff lookup across all orders from 1 up to NGRAM_ORDER"""

    def __init__(self, n: int = 3):
        self.n = n
        self.counts = defaultdict(int)

    def train(self, tokens: List[str]):
        """Train on a sequence of tokens (placeholder)."""
        if not tokens:
            return
        # placeholder: count n-grams
        for i in range(len(tokens) - self.n + 1):
            gram = tuple(tokens[i : i + self.n])
            self.counts[gram] += 1

    def build_vocab(self, unkThreshold=3, filename="hello.txt", encoding="utf-8"):
        """collect all unique words; replace any word appearing fewer than UNK_THRESHOLD times with UNK"""
        with open(filename, "r") as file:
            # if file.is_file():
            #     print(f"Building vocab from {filename} with UNK threshold {unkThreshold}...")
            # sentTokens = file.read_text(encoding=encoding)
            sentTokensList = file.readlines(); ## list
        sentTokensText = "".join(sentTokensList); ## string
        wordTokens = list();
        for sentence in sentTokensList:
            # line.strip()
            wordTokens.extend(re.split(r' ', sentence.strip())); ## strip used to remove \n
        print(f"Total tokens: {len(wordTokens)}")
        wordTokensSet = set(wordTokens)
        print(f"Unique tokens: {len(wordTokensSet)}")
        line = 0
        # wordTokensSet = {"unite"}
        newWordTokensSet = set()
        for word in wordTokensSet:
            # print(f"Token: '{word}' Count: {wordTokens.count(word)} Line: {line}")
            line = line + 1
            if line % 1000 == 0: print(f"Processed {line} unique tokens out of {len(wordTokensSet)}...")
            # if line == 1000: break; ## limit to 1000 unique tokens for demo
            if wordTokens.count(word) >= unkThreshold:
                newWordTokensSet.add(word)
                # print(f"Token: '{word}' Count: {wordTokens.count(word)} replaced with UNK")
                # wordTokensSet.remove(word)
                # wordTokensSet.add("UNK")
            else:
                newWordTokensSet.add("UNK")
        # wordTokensSet = set(wordTokens)
        newWordTokensText = "\n".join(newWordTokensSet)
        return newWordTokensText
        # print(sentTokens)
    

if __name__ == "__main__":
    load_dotenv(dotenv_path="config/.env")  # Loads variables from .env
    trainTokens = os.getenv("TRAIN_TOKENS")
    unkThreshold = os.getenv("UNK_THRESHOLD")


    ngr = NGramModel();
    demoVocab = ngr.build_vocab(unkThreshold=3, filename=trainTokens)
    # print(demoVocab)
    with open("demofile.txt", "w", encoding="utf-8") as f:
        f.write(demoVocab)