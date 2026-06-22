from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.task import  Task, TaskPriority, TaskStatus
from app.schemas.task import TaskCreate,TaskUpdate


async def create_task(db: AsyncSession, task_data: TaskCreate,  user_id: UUID) ->  Task:
    task  = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status=task_data.status,
        category=task_data.category,
        due_date=task_data.due_date,
        user_id= user_id,
    )
    db.add(task)
    await db.flush()
    return task

async def get_task_by_id(db: AsyncSession, task_id: UUID, user_id: UUID) -> Task | None:
    result  = await db.execute(
        select(Task).where(Task.id==  task_id, Task.user_id==user_id)
        
    )
    return result.scalar_one_or_none()

async def get_tasks(
    db:  AsyncSession,
    user_id: UUID,
    skip: int = 0,
    limit: int= 10,
    status: str | None = None,
    priority: str | None = None,
    search: str | None = None,
) -> tuple[list[Task], int]:
    query = select(Task).where(Task.user_id == user_id)
    
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if search:
        query = query.where(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%"),
                Task.category.ilike(f"%{search}%"),
                Task.priority.ilike(f"%{search}%"),
                Task.status.ilike(f"%{search}%"),
                Task.due_date.ilike(f"%{search}%"),
            )
        )
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    query = query.order_by(Task.due_date.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    return list(tasks), total

async def update_task(db: AsyncSession, task:Task, task_data: TaskUpdate) -> Task:
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task,field,value)
    await db.flush()
    return task

async def delete_task(db: AsyncSession, task:Task) -> None:
    await db.delete(task)
    await db.flush()
    
