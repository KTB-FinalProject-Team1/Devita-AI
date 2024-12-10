from abc import ABCMeta, abstractmethod
from api.interface.controllers.model.model import Mission


class IRepository(metaclass=ABCMeta):
    @abstractmethod
    def daily(
            self,
            userId: int,
            categories: list[str]
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def autonomous(
            self,
            userId: int,
            subCategory: str
    ) -> list[Mission]:
        raise NotImplementedError

    @abstractmethod
    def save_completed_mission(
            self,
            userId: int,
            title: str,
            completionDate: str,
            missionType: str,
            category: str
    ) -> int:
        raise NotImplementedError
