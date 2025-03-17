"""
Framework para agentes personalizados
"""

import logging
from typing import Any, Callable, Dict, Optional

from agentforge_core.agent.base import Agent
from agentforge_core.agent.frameworks.base import AgentFramework

# Configurar logger
logger = logging.getLogger(__name__)

class CustomAgent(Agent):
    """
    Agente personalizado con funcionalidad definida por el usuario
    """
    
    def __init__(self, id: str, name: Optional[str] = None, role: Optional[str] = None, 
                 processor: Optional[Callable] = None):
        super().__init__(id, name, role)
        self.processor = processor
        
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa un mensaje usando la función processor definida por el usuario
        
        Args:
            message: Mensaje a procesar
            
        Returns:
            dict: Resultado del procesamiento
        """
        if not self.processor:
            logger.warning(f"Agente {self.id} no tiene processor definido")
            return {
                "status": "error",
                "agent": self.id,
                "error": "No processor function defined",
                "input": message
            }
            
        try:
            if callable(self.processor):
                result = await self.processor(self, message)
                
                # Asegurar que el resultado tenga un formato estándar
                if isinstance(result, dict):
                    if "status" not in result:
                        result["status"] = "success"
                    if "agent" not in result:
                        result["agent"] = self.id
                    return result
                else:
                    return {
                        "status": "success",
                        "agent": self.id,
                        "response": result,
                        "input": message
                    }
            else:
                raise TypeError("El processor no es una función válida")
        except Exception as e:
            logger.error(f"Error procesando mensaje en agente Custom {self.id}: {e}")
            return {
                "status": "error",
                "agent": self.id,
                "error": str(e),
                "input": message
            }

class CustomAgentFramework(AgentFramework):
    """
    Framework para crear agentes personalizados
    """
    
    def __init__(self):
        super().__init__("CustomAgents")
        
    def create_agent(self, agent_id: str, **kwargs) -> CustomAgent:
        """
        Crea un agente personalizado
        
        Args:
            agent_id: ID único del agente
            processor: Función que procesa los mensajes
            **kwargs: Parámetros adicionales
            
        Returns:
            CustomAgent: Instancia del agente creado
        """
        processor = kwargs.pop("processor", None)
        agent = CustomAgent(agent_id, processor=processor, **kwargs)
        logger.debug(f"Agente Custom {agent_id} creado")
        return agent
