from dataclasses import dataclass
from typing import Optional
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class BlackGreyWhiteListEntry:
    """
    A generic dataclass for either black or white list entries
    """

    keyword: str
    keyword_len: int
    wordsAPI_pos: str
    algorithm: str
    name: str
    occurence: Optional[int] = 0

    def __eq__(self, o: object) -> bool:
        return self.keyword == o.keyword and self.wordsAPI_pos == o.wordsAPI_pos

    def __ne__(self, o: object) -> bool:
        return self.keyword != o.keyword and self.wordsAPI_pos != o.wordsAPI_pos

    def __hash__(self) -> int:
        return hash((self.name, self.keyword_len, self.keyword, self.algorithm))
