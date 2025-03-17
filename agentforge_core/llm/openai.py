"""
Proveedor para OpenAI
"""

import json
import logging
from typing import Any, Dict, List, Optional, Union

from agentforge_core.llm.provider import Provider

# Configurar logger
logger = logging.getLogger(__name__)

class OpenAIProvider(Provider):
    """
    Proveedor para modelos de OpenAI
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o", **kwargs):
        super().__init__("OpenAI", api_key)
        self.model = model
        self.extra_params = kwargs
        
    def _initialize_client(self) -> None:
        """
        Inicializa el cliente de OpenAI
        """
        try:
            # Importación real para OpenAI
            import openai
            self._client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("Módulo 'openai' no encontrado. Instálalo con 'pip install openai'")
        
    async def generate(self, prompt: str, **kwargs) -> Optional[str]:
        """
        Genera una respuesta usando modelos de OpenAI
    
        Args:
            prompt: Prompt para el modelo
            **kwargs: Parámetros adicionales
        
        Returns:
            str: Respuesta generada o None si hay error
        """
        if not self._client:
            self.start()
        
        params = {
            "model": kwargs.get("model", self.model),
            "messages": [{"role": "user", "content": prompt}],
            **self.extra_params
        }
    
        # Actualizar con parámetros adicionales
        for key, value in kwargs.items():
            if key != "messages":  # Evitar conflicto con messages que ya se procesa
                params[key] = value
        
        # Eliminar messages duplicado si está en kwargs
        if "messages" in kwargs:
            params["messages"] = kwargs["messages"]
        
        try:
            # La API de OpenAI ahora devuelve directamente el objeto, no requiere await
            response = self._client.chat.completions.create(**params)
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generando respuesta con OpenAI: {e}")
            return None


    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Genera una respuesta a partir de una conversación
    
        Args:
            messages: Lista de mensajes de la conversación
            **kwargs: Parámetros adicionales
        
        Returns:
            dict: Respuesta generada
        """
        if not self._client:
            self.start()
        
        params = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            **self.extra_params
        }
    
        # Actualizar con parámetros adicionales
        for key, value in kwargs.items():
            if key != "messages":  # Evitar conflicto con messages que ya se procesa
                params[key] = value
    
        try:
            # La API de OpenAI ahora devuelve directamente el objeto, no requiere await
            response = self._client.chat.completions.create(**params)
            return {
                "content": response.choices[0].message.content,
                "role": "assistant",
                "finish_reason": response.choices[0].finish_reason,
                "raw_response": json.loads(response.model_dump_json())
            }
        except Exception as e:
            logger.error(f"Error generando chat con OpenAI: {e}")
            return {
                "content": f"Error: {str(e)}",
                "role": "error",
                "finish_reason": "error"
            }

