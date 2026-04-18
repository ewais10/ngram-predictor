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
        myDict = {}
        wordsCountDict = {}
        myDict["1gram"] = {}
        myDict["2gram"] = {}
        # myDict["chink"] = 5; word = "chink"
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
            wordsCountDict[word] = wordCount
            if wordProbability > 0:
                myDict["1gram"][word] = wordProbability

        n_1Grams = list(myDict["1gram"].keys())
        print(f"Total 1-grams with non-zero probability: {len(n_1Grams)}")
        
        for word in n_1Grams:
            # wordMatch = re.findall(fr'\b{word}\s\w+\b', sentTokensText); ## matches new lines also
            wordMatch = re.findall(fr'\b{word}[ \t]\w+\b', sentTokensText)
            wordMatchSet = set(wordMatch)
            # print(wordMatchSet)
            print(len(wordMatch))
            print(len(wordMatchSet))
            for twoGramWord in wordMatchSet:
            # for twoGramWord in {"holmes drew"}:
                print(f"Match: '{twoGramWord}'")
                # myDict["2gram"][twoGramWord] = {}
                twoGramWordCount = wordMatch.count(twoGramWord)
                matchProbability = twoGramWordCount / wordsCountDict[word]
                wordsCountDict[twoGramWord] = twoGramWordCount
                subWordMatches = re.findall(fr'\b{twoGramWord}[ \t]\w+\b', sentTokensText)
                if subWordMatches:
                    # print(f"Sub-matches for '{twoGramWord}': {len(subWordMatches)}")
                    subWordMatchSet = set(subWordMatches)
                    # print(subWordMatchSet)
                    # print(len(subWordMatchSet))
                    for subWordMatch in subWordMatchSet:
                        print(f"Sub-match: '{subWordMatch}'")
                        subWordCount = subWordMatches.count(subWordMatch)
                        wordsCountDict[subWordMatch] = subWordCount
                        subWordProb = subWordCount / twoGramWordCount
                        subWord = subWordMatch.split(" ")[-1]
                        # myDict.setdefault("2gram", {})[twoGramWord] = matchProbability
                        # myDict.setdefault("2gram", {})[subWordMatch] = subWordProb
                        # myDict["2gram"].setdefault(twoGramWord, {})
                        # myDict["2gram"][twoGramWord] = {} 
                        # myDict["2gram"][twoGramWord][subWord] = subWordProb
                        # myDict["2gram"][twoGramWord] = {subWord: subWordProb}
                        if twoGramWord not in myDict["2gram"]:
                            myDict["2gram"][twoGramWord] = {}
                        # if not isinstance(myDict.get("2gram", {}).get(twoGramWord), dict): 
                            # print("hello")
                            # myDict["2gram"][twoGramWord] = {}
                        myDict["2gram"][twoGramWord].update({subWord: subWordProb})

                        print(f"Sub-match count for '{subWordMatch}': {subWordCount}")

                    # subWordMatchCount = subWordMatch.count(subWordMatch)
                
                    


        with open('data.json', 'w') as fjson:
            json.dump(myDict, fjson, indent=4)
        # print(myDict[word])
        pass

if __name__ == "__main__":
    load_dotenv(dotenv_path="config/.env")  # Loads variables from .env
    trainTokens = os.getenv("TRAIN_TOKENS")
    unkThreshold = os.getenv("UNK_THRESHOLD")


    ngr = NGramModel();
    # demoVocab = ngr.build_vocab(unkThreshold=3, filename=trainTokens)
    # with open("tmpWordTokens.txt", "w", encoding="utf-8") as f:
    #     f.write(demoVocab)
    demoCounts = ngr.build_counts_and_probabilities(tokenFile=trainTokens, ngramOrder=4)
    # print(demoVocab)
    # with open("demofile.txt", "w", encoding="utf-8") as f:
    #     f.write(demoCounts)