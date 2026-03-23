import frontmatter
from pathlib import Path
from typing import List
from domain.models import Skill

def load_skills_from_disk() -> List[Skill]:
    """Load and parse skill definitions from the skills_data directory."""
    skills_dir = Path(__file__).parent / "skills_data"
    skills = []
    
    if not skills_dir.exists():
        return []
        
    for md_file in skills_dir.glob("*.md"):
        skill_name = md_file.stem
        
        # Load frontmatter and content
        post = frontmatter.load(md_file)
        description = post.get("description", f"Documentation for {skill_name}")
        content = post.content
        
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
