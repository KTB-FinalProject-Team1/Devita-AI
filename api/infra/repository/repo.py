from api.domain.repository.repo import IRepository
from model.llm import LLMManager
from api.interface.controllers.model.model import Mission
import json

from model.mission_generator import mission_generator_free, mission_generator_daily


class Repository(IRepository):
    def daily(
            self,
            userId: int,
            categories: list[str]
    ) -> str:
        l = LLMManager.get_instance()
        res = mission_generator_daily(l._client, categories)
        print(str(res))
        return res

    def autonomous(
            self,
            userId: int,
            subCategory: str
    ) -> list[Mission]:
        res = mission_generator_free(LLMManager.get_instance()._client, subCategory)
        return [Mission(level=1, missionTitle=res[0]),
                Mission(level=2, missionTitle=res[1]),
                Mission(level=3, missionTitle=res[2])
        ]
