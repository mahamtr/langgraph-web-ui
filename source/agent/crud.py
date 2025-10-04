from models import Task
from datetime import datetime
from typing import List

async def add_task(title: str, due_date: datetime | None = None, priority: str | None = None):
    """Adds a task to the TODO list.

    Args:
        title: The title of the task.
        due_date: The due date of the task.
        priority: The priority of the task.
    """
    task = Task(title=title, due_date=due_date, priority=priority)
    await task.insert()
    return task

async def list_tasks(show_completed: bool = False):
    """Lists all tasks.

    Args:
        show_completed: Whether to show completed tasks.
    """
    if show_completed:
        tasks = await Task.find_all().to_list()
    else:
        tasks = await Task.find(Task.status != "completed").to_list()
    return tasks

async def update_task_status(task_id: str, status: str):
    """Updates the status of a task.

    Args:
        task_id: The ID of the task to update.
        status: The new status of the task.
    """
    task = await Task.get(task_id)
    if task:
        task.status = status
        task.updated_at = datetime.utcnow()
        await task.save()
    return task

async def delete_task(task_id: str):
    """Deletes a task.

    Args:
        task_id: The ID of the task to delete.
    """
    task = await Task.get(task_id)
    if task:
        await task.delete()
    return task