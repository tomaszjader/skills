import pytest
from domain.tools import load_skill
from domain.skills import SKILLS

def test_load_skill_valid():
    """Test loading a valid skill."""
    if not SKILLS:
        pytest.skip("No skills defined in domain.skills")
        
    skill_to_load = SKILLS[0]["name"]
    result = load_skill.invoke({"skill_name": skill_to_load})
    
    assert f"Loaded skill: {skill_to_load}" in result
    assert SKILLS[0]["content"] in result

def test_load_skill_invalid():
    """Test loading a non-existent skill."""
    invalid_name = "non_existent_skill_12345"
    result = load_skill.invoke({"skill_name": invalid_name})
    
    assert f"Skill '{invalid_name}' not found" in result
    assert "Available skills:" in result
    for skill in SKILLS:
        assert skill["name"] in result
