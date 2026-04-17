from importlib_metadata import files
from pathlib import Path
from typing import Dict
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
        reTextStart = re.search(r"\*\*\*\ START OF THE PROJECT GUTENBERG EBOOK.*\*\*\*", text)
        reTextEnd = re.search(r"\*\*\*\ END OF THE PROJECT GUTENBERG EBOOK.*\*\*\*", text)

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
        return re.sub(r'[^\w\s]', '', text)

    @staticmethod
    def remove_numbers(text: str):
        """Remove numbers from text."""
        return re.sub(r'\d', '', text)

    @staticmethod
    def remove_whitespace(text: str):
        """Remove blank lines and extra spaces from text."""
        text = re.sub(r'\n\n+', '\n', text); # Remove blank lines
        text = re.sub(r'[ \t][ \t]+', ' ', text); # Remove extra white spaces
        text = re.sub(r'\n\s', '\n', text); # Remove white spaces at the beginning of lines
        return text

    @staticmethod
    def sentence_tokenize(text: str):
        """Split text into sentences based on punctuations"""
        return re.split(r'([,.!?;])', text)
    
if __name__ == "__main__":
    # Example usage
    dataN = Normalizer.load("data/raw/train")
    print(f"Loaded {len(dataN)} files.")
    # print(dataN.keys())
    y=(dataN['data\\raw\\train\\108.txt'])
    newText = Normalizer.strip_gutenberg(y)
    # newText = Normalizer.lowercase(newText)
    # newText = Normalizer.remove_punctuation(newText)
    # newText = Normalizer.remove_numbers(newText)
    # newText = Normalizer.remove_whitespace(newText)
    # newText = Normalizer.remove_whitespace(newText)
    # newText = Normalizer.sentence_tokenize(newText)

    normalizer = Normalizer()
    newText = normalizer.normalize(newText, remPunc=False)
    # print in out file
    x = "hello"
    # print(newText)
    with open("demofile.txt", "w", encoding="utf-8") as f:
        f.write(newText)
    # with open("demofile.txt", "w", encoding="utf-8") as f:
    #     for item in newText:
    #         f.write(item)
    # print(newText)
    # print(Normalizer.__doc__)
    # # help(Normalizer.load)