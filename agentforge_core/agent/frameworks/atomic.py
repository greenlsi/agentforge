"""
Integración completa con el framework Atomic Agents
Corregido el parámetro chat_message según el ejemplo
"""

import logging
from typing import Any, Dict, List, Optional, Union
import os

from agentforge_core.agent.base import Agent
from agentforge_core.agent.frameworks.base import AgentFramework

# Configurar logger
logger = logging.getLogger(__name__)

class AtomicAgent(Agent):
    """
    Implementación de agente usando Atomic Agents
    """
    
    def __init__(self, id: str, name: Optional[str] = None, role: Optional[str] = None, **kwargs):
        super().__init__(id, name, role)
        self.atomic_config = kwargs
        self._atomic_agent = None
        self._initialized = False
        self._input_schema = None
        
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa un mensaje usando el agente de Atomic Agents
        
        Args:
            message: Mensaje a procesar
            
        Returns:
            dict: Resultado del procesamiento
        """
        if not self._initialized:
            self.initialize()
            
        if not self._atomic_agent:
            return {
                "status": "error",
                "agent": self.id,
                "error": f"El agente Atomic {self.id} no ha sido inicializado correctamente",
                "input": message
            }
            
        try:
            # Obtener el contenido del mensaje
            content = message.get('content', '')
            
            # Crear la instancia correcta de InputSchema usando chat_message según el ejemplo
            if self._input_schema:
                input_data = self._input_schema(chat_message=content)
                # Procesar con el agente atómico pasando la instancia del esquema
                atomic_response = self._atomic_agent.run(input_data)
            else:
                # Alternativa: probar pasando un diccionario
                atomic_response = self._atomic_agent.run({"chat_message": content})
            
            # Construir respuesta en formato estándar
            return {
                "status": "success",
                "agent": self.id,
                "role": self.role,
                "response": atomic_response.chat_message,
                "input": message,
            }
        except Exception as e:
            logger.error(f"Error procesando mensaje en agente Atomic {self.id}: {e}")
            return {
                "status": "error",
                "agent": self.id,
                "error": str(e),
                "input": message
            }
        
    def initialize(self) -> bool:
        """
        Inicializa el agente de Atomic Agents
        
        Returns:
            bool: True si se inicializó correctamente
        """
        if self._initialized:
            return True
            
        try:
            # Obtener cliente del framework
            framework = self.get_metadata("framework")
            if not framework or not hasattr(framework, "_client") or not framework._client:
                logger.error(f"No se encontró cliente para el agente {self.id}")
                return False
                
            client = framework._client
            
            # Importar atomic_agents con la ruta correcta
            import atomic_agents as aa
            from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig
            from atomic_agents.agents.base_agent import BaseAgentInputSchema, BaseAgentOutputSchema
            
            # Obtener parámetros específicos
            system_prompt = self.atomic_config.pop("system_prompt", "")
            
            # Guardar referencia al esquema de entrada para usarlo en process()
            self._input_schema = BaseAgentInputSchema
            
            # Crear la configuración completa
            agent_config = BaseAgentConfig(
                system_prompt=system_prompt,
                client=client,
                input_schema=BaseAgentInputSchema,
                output_schema=BaseAgentOutputSchema
            )
            
            # Crear el agente con la configuración
            self._atomic_agent = BaseAgent(config=agent_config)
            
            self._initialized = True
            logger.info(f"Agente Atomic {self.id} inicializado correctamente")
            return True
        except Exception as e:
            logger.error(f"Error inicializando agente Atomic {self.id}: {e}")
            return False

    def connect_to(self, agent: "Agent") -> bool:
        """
        Conecta este agente a otro
        
        Args:
            agent: Agente al que conectarse
            
        Returns:
            bool: True si la conexión fue exitosa
        """
        # En Atomic Agents no hay un método directo para conectar agentes
        return super().connect_to(agent)

class AtomicAgentsFramework(AgentFramework):
    """
    Framework para trabajar con Atomic Agents
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("AtomicAgents")
        self.config = config or {}
        self._initialized = False
        self._client = None
        
    def create_agent(self, agent_id: str, **kwargs) -> AtomicAgent:
        """
        Crea un agente de tipo Atomic
        
        Args:
            agent_id: ID único del agente
            **kwargs: Parámetros del agente
            
        Returns:
            AtomicAgent: Instancia del agente creado
        """
        agent = AtomicAgent(agent_id, **kwargs)
        # Guardar referencia al framework en el agente
        agent.set_metadata("framework", self)
        logger.debug(f"Agente Atomic {agent_id} creado")
        return agent
        
    def start(self) -> bool:
        """
        Inicia el framework de Atomic Agents
        
        Returns:
            bool: True si se inició correctamente
        """
        if self._initialized:
            return True
            
        try:
            # Verificar que instructor está instalado
            try:
                import instructor
            except ImportError:
                logger.error("La biblioteca 'instructor' no está instalada. Es necesaria para usar atomic_agents.")
                logger.error("Instálala con: pip install instructor")
                return False
                
            # Obtener configuración
            api_key = self.config.get("api_key", None)
            model = self.config.get("model", "gpt-3.5-turbo")
            
            # Si no se proporciona API key, intentar obtenerla de la variable de entorno
            if not api_key:
                api_key = os.environ.get("OPENAI_API_KEY")
            
            # Verificar que tenemos una API key
            if not api_key:
                logger.error("No se encontró API key para OpenAI.")
                return False
            
            # Inicializar el cliente con Instructor
            from openai import OpenAI
                
            # Crear cliente con instructor
            base_client = OpenAI(api_key=api_key)
            client_with_instructor = instructor.from_openai(
                client=base_client,
                mode=instructor.Mode.TOOLS
            )
            
            # Almacenar el cliente
            self._client = client_with_instructor
            logger.info(f"Cliente OpenAI con Instructor inicializado correctamente usando modelo {model}")
            
            self._initialized = True
            logger.info(f"Framework AtomicAgents inicializado correctamente")
            return True
        except Exception as e:
            logger.error(f"Error inicializando AtomicAgentsFramework: {e}")
            return False
        
    def stop(self) -> bool:
        """
        Detiene el framework de Atomic Agents
        
        Returns:
            bool: True si se detuvo correctamente
        """
        if not self._initialized:
            return True
            
        # Liberar referencias
        self._client = None
        self._initialized = False
        logger.info(f"Framework AtomicAgents detenido correctamente")
        return True
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configura el framework con parámetros específicos
        
        Args:
            config: Diccionario con la configuración
        """
        super().configure(config)