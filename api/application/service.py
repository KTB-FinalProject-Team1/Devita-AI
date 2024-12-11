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

    def save_completed_mission(
            self,
            userId: int,
            title: str,
            date: str,
            missionType: str,
            category: str,
    ) -> int:
        http_code = self.repo.save_completed_mission(userId, title, date, missionType, category)
        return http_code
