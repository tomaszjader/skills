from langchain.tools import tool
from domain.skills import SKILLS

@tool
def load_skill(skill_name: str) -> str:
    """Load the full technical documentation for a specific skill.
    
    Use this when you need detailed information about a business area, its database 
    schema, or specific business logic rules. Providing the skill name will return 
    the full reference documentation.
    
    Args:
        skill_name: The exact name of the skill to load (e.g., "sales_analytics", "inventory_management")
    """
    # Find and return the requested skill
    for skill in SKILLS:
        if skill.name == skill_name:
            return f"### Document: {skill_name}\n\n{skill.content}"
    
    # Skill not found
    available = ", ".join(f"'{s.name}'" for s in SKILLS)
    return (
        f"Error: Skill '{skill_name}' not found.\n"
        f"Please choose from the following Available skills: {available}. "
        "Make sure to use the exact name as listed."
    )
