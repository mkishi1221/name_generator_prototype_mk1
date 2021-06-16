from dataclasses import dataclass
from json import JSONEncoder
from typing import Dict


@dataclass
class Names:
    """
    A simple helper class for Names adding a comparator for better readability
    """

    algorithm: str
    length: int
    name: str
    domain: str
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
                self.algorithm,
                self.length,
                self.name,
                self.domain,
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
                    "algorithm": w.algorithm,
                    "length": w.length,
                    "name": w.name,
                    "domain": w.domain,
                    "all_keywords": w.all_keywords,
                    "keyword1": w.keyword1,
                    "keyword2": w.keyword2,
                }
                for w in o
            ]
        elif isinstance(o, Names):
            return {
                "algorithm": o.algorithm,
                "length": o.length,
                "name": o.name,
                "domain": o.domain,
                "all_keywords": o.all_keywords,
                "keyword1": o.keyword1,
                "keyword2": o.keyword2,
            }
        else:
            return JSONEncoder.default(self, o)
