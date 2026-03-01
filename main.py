from dotenv import load_dotenv
import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api
from context import UserSessionContext
from agent import main_agent
from hooks import CustomRunHooks

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

# Initialize context and runner with hooks
user_context = UserSessionContext(name="User", uid=1)
runner = Runner()

# Test inputs covering all requirements
test_inputs = [
    # Test 1: Weekly Diet and Exercise Planning
    "Hi! I'm a 30-year-old male, 180cm tall, weighing 75kg. I have no medical conditions. I prefer a vegetarian diet and my fitness level is intermediate. My goal is to lose 5kg in 2 months while building muscle.",

    # Test 2: Health Report Tracking
    "I want to log my progress: My current weight is 74kg, blood pressure is 120/80, blood sugar is 90mg/dL. I completed 4 workouts this week and followed my diet plan for 6 days.",

    # Test 3: Improvement Suggestions
    "Based on my progress so far, can you give me suggestions to improve my diet and exercise routine?"
]

# Main interaction loop
async def main():
    print("=" * 70)
    print("HEALTH WELLNESS AGENT - AUTOMATED TESTING")
    print("=" * 70)
    print("\nTesting all three core requirements:")
    print("1. Weekly Diet and Exercise Planning")
    print("2. Health Report Tracking")
    print("3. Improvement Suggestions")
    print("\n" + "=" * 70 + "\n")

    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}: {['Diet & Exercise Planning', 'Health Report Tracking', 'Improvement Suggestions'][i-1]}")
        print(f"{'='*70}")
        print(f"\nUser Input:\n{user_input}\n")
        print(f"{'-'*70}")
        print("Agent Response:")
        print(f"{'-'*70}\n")

        try:
            result = await runner.run(main_agent, input=user_input, context=user_context)
            print(result)
        except Exception as e:
            print(f"ERROR: {str(e)}")

        print(f"\n{'='*70}\n")

    print("\n" + "=" * 70)
    print("TESTING COMPLETED")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
