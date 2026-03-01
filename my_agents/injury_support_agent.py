
from agents import Agent

injury_support_agent = Agent(
    name="InjurySupport",
    instructions="You are an injury support assistant. Provide workout plans tailored for users with physical limitations or injuries, ensuring safety and recovery.",
    model="openai/gpt-3.5-turbo"
)