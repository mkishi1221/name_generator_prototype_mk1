from dataclasses import dataclass
from json import JSONEncoder
from typing import Dict


@dataclass
class Keyword:
    """
    A simple helper class for keywords adding a comparator for better readability
    """

    word: str
    base_len: int
    base: str
    origin: str
    spacy_pos: str = ""
    wordsAPI_pos: str = ""
    lemma: str = ""
    occurence: int = 0

    def __eq__(self, o: object) -> bool:
        return self.base == o.base and self.wordsAPI_pos == o.wordsAPI_pos

    def __ne__(self, o: object) -> bool:
        return self.base != o.base and self.wordsAPI_pos != o.wordsAPI_pos

    def __hash__(self) -> int:
        return hash((self.word, self.base_len, self.base, self.origin))