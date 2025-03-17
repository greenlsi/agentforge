#!/usr/bin/env python3
"""
Ejemplo de uso del framework AgentForge
"""

import asyncio
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

from agentforge_core import AgentSystem
from agentforge_core.llm import OpenAIProvider
from agentforge_core.agent.frameworks import AtomicAgentsFramework, CustomAgentFramework

# Cargar variables de entorno (.env en directorio actual o padres)
dotenv_path = Path('.env')
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    # Buscar en directorios superiores
    parent = Path().absolute()
    for _ in range(3):  # Buscar hasta 3 niveles arriba
        parent = parent.parent
        dotenv_path = parent / '.env'
        if dotenv_path.exists():
            load_dotenv(dotenv_path=dotenv_path)
            break
    else:
        print("ADVERTENCIA: No se encontró archivo .env - Se usarán variables de entorno del sistema si existen")
        load_dotenv()  # Intentar cargar de todas formas

# Configurar logging
logging.basicConfig(
    level=getattr(logging, os.getenv("AGENTFORGE_LOG_LEVEL", "INFO").upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Definir un procesador simple para el agente Custom
async def simple_processor(agent, message):
    """Procesador simple que usa el LLM del sistema para responder"""
    system = agent.get_metadata("system")
    if not system:
        return {
            "status": "error",
            "error": "Sistema no configurado"
        }
        
    provider = system.get_provider()
    if not provider:
        return {
            "status": "error",
            "error": "Proveedor LLM no disponible"
        }
    
    # Convertir el mensaje a formato de chat
    chat_message = [{
        "role": "user",
        "content": f"Actuando como un {agent.role}, responde al siguiente mensaje: {message.get('content', '')}"
    }]
    
    # Generar respuesta
    response = await provider.chat(chat_message)
    
    return {
        "status": "success",
        "response": response.get("content", ""),
        "provider": provider.name,
        "model": provider.__class__.__name__
    }

async def main():
    # Crear sistema
    system = AgentSystem()
    
    # Obtener API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Verificar API keys
    if not openai_api_key:
        print("ERROR: No se encontró la variable de entorno OPENAI_API_KEY.")
        print("Por favor, configura esta variable en el archivo .env o en las variables de entorno del sistema.")
        return
    
    # Añadir proveedores
    system.add_provider(OpenAIProvider(api_key=openai_api_key))
    
    # Ejemplo 1: Usando Custom Agents Framework
    print("\n=== Ejemplo 1: Usando Custom Agents Framework ===")
    
    # Configurar framework personalizado
    custom_framework = CustomAgentFramework()
    system.set_framework(custom_framework)
    
    # Crear agentes personalizados
    asistente = system.create_agent(
        "asistente",
        name="Asistente Personal",
        role="asistente personal amable y servicial",
        processor=simple_processor
    )
    
    # Añadir referencia al sistema en los agentes
    asistente.set_metadata("system", system)
    
    # Iniciar el sistema
    system.start()
    
    # Probar con un mensaje
    print("\n> Enviando mensaje al asistente personal (Custom Framework)")
    resultado_asistente = await system.process_message("asistente", {
        "content": "¿Qué actividades recomiendas para el fin de semana?"
    })
    print(f"Respuesta: {resultado_asistente.get('response')}")
    
    # Detener el sistema
    system.stop()
    
    # Ejemplo 2: Usando Atomic Agents
    try:
        import instructor
        import atomic_agents
        
        print("\n=== Ejemplo 2: Usando Atomic Agents ===")
        
        # Configurar framework de Atomic Agents
        atomic_framework = AtomicAgentsFramework({
            "api_key": openai_api_key
        })
        system.set_framework(atomic_framework)
        
        # Crear agentes atómicos
        asistente_atomic = system.create_agent(
            "asistente_atomic",
            name="Asistente Atomic",
            role="asistente virtual inteligente",
            system_prompt="Eres un asistente virtual amable y servicial que proporciona respuestas claras y concisas."
        )
        
        # Iniciar el sistema
        system.start()
        
        # Probar con un mensaje
        print("\n> Enviando mensaje al asistente (Atomic Framework)")
        resultado_atomic = await system.process_message("asistente_atomic", {
            "content": "¿Puedes recomendarme algunas películas recientes?"
        })
        print(f"Respuesta: {resultado_atomic.get('response')}")
        
        # Detener el sistema
        system.stop()
    except ImportError as e:
        print(f"\nNota: No se pudo ejecutar el ejemplo de Atomic Agents: {e}")
        print("Para ejecutar este ejemplo, asegúrate de tener instaladas las dependencias necesarias:")
        print("  - instructor (pip install instructor)")
        print("  - atomic-agents (pip install git+https://github.com/BrainBlend-AI/atomic-agents.git)")

if __name__ == "__main__":
    asyncio.run(main())
