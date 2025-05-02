from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from project_tasker.api import deps
from project_tasker.api.schemas import base as schemas
from project_tasker.core import models
from project_tasker.nlp import feature_parser

router = APIRouter()

@router.post("/projects", response_model=schemas.Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: schemas.ProjectCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Create new project."""
    project = models.Project(
        **project_in.dict(),
        owner_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/projects", response_model=List[schemas.Project])
def get_projects(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve projects."""
    projects = (
        db.query(models.Project)
        .filter(models.Project.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return projects

@router.post("/projects/{project_id}/tasks/analyze", response_model=List[schemas.TaskCreate])
async def analyze_feature(
    *,
    project_id: int,
    feature_description: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Analyze feature description and break it down into tasks."""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Use NLP module to break down the feature
    tasks = await feature_parser.analyze_feature(feature_description, project_id)
    return tasks

@router.post("/projects/{project_id}/tasks", response_model=schemas.Task)
def create_task(
    *,
    project_id: int,
    task_in: schemas.TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Create new task in project."""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    task = models.Task(**task_in.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/projects/{project_id}/tasks", response_model=List[schemas.Task])
def get_tasks(
    *,
    project_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve tasks for a project."""
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    tasks = (
        db.query(models.Task)
        .filter(models.Task.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return tasks
