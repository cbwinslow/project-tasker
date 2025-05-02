from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from project_tasker.core.database import Base

# Association tables
user_platform = Table(
    "user_platform",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("platform_id", Integer, ForeignKey("platforms.id")),
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    platforms = relationship("Platform", secondary=user_platform, back_populates="users")
    projects = relationship("Project", back_populates="owner")

class Platform(Base):
    __tablename__ = "platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)  # e.g., "github", "jira", "gitlab"
    api_base_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", secondary=user_platform, back_populates="platforms")
    integrations = relationship("Integration", back_populates="platform")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    integrations = relationship("Integration", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"))
    parent_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="tasks")
    parent = relationship("Task", remote_side=[id], backref="subtasks")
    platform_tasks = relationship("PlatformTask", back_populates="task")

class Integration(Base):
    __tablename__ = "integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    external_project_id = Column(String)
    credentials = Column(String)  # Encrypted OAuth tokens or API keys
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="integrations")
    platform = relationship("Platform", back_populates="integrations")

class PlatformTask(Base):
    __tablename__ = "platform_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    integration_id = Column(Integer, ForeignKey("integrations.id"))
    external_id = Column(String)  # ID of the task in the external platform
    external_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    task = relationship("Task", back_populates="platform_tasks")
    integration = relationship("Integration")
