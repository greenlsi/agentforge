"""
Sistema central de gestión de agentes
"""

from typing import Any, Dict, List, Optional, Type, Union
import asyncio
import logging

from agentforge_core.agent.base import Agent
from agentforge_core.agent.registry import AgentRegistry
from agentforge_core.llm.provider import Provider

# Configurar logger
logger = logging.getLogger(__name__)

class AgentSystem:
    """
    Sistema central para la gestión de agentes, proveedores y frameworks
    """
    
    def __init__(self):
        self.registry = AgentRegistry()
        self.providers: Dict[str, Provider] = {}
        self.framework = None
        self._running = False
        self._default_provider = None
        
    def add_provider(self, provider: Provider) -> bool:
        """
        Añade un proveedor de LLM al sistema
        
        Args:
            provider: Proveedor de LLM
            
        Returns:
            bool: True si se añadió correctamente
        """
        self.providers[provider.name] = provider
        
        # Establecer como proveedor por defecto si es el primero
        if len(self.providers) == 1:
            self._default_provider = provider.name
            
        return True
        
    def set_default_provider(self, provider_name: str) -> bool:
        """
        Establece el proveedor por defecto
        
        Args:
            provider_name: Nombre del proveedor
            
        Returns:
            bool: True si se estableció correctamente
        """
        if provider_name not in self.providers:
            return False
        self._default_provider = provider_name
        return True
        
    def get_provider(self, name: Optional[str] = None) -> Optional[Provider]:
        """
        Obtiene un proveedor por su nombre o el proveedor por defecto
        
        Args:
            name: Nombre del proveedor o None para el proveedor por defecto
            
        Returns:
            Provider: Instancia del proveedor o None si no existe
        """
        if name:
            return self.providers.get(name)
        elif self._default_provider:
            return self.providers.get(self._default_provider)
        return None
        
    def set_framework(self, framework) -> None:
        """
        Establece el framework de agentes a utilizar
        
        Args:
            framework: Framework de agentes
        """
        self.framework = framework
        
    def create_agent(self, agent_id: str, **kwargs) -> Agent:
        """
        Crea un nuevo agente en el sistema
        
        Args:
            agent_id: ID único del agente
            **kwargs: Parámetros adicionales para el agente
            
        Returns:
            Agent: Instancia del agente creado
        """
        if not self.framework:
            raise ValueError("No se ha establecido un framework de agentes")
            
        agent = self.framework.create_agent(agent_id, **kwargs)
        self.registry.register(agent_id, agent)
        return agent
        
    def start(self) -> bool:
        """
        Inicia el sistema de agentes
        
        Returns:
            bool: True si el sistema se inició correctamente
        """
        if self._running:
            return False
            
        # Iniciar todos los proveedores
        for provider_name, provider in self.providers.items():
            try:
                provider.start()
                logger.info(f"Proveedor {provider_name} iniciado correctamente")
            except Exception as e:
                logger.error(f"Error iniciando proveedor {provider_name}: {e}")
                
        # Iniciar framework
        if self.framework:
            try:
                self.framework.start()
                logger.info(f"Framework {self.framework.name} iniciado correctamente")
            except Exception as e:
                logger.error(f"Error iniciando framework {self.framework.name}: {e}")
            
        self._running = True
        return True
        
    def stop(self) -> bool:
        """
        Detiene el sistema de agentes
        
        Returns:
            bool: True si el sistema se detuvo correctamente
        """
        if not self._running:
            return False
            
        # Detener framework
        if self.framework:
            try:
                self.framework.stop()
                logger.info(f"Framework {self.framework.name} detenido correctamente")
            except Exception as e:
                logger.error(f"Error deteniendo framework {self.framework.name}: {e}")
            
        # Detener todos los proveedores
        for provider_name, provider in self.providers.items():
            try:
                provider.stop()
                logger.info(f"Proveedor {provider_name} detenido correctamente")
            except Exception as e:
                logger.error(f"Error deteniendo proveedor {provider_name}: {e}")
            
        self._running = False
        return True
        
    async def process_message(self, agent_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa un mensaje enviándolo a un agente específico
        
        Args:
            agent_id: ID del agente destinatario
            message: Mensaje a procesar
            
        Returns:
            dict: Respuesta del agente
        """
        agent = self.registry.get(agent_id)
        if not agent:
            raise ValueError(f"Agente {agent_id} no encontrado")
            
        try:
            result = await agent.process(message)
            return result
        except Exception as e:
            logger.error(f"Error procesando mensaje en agente {agent_id}: {e}")
            return {
                "status": "error",
                "agent": agent_id,
                "error": str(e)
            }
            
    async def broadcast_message(self, message: Dict[str, Any], filter_func=None) -> Dict[str, Dict[str, Any]]:
        """
        Envía un mensaje a múltiples agentes
        
        Args:
            message: Mensaje a enviar
            filter_func: Función para filtrar los agentes destinatarios
            
        Returns:
            dict: Diccionario con las respuestas de cada agente {id: respuesta}
        """
        agents = self.registry.list_agents()
        
        if filter_func:
            agents = {agent_id: agent for agent_id, agent in agents.items() if filter_func(agent)}
            
        tasks = {
            agent_id: asyncio.create_task(agent.process(message.copy()))
            for agent_id, agent in agents.items()
        }
        
        # Esperar a que todas las tareas terminen
        results = {}
        for agent_id, task in tasks.items():
            try:
                results[agent_id] = await task
            except Exception as e:
                logger.error(f"Error en broadcast a agente {agent_id}: {e}")
                results[agent_id] = {
                    "status": "error",
                    "agent": agent_id,
                    "error": str(e)
                }
                
        return results
