from datetime import date

from pydantic import BaseModel

from api.interface.controllers.model.model import Mission


class DailyRequestDTO(BaseModel):
    userId: int
    categories: list[str]


class DailyResponseDTO(BaseModel):
    # missions: list[Mission]
    missionTitle: str


class AutonomousRequestDTO(BaseModel):
    userId: int
    subCategory: str


class AutonomousResponseDTO(BaseModel):
    missions: list[Mission]


class CompletedMissionRequestDTO(BaseModel):
    userId: int
    title: str
    date: str
    missionType: str
    category: str

