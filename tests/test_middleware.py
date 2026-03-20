import pytest
from langchain.messages import SystemMessage
from core.middleware import SkillMiddleware
from domain.skills import SKILLS

def test_middleware_init():
    """Test that SkillMiddleware initializes and builds the skills prompt correctly."""
    middleware = SkillMiddleware()
    
    # Check that all skills from domain.skills are in the prompt
    for skill in SKILLS:
        assert f"**{skill['name']}**" in middleware.skills_prompt
        assert skill['description'] in middleware.skills_prompt

def test_middleware_wrap_model_call(mock_model_request):
    """Test that the middleware correctly modifies the ModelRequest."""
    middleware = SkillMiddleware()
    
    # Define a simple handler that returns a dummy response
    def mock_handler(request):
        return request

    modified_request = middleware.wrap_model_call(mock_model_request, mock_handler)
    
    # Verify the system message was updated
    new_system_message = modified_request.system_message
    assert isinstance(new_system_message, SystemMessage)
    
    # Check that the skills addendum is present in the content blocks
    content_text = "".join([block["text"] for block in new_system_message.content_blocks if block["type"] == "text"])
    assert "## Available Skills" in content_text
    assert middleware.skills_prompt in content_text
    assert "Use the load_skill tool" in content_text
