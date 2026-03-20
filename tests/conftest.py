import pytest
from unittest.mock import MagicMock
from langchain.agents.middleware import ModelRequest
from langchain.messages import SystemMessage

@pytest.fixture
def mock_model_request():
    """Fixture to create a mock ModelRequest."""
    system_message = SystemMessage(
        content=[{"type": "text", "text": "Initial system prompt."}]
    )
    mock_model = MagicMock()
    return ModelRequest(
        model=mock_model,
        messages=[],
        system_message=system_message,
        tools=[],
        tool_choice="auto"
    )

@pytest.fixture
def sample_skills():
    """Fixture providing sample skills for manual verification if needed."""
    return [
        {"name": "test_skill", "description": "A test skill description.", "content": "Full content of test skill."}
    ]
