from dataclasses import dataclass
from json import JSONEncoder
from typing import Dict


@dataclass
class Keyword:
    """
    A simple helper class for keywords adding a comparator for better readability
    """

    word: str = ""
    keyword_len: int = 0
    keyword: str = ""
    origin: str =  ""
    spacy_pos: str = ""
    wordsAPI_pos: str = ""
    lemma: str = ""
    occurrence: int = 0

    def __eq__(self, o: object) -> bool:
        return self.keyword == o.keyword and self.wordsAPI_pos == o.wordsAPI_pos

    def __ne__(self, o: object) -> bool:
        return self.keyword != o.keyword and self.wordsAPI_pos != o.wordsAPI_pos

    def __hash__(self) -> int:
        return hash((self.word, self.keyword_len, self.keyword, self.origin))
