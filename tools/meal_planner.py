from agents import function_tool, RunContextWrapper
from guaidrails import validate_dietary_input, validate_meal_plan_output
from context import UserSessionContext
import asyncio
from duckduckgo_search import DDGS
import warnings
import random

warnings.filterwarnings("ignore", module="duckduckgo_search")

REAL_MEALS = {
    'vegetarian': ["Avocado Toast with Egg", "Quinoa Salad", "Vegetable Stir-fry", "Lentil Soup", "Paneer Tikka", "Mushroom Risotto", "Greek Salad", "Caprese Sandwich", "Stuffed Bell Peppers", "Eggplant Parmesan"],
    'vegan': ["Oatmeal with Berries", "Chickpea Salad Sandwich", "Tofu Scramble", "Vegan Buddha Bowl", "Black Bean Burgers", "Vegan Mac and Cheese", "Chia Pudding", "Lentil Shepherd's Pie", "Vegan Pad Thai", "Falafel Wrap"],
    'keto': ["Bacon and Eggs", "Caesar Salad (no croutons)", "Keto Zucchini Noodles", "Grilled Salmon with Asparagus", "Keto Chicken Parmesan", "Avocado Chicken Salad", "Keto Meatballs", "Steak and Broccoli", "Keto Taco Salad", "Pork Chops with Cabbage"],
    'gluten-free': ["Gluten-Free Pancakes", "Chicken and Rice", "Gluten-Free Pasta", "Quinoa Bowl", "Steak and Sweet Potato", "Gluten-Free Pizza", "Chicken Salad", "Shrimp Tacos on Corn Tortillas", "Baked Salmon", "Turkey Chili"],
    'diabetic': ["Scrambled Eggs with Spinach", "Grilled Chicken Salad", "Baked Cod with Broccoli", "Turkey Chili", "Greek Yogurt with Almonds", "Tuna Salad", "Zucchini Noodles with Meat Sauce", "Grilled Tofu", "Roasted Chicken and Vegetables", "Quinoa and Black Beans"],
    'balanced': ["Oatmeal with Fruit", "Cucumber Salad", "Grilled Chicken and Quinoa", "Salmon and Sweet Potato", "Turkey Wrap", "Mixed Bean Salad", "Chicken Stir-fry", "Beef and Broccoli", "Greek Yogurt with Honey", "Tuna Salad Sandwich", "Shrimp and Brown Rice"],
    'default': ["Cucumber Salad", "Grilled Chicken Bowl", "Vegetable Soup", "Avocado Turkey Wrap", "Baked Salmon with Asparagus", "Greek Yogurt with Berries", "Egg White Omelette", "Quinoa Salad", "Tofu Stir-fry", "Steak and Green Beans"]
}

@function_tool
async def meal_planner(ctx: RunContextWrapper[UserSessionContext], diet_preferences: str) -> dict:
    """Generates a 7-day meal plan based on dietary preferences.

    Args:
        diet_preferences: The user's dietary preferences (e.g., 'vegetarian', 'vegan').

    Returns:
        A dictionary with a list of meal suggestions for 7 days.
    """
    if not validate_dietary_input(diet_preferences):
        raise ValueError("Invalid dietary preference. Use: 'vegetarian', 'vegan', 'keto', 'gluten-free', or 'diabetic'")
    
    meals = []
    try:
        # Search the internet for best meals matching the diet preference
        # Run synchronous web search in a thread to not block event loop
        def search():
            with DDGS() as ddgs:
                results = ddgs.text(f"best {diet_preferences} healthy meals recipes", max_results=10)
                if results:
                    return [r['title'] for r in results]
            return []
            
        found_meals = await asyncio.to_thread(search)
        if found_meals:
            # Filter out obvious article titles, keep ones that might be recipes
            for m in found_meals:
                if "recipe" not in m.lower() or len(m.split()) < 10:
                    meals.append(m.split(' | ')[0].split(' - ')[0])
    except Exception as e:
        pass

    # Fallback to generic names if search fails or doesn't return enough meals
    diet_key = diet_preferences.lower()
    fallback_list = REAL_MEALS.get(diet_key, REAL_MEALS['default'])
    
    available_meals = list(fallback_list)
    random.shuffle(available_meals)

    while len(meals) < 7:
        if available_meals:
            meals.append(available_meals.pop())
        else:
            meals.append(f"{diet_preferences.capitalize()} Meal {len(meals)+1}")
        
    # Ensure exactly 7 meals
    meals = meals[:7]
    
    ctx.context.meal_plan = meals
    return validate_meal_plan_output({"meals": meals}).dict()