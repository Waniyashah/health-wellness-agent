from agents import function_tool, RunContextWrapper
from guaidrails import validate_goal_input, validate_goal_output
from context import UserSessionContext
import re

@function_tool
def goal_analyzer(ctx: RunContextWrapper[UserSessionContext], input_data: str) -> dict:
    """Analyzes user's fitness goal and extracts structured information.

    Args:
        input_data: The user's goal statement (e.g., 'lose 5kg in 2 months').

    Returns:
        A dictionary with the structured goal.
    """
    if not validate_goal_input(input_data):
        raise ValueError("Invalid goal format. Use: '[lose/gain] [number] [kg/lbs] in [number] [months/weeks]'")

    # Use regex to extract goal components
    pattern = r"(lose|gain)\s+(\d+\.?\d*)\s*(kg|lbs|pounds)\s*(?:in)?\s*(\d+)\s*(months|weeks)"
    match = re.search(pattern, input_data.lower())

    if not match:
        raise ValueError("Could not parse goal from input")

    action, quantity, metric, duration_num, duration_unit = match.groups()

    goal = {
        "action": action,
        "quantity": float(quantity),
        "metric": metric,
        "duration": f"{duration_num} {duration_unit}"
    }
    ctx.context.goal = goal
    return validate_goal_output(goal).dict()