import os
from typing import List
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data_prep.normalizer import Normalizer
from src.model.ngram_model import NGramModel


class Predictor:
    """Predictor wrapper around an n-gram model."""

    def __init__(self, model: NGramModel, normalizer: Normalizer):
        self.model = model
        self.normalizer = normalizer
    
    def map_oov(self, context: str) -> str:
        """Map out-of-vocabulary tokens to <UNK>."""
        contextList = context.split(" ")
        ##########################################################
        ## Checking if the context words are out of vocab
        for word in contextList:
            if word not in self.model.wordTokens:
                # print(f"Context word '{word}' is out of vocabulary, replacing with <UNK>")
                contextList[contextList.index(word)] = "<UNK>"
        return " ".join(contextList)

    def normalize(self, text: str) -> str:
        """Normalize input text using the normalizer."""
        newContext=self.normalizer.normalize(text)
        contextList = newContext.split(" ")
        ngramMaxWght = len(self.model.myDict.keys());
        if len(contextList) > ngramMaxWght:
            contextList = contextList[-ngramMaxWght:]
        return " ".join(contextList)
    
    def predict_next(self, text: List[str], topK: int = 3) -> List[str]:
        """Return up to `topK` next-token predictions."""
        context = self.normalize(text=text)
        context = self.map_oov(context)
        probWords = self.model.lookup(context=context, topK=topK)
        return list(probWords.keys())

if __name__ == "__main__":
        print("Hello from predictor!")
        # Load the tokenized sentences
        load_dotenv(dotenv_path="config/.env")  # Loads variables from .env
        trainTokens = os.getenv("TRAIN_TOKENS")
        unkThreshold = int(os.getenv("UNK_THRESHOLD"))
        modelFile = os.getenv("MODELF")
        vocabFile = os.getenv("VOCAB")
        ngramOrder = int(os.getenv("NGRAM_ORDER"))
        topK = int(os.getenv("TOP_K"))
        # Example usage
        normalizer = Normalizer()
        model = NGramModel()
        model.load(model_path=modelFile, vocab_path=vocabFile)
        predictor = Predictor(model=model, normalizer=normalizer)
        context = "the"
        newContext = predictor.map_oov(context)
        print(f"Mapped context: {newContext}")
        newContext = predictor.normalize(text=context)
        print(f"Normalized context: {newContext}")
        predict_next = predictor.predict_next(text=context, topK=topK)
        print(f"Predicted next tokens: {predict_next}")
        # predictions = predictor.predict(context, k=5)
        # print(predictions)