class DatabaseOperationError(Exception):
    """Raised when a database query or connection fails."""
    pass

class AgentExecutionError(Exception):
    """Raised when the LLM/Agent fails to process a request."""
    pass

class ToolExecutionError(Exception):
    """Raised when a tool execution fails."""
    pass
