from unicodedata import category
from pydantic import BaseModel,ConfigDict,Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.task import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    category: Optional[str] = Field(None, max_length=100)
    due_date: Optional[datetime] = Field(None)
    
    
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[TaskPriority] = Field(None)
    status: Optional[TaskStatus] = Field(None)
    category: Optional[str] = Field(None, max_length=100)
    due_date: Optional[datetime] = Field(None)
    
class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    priority: TaskPriority
    status:  TaskStatus
    category: Optional[str]
    due_date: Optional[datetime]
    user_id : UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    