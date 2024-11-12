from fastapi import APIRouter, Depends
from api.application.service import Service
from dependency_injector.wiring import inject, Provide

from api.interface.controllers.dto.dto import DailyRequestDTO, DailyResponseDTO, AutonomousRequestDTO, \
    AutonomousResponseDTO
from api.interface.controllers.model.model import Mission
from containers import Container

router = APIRouter(prefix='/ai/v1/mission')


@router.post(
    '/daily',
    response_model=DailyResponseDTO,
    summary="데일리 미션"
)
@inject
def daily(
        req: DailyRequestDTO,
        service: Service = Depends(Provide[Container.service])
) -> DailyResponseDTO:
    """
    데일리 미션을 생성하는 API입니다. 유저 ID와 원하는 분야를 함께 바디에 실어줘야 합니다.
    - **userId**: 유저 식별 PK
    - **categories**: 미션 생성 분야

    ## Request Body 예시
    ```json
    {
        "userId": 1234,
        "categories": ["자료구조", "javascript"]
    }
    ```

    ## Response Body 예시
    ```json
    {
        "missionTitle": "자바에서 new와 this 키워드는 각각 어떤 역할을 하는지 설명하라. new 키워드를 사용해 객체를 생성하는 과정과, this 키워드가 메서드와 생성자에서 어떻게 쓰이는지 구체적인 예를 들어 설명하라."
    }
    ```
    """
    mission = service.daily(req.userId, req.categories)
    # res = [
    #     Mission(level="상", content=missions[0]),
    #     Mission(level="중", content=missions[1]),
    #     Mission(level="하", content=missions[2])
    # ]

    print(mission)
    print(type(mission))
    return DailyResponseDTO(missionTitle=mission)


@router.post(
    '/free',
    response_model=AutonomousResponseDTO,
    summary="자율 미션"
)
@inject
def autonomous(
        req: AutonomousRequestDTO,
        service: Service = Depends(Provide[Container.service])
) -> AutonomousResponseDTO:
    """
    자율 미션을 생성하는 API입니다. 유저 ID와 원하는 분야를 함께 바디에 실어줘야 합니다.

    - **userId**: 유저 식별 PK
    - **subCategory**: 미션 생성 분야

    Request Body 예시
    ```json
    {
        "userId": 1234,
        "subCategory": "자료구조"
    }
    ```
    Response Body 예시
    ```json
    {
        "missions": [
            {
                "level": 1,
                "missionTitle": "자바에서 new와 this 키워드는 각각 어떤 역할을 하는지 설명하라. new 키워드를 사용해 객체를 생성하는 과정과, this 키워드가 메서드와 생성자에서 어떻게 쓰이는지 구체적인 예를 들어 설명하라.",
            },
            {
                "level": 2,
                "missionTitle": "자바에서 상속(Inheritance)과 다형성(Polymorphism)의 차이를 설명하고, 이 두 개념이 객체 지향 프로그래밍에서 어떻게 유용하게 쓰이는지 실제 사례를 들어 설명하라. 특히 다형성이 어떻게 코드 재사용성을 높이는지 중점적으로 논의하라.",
            },
            {
                "level": 3,
                "missionTitle": "자바에서 멀티스레드 프로그래밍의 기본 개념을 설명하고, 멀티스레드 환경에서 발생할 수 있는 문제(예: 데드락, 레이스 컨디션)에 대해 설명하라. 또한, 자바 버전의 설계적 결함을 조사하고, 해당 결함이 프로그램에 미치는 영향을 분석하라."
            }
        ]
    }
    """
    missions = service.autonomous(req.userId, req.subCategory)

    print(len(missions))
    return AutonomousResponseDTO(missions=missions)
