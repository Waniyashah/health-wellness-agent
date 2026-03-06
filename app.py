from dotenv import load_dotenv
import os
import sys
import uuid
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from agents import Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api
from context import UserSessionContext
from agent import main_agent

# Load environment variables
load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# Configure OpenAI client with OpenRouter (only if key is available)
if openrouter_api_key:
    set_tracing_disabled(True)
    set_default_openai_api("chat_completions")
    external_client = AsyncOpenAI(
        api_key=openrouter_api_key,
        base_url="https://openrouter.ai/api/v1"
    )
    set_default_openai_client(external_client)
else:
    print("WARNING: OPENROUTER_API_KEY not found. Chat functionality will not work.", file=sys.stderr)

# Create FastAPI app
app = FastAPI(title="Health Wellness Agent")

# Determine the base directory (handles Vercel's file structure)
BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR / "static"

# Mount static files
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

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
    index_path = BASE_DIR / "static" / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    else:
        # Vercel extracts static files from the Lambda bundle, so we can redirect to the static Edge URL
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/static/index.html")


@app.post("/api/chat")
async def chat(request: Request):
    """Handle chat messages from the frontend."""
    try:
        if not openrouter_api_key:
            return JSONResponse({"error": "OPENROUTER_API_KEY not configured. Please add it to your Vercel environment variables."}, status_code=500)

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


# Vercel will automatically find the `app` variable which is our FastAPI instance

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
