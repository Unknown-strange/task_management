import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING
from sqlalchemy import Enum as SAEnum
from sqlalchemy.schema import ForeignKey
from sqlalchemy import String, Boolean, DateTime, func, Text
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from app.models.user import User


class TaskPriority(str, PyEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    
class TaskStatus(str, PyEnum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    
class Task(Base):
    __tablename__ = "tasks"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SAEnum(TaskPriority, name="TaskPriority"),
        default=TaskPriority.MEDIUM,
        nullable=False
    )
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, default=TaskStatus.TODO),
        nullable=False
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["User"] = relationship("User", back_populates="tasks")
    due_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
        
    
    

    

    