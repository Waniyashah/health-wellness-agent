from pydantic import BaseModel
from agents import function_tool, RunContextWrapper
from guaidrails import validate_progress_update_output
from context import UserSessionContext

class ProgressUpdate(BaseModel):
    weight: str | None = None
    blood_pressure: str | None = None
    blood_sugar: str | None = None
    workouts_completed: int | None = None
    diet_adherence_days: int | None = None
    date: str | None = None
    notes: str | None = None

@function_tool
def progress_tracker(ctx: RunContextWrapper[UserSessionContext], update: ProgressUpdate) -> dict:
    """Tracks user progress and updates session context.

    Args:
        update: A ProgressUpdate object with health metrics including:
            - weight: Current weight (e.g., '74kg')
            - blood_pressure: Blood pressure reading (e.g., '120/80')
            - blood_sugar: Blood sugar level (e.g., '90mg/dL')
            - workouts_completed: Number of workouts completed this week
            - diet_adherence_days: Number of days followed diet plan
            - date: Date of the update
            - notes: Any additional notes

    Returns:
        A dictionary with the progress update.
    """
    update_dict = update.model_dump(exclude_none=True)
    if ctx.context.progress_logs is None:
        ctx.context.progress_logs = []
    ctx.context.progress_logs.append(update_dict)
    return validate_progress_update_output({"update": update_dict}).dict()
