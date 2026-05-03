from agents import function_tool, RunContextWrapper
from guaidrails import validate_goal_output
from context import UserSessionContext

from typing import Optional

@function_tool
def goal_analyzer(
    ctx: RunContextWrapper[UserSessionContext], 
    goal_description: str,
    action: str = "", 
    quantity: str = "", 
    metric: str = "", 
    duration: str = ""
) -> dict:
    """Analyzes user's fitness and wellness goal from their natural language input.

    Args:
        goal_description: The full natural language description of the user's goal (e.g. 'I want to lose 5 kg in 1 month').
        action: Extracted action (e.g., 'lose', 'gain', 'maintain', 'improve') if applicable.
        quantity: Extracted numerical value as a string (e.g., '5') if applicable.
        metric: Extracted unit of measurement (e.g., 'kg', 'lbs', 'level') if applicable.
        duration: Extracted timeframe for the goal (e.g., '2 months', '1 week', 'ongoing') if applicable.

    Returns:
        A dictionary with the structured goal.
    """
    parsed_quantity = None
    if quantity:
        try:
            parsed_quantity = float(quantity)
        except ValueError:
            pass

    goal = {
        "goal_description": goal_description,
        "action": action if action else None,
        "quantity": parsed_quantity,
        "metric": metric if metric else None,
        "duration": duration if duration else None
    }
    ctx.context.goal = goal
    return validate_goal_output(goal).dict()