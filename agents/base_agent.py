from abc import ABC, abstractmethod
from typing import List, Dict

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, name: str, emoji: str, description: str):
        self.name = name
        self.emoji = emoji
        self.description = description
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass
    
    def get_display_name(self) -> str:
        """Return formatted display name"""
        return f"{self.emoji} {self.name}"
    
    def enhance_context(self, messages: List[Dict], knowledge: List[str] = None) -> List[Dict]:
        """Optionally enhance conversation context with knowledge"""
        if knowledge:
            context = f"\n\nRelevant stored facts: {', '.join(knowledge)}"
            if messages and messages[0]['role'] == 'user':
                messages[0]['content'] += context
        return messages
