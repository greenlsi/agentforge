"""
Clase base para proveedores de LLM
"""

import logging
from typing import Any, Dict, List, Optional, Union

# Configurar logger
logger = logging.getLogger(__name__)

class Provider:
    """
    Clase base para todos los proveedores de LLM
    
    Attributes:
        name (str): Nombre del proveedor
        api_key (str): Clave API para el proveedor
    """
    
    def __init__(self, name: str, api_key: Optional[str] = None):
        self.name = name
        self.api_key = api_key
        self._client = None
        
    def start(self) -> bool:
        """
        Inicializa el cliente del proveedor
        
        Returns:
            bool: True si se inicializó correctamente
        """
        if self._client:
            return True
            
        try:
            self._initialize_client()
            logger.info(f"Proveedor {self.name} inicializado correctamente")
            return True
        except Exception as e:
            logger.error(f"Error inicializando proveedor {self.name}: {e}")
            return False
    
    def stop(self) -> bool:
        """
        Cierra el cliente del proveedor
        
        Returns:
            bool: True si se cerró correctamente
        """
        self._client = None
        logger.info(f"Proveedor {self.name} detenido")
        return True
        
    def _initialize_client(self) -> None:
        """
        Inicializa el cliente del proveedor (a implementar por subclases)
        """
        raise NotImplementedError("Los proveedores deben implementar _initialize_client")
        
    async def generate(self, prompt: str, **kwargs) -> Optional[str]:
        """
        Genera una respuesta a partir de un prompt
        
        Args:
            prompt: Prompt para el LLM
            **kwargs: Parámetros adicionales
            
        Returns:
            str: Respuesta generada o None si hay error
        """
        raise NotImplementedError("Los proveedores deben implementar generate")
        
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Genera una respuesta a partir de una conversación
        
        Args:
            messages: Lista de mensajes de la conversación
            **kwargs: Parámetros adicionales
            
        Returns:
            dict: Respuesta generada
        """
        raise NotImplementedError("Los proveedores deben implementar chat")
