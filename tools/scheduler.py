from pydantic import BaseModel
from agents import function_tool
# Define input model
class ScheduleInput(BaseModel):
    pass

# Define output model
class ScheduleOutput(BaseModel):
    checkins: list[str]

@function_tool
def checkin_scheduler(input_data: ScheduleInput) -> ScheduleOutput:
    """Schedules recurring weekly progress checks.

    Args:
        input_data: A dictionary with scheduling preferences (currently unused).

    Returns:
        A structured list of scheduled check-in times.
    """
    checkins = ["Monday 8 AM", "Thursday 8 AM"]
    return ScheduleOutput(checkins=checkins)
