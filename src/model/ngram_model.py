from collections import defaultdict
from typing import List
from dotenv import load_dotenv
import os
import re
import json

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
            # print(word)
            if wordTokens.count(word) >= unkThreshold:
                newWordTokensSet.add(word)
                # print(f"Token: '{word}' Count: {wordTokens.count(word)} replaced with UNK")
                # wordTokensSet.remove(word)
                # wordTokensSet.add("UNK")
            else:
                newWordTokensSet.add("UNK")
        # wordTokensSet = set(wordTokens)
        newWordTokensText = "\n".join(newWordTokensSet)
        self.wordTokens = newWordTokensSet
        return newWordTokensText
        # print(sentTokens)
    
    def build_counts_and_probabilities(self, tokenFile="hello.txt", encoding="utf-8", ngramOrder=4, wordTokenFile="tmpWordTokens.txt"):
        """build n-gram counts and probabilities."""
        ##################################################
        with open(wordTokenFile, "r", encoding="utf-8") as f:
            wordTokensText = f.readlines()    
        wordTokensText = "".join(wordTokensText); ## string
        wordTokensText = re.sub(r'\n', ' ', wordTokensText)
        self.wordTokens = wordTokensText.split(" ")
        ###################################################
        with open(tokenFile, "r", encoding="utf-8") as myTokenFile:
            sentTokens = myTokenFile.readlines(); ## list
        sentTokensText = "".join(sentTokens); ## string
        ###################################################


        print(len(self.wordTokens))
        totalWordsCount = len(re.findall(fr'\b\w+\b', sentTokensText))
        # print(f"Total words count: {totalWordsCount}")
        self.myDict = {}
        self.wordsCountDict = {}
        self.myDict["1gram"] = {}
        # self.myDict["2gram"] = {}
        # self.myDict["chink"] = 5; word = "chink"
        line = 0;
        self.wordTokens = ["the", "and", "watson", "sherlock", "holmes", "unite", "UNK"]
        self.wordTokens = ["holmes", "and"]
        self.wordTokens = ["holmes"]

        for word in self.wordTokens:
            # wordCount = sentTokensText.count(word)
            if line % 100 == 0: print(f"Processed {line} unique tokens out of {len(self.wordTokens)}...");
            if line == 500: break; ## limit to 1000 unique tokens for demo
            line = line + 1
            wordCount = len(re.findall(fr'\b{word}\b', sentTokensText))
            # print(wordCount)
            wordProbability = wordCount / totalWordsCount
            self.wordsCountDict[word] = wordCount
            if wordProbability > 0:
                self.myDict["1gram"][word] = wordProbability


# for word, prob in self.myDict["1gram"].items():
        gramIndex = 2
        n_1Grams = list(self.myDict["1gram"].keys())
        print(f"Total 1-grams with non-zero probability: {len(n_1Grams)}")


        ## build 2-grams and their probabilities
        for gramIndex in range(2, ngramOrder + 1):
            n_1Grams = list(self.myDict[f"{gramIndex-1}gram"].keys())
            if f"{gramIndex}gram" not in self.myDict:
                self.myDict[f"{gramIndex}gram"] = {}
            print(f"Processing the {gramIndex}-gram")
            lineWord = 0;
            for word in n_1Grams:
                if lineWord % 100 == 0: print(f"Processing the {gramIndex}-gram for word: '{word}' processed {lineWord} out of {len(n_1Grams)} unique {gramIndex-1}-grams ...")
                lineWord = lineWord + 1
                # wordMatch = re.findall(fr'\b{word}\s\w+\b', sentTokensText); ## matches new lines also
                wordMatch = re.findall(fr'\b{word}[ \t]\w+\b', sentTokensText)
                wordMatchSet = set(wordMatch)
                # print(wordMatchSet)
                # print(len(wordMatch))
                # print(len(wordMatchSet))
                lineGram = 0
                for twoGramWord in wordMatchSet:
                # for twoGramWord in {"holmes drew"}:
                    if lineGram % 100 == 0: print(f"Processed {gramIndex}-gram for {lineGram} matches out of {len(wordMatchSet)}...");
                    lineGram = lineGram + 1
                    # print(f"Processing 2-gram: '{twoGramWord}'")
                    # if line % 100 == 0: print(f"Processed {line} unique tokens out of {len(self.wordTokens)}...");
                    # self.myDict["2gram"][twoGramWord] = {}
                    twoGramWordCount = wordMatch.count(twoGramWord)
                    matchProbability = twoGramWordCount / self.wordsCountDict[word]
                    self.wordsCountDict[twoGramWord] = twoGramWordCount
                    subWordMatches = re.findall(fr'\b{twoGramWord}[ \t]\w+\b', sentTokensText)
                    if subWordMatches:
                        # print(f"Sub-matches for '{twoGramWord}': {len(subWordMatches)}")
                        subWordMatchSet = set(subWordMatches)
                        # print(subWordMatchSet)
                        # print(len(subWordMatchSet))
                        for subWordMatch in subWordMatchSet:
                            # print(f"Sub-match: '{subWordMatch}'")
                            subWordCount = subWordMatches.count(subWordMatch)
                            self.wordsCountDict[subWordMatch] = subWordCount
                            subWordProb = subWordCount / twoGramWordCount
                            subWord = subWordMatch.split(" ")[-1]
                            # self.myDict.setdefault("2gram", {})[twoGramWord] = matchProbability
                            # self.myDict.setdefault("2gram", {})[subWordMatch] = subWordProb
                            # self.myDict["2gram"].setdefault(twoGramWord, {})
                            # self.myDict["2gram"][twoGramWord] = {} 
                            # self.myDict["2gram"][twoGramWord][subWord] = subWordProb
                            # self.myDict["2gram"][twoGramWord] = {subWord: subWordProb}
                            if twoGramWord not in self.myDict[f"{gramIndex}gram"]:
                                self.myDict[f"{gramIndex}gram"][twoGramWord] = {}
                            # if not isinstance(self.myDict.get("{gramIndex}gram", {}).get(twoGramWord), dict): 
                                # print("hello")
                                # self.myDict["{gramIndex}gram"][twoGramWord] = {}
                            self.myDict[f"{gramIndex}gram"][twoGramWord].update({subWord: subWordProb})
                            # print(f"Sub-match count for '{subWordMatch}': {subWordCount}")

        with open('data.json', 'w') as fjson:
            json.dump(self.myDict, fjson, indent=4)
        # print(self.myDict[word])
        pass

    def lookup(self, context: str, ndict) -> dict[str, float]:
        """Given a context (list of preceding words), return a dictionary of next-word probabilities."""
        contextList = context.split(" ")
        # for word in contextList:
            # if word not in 
        print(contextList)
        # placeholder: return dummy probabilities
        return {"the": 0.5, "and": 0.3, "UNK": 0.2}

    def save_vocab(self, vocab_path):
        """Save the vocabulary to a file."""
        with open(vocab_path, "w", encoding="utf-8") as f:
            json.dump(list(self.wordTokens), f)
        print(f"Vocabulary saved to {vocab_path}")
        pass

    def save_model(self, model_path):
        """Save the model to a file."""
        # self.myDict = {}
        with open(model_path, "w", encoding="utf-8") as f:
            json.dump(self.myDict, f, indent=4)
        print(f"model saved to {model_path}")
        pass

    def load(self, vocab_path, model_path):
        """Load the vocab and model datasets."""

        with open(vocab_path, 'r', encoding='utf-8') as vocabFile:
            self.wordTokens = set(json.load(vocabFile))
            # self.wordTokens = set(newWordTokensText)
            # print(self.wordTokens)
            # print(len(self.wordTokens))
        print(f"vocabulary loaded from {vocab_path}")

        with open(model_path, 'r', encoding='utf-8') as modelFile:
            self.myDict = json.load(modelFile)
            # self.wordTokens = set(newWordTokensText)
            # print(self.myDict.keys())
            # print(len(self.myDict.keys()))
        print(f"dictionary model loaded from {model_path}")

        pass

if __name__ == "__main__":
    load_dotenv(dotenv_path="config/.env")  # Loads variables from .env
    trainTokens = os.getenv("TRAIN_TOKENS")
    unkThreshold = os.getenv("UNK_THRESHOLD")

    modelFile = os.getenv("MODELF")
    # print(modelFile)
    vocabFile = os.getenv("VOCAB")
    # print(vocabFile)

    ngr = NGramModel();
    # demoVocab = ngr.build_vocab(unkThreshold=3, filename=trainTokens)
    # ngr.save_vocab(vocabFile)
    ngr.load(vocab_path=vocabFile, model_path=modelFile)

    # with open("tmpWordTokens.txt", "w", encoding="utf-8") as f:
    #     f.write(demoVocab)
    # demoCounts = ngr.build_counts_and_probabilities(tokenFile=trainTokens, ngramOrder=4)
    ngr.save_model(modelFile)

    # with open('data.json', 'r', encoding='utf-8') as file:
    #     data = json.load(file)
    # print(data["1gram"])
    # demoLookup = ngr.lookup(context="holmes is", ndict=data)
    # print(demoVocab)
    # with open("demofile.txt", "w", encoding="utf-8") as f:
    #     f.write(demoCounts)