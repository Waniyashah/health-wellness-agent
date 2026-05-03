from agents import function_tool, RunContextWrapper
from guaidrails import validate_relaxation_plan_output
from context import UserSessionContext

@function_tool
def relaxation_recommender(ctx: RunContextWrapper[UserSessionContext], mental_health_status: str, stressors: str = "", preferred_techniques: str = "") -> dict:
    """Suggests relaxation, stress-free, and mental wellness techniques for comprehensive health.

    Args:
        mental_health_status: User's current mental state or natural language description of how they feel (e.g., 'I feel very stressed out from work', 'I want to relax more').
        stressors: Specific reported stressors if any (e.g., 'work stress', 'anxiety', 'poor sleep').
        preferred_techniques: Any techniques they prefer (e.g., 'meditation', 'yoga', 'reading') or 'none'.

    Returns:
        A dictionary with suggested relaxation and stress-free techniques.
    """
    # Expanded logic for comprehensive mental health and stress-free recommendations
    suggestions = []
    
    combined_input = f"{mental_health_status} {stressors} {preferred_techniques}".lower()
    
    if 'sleep' in combined_input or 'insomnia' in combined_input:
        suggestions.extend(["10 minutes of deep breathing before bed", "Limit screen time 1 hour before sleep", "Try a calming chamomile tea before bed"])
    if 'work' in combined_input or 'stress' in combined_input:
        suggestions.extend(["5-minute mindfulness meditation during work breaks", "Progressive Muscle Relaxation (PMR)", "Time-blocking technique to reduce overwhelm"])
    if 'anxiety' in combined_input or 'panic' in combined_input:
        suggestions.extend(["4-7-8 breathing exercise for immediate calm", "Grounding techniques (5-4-3-2-1 method)", "Daily journaling to process anxious thoughts"])
        
    if 'yoga' in combined_input:
        suggestions.append("15 minutes of gentle restorative yoga or stretching")
    if 'meditation' in combined_input:
        suggestions.append("Daily 10-minute guided meditation")
    if 'nature' in combined_input or 'walk' in combined_input:
        suggestions.append("20-minute daily walk outdoors in nature")
        
    if not suggestions:
        # Default stress-free package
        suggestions = [
            "Daily 10-minute mindfulness meditation to build mental resilience",
            "Take short walking breaks away from your desk",
            "Practice gratitude journaling before bed",
            "Digital detox for at least 30 minutes every evening"
        ]
        
    ctx.context.relaxation_plan = suggestions
    return validate_relaxation_plan_output({"techniques": suggestions}).dict()
