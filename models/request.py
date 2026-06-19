from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedTask(BaseModel):
    title: str
    priority: Optional[str] = "Medium"
    estimated_minutes: Optional[int] = 30

class ExtractedHabit(BaseModel):
    habit_name: str
    frequency: Optional[str] = "Daily"

class ExtractedItem(BaseModel):
    item_name: str
    category: Optional[str] = "General"

class OrganizedBrainDump(BaseModel):
    # Using default values guarantees Pydantic won't crash if the AI omits a section
    tasks: List[ExtractedTask] = []
    habits: List[ExtractedHabit] = []
    shopping_cart: List[ExtractedItem] = []
    contextual_summary: Optional[str] = "Brain dump parsed successfully."

class TextInputPayload(BaseModel):
    text: str