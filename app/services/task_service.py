from fastapi import HTTPException, status
from sqlalchemy.ext.asychio import AsyncSession
from uuid import UUID

from app.repositories  import task_repo
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import Task


async def create_task(db:AsyncSession, user_id: UUID, task_data:TaskCreate) ->  Task:
    return await task_repo.create_task(db,task_data, user_id)

async def  get_tasks(
    db:AsyncSession,
    user_id: UUID,
    skip: int=0,
    limit: int=10,
    status: str | None = None,
    priority: str |  None=None,
    search: str | None = None
) -> dict:
    tasks, total = await  task_repo.get_tasks(db,user_id,skip,limit,status,priority,search)
    return  {
        "items": tasks,
        "total": total,
        "page": skip // limit + 1 if limit else 1,
        "size": limit,
        
    }
    
async def update_task(db:AsyncSession, task_id: UUID, user_id: UUID, task_data: TaskUpdate)-> Task:
    task  =  await get_tasks(db,user_id,task_id)
    return await task_repo.update_task(db,task,task_data)

async def delete_task(db:AsyncSession, task_id: UUID, user_id: UUID)-> None:
    task = await task_repo.get_tasks(db,user_id,task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await task_repo.delete_task(db,task)