from dependency_injector import providers, containers
from api.application.service import Service
from api.infra.repository.repo import Repository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["api"]
    )

    repo = providers.Factory(Repository)
    service = providers.Factory(Service, repo=repo)
