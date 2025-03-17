"""
Módulo para diferentes frameworks de agentes
"""

from agentforge_core.agent.frameworks.base import AgentFramework
from agentforge_core.agent.frameworks.atomic import AtomicAgentsFramework
from agentforge_core.agent.frameworks.custom import CustomAgentFramework

__all__ = ["AgentFramework", "AtomicAgentsFramework", "CustomAgentFramework"]
