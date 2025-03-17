"""
Clase base para frameworks de agentes
"""

from typing import Any, Dict, Optional
import logging

from agentforge_core.agent.base import Agent

# Configurar logger
logger = logging.getLogger(__name__)

class AgentFramework:
    """
    Clase base para todos los frameworks de agentes
    """
    
    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__
        self.config: Dict[str, Any] = {}
        
    def create_agent(self, agent_id: str, **kwargs) -> Agent:
        """
        Crea un agente utilizando este framework
        
        Args:
            agent_id: ID único del agente
            **kwargs: Parámetros adicionales para el agente
            
        Returns:
            Agent: Instancia del agente creado
        """
        raise NotImplementedError("Los frameworks deben implementar create_agent")
        
    def start(self) -> bool:
        """
        Inicia el framework
        
        Returns:
            bool: True si se inició correctamente
        """
        logger.info(f"Iniciando framework {self.name}")
        return True
        
    def stop(self) -> bool:
        """
        Detiene el framework
        
        Returns:
            bool: True si se detuvo correctamente
        """
        logger.info(f"Deteniendo framework {self.name}")
        return True
        
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configura el framework con parámetros específicos
        
        Args:
            config: Diccionario con la configuración
        """
        self.config.update(config)
        logger.debug(f"Framework {self.name} configurado con {len(config)} parámetros")
