import logging
from typing import Callable
from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware
from langchain.messages import SystemMessage
from domain.skills import SKILLS
from domain.tools import load_skill

logger = logging.getLogger(__name__)

class SkillMiddleware(AgentMiddleware):
    """Middleware that injects skill descriptions into the system prompt."""
    
    # Register the load_skill tool as a class variable
    tools = [load_skill]
    
    def __init__(self):
        """Initialize and generate the skills prompt from SKILLS."""
        self.skills_prompt = self._build_skills_prompt()

    def _build_skills_prompt(self) -> str:
        """Helper to create the skills description string."""
        if not SKILLS:
            return "No specialized skills currently available."
            
        skills_list = [
            f"- **{skill.name}**: {skill.description}" 
            for skill in SKILLS
        ]
        return "\n".join(skills_list)

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Inject skill descriptions into the system prompt before the model call."""
        
        skills_section = (
            "\n\n## Available Skills\n\n"
            f"{self.skills_prompt}\n\n"
            "INSTRUCTION: Use the `load_skill` tool when you need detailed technical "
            "information, schemas, or business logic for a specific skill area."
        )
        
        # Access existing content blocks
        current_blocks = list(request.system_message.content_blocks)
        
        # Append the skills section
        new_blocks = current_blocks + [
            {"type": "text", "text": skills_section}
        ]
        
        logger.debug(f"Injecting skills section into system prompt. Available skills: {len(SKILLS)}")
        
        # Create a new system message and override request
        new_system_message = SystemMessage(content=new_blocks)
        modified_request = request.override(system_message=new_system_message)
        
        return handler(modified_request)
