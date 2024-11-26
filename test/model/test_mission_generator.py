from model.mission_generator import mission_generator_free, mission_generator_daily
import pytest
from unittest.mock import Mock, patch
import json
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from model.mission_generator import mission_generator_free_langchain, _cs_categories, _language_categories, _tool_categories


# Mock OpenAI 응답 클래스
class MockResponse:
    def __init__(self, content):
        class Choice:
            def __init__(self, content):
                self.message = Mock(content=content)

        self.choices = [Choice(content)]


# Fixture for mock client
@pytest.fixture
def mock_client():
    client = Mock()
    return client


def test_mission_generator_free_valid_cs_category(mock_client):
    # Arrange
    mock_json_response = {
        "mission_1": "높은 난이도 미션",
        "mission_2": "중간 난이도 미션",
        "mission_3": "쉬운 난이도 미션"
    }
    mock_client.chat.completions.create.return_value = MockResponse(json.dumps(mock_json_response))

    # Act
    result = mission_generator_free(mock_client, "DATA_STRUCTURE")

    # Assert
    assert len(result) == 3
    assert isinstance(result, list)
    assert all(isinstance(mission, str) for mission in result)
    mock_client.chat.completions.create.assert_called_once()


def test_mission_generator_free_invalid_category():
    # Arrange
    mock_client = Mock()

    # Act & Assert
    with pytest.raises(ValueError, match="지원하지 않는 카테고리입니다"):
        mission_generator_free(mock_client, "INVALID_CATEGORY")


def test_mission_generator_free_json_decode_error(mock_client):
    # Arrange
    mock_client.chat.completions.create.return_value = MockResponse("invalid json")

    # Act & Assert
    with pytest.raises(ValueError, match="미션 생성 중 오류가 발생했습니다"):
        mission_generator_free(mock_client, "DATA_STRUCTURE")


def test_mission_generator_daily_valid_categories(mock_client):
    # Arrange
    mock_client.chat.completions.create.return_value = MockResponse("일일 미션 테스트")

    # Act
    result = mission_generator_daily(mock_client, ["PYTHON", "JAVA"])

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0
    mock_client.chat.completions.create.assert_called_once()


def test_mission_generator_daily_invalid_categories():
    # Arrange
    mock_client = Mock()

    # Act & Assert
    with pytest.raises(ValueError, match="올바른 sub_category를 입력하세요"):
        mission_generator_daily(mock_client, ["INVALID_CATEGORY"])


def test_mission_generator_daily_empty_categories():
    # Arrange
    mock_client = Mock()

    # Act & Assert
    with pytest.raises(ValueError):
        mission_generator_daily(mock_client, [])


def test_mission_generator_daily_response_format(mock_client):
    # Arrange
    expected_mission = "테스트 미션"
    mock_client.chat.completions.create.return_value = MockResponse(expected_mission)

    # Act
    result = mission_generator_daily(mock_client, ["PYTHON"])

    # Assert
    assert result == expected_mission
    assert isinstance(result, str)


# 통합 테스트
def test_integration_both_generators(mock_client):
    # Arrange
    mock_json_response = {
        "mission_1": "높은 난이도 미션",
        "mission_2": "중간 난이도 미션",
        "mission_3": "쉬운 난이도 미션"
    }
    mock_client.chat.completions.create.return_value = MockResponse(json.dumps(mock_json_response))

    # Act
    free_result = mission_generator_free(mock_client, "PYTHON")
    daily_result = mission_generator_daily(mock_client, ["PYTHON"])

    # Assert
    assert len(free_result) == 3
    assert isinstance(daily_result, str)


class TestMissionGeneratorLangchain:
    @pytest.fixture
    def mock_llm_manager(self):
        with patch('model.mission_generator.LLMManager') as mock_manager:
            instance = Mock()
            mock_manager.get_instance.return_value = instance
            yield instance

    def test_valid_cs_category(self, mock_llm_manager):
        # Arrange
        expected_response = {
            "mission_1": "높은 난이도 테스트 미션",
            "mission_2": "중간 난이도 테스트 미션",
            "mission_3": "쉬운 난이도 테스트 미션"
        }
        mock_llm_manager.invoke.return_value = AIMessage(content=json.dumps(expected_response))

        # Act
        result = mission_generator_free_langchain("DATA_STRUCTURE")

        # Assert
        assert isinstance(result, str)
        parsed_result = json.loads(result)
        assert "mission_1" in parsed_result
        assert "mission_2" in parsed_result
        assert "mission_3" in parsed_result
        mock_llm_manager.invoke.assert_called_once()

    def test_valid_language_category(self, mock_llm_manager):
        # Arrange
        expected_response = {
            "mission_1": "높은 난이도 테스트 미션",
            "mission_2": "중간 난이도 테스트 미션",
            "mission_3": "쉬운 난이도 테스트 미션"
        }
        mock_llm_manager.invoke.return_value = AIMessage(content=json.dumps(expected_response))

        # Act
        result = mission_generator_free_langchain("PYTHON")

        # Assert
        parsed_result = json.loads(result)
        assert len(parsed_result) == 3
        assert all(key in parsed_result for key in ["mission_1", "mission_2", "mission_3"])

    def test_valid_tool_category(self, mock_llm_manager):
        # Arrange
        expected_response = {
            "mission_1": "높은 난이도 테스트 미션",
            "mission_2": "중간 난이도 테스트 미션",
            "mission_3": "쉬운 난이도 테스트 미션"
        }
        mock_llm_manager.invoke.return_value = AIMessage(content=json.dumps(expected_response))

        # Act
        result = mission_generator_free_langchain("SPRING")

        # Assert
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, dict)
        assert all(len(mission) <= 100 for mission in parsed_result.values())

    def test_invalid_category(self):
        # Act & Assert
        with pytest.raises(ValueError, match="지원하지 않는 카테고리입니다"):
            mission_generator_free_langchain("INVALID_CATEGORY")

    def test_message_format(self, mock_llm_manager):
        # Arrange
        expected_response = {
            "mission_1": "테스트 미션 1",
            "mission_2": "테스트 미션 2",
            "mission_3": "테스트 미션 3"
        }
        mock_llm_manager.invoke.return_value = AIMessage(content=json.dumps(expected_response))

        # Act
        result = mission_generator_free_langchain("PYTHON")
        messages = mock_llm_manager.invoke.call_args[0][0]

        # Assert
        assert len(messages) == 2
        assert isinstance(messages[0], SystemMessage)
        assert isinstance(messages[1], HumanMessage)
        assert "PYTHON" in messages[0].content

    @pytest.mark.parametrize("category", [
        pytest.param("DATA_STRUCTURE", id="cs_category"),
        pytest.param("PYTHON", id="language_category"),
        pytest.param("SPRING", id="tool_category")
    ])
    def test_different_categories(self, mock_llm_manager, category):
        # Arrange
        expected_response = {
            "mission_1": f"{category} 높은 난이도 미션",
            "mission_2": f"{category} 중간 난이도 미션",
            "mission_3": f"{category} 쉬운 난이도 미션"
        }
        mock_llm_manager.invoke.return_value = AIMessage(content=json.dumps(expected_response))

        # Act
        result = mission_generator_free_langchain(category)

        # Assert
        parsed_result = json.loads(result)
        assert len(parsed_result) == 3
        assert all(category in mission for mission in parsed_result.values())

    def test_json_structure(self, mock_llm_manager):
        # Arrange
        mock_llm_manager.invoke.return_value = AIMessage(content="""
        {
            "mission_1": "테스트 미션 1",
            "mission_2": "테스트 미션 2",
            "mission_3": "테스트 미션 3"
        }
        """)

        # Act
        result = mission_generator_free_langchain("PYTHON")

        # Assert
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, dict)
        assert list(parsed_result.keys()) == ["mission_1", "mission_2", "mission_3"]

    def test_mission_length_constraint(self, mock_llm_manager):
        # Arrange
        long_mission = "a" * 101  # 100자 초과
        expected_response = {
            "mission_1": long_mission,
            "mission_2": "중간 난이도 미션",
            "mission_3": "쉬운 난이도 미션"
        }
        mock_llm_manager.invoke.return_value = AIMessage(content=json.dumps(expected_response))

        # Act
        result = mission_generator_free_langchain("PYTHON")
        parsed_result = json.loads(result)

        # Assert
        assert all(len(mission) <= 100 for mission in parsed_result.values())

    @pytest.mark.parametrize("category,main_category", [
        ("DATA_STRUCTURE", "CS"),
        ("PYTHON", "LANGUAGE"),
        ("SPRING", "TOOL")
    ])
    def test_main_category_determination(self, mock_llm_manager, category, main_category):
        # Arrange
        expected_response = {"mission_1": "", "mission_2": "", "mission_3": ""}
        mock_llm_manager.invoke.return_value = AIMessage(content=json.dumps(expected_response))

        # Act
        mission_generator_free_langchain(category)
        messages = mock_llm_manager.invoke.call_args[0][0]

        # Assert
        assert main_category in messages[0].content


# Helper function tests
def test_all_categories_unique():
    # 모든 카테고리가 유일한지 검증
    all_categories = _cs_categories + _language_categories + _tool_categories
    assert len(all_categories) == len(set(all_categories))