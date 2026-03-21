from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from core.middleware import SkillMiddleware

def get_agent(model_name: str = "gpt-4o", temperature: float = 0):
    """Initialize and return the SQL assistant agent.
    
    Args:
        model_name: The OpenAI model name to use.
        temperature: Sampling temperature for the model.
    """
    model = ChatOpenAI(model=model_name, temperature=temperature)
    
    agent = create_agent(
        model,
        system_prompt=(
            "You are a professional SQL query assistant. Your goal is to help users "
            "write efficient and accurate queries against business databases. "
            "You have access to specialized skills that provide detailed schema "
            "and business logic information."
        ),
        middleware=[SkillMiddleware()],
        checkpointer=InMemorySaver(),
    )
    return agent
