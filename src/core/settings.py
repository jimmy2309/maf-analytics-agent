import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")

    @classmethod
    def validate(cls):
        missing = []
        if not cls.DATABASE_URL:
            missing.append("DATABASE_URL")
        if not cls.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
        if not cls.MCP_SERVER_URL:
            missing.append("MCP_SERVER_URL")
            
        if missing:
            raise ValueError(f"CRITICAL ERROR: Missing environment variables in .env: {', '.join(missing)}")

# Validate settings on module import
Settings.validate()
