from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from taskpilot.core import prioritize, rank_tasks

app = FastAPI(title="TaskPilot API", version="1.0.0")

class Task(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""
    impact: int = Field(default=3, ge=1, le=5)
    effort: int = Field(default=3, ge=1, le=5)
    due_date: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/prioritize")
def classify(task: Task):
    try:
        return prioritize(task.model_dump(exclude_none=True))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.post("/rank")
def rank(tasks: list[Task]):
    try:
        return rank_tasks([task.model_dump(exclude_none=True) for task in tasks])
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
