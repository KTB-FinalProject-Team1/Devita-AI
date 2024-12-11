import pytest
from unittest.mock import Mock, patch
import json
from model.mission_generator import mission_generator_free, mission_generator_daily


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