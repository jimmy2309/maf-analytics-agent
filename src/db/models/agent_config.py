from sqlalchemy import Column, Integer, String, Text, Boolean
from .base import Base

class AgentConfig(Base):
    __tablename__ = "agents_config"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, unique=True, index=True, nullable=False)
    system_prompt = Column(Text, nullable=False)
    model_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
