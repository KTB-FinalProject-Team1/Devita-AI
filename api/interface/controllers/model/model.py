from pydantic import BaseModel


class Mission(BaseModel):
    level: int
    missionTitle: str
