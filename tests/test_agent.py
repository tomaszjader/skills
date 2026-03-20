import pytest
from langgraph.graph.state import CompiledStateGraph
from core.agent import get_agent

def test_get_agent_creation(monkeypatch):
    """Test that the agent is initialized successfully."""
    # Mock OPENAI_API_KEY to avoid ValidationError
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    
    agent = get_agent()
    
    # Verify the agent is a CompiledStateGraph
    assert isinstance(agent, CompiledStateGraph)
    
    # Basic check - ensure it's not None
    assert agent is not None
