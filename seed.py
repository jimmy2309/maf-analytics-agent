import os
import sys
from src.db.session import engine, SessionLocal
from src.db.models.base import Base
from src.db.models.agent_config import AgentConfig

def seed_db():
    print("Creating tables in database...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Seed Agent Configuration from Prompt File
    if db.query(AgentConfig).filter_by(agent_name="Local Researcher").count() == 0:
        print("Inserting Local Researcher Agent config...")
        prompt_path = os.path.join(os.path.dirname(__file__), "src", "prompts", "local_researcher_prompt.txt")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()
            
        agent_config = AgentConfig(
            agent_name="Local Researcher",
            system_prompt=system_prompt,
            model_name="llama3"
        )
        db.add(agent_config)
        db.commit()
        print("Agent config seeded successfully.")
    else:
        print("Agent config already exists. Skipping.")

    db.close()

if __name__ == "__main__":
    seed_db()
