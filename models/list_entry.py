from dataclasses import dataclass


@dataclass
class ListEntry:
    """
    A generic dataclass for either black or white list entries
    """

    keyword: str
    occurence: int

    @classmethod
    def from_json(cls, json: str):
        return cls(json["keyword"], json["occurence"])