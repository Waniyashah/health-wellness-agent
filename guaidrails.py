from pydantic import BaseModel, ValidationError
from typing import Optional, List, Dict

class Goal(BaseModel):
    goal_description: str
    action: Optional[str] = None
    quantity: Optional[float] = None
    metric: Optional[str] = None
    duration: Optional[str] = None

class MealPlan(BaseModel):
    meals: List[str]

class WorkoutPlan(BaseModel):
    exercises: Dict[str, str]

class Schedule(BaseModel):
    checkins: List[str]

class ProgressUpdate(BaseModel):
    update: Dict[str, str | int | None]

class RelaxationPlan(BaseModel):
    techniques: List[str]

def validate_goal_input(input_str: str) -> bool:
    # Allow any non-empty string so LLM can understand natural language
    return bool(input_str.strip())

def validate_goal_output(data: dict) -> Goal:
    try:
        return Goal(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid goal output format: {e}")

def validate_dietary_input(input_str: str) -> bool:
    # Allow any non-empty string to support diverse diets in human language
    return bool(input_str.strip())

def validate_meal_plan_output(data: dict) -> MealPlan:
    try:
        return MealPlan(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid meal plan output format: {e}")

def validate_workout_plan_output(data: dict) -> WorkoutPlan:
    try:
        return WorkoutPlan(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid workout plan output format: {e}")

def validate_schedule_output(data: dict) -> Schedule:
    try:
        return Schedule(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid schedule output format: {e}")

def validate_progress_update_output(data: dict) -> ProgressUpdate:
    try:
        return ProgressUpdate(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid progress update output format: {e}")

def validate_relaxation_plan_output(data: dict) -> RelaxationPlan:
    try:
        return RelaxationPlan(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid relaxation plan output format: {e}")