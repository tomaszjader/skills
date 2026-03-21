import os
from pathlib import Path
from typing import List
from domain.models import Skill

def load_skills_from_disk() -> List[Skill]:
    """Load and parse skill definitions from the skills_data directory."""
    skills_dir = Path(__file__).parent / "skills_data"
    skills = []
    
    # Map of names to descriptions (could also be in a config file or frontmatter)
    descriptions = {
        "sales_analytics": "Database schema and business logic for sales data analysis including customers, orders, and revenue.",
        "inventory_management": "Database schema and business logic for inventory tracking including products, warehouses, and stock levels."
    }
    
    if not skills_dir.exists():
        return []
        
    for md_file in skills_dir.glob("*.md"):
        skill_name = md_file.stem
        description = descriptions.get(skill_name, f"Documentation for {skill_name}")
        
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        skills.append(
            Skill(
                name=skill_name,
                description=description,
                content=content
            )
        )
    return skills

# Load skills once at module level
SKILLS: List[Skill] = load_skills_from_disk()
