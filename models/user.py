from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    name: str
    id: UUID
