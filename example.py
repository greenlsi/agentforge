#!/usr/bin/env python3
"""
Ejemplo simple de uso del framework Atomic Agents con Instructor
"""

import asyncio
import os
import logging
from dotenv import load_dotenv

from agentforge_core import AgentSystem
from agentforge_core.llm import OpenAIProvider
from agentforge_core.agent.frameworks import AtomicAgentsFramework, CustomAgentFramework

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Cargar variables de entorno
load_dotenv()

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
    
    # Añadir proveedores (con claves de API desde variables de entorno)
    if os.getenv("OPENAI_API_KEY"):
        system.add_provider(OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY")))
    
    if not system.providers:
        print("ERROR: No se encontró la clave de API para OpenAI. Por favor configura la variable de entorno OPENAI_API_KEY.")
        return
    
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
    
    # Ejemplo 2: Usando Atomic Agents con Instructor
    try:
        import instructor
        
        print("\n=== Ejemplo 2: Usando Atomic Agents con Instructor ===")
        
        # Configurar framework de Atomic Agents
        atomic_framework = AtomicAgentsFramework({
            "api_key": os.getenv("OPENAI_API_KEY")
        })
        system.set_framework(atomic_framework)
        
        # Crear agentes atómicos
        asistente_atomic = system.create_agent(
            "asistente_atomic",
            name="Asistente Atomic",
            role="asistente virtual inteligente",
            system_prompt="Eres un asistente virtual amable y servicial que proporciona respuestas claras y concisas."
        )
        
        planificador = system.create_agent(
            "planificador",
            name="Planificador",
            role="experto en planificación",
            system_prompt="Eres un planificador experto que desarrolla planes detallados y estructurados para cualquier tarea o proyecto."
        )
        
        # Iniciar el sistema
        system.start()
        
        # Probar con un mensaje para el asistente
        print("\n> Enviando mensaje al asistente (Atomic Framework)")
        resultado_asistente = await system.process_message("asistente_atomic", {
            "content": "¿Puedes recomendarme algunas películas recientes?"
        })
        print(f"Respuesta: {resultado_asistente.get('response')}")
        
        # Probar con un mensaje para el planificador
        print("\n> Enviando mensaje al planificador (Atomic Framework)")
        resultado_planificador = await system.process_message("planificador", {
            "content": "Necesito organizar una conferencia virtual para 100 personas"
        })
        print(f"Respuesta: {resultado_planificador.get('response')}")
        
        # Detener el sistema
        system.stop()
    except ImportError:
        print("\nNota: No se pudo inicializar AtomicAgentsFramework porque 'instructor' no está instalado.")
        print("Instálalo con: pip install instructor")

if __name__ == "__main__":
    asyncio.run(main())