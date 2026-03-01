from dotenv import load_dotenv
import os
import uuid
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from agents import Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api
from context import UserSessionContext
from agent import main_agent

# Load environment variables
load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# Configure OpenAI client with OpenRouter
set_tracing_disabled(True)
set_default_openai_api("chat_completions")
external_client = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1"
)
set_default_openai_client(external_client)

# Create FastAPI app
app = FastAPI(title="Health Wellness Agent")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory session storage
sessions = {}


def get_or_create_session(session_id: str):
    """Get existing session or create a new one."""
    if session_id not in sessions:
        sessions[session_id] = {
            "context": UserSessionContext(name="User", uid=1),
            "history": [],
        }
    return sessions[session_id]


@app.get("/")
async def serve_index():
    """Serve the chat UI."""
    return FileResponse("static/index.html")


@app.post("/api/chat")
async def chat(request: Request):
    """Handle chat messages from the frontend."""
    try:
        body = await request.json()
        user_message = body.get("message", "").strip()
        session_id = body.get("session_id", str(uuid.uuid4()))

        if not user_message:
            return JSONResponse({"error": "Empty message"}, status_code=400)

        # Get or create session
        session = get_or_create_session(session_id)
        context = session["context"]
        history = session["history"]

        # Build input: append new user message to history
        if history:
            input_data = history.copy()
            input_data.append({"role": "user", "content": user_message})
        else:
            input_data = user_message

        # Run the agent
        runner = Runner()
        result = await runner.run(main_agent, input=input_data, context=context)

        # Extract the final output text
        agent_reply = str(result.final_output)

        # Save conversation history for next turn
        session["history"] = result.to_input_list()

        # Build context summary for the UI
        context_info = {}
        if context.goal:
            context_info["goal"] = context.goal
        if context.meal_plan:
            context_info["meal_plan"] = context.meal_plan
        if context.workout_plan:
            context_info["workout_plan"] = context.workout_plan
        if context.progress_logs:
            context_info["progress_logs"] = context.progress_logs
        if context.checkin_schedule:
            context_info["checkin_schedule"] = context.checkin_schedule

        return JSONResponse({
            "reply": agent_reply,
            "session_id": session_id,
            "context": context_info
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/reset")
async def reset_session(request: Request):
    """Reset a chat session."""
    body = await request.json()
    session_id = body.get("session_id", "")
    if session_id in sessions:
        del sessions[session_id]
    return JSONResponse({"status": "reset", "session_id": session_id})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
