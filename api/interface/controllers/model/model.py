from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class Mission:
    level: int
    missionTitle: str
