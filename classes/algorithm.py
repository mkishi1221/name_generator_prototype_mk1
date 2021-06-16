from dataclasses import dataclass
from json import JSONEncoder
from typing import Dict


@dataclass
class Algorithm:
    """
    A simple helper class for keywords adding a comparator for better readability
    """

    keyword_1: str
    keyword_2: int
    joint: str

    def __eq__(self, o: object) -> bool:
        return self.keyword_1 == o.keyword_1 and self.keyword_2 == o.keyword_2 and self.joint == o.joint

    def __ne__(self, o: object) -> bool:
        return self.keyword_1 != o.keyword_1 and self.keyword_2 != o.keyword_2 and self.joint != o.joint

    def __hash__(self) -> int:
        return hash((self.keyword_1, self.keyword_2, self.joint))


class KeywordEncoder(JSONEncoder):
    def default(self, o: Algorithm) -> Dict:
        if isinstance(o, set) or isinstance(o, list):
            return [
                {
                    "keyword_1": w.keyword_1,
                    "keyword_2": w.keyword_2,
                    "joint": w.joint,
                }
                for w in o
            ]
        elif isinstance(o, Algorithm):
            return {
                "keyword_1": o.keyword_1,
                "keyword_2": o.keyword_2,
                "joint": o.joint,
            }
        else:
            return JSONEncoder.default(self, o)
