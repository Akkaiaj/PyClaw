from agents.friendly import FriendlyAgent
from agents.expert import ExpertAgent
from agents.researcher import ResearcherAgent
from agents.creative import CreativeAgent

AGENTS = {
    'friendly': FriendlyAgent(),
    'expert': ExpertAgent(),
    'researcher': ResearcherAgent(),
    'creative': CreativeAgent()
}

def get_agent(agent_name: str):
    """Get agent by name"""
    return AGENTS.get(agent_name, AGENTS['friendly'])

def list_agents() -> str:
    """List all available agents"""
    return '\n'.join([f"/{key} - {agent.get_display_name()}: {agent.description}" 
                      for key, agent in AGENTS.items()])
