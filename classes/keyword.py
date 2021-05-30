from dataclasses import dataclass
from json import JSONEncoder
from typing import Dict


@dataclass
class Keyword():
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


class KeywordEncoder(JSONEncoder):
    def default(self, o: Keyword) -> Dict:
        if isinstance(o, set) or isinstance(o, list):
            return [{
                "word": w.word,
                "base_len": w.base_len,
                "base": w.base,
                "origin": w.origin,
                "spacy_pos": w.spacy_pos,
                "wordsAPI_pos": w.wordsAPI_pos,
                "lemma": w.lemma,
                "occurence": w.occurence
            } for w in o]
        elif isinstance(o, Keyword):
            return {
                "word": o.word,
                "base_len": o.base_len,
                "base": o.base,
                "origin": o.origin,
                "spacy_pos": o.spacy_pos,
                "wordsAPI_pos": o.wordsAPI_pos,
                "lemma": o.lemma,
                "occurence": o.occurence
            }
        else:
            return JSONEncoder.default(self, o)