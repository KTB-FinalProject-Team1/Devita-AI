import json
import random


_cs_categories = ("DATA_STRUCTURE", "ALGORITHM", "COMPUTER_ARCHITECTURE", "NETWORK", "OPERATING_SYSTEM",
                  "DATABASE")
_language_categories = ("JAVA", "JAVASCRIPT", "PYTHON")
_tool_categories = ("SPRING", "REACT", "PYTORCH", "DOCKER")

def mission_generator_free(_client, sub_category: str) -> list[str]:
    def determine_main_category(sub_category: str) -> str:
        if sub_category in _cs_categories:
            return "CS"
        elif sub_category in _language_categories:
            return "LANGUAGE"
        elif sub_category in _tool_categories:
            return "TOOL"
        else:
            raise ValueError(f"지원하지 않는 카테고리입니다: {sub_category}")

    main_category = determine_main_category(sub_category)

    def generate_mission_prompt(main_category, sub_category):
        if main_category == "cs":
            if sub_category == "네트워크":
                example_text = """
                        높은 난이도: TCP와 UDP의 차이점을 설명하고, TCP의 혼잡 제어 메커니즘(예: 슬라이딩 윈도우, 혼잡 회피)을 분석하라.
                        중간 난이도: 라우팅 테이블의 동작 원리와 OSPF 프로토콜의 작동 방식을 설명하고, 기본적인 OSPF 설정 예시를 작성하라.
                        쉬운 난이도: OSI 7계층 모델의 각 계층 역할을 간단히 설명하고, 해당 계층에서 사용하는 프로토콜(예: HTTP, TCP, IP)을 예시로 들어라.
                        """
            elif sub_category == "알고리즘":
                example_text = """
                        높은 난이도: 다익스트라 알고리즘을 사용한 최단 경로 탐색 원리를 분석하고, 우선순위 큐를 이용한 최적화 방안을 설명하라.
                        중간 난이도: 퀵 정렬 알고리즘의 분할 정복 방식을 설명하고, 시간 복잡도를 분석하며, 퀵 정렬의 성능을 개선하는 방법을 제시하라.
                        쉬운 난이도: 선택 정렬 알고리즘의 동작 과정을 설명하고, 시간 복잡도와 공간 복잡도를 계산하라.
                        """
            else:
                example_text = """
                        높은 난이도: 다익스트라 알고리즘을 사용한 최단 경로 탐색 원리를 분석하고, 우선순위 큐를 이용한 최적화 방안을 설명하라.
                        중간 난이도: 퀵 정렬 알고리즘의 분할 정복 방식을 설명하고, 시간 복잡도를 분석하며, 퀵 정렬의 성능을 개선하는 방법을 제시하라.
                        쉬운 난이도: 선택 정렬 알고리즘의 동작 과정을 설명하고, 시간 복잡도와 공간 복잡도를 계산하라.
                        """
            prompt_description = "심화된 대학교 전공 수준의 개념 이해와 분석 능력을 테스트할 수 있는 미션"

        elif main_category == "language":
            if sub_category == "Java":
                example_text = """
                        높은 난이도: 멀티스레드 환경에서의 동기화 필요성을 설명하고, synchronized 키워드를 사용해 데이터 레이스 문제를 해결하는 방법을 분석하라.
                        중간 난이도: 자바 메모리 구조(스택과 힙)의 차이점을 설명하고, 가비지 컬렉션 방식 중 '마크-스윕'의 작동 원리를 이해할 수 있도록 예시를 제시하라.
                        쉬운 난이도: 객체 지향 프로그래밍의 4가지 개념(캡슐화, 상속, 다형성, 추상화)을 각각 설명하라.
                        """
            elif sub_category == "Python":
                example_text = """
                        높은 난이도: 비동기 프로그래밍의 필요성과 개념을 설명하고, asyncio와 aiohttp를 사용해 비동기 웹 크롤러를 구현하라.
                        중간 난이도: 데코레이터와 클로저의 차이점을 설명하고, 함수 실행 시간을 측정하는 로깅 기능을 데코레이터로 구현하라.
                        쉬운 난이도: 리스트와 딕셔너리와 같은 기본 자료구조의 특징을 설명하라.
                        """
            else:
                example_text = """
                        높은 난이도: 비동기 프로그래밍의 필요성과 개념을 설명하고, asyncio와 aiohttp를 사용해 비동기 웹 크롤러를 구현하라.
                        중간 난이도: 데코레이터와 클로저의 차이점을 설명하고, 함수 실행 시간을 측정하는 로깅 기능을 데코레이터로 구현하라.
                        쉬운 난이도: 리스트와 딕셔너리와 같은 기본 자료구조의 특징을 설명하라.
                        """
            prompt_description = "언어적 특성을 이해하고 사용하는 데 중점을 둔 미션"

        else:  # main_category == "tool"
            if sub_category == "Spring":
                example_text = """
                        높은 난이도: Spring과 JPA를 사용하여 다중 테이블 간 연관 관계를 매핑하고, 복잡한 쿼리를 최적화하는 방법을 설명하라.
                        중간 난이도: Spring MVC 패턴을 활용하여 간단한 CRUD 기능을 갖춘 게시판 애플리케이션을 설계하고 구현하라.
                        쉬운 난이도: Spring Boot를 사용하여 간단한 REST API를 생성하고, 이를 통해 기본적인 GET/POST 요청을 처리하라.
                        """
            elif sub_category == "Pytorch":
                example_text = """
                        높은 난이도: PyTorch로 커스텀 신경망을 설계하고, 대규모 데이터셋을 활용하여 모델 학습 및 최적화 방법을 분석하라.
                        중간 난이도: PyTorch에서 CNN을 사용해 이미지 분류 모델을 구현하고, 학습 및 평가 과정을 설명하라.
                        쉬운 난이도: PyTorch에서 텐서 기본 연산과 자동 미분 기능을 사용하여 간단한 수학적 계산을 수행하라.
                        """
            else:
                example_text = """
                        높은 난이도: PyTorch로 커스텀 신경망을 설계하고, 대규모 데이터셋을 활용하여 모델 학습 및 최적화 방법을 분석하라.
                        중간 난이도: PyTorch에서 CNN을 사용해 이미지 분류 모델을 구현하고, 학습 및 평가 과정을 설명하라.
                        쉬운 난이도: PyTorch에서 텐서 기본 연산과 자동 미분 기능을 사용하여 간단한 수학적 계산을 수행하라.
                        """
            prompt_description = "도구의 사용법과 주요 기능을 실습하는 미션"

        # 최종 프롬프트 생성
        prompt = {
            "system": f"""
                    너는 개발자의 성장을 위한 일일 미션 생성기야.
                    사용자가 관심 있는 개발 분야는 {main_category}의 {sub_category}야.

                    [행동 지침]
                    - 미션 제목만 출력하며, 미션 설명, 미션 목표 등 추가 내용은 포함하지 않아. '높은 난이도:', '중간 난이도:', '쉬운 난이도:'와 같은 난이도 표시를 포함하지 마.
                    - 미션은 반드시 {main_category}, {sub_category}와 관련된 주제여야 하며, 그 외 내용은 포함하지 않아.
                    - 예시는 단지 참고용일 뿐이야, 예시 내용에 너무 의존하거나 복사하지 마.
                    - 개념을 확인하고 이해를 테스트할 수 있는 미션을 중심으로 생성해.
                    - 미션 난이도는 높은 난이도, 중간 난이도, 쉬운 난이도 순으로 구분되며, 난이도 차이가 명확해야 해.
                      * 쉬운 난이도의 미션은 개념을 알고 있는지 확인하는 수준보다 어려우면 안 돼.
                      * 중간 난이도의 미션은 개념의 작동 원리를 알 수 있는 수준보다 어려우면 안 돼.
                      * 높은 난이도의 미션은 개념의 응용을 할 수 있는 수준이어야 합니다.

                    아래는 생성된 미션 예시야.
                    ------------------------
                    {example_text}
                    ------------------------

                    다음과 같은 JSON schema로 출력해야 합니다:
                    {{
                        "mission_1": "높은 난이도 미션(100자 이내)",
                        "mission_2": "중간 난이도 미션(100자 이내)",
                        "mission_3": "쉬운 난이도 미션(100자 이내)"
                    }}
                    """,
            "user": f"""
                    질문: {main_category} 안에 {sub_category}를 바탕으로 개발자를 위한 높은 난이도, 중간 난이도, 쉬운 난이도 {prompt_description}을 생성하시오.
                    답:
                    """
        }

        return prompt

    # 프롬프트 생성
    prompt = generate_mission_prompt(main_category.lower(), sub_category)

    # 미션 생성
    response = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt['system']},
            {"role": "user", "content": prompt['user']},
        ],
        max_tokens=300,
        temperature=1.0,
        top_p=0.95,
        response_format={"type": "json_object"}
    )

    # JSON 응답 파싱
    try:
        missions = json.loads(response.choices[0].message.content)
        return [
            missions["mission_1"],
            missions["mission_2"],
            missions["mission_3"]
        ]
    except json.JSONDecodeError:
        raise ValueError("미션 생성 중 오류가 발생했습니다.")


def mission_generator_daily(_client, sub_categories: list[str]):
    # main_category를 sub_category에 따라 자동 지정


    for category in sub_categories:
        if category not in _cs_categories + _language_categories + _tool_categories:
            raise ValueError(f"올바른 sub_category를 입력하세요. 잘못된 카테고리: {category}")

    category_mapping = {}
    example_texts = []
    prompt_descriptions = []

    for sub_category in sub_categories:
        if sub_category in _cs_categories:
            category_mapping[sub_category] = "CS"
            if sub_category == "DATA_STRUCTURE":
                example_texts.append("""
                예시 1: 해시 충돌 해결을 위해 체이닝(Linked List)을 사용하는 해시 테이블을 구현하시오.
                예시 2: 이진 탐색 트리에서 노드 삽입과 탐색 알고리즘을 구현하시오.
                """)
            elif sub_category == "ALGORITHM":
                example_texts.append("""
                예시 1: 퀵 정렬 알고리즘의 분할 정복 방식을 설명하고, 시간 복잡도를 분석하며, 퀵 정렬의 성능을 개선하는 방법을 제시하시오.
                예시 2: 선택 정렬 알고리즘의 동작 과정을 설명하고, 시간 복잡도와 공간 복잡도를 계산하시오.
                """)
            elif sub_category == "COMPUTER_ARCHITECTURE":
                example_texts.append("""
                예시 1: 파이프라인의 단계별 동작을 설명하고 간단한 명령어 흐름을 시뮬레이션하시오.
                예시 2: 2진수 덧셈과 보수 연산을 사용하여 산술 연산을 수행하는 알고리즘을 구현하시오.
                """)
            elif sub_category == "NETWORK":
                example_texts.append("""
                예시 1: 라우팅 테이블의 동작 원리와 OSPF 프로토콜의 작동 방식을 설명하고, 기본적인 OSPF 설정 예시를 작성하시오.
                예시 2: OSI 7계층 모델의 각 계층 역할을 간단히 설명하고, 해당 계층에서 사용하는 프로토콜(예: HTTP, TCP, IP)을 예시로 드시오.
                """)
            elif sub_category == "DATABASE":
                example_texts.append("""
                예시 1: B+ 트리 인덱스를 이용해 효율적인 데이터 검색 알고리즘을 설계하시오.
                예시 2: 관계 대수의 기본 연산을 사용하여 간단한 SQL 쿼리를 관계 대수로 변환하시오.
                """)
            else:  # "OPERATING_SYSTEM"
                example_texts.append("""
                예시 1: 다단계 피드백 큐 스케줄링 알고리즘을 설계하고 시뮬레이션하시오.
                예시 2: 페이징 기법에서 페이지 교체 알고리즘의 FIFO 방식을 구현하시오.
                """)
            prompt_descriptions.append("심화된 대학교 전공 수준의 개념 이해와 분석 능력을 테스트할 수 있는 미션")

        elif sub_category in _language_categories:
            category_mapping[sub_category] = "LANGUAGE"
            if sub_category == "JAVA":
                example_texts.append("""
                예시 1: 자바 메모리 구조(스택과 힙)의 차이점을 설명하고, 가비지 컬렉션 방식 중 '마크-스윕'의 작동 원리를 이해할 수 있도록 예시를 제시하시오.
                예시 2: 객체 지향 프로그래밍의 4가지 개념(캡슐화, 상속, 다형성, 추상화)을 각각 설명하시오.
                """)
            elif sub_category == "JAVASCRIPT":
                example_texts.append("""
                예시 1: JavaScript의 this 키워드가 다른 컨텍스트에서 어떻게 동작하는지 예제 코드를 작성하고 분석하시오.
                예시 2: JavaScript에서 var, let, const의 차이를 설명하고 각 변수 선언 키워드의 예제 코드를 작성하시오.
                """)
            else:  # "PYTHON"
                example_texts.append("""
                예시 1: Python의 제너레이터와 이터레이터의 차이를 설명하고 제너레이터를 이용한 데이터 스트림 생성기를 작성하시오.
                예시 2: Python의 리스트 내포(List Comprehension)를 사용하여 1부터 100까지의 짝수 리스트를 생성하는 코드를 작성하시오.
                """)
            prompt_descriptions.append("언어적 특성을 이해하고 사용하는 데 중점을 둔 미션")

        elif sub_category in _tool_categories:
            category_mapping[sub_category] = "TOOL"
            if sub_category == "SPRING":
                example_texts.append("""
                예시 1: Spring MVC 패턴을 활용하여 간단한 CRUD 기능을 갖춘 게시판 애플리케이션을 설계하고 구현하시오.
                예시 2: Spring Boot를 사용하여 간단한 REST API를 생성하고, 이를 통해 기본적인 GET/POST 요청을 처리하시오.
                """)
            elif sub_category == "REACT":
                example_texts.append("""
                예시 1: React에서 커스텀 Hook을 작성하여 데이터 페칭 로직을 재사용할 수 있도록 하시오.
                예시 2: React 컴포넌트를 사용하여 단순한 버튼 클릭 카운터 애플리케이션을 작성하시오.
                """)
            elif sub_category == "PYTORCH":
                example_texts.append("""
                예시 1: PyTorch에서 CNN을 사용해 이미지 분류 모델을 구현하고, 학습 및 평가 과정을 설명하시오.
                예시 2: PyTorch에서 텐서 기본 연산과 자동 미분 기능을 사용하여 간단한 수학적 계산을 수행하시오.
                """)
            else:  # "DOCKER"
                example_texts.append("""
                예시 1: Dockerfile을 작성하여 Python 애플리케이션을 컨테이너화하고 이미지를 빌드 및 실행하시오.
                예시 2: Docker CLI를 사용하여 간단한 Nginx 컨테이너를 실행하고 로컬에서 접근하시오.
                """)
            prompt_descriptions.append("도구의 사용법과 주요 기능을 실습하는 미션")

    # 랜덤하게 하나의 카테고리 선택
    selected_idx = random.randint(0, len(sub_categories) - 1)
    selected_category = sub_categories[selected_idx]

    prompt = {
        "system": f"""
        너는 개발자의 성장을 위한 일일 미션 생성기야.
        사용자가 관심 있는 개발 분야는 {category_mapping[selected_category]}의 {selected_category}야.

        [행동 지침]
        - 미션은 반드시 {category_mapping[selected_category]}, {selected_category}와 관련된 주제여야 하며, 그 외 내용은 포함하지 않아.
        - 예시는 단지 참고용일 뿐이야, 예시 내용에 너무 의존하거나 복사하지 마.
        - 개념을 확인하고 이해를 테스트할 수 있는 미션을 중심으로 생성해.
        - '미션:'과 같은 텍스트를 붙이지 말고 미션에 해당하는 텍스트만 생성해줘.

        아래는 생성된 미션 예시야.
        ------------------------
        {example_texts[selected_idx]}
        ------------------------
        """,
        "user": f"""
        질문: {category_mapping[selected_category]} 안에 {selected_category}를 바탕으로 개발자를 위한 {prompt_descriptions[selected_idx]} 1개를 생성하시오.
        답:
        """
    }

    response = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt['system']},
            {"role": "user", "content": prompt['user']},
        ],
        max_tokens=100,
        temperature=1.2,
        top_p=0.95,
        response_format={"type": "text"}
    )

    mission = response.choices[0].message.content

    return mission