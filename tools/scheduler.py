from pydantic import BaseModel
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

# Define input model
class ScheduleInput(BaseModel):
    pass

# Define output model
class ScheduleOutput(BaseModel):
    checkins: list[str]

@function_tool
def checkin_scheduler(ctx: RunContextWrapper[UserSessionContext], input_data: ScheduleInput) -> ScheduleOutput:
    """Schedules recurring weekly progress checks.

    Args:
        input_data: A dictionary with scheduling preferences (currently unused).

    Returns:
        A structured list of scheduled check-in times.
    """
    checkins = ["Monday 8 AM", "Thursday 8 AM"]
    ctx.context.checkin_schedule = checkins
    return ScheduleOutput(checkins=checkins)
