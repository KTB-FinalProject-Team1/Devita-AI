from api.domain.repository.repo import IRepository
from model.llm import LLMManager
from api.interface.controllers.model.model import Mission
import json

from model.mission_generator import mission_generator_free_langchain, mission_generator_daily_langchain


class Repository(IRepository):
    def daily(
            self,
            userId: int,
            categories: list[str]
    ) -> str:
        res = mission_generator_daily_langchain(categories)
        return res

    def autonomous(
            self,
            userId: int,
            subCategory: str
    ) -> list[Mission]:
        res = mission_generator_free_langchain(subCategory)
        return [Mission(level=1, missionTitle=res['mission_1']),
                Mission(level=2, missionTitle=res['mission_2']),
                Mission(level=3, missionTitle=res['mission_3'])
        ]

    def save_completed_mission(
            self,
            userId: int,
            title: str,
            completionDate: str,
            missionType: str,
            category: str
    ):
        pass
