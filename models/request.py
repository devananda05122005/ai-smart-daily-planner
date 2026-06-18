from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    name: str
    deadline: str
    duration: str
    priority: str
    energy_required: Optional[str] = "Medium"

class FixedTask(BaseModel):
    name: str
    start_time: str
    end_time: str

class PlannerRequest(BaseModel):
    tasks: List[Task]
    free_time: List[str]
    peak_hours: List[str] = []
    fixed_tasks: List[FixedTask] = []