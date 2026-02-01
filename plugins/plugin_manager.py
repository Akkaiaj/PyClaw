import importlib
import inspect
from typing import Dict, Callable, Any

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.commands = {}
    
    def register_plugin(self, name: str, plugin_class):
        """Register a plugin"""
        self.plugins[name] = plugin_class()
    
    def register_command(self, command: str, handler: Callable, description: str = ""):
        """Register a command handler"""
        self.commands[command] = {
            'handler': handler,
            'description': description
        }
    
    def get_plugin(self, name: str) -> Any:
        """Get plugin instance"""
        return self.plugins.get(name)
    
    def list_commands(self) -> str:
        """List all registered commands"""
        return '\n'.join([f"/{cmd} - {info['description']}" 
                         for cmd, info in self.commands.items()])
    
    async def execute_command(self, command: str, *args, **kwargs):
        """Execute a plugin command"""
        if command in self.commands:
            return await self.commands[command]['handler'](*args, **kwargs)
        return None
