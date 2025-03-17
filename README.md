# AgentForge Core

Framework modular para sistemas de agentes de IA, con soporte para múltiples proveedores de LLM y frameworks de agentes.

## Instalación

```bash
# Instalación básica
pip install agentforge-core

# Con soporte para todos los proveedores de LLM
pip install agentforge-core[all]

# O seleccionar proveedores específicos
pip install agentforge-core[openai,anthropic]

# Para desarrollo
pip install agentforge-core[dev]
```

## Características

- Soporte para múltiples frameworks de agentes (Atomic Agents y más)
- Integración con diferentes proveedores de LLM (OpenAI, Anthropic, Groq, Grok)
- Diseño modular y extensible
- Fácil configuración y uso

## Uso básico

```python
from agentforge_core import AgentSystem
from agentforge_core.llm import AnthropicProvider
from agentforge_core.agent.frameworks import AtomicAgentsFramework

# Configurar sistema con diferentes proveedores
system = AgentSystem()
system.add_provider(AnthropicProvider(api_key="your_key"))

# Establecer el framework de agentes
framework = AtomicAgentsFramework()
system.set_framework(framework)

# Crear y configurar agentes
planner = system.create_agent("planner", role="Crear planes de alto nivel")
researcher = system.create_agent("researcher", role="Buscar información")

# Conectar agentes entre sí
planner.connect_to(researcher)

# Iniciar el sistema
system.start()

# Procesar un mensaje
response = await system.process_message("planner", {"task": "Analizar datos"})
```

## Licencia

MIT
# agentforge
