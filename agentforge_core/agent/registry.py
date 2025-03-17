"""
Registro de agentes disponibles
"""

from typing import Dict, List, Optional, Union

from agentforge_core.agent.base import Agent

class AgentRegistry:
    """
    Registro centralizado de agentes disponibles
    """
    
    def __init__(self):
        self._agents: Dict[str, Agent] = {}
        
    def register(self, agent_id: str, agent: Agent) -> bool:
        """
        Registra un agente en el sistema
        
        Args:
            agent_id: ID único del agente
            agent: Instancia del agente
            
        Returns:
            bool: True si el agente fue registrado con éxito
        """
        if agent_id in self._agents:
            return False
        self._agents[agent_id] = agent
        return True
        
    def get(self, agent_id: str) -> Optional[Agent]:
        """
        Obtiene un agente por su ID
        
        Args:
            agent_id: ID del agente a buscar
            
        Returns:
            Agent: Instancia del agente o None si no existe
        """
        return self._agents.get(agent_id)
        
    def list_agents(self) -> Dict[str, Agent]:
        """
        Lista todos los agentes registrados
        
        Returns:
            dict: Diccionario con todos los agentes {id: agente}
        """
        return self._agents.copy()
        
    def remove(self, agent_id: str) -> bool:
        """
        Elimina un agente del registro
        
        Args:
            agent_id: ID del agente a eliminar
            
        Returns:
            bool: True si el agente fue eliminado con éxito
        """
        if agent_id in self._agents:
            del self._agents[agent_id]
            return True
        return False
        
    def filter_by_metadata(self, key: str, value: any) -> List[Agent]:
        """
        Filtra agentes por un valor específico de metadatos
        
        Args:
            key: Clave de metadatos a buscar
            value: Valor a comparar
            
        Returns:
            list: Lista de agentes que coinciden con el criterio
        """
        return [
            agent for agent in self._agents.values()
            if key in agent.metadata and agent.metadata[key] == value
        ]
