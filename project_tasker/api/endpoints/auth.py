from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from project_tasker.api import deps
from project_tasker.api.schemas import base as schemas
from project_tasker.core import models
from project_tasker.core.config import settings
from project_tasker.core.security import utils

router = APIRouter()

@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests."""
    user = deps.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": utils.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/users", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """Create new user."""
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    user = models.User(
        email=user_in.email,
        hashed_password=utils.get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get current user."""
    return current_user

@router.put("/users/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    user_in: schemas.UserUpdate,
) -> Any:
    """Update current user."""
    if user_in.password is not None:
        current_user.hashed_password = utils.get_password_hash(user_in.password)
    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name
    if user_in.email is not None:
        current_user.email = user_in.email
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
