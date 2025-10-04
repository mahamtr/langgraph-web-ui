from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import react_graph
from database import init_db
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Optional
from crud import add_task,list_tasks,delete_task,update_task_status


import asyncio

app = FastAPI(title="TODO Planner Agent")

# Pydantic models for various endpoints
class UserPrompt(BaseModel):
    text: str

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await init_db()

@app.post("/chat")
async def chat(prompt: UserPrompt):
    messages = [HumanMessage(content=prompt.text)]
    response = await react_graph.ainvoke({"messages": messages})
    return {"response": response}

@app.get("/tasks")
async def get_tasks(show_completed: Optional[bool] = False):

    tasks = await list_tasks(show_completed=show_completed)
    try:
        return [t.dict() for t in tasks]
    except Exception:
        return tasks

