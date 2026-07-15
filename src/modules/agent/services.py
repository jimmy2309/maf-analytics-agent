import os
import json
import httpx
from openai import AsyncOpenAI
from src.core.settings import Settings
from src.db.session import SessionLocal
from src.db.models.agent_config import AgentConfig
from src.utils.logger import conversation_logger, tool_logger, system_logger
from src.exceptions.custom_exceptions import AgentExecutionError, DatabaseOperationError, ToolExecutionError

class AnalyticsAgentService:
    def __init__(self):
        try:
            self.client = AsyncOpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=Settings.GROQ_API_KEY
            )
            self.mcp_base_url = Settings.MCP_SERVER_URL
        except Exception as e:
            system_logger.error(f"Failed to initialize Agent Service: {e}")
            raise AgentExecutionError("Failed to initialize the Analytics Agent.")

    async def _fetch_tools_schemas(self):
        """Fetches the available tool schemas from the MCP Server."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.mcp_base_url}/api/v1/tools")
                response.raise_for_status()
                data = response.json()
                return data.get("tools", [])
        except Exception as e:
            system_logger.error(f"Failed to fetch tool schemas from MCP server: {e}")
            raise ToolExecutionError("Could not retrieve tools from MCP server.")

    async def _execute_mcp_tool(self, function_name: str, function_args: dict) -> str:
        """Sends a request to the MCP server to execute a specific tool."""
        try:
            payload = {
                "tool_name": function_name,
                "arguments": function_args
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.mcp_base_url}/api/v1/tools/execute", json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("result", str(data))
        except Exception as e:
            system_logger.error(f"MCP Tool execution failed ({function_name}): {e}")
            raise ToolExecutionError(f"Execution failed on MCP server for {function_name}.")

    def _get_agent_prompt(self) -> str:
        db = SessionLocal()
        try:
            config = db.query(AgentConfig).filter_by(agent_name="Local Researcher").first()
            if not config:
                raise DatabaseOperationError("AgentConfig 'Local Researcher' not found in database.")
            return config.system_prompt
        except Exception as e:
            system_logger.error(f"Error fetching agent prompt from DB: {e}")
            raise DatabaseOperationError("Failed to retrieve agent configuration from database.")
        finally:
            db.close()

    async def process_chat(self, user_message: str) -> str:
        conversation_logger.info(f"User: {user_message}")
        
        try:
            system_prompt = self._get_agent_prompt()
            tools_schema = await self._fetch_tools_schemas()
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Step 1: Call Groq
            response = await self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages,
                tools=tools_schema,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            
            # Step 2: Check for tool calls
            if response_message.tool_calls:
                messages.append(response_message)
                
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    tool_logger.info(f"Requesting MCP Server to execute Tool: {function_name} with args {function_args}")
                    
                    try:
                        tool_result = await self._execute_mcp_tool(function_name, function_args)
                        tool_logger.info(f"MCP Tool Result ({function_name}): {tool_result}")
                    except Exception as te:
                        tool_logger.error(f"MCP Tool Execution Failed ({function_name}): {te}")
                        tool_result = f"Tool execution failed: {str(te)}"
                        
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(tool_result)
                    })
                    
                # Final LLM call
                final_response = await self.client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=messages
                )
                final_content = final_response.choices[0].message.content
                conversation_logger.info(f"Agent (After Tools): {final_content}")
                return final_content
                
            final_content = response_message.content
            conversation_logger.info(f"Agent: {final_content}")
            return final_content
            
        except Exception as e:
            system_logger.error(f"Error during agent chat processing: {e}", exc_info=True)
            raise AgentExecutionError("Agent processing failed.")
