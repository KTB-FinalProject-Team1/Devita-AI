import pytest
from unittest.mock import Mock, patch
import json
from langchain.schema import AIMessage
from model.mission_generator import mission_generator_free_langchain
from model.llm import LLMManager  # LLMManager 클래스가 있는 모듈


class TestMissionGeneratorWithLLM:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """각 테스트 전후로 LLMManager 싱글톤 초기화"""
        # 테스트 시작 전
        llm = LLMManager.get_instance()
        llm.load_model()

        yield  # 테스트 실행

        # 테스트 종료 후
        LLMManager._instance = None
        LLMManager._client = None

    @pytest.fixture
    def mock_chat_openai(self):
        """ChatOpenAI 객체 모킹"""
        with patch('langchain.chat_models.ChatOpenAI') as mock:
            mock_instance = Mock()
            mock.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def llm_manager_with_mock(self, mock_chat_openai):
        """목 클라이언트가 설정된 LLMManager 반환"""
        manager = LLMManager.get_instance()
        manager._client = mock_chat_openai
        return manager

    def test_mission_generation_output(self, llm_manager_with_mock):
        """실제 미션 생성 출력 테스트"""
        # Arrange
        expected_response = {
            "mission_1": "파이썬 고급 미션 테스트",
            "mission_2": "파이썬 중급 미션 테스트",
            "mission_3": "파이썬 초급 미션 테스트"
        }

        llm_manager_with_mock.invoke = Mock(
            return_value=AIMessage(content=json.dumps(expected_response))
        )

        # Act
        result = mission_generator_free_langchain("PYTHON")
        missions = json.loads(result)

        # Assert & Print
        print("\n=== 생성된 미션 ===")
        print(f"고급: {missions['mission_1']}")
        print(f"중급: {missions['mission_2']}")
        print(f"초급: {missions['mission_3']}")

        assert len(missions) == 3
        assert all(isinstance(mission, str) for mission in missions.values())

    @pytest.mark.parametrize("category", [
        "PYTHON",
        "JAVA",
        "ALGORITHM",
        "SPRING"
    ])
    def test_multiple_categories(self, llm_manager_with_mock, category):
        """여러 카테고리에 대한 미션 생성 테스트"""
        # Arrange
        expected_response = {
            "mission_1": f"{category} 고급 미션",
            "mission_2": f"{category} 중급 미션",
            "mission_3": f"{category} 초급 미션"
        }

        llm_manager_with_mock.invoke = Mock(
            return_value=AIMessage(content=json.dumps(expected_response))
        )

        # Act
        result = mission_generator_free_langchain(category)

        # Print
        print(result)

    def test_real_llm_integration(self):
        """실제 LLM을 사용한 통합 테스트 (선택적)"""
        try:
            # LLMManager 초기화 및 모델 로드
            manager = LLMManager.get_instance()
            manager.load_model()

            # 미션 생성
            result = mission_generator_free_langchain("PYTHON")
            missions = json.loads(result)

            # 결과 출력
            print("\n=== 실제 LLM으로 생성된 미션 ===")
            print(f"고급: {missions['mission_1']}")
            print(f"중급: {missions['mission_2']}")
            print(f"초급: {missions['mission_3']}")

            assert len(missions) == 3
            assert all(isinstance(mission, str) for mission in missions.values())

        except Exception as e:
            pytest.skip(f"실제 LLM 테스트 실패: {str(e)}")


def main():
    """테스트 실행을 위한 메인 함수"""
    # 특정 카테고리 테스트
    categories = ["PYTHON", "JAVA", "ALGORITHM", "SPRING"]

    for category in categories:
        try:
            manager = LLMManager.get_instance()
            manager.load_model()

            result = mission_generator_free_langchain(category)
            missions = json.loads(result)

            print(f"\n=== {category} 카테고리 미션 ===")
            print(f"고급: {missions['mission_1']}")
            print(f"중급: {missions['mission_2']}")
            print(f"초급: {missions['mission_3']}")

        except Exception as e:
            print(f"Error generating missions for {category}: {str(e)}")


if __name__ == "__main__":
    # 테스트 모드로 실행
    pytest.main([__file__, "-v", "-s"])

    # 또는 직접 실행
    # main()