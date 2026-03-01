
from agents import function_tool, RunContextWrapper
from guaidrails import Goal, validate_workout_plan_output
from context import UserSessionContext

@function_tool
def workout_recommender(ctx: RunContextWrapper[UserSessionContext], goal: Goal) -> dict:
    """Suggests a workout plan based on parsed goals and experience.

    Args:
        goal: A Goal model containing the parsed goal (e.g., {'action': 'lose', 'quantity': 5, 'metric': 'kg'}).

    Returns:
        A dictionary with the workout plan.
    """
    # Mock implementation (replace with model-based generation)
    exercises = {
        "Monday": "Strength Training",
        "Wednesday": "Cardio",
        "Friday": "Yoga"
    }
    ctx.context.workout_plan = exercises
    return validate_workout_plan_output({"exercises": exercises}).dict()
