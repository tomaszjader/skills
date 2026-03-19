from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from core.middleware import SkillMiddleware

def get_agent():
    """Initialize and return the SQL assistant agent."""
    model = ChatOpenAI(model="gpt-4o") # Using gpt-4o as it's modern and capable
    
    agent = create_agent(
        model,
        system_prompt=(
            "You are a SQL query assistant that helps users "
            "write queries against business databases."
        ),
        middleware=[SkillMiddleware()],
        checkpointer=InMemorySaver(),
    )
    return agent
