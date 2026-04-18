from importlib_metadata import files
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv
import os
import re

class Normalizer:
    """The Normalizer class handles loading, cleaning, tokenizing, and saving the corpus."""

    def normalize(self, text: str, remPunc: bool = True) -> str:
        """Normalize text to lower-case, remove punctuation (optionally), remove numbers and extra whitespaces."""
        if text is None:
            return ""
        text = Normalizer.lowercase(text)
        if remPunc: text = Normalizer.remove_punctuation(text)
        text = Normalizer.remove_numbers(text)
        text = Normalizer.remove_whitespace(text)        
        return text.strip().lower()

    @staticmethod
    def load(folder: str | Path,  encoding: str = "utf-8") -> Dict[str, str]:
        """Load all .txt files from a folder in a dictionary."""
        p = Path(folder)
        files = p.rglob("*.txt")
        texts: Dict[str, str] = {}
        for f in files: 
            if f.is_file:
                try:
                    texts[str(f)] = f.read_text(encoding=encoding)
                    # print(str(f)); ## For debugging
                except Exception as e:
                    print(f"Warning: failed to read {f}: {e}")
        return texts
    
    @staticmethod
    def strip_gutenberg(text: str):
        """Strip Gutenberg header and footer from text."""
        # reTextStart = re.search(r"\*\*\*\ START OF THE PROJECT GUTENBERG EBOOK.*\*\*\*", text)
        reTextStart = re.search(r"\*\*\*\ START OF THE PROJECT GUTENBERG EBOOK.*\n?.*\s\*\*\*", text)
        reTextEnd = re.search(r"\*\*\*\ END OF THE PROJECT GUTENBERG EBOOK.*\n?.*\s\*\*\*", text)

        gbStartIndex = reTextStart.span()[1] + 1
        gbEndIndex = reTextEnd.span()[0] - 1

        # print(f"Gutenberg header ends at index: {gbStartIndex} and footer starts at index: {gbEndIndex}"); ## For debugging
        text = text[gbStartIndex:gbEndIndex]
        return text;

    @staticmethod
    def lowercase(text: str):
        """Convert text to lowercase."""
        return text.lower();

    @staticmethod
    def remove_punctuation(text: str):
        """Remove punctuation from text."""
        text =re.sub(r'[-_]', '', text)
        return re.sub(r'[^\w\s]', '', text)

    @staticmethod
    def remove_numbers(text: str):
        """Remove numbers from text."""
        return re.sub(r'\d', '', text)

    @staticmethod
    def remove_whitespace(text: str):
        """Remove blank lines and extra spaces from text."""
        text = re.sub(r'\n\n+', '\n', text); # Remove blank lines
        text = re.sub(r'\n\s(\w)', r'\n\1', text); # Remove white spaces at the beginning of lines, preserve word char
        text = re.sub(r'[ \t][ \t]+', ' ', text); # Remove extra white spaces
        text = re.sub(r'\n\s', ' ', text); # Remove white spaces at the beginning of lines per each chapter
        return text

    def sentence_tokenize(self, text: str):
        """Split text into sentences based on punctuations and returns a list for each line"""
        newText = self.normalize(text, remPunc=False)
        sentencesList = re.split(r'([,.!?;])', newText)
        sentText="\n".join(sentencesList);
        sentText = self.normalize(sentText, remPunc=True)
        sentencesList = re.split(r'\n', sentText)
        return sentencesList
    
    def word_tokenize(sentence):
        """Split sentence words into tokens"""
        return re.split(r' ', sentence)
        # return " ".join(sentence)

    def save(sentences, filepath):
        """Write tokenized sentences to output file"""
        sentText="\n".join(sentences);
        with open(f"{filepath}", "w", encoding="utf-8") as f:
            f.write(sentText)
            print(f"Output saved in {filepath}")

     
    
if __name__ == "__main__":
    # Example usage
    load_dotenv(dotenv_path="config/.env")  # Loads variables from .env
    trainRawDir = os.getenv("TRAIN_RAW_DIR")
    trainTokens = os.getenv("TRAIN_TOKENS")

    print(trainRawDir)
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
    
    Normalizer.save(trainSntns, filepath=trainTokens)
    


    # print(dataN.keys())
    # y=(dataN['data\\raw\\train\\108.txt'])
    # newText = Normalizer.strip_gutenberg(y)
    # newText = Normalizer.lowercase(newText)
    # newText = Normalizer.remove_punctuation(newText)
    # newText = Normalizer.remove_numbers(newText)
    # newText = Normalizer.remove_whitespace(newText)
    # newText = Normalizer.remove_whitespace(newText)

    # normalizer = Normalizer()
    # newText = normalizer.normalize(newText, remPunc=False)
    # newText = normalizer.sentence_tokenize(newText)
    # Normalizer.save(newText, filepath="data/processed")
    # print(sentText)
    # print in out file
    # print(newText)
    # with open("demofile.txt", "w", encoding="utf-8") as f:
    #     f.write(newText)
    # print(newText[1:5])
    # print(Normalizer.word_tokenize(newText[1]))
    # print(Normalizer.word_tokenize(newText[0]))
    # with open("demofile.txt", "w", encoding="utf-8") as f:
    #     for item in newText:
    #         f.write(item)
    # print(newText)
    # print(Normalizer.__doc__)
    # # help(Normalizer.load)