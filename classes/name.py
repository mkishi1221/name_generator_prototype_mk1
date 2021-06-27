from classes.algorithm import Algorithm
from dataclasses import dataclass


@dataclass
class Name:
    """
    A simple helper class for Names adding a comparator for better readability
    """

    algorithm: Algorithm
    length: int
    name: str
    domain: str
    all_keywords: str
    keyword1: tuple[str]
    keyword2: tuple[str]

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
