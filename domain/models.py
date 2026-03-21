from pydantic import BaseModel, Field

class Skill(BaseModel):
    """A skill that can be progressively disclosed to the agent."""
    name: str = Field(..., description="The unique name of the skill")
    description: str = Field(..., description="A short description of the skill for the agent")
    content: str = Field(..., description="The full technical documentation of the skill")
