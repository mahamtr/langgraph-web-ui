from beanie import Document
from datetime import datetime

class Task(Document):
    title: str
    status: str = "pending"
    due_date: datetime | None = None
    priority: str | None = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "tasks"