from pydantic import BaseModel
from agents import function_tool
from guaidrails import validate_progress_update_output

class ProgressUpdate(BaseModel):
    weight: str | None = None
    date: str | None = None

@function_tool
def progress_tracker(update: ProgressUpdate) -> dict:
    """Tracks user progress and updates session context.

    Args:
        update: A dictionary with progress updates (e.g., {'weight': '70kg', 'date': '2025-07-01'}).

    Returns:
        A dictionary with the progress update.
    """
    return validate_progress_update_output({"update": update}).dict()
