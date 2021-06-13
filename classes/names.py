from dataclasses import dataclass
from json import JSONEncoder
from typing import Dict


@dataclass
class Names:
    """
    A simple helper class for Names adding a comparator for better readability
    """

    length: int
    name: str
    domain: str
    algorithm: str
    joint: str
    all_keywords: str
    keyword1: str
    keyword2: str

    def __eq__(self, o: object) -> bool:
        return self.name == o.name and self.all_keywords == o.all_keywords

    def __ne__(self, o: object) -> bool:
        return self.name != o.name and self.all_keywords != o.all_keywords

    def __hash__(self) -> int:
        return hash(
            (
                self.length,
                self.name,
                self.domain,
                self.algorithm,
                self.joint,
                self.all_keywords,
                self.keyword1,
                self.keyword2,
            )
        )


class NameEncoder(JSONEncoder):
    def default(self, o: Names) -> Dict:
        if isinstance(o, set) or isinstance(o, list):
            return [
                {
                    "length": w.length,
                    "name": w.name,
                    "domain": w.domain,
                    "algorithm": w.algorithm,
                    "joint": w.joint,
                    "all_keywords": w.all_keywords,
                    "keyword1": w.keyword1,
                    "keyword2": w.keyword2,
                }
                for w in o
            ]
        elif isinstance(o, Names):
            return {
                "length": o.length,
                "name": o.name,
                "domain": o.domain,
                "algorithm": o.algorithm,
                "joint": o.joint,
                "all_keywords": o.all_keywords,
                "keyword1": o.keyword1,
                "keyword2": o.keyword2,
            }
        else:
            return JSONEncoder.default(self, o)
