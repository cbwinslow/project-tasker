import pytest
from project_tasker.nlp.feature_parser import analyze_feature

@pytest.mark.asyncio
async def test_feature_analysis():
    feature_description = """
    Create a user authentication system with login and registration.
    The system should handle password reset and email verification.
    """
    project_id = 1
    
    tasks = await analyze_feature(feature_description, project_id)
    
    assert len(tasks) > 0
    assert all(isinstance(task, dict) for task in tasks)
    assert all("title" in task and "description" in task for task in tasks)
    assert all(task["project_id"] == project_id for task in tasks)
