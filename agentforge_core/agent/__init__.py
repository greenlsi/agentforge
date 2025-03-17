"""
Módulo principal para la gestión de agentes
"""

from agentforge_core.agent.base import Agent
from agentforge_core.agent.registry import AgentRegistry
from agentforge_core.agent.system import AgentSystem

__all__ = ["Agent", "AgentRegistry", "AgentSystem"]
