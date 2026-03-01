from dotenv import load_dotenv
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api
from context import UserSessionContext
from agent import main_agent

# Load environment variables
load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY not found")

# Configure OpenAI client with OpenRouter
set_tracing_disabled(True)
set_default_openai_api("chat_completions")
external_client = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1"
)
set_default_openai_client(external_client)

# Initialize context and runner
user_context = UserSessionContext(name="User", uid=1)
runner = Runner()

# Single session test with context preservation
async def main():
    print("=" * 70)
    print("HEALTH WELLNESS AGENT - SINGLE SESSION TEST")
    print("Testing context preservation across multiple interactions")
    print("=" * 70 + "\n")

    # Test 1: Set up profile and goals
    print("\n" + "="*70)
    print("INTERACTION 1: Setting up profile and goals")
    print("="*70)
    user_input_1 = "Hi! I'm a 30-year-old male, 180cm tall, weighing 75kg. I have no medical conditions. I prefer a vegetarian diet and my fitness level is intermediate. My goal is to lose 5kg in 2 months while building muscle."
    print(f"\nUser: {user_input_1}\n")
    result_1 = await runner.run(main_agent, input=user_input_1, context=user_context)
    print(f"Agent Response:\n{result_1}\n")

    # Test 2: Log progress
    print("\n" + "="*70)
    print("INTERACTION 2: Logging health progress")
    print("="*70)
    user_input_2 = "I want to log my progress: My current weight is 74kg, blood pressure is 120/80, blood sugar is 90mg/dL. I completed 4 workouts this week and followed my diet plan for 6 days."
    print(f"\nUser: {user_input_2}\n")
    history_1 = result_1.to_input_list()
    history_1.append({"role": "user", "content": user_input_2})
    result_2 = await runner.run(main_agent, input=history_1, context=user_context)
    print(f"Agent Response:\n{result_2}\n")

    # Test 3: Request improvement suggestions
    print("\n" + "="*70)
    print("INTERACTION 3: Requesting improvement suggestions")
    print("="*70)
    user_input_3 = "Based on my progress so far, can you give me suggestions to improve my diet and exercise routine?"
    print(f"\nUser: {user_input_3}\n")
    history_2 = result_2.to_input_list()
    history_2.append({"role": "user", "content": user_input_3})
    result_3 = await runner.run(main_agent, input=history_2, context=user_context)
    print(f"Agent Response:\n{result_3}\n")

    # Display context summary
    print("\n" + "="*70)
    print("CONTEXT SUMMARY")
    print("="*70)
    print(f"Goal: {user_context.goal if hasattr(user_context, 'goal') else 'Not set'}")
    print(f"Meal Plan: {user_context.meal_plan if hasattr(user_context, 'meal_plan') else 'Not set'}")
    print(f"Workout Plan: {user_context.workout_plan if hasattr(user_context, 'workout_plan') else 'Not set'}")
    print(f"Progress Logs: {user_context.progress_logs if hasattr(user_context, 'progress_logs') else 'Not set'}")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
