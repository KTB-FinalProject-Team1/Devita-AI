from dependency_injector.wiring import inject
from api.domain.repository.repo import IRepository


class Service:
    def __init__(
            self,
            repo: IRepository,
    ):
        self.repo = repo

    def daily(
            self,
            userId: int,
            categories: list[str]
    ) -> str:
        mission = self.repo.daily(userId, categories)
        return mission

    def autonomous(
            self,
            userId: int,
            subCategory: str
    ) -> list[str]:
        missions = self.repo.autonomous(userId, subCategory)
        return missions
