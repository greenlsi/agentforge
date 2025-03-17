"""
Clase base para todos los agentes
"""

from typing import Any, Dict, List, Optional, Union

class Agent:
    """
    Clase base para todos los agentes en el sistema
    
    Attributes:
        id (str): Identificador único del agente
        name (str): Nombre legible del agente
        role (str): Descripción del rol del agente
        connections (list): Lista de agentes conectados
    """
    
    def __init__(self, id: str, name: Optional[str] = None, role: Optional[str] = None):
        self.id = id
        self.name = name or id
        self.role = role or ""
        self.connections: List["Agent"] = []
        self.metadata: Dict[str, Any] = {}
        
    def connect_to(self, agent: "Agent") -> bool:
        """
        Conecta este agente a otro
        
        Args:
            agent: Agente al que conectarse
            
        Returns:
            bool: True si la conexión fue exitosa
        """
        if agent not in self.connections:
            self.connections.append(agent)
            return True
        return False
        
    async def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa un mensaje recibido
        
        Args:
            message: Mensaje a procesar
            
        Returns:
            dict: Resultado del procesamiento
        """
        raise NotImplementedError("Los agentes deben implementar el método process")
        
    def set_metadata(self, key: str, value: Any) -> None:
        """
        Establece un valor de metadatos para el agente
        
        Args:
            key: Clave del metadato
            value: Valor a almacenar
        """
        self.metadata[key] = value
        
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de metadatos del agente
        
        Args:
            key: Clave del metadato
            default: Valor por defecto si no existe
            
        Returns:
            El valor del metadato o el valor por defecto
        """
        return self.metadata.get(key, default)
