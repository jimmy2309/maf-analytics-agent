from fastapi import FastAPI
from pydantic import BaseModel
from src.modules.agent.services import AnalyticsAgentService
from src.exceptions.handlers import register_exception_handlers
from src.utils.logger import system_logger

app = FastAPI(title="MAF Analytics Agent (Local Researcher)")

# Register global exception handlers
register_exception_handlers(app)

# Initialize the agent service once for the application
try:
    agent_service = AnalyticsAgentService()
except Exception as e:
    system_logger.critical(f"App Startup Failed: {e}")
    # In a real app we might want to crash here, but for POC we let it run 
    # so we can see the logs/errors.
    agent_service = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    if not agent_service:
        raise Exception("Agent Service failed to initialize.")
    
    reply = await agent_service.process_chat(request.message)
    return ChatResponse(reply=reply)

@app.get("/")
def read_root():
    return {"message": "Welcome to maf-analytics-agent API. Use POST /chat to interact."}
