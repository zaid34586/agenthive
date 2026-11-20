"""Pydantic schemas for AgentHive SaaS."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str = ""


class TaskRead(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    status: str
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    tasks: List[TaskRead]


class AgentStatus(BaseModel):
    name: str
    type: str
    status: str
    last_run: Optional[str] = None