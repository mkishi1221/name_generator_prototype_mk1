from dataclasses import dataclass
from json import JSONEncoder
from typing import Dict

@dataclass
class Names():
    """
    A simple helper class for Names adding a comparator for better readability
    """

    name: str
    domain: str
    algorithm: str
    keywords: str
    joint: str
    length: int

    def __eq__(self, o: object) -> bool:
        return self.name == o.name and self.keywords == o.keywords

    def __ne__(self, o: object) -> bool:
        return self.name != o.name and self.keywords != o.keywords

    def __hash__(self) -> int:
        return hash((self.name, self.domain, self.algorithm, self.keywords, self.joint, self.length))

class NameEncoder(JSONEncoder):
    def default(self, o: Names) -> Dict:
        if isinstance(o, set) or isinstance(o, list):
            return [{
                "name": w.name,
                "domain": w.domain,
                "algorithm": w.algorithm,
                "keywords": w.keywords,
                "joint": w.joint,
                "length": w.length
            } for w in o]
        elif isinstance(o, Names):
            return {
                "name": o.name,
                "domain": o.domain,
                "algorithm": o.algorithm,
                "keywords": o.keywords,
                "joint": o.joint,
                "length": o.length
            }
        else:
            return JSONEncoder.default(self, o)
