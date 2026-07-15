from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .custom_exceptions import DatabaseOperationError, AgentExecutionError, ToolExecutionError
from src.utils.logger import system_logger

def register_exception_handlers(app: FastAPI):
    
    @app.exception_handler(DatabaseOperationError)
    async def db_error_handler(request: Request, exc: DatabaseOperationError):
        system_logger.error(f"Database Error: {exc}")
        return JSONResponse(status_code=500, content={"error": "A database operation failed.", "details": str(exc)})

    @app.exception_handler(AgentExecutionError)
    async def agent_error_handler(request: Request, exc: AgentExecutionError):
        system_logger.error(f"Agent Error: {exc}")
        return JSONResponse(status_code=502, content={"error": "The AI Agent encountered an issue.", "details": str(exc)})

    @app.exception_handler(ToolExecutionError)
    async def tool_error_handler(request: Request, exc: ToolExecutionError):
        system_logger.error(f"Tool Error: {exc}")
        return JSONResponse(status_code=400, content={"error": "Tool execution failed.", "details": str(exc)})

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        system_logger.critical(f"Unhandled Global Exception: {exc}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "An unexpected system error occurred."})
