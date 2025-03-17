#!/bin/bash

# Colores para mejor visualización
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Configurando proyecto AgentForge con Poetry${NC}"

# Verificar si Poetry está instalado
if ! command -v poetry &> /dev/null; then
    echo -e "${YELLOW}Poetry no está instalado. Instalando Poetry...${NC}"
    curl -sSL https://install.python-poetry.org | python3 -
else
    echo -e "${GREEN}Poetry ya está instalado.${NC}"
fi

# Crear estructura básica si no existe
if [ ! -d "agentforge_core" ] || [ ! -d "agentforge_common" ]; then
    echo -e "${YELLOW}Estructura de directorio incompleta. Generando directorios necesarios...${NC}"
    
    # Ejecutar scripts de generación si existen
    if [ -f "generate_agentforge_common.sh" ]; then
        echo -e "${BLUE}Ejecutando generate_agentforge_common.sh...${NC}"
        bash generate_agentforge_common.sh
    fi
    
    if [ -f "generate_agentforge.sh" ]; then
        echo -e "${BLUE}Ejecutando generate_agentforge.sh...${NC}"
        bash generate_agentforge.sh
    fi
else
    echo -e "${GREEN}Estructura de directorios encontrada.${NC}"
fi

# Crear archivo .env para las API keys si no existe
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creando archivo .env para API keys...${NC}"
    cat > .env << 'EOF'
# API Keys para proveedores LLM
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GROQ_API_KEY=gsk-your-groq-key

# Configuración general
AGENTFORGE_LOG_LEVEL=info
AGENTFORGE_DEBUG_MODE=false
EOF
    echo -e "${GREEN}Archivo .env creado. Por favor, edita el archivo para añadir tus API keys.${NC}"
else
    echo -e "${GREEN}Archivo .env ya existe.${NC}"
fi

# Inicializar proyecto Poetry si no existe pyproject.toml
if [ ! -f "pyproject.toml" ]; then
    echo -e "${BLUE}Inicializando proyecto Poetry...${NC}"
    poetry init --no-interaction --name "agentforge" --description "Framework modular para sistemas de agentes de IA" --author "Your Name <your.email@example.com>" --python "^3.8"
    
    # Agregar dependencias principales
    echo -e "${BLUE}Agregando dependencias principales...${NC}"
    poetry add aiohttp pydantic python-dotenv tenacity typing-extensions openai instructor
    
    # Intentar agregar atomic-agents (puede que no esté disponible en PyPI)
    echo -e "${BLUE}Intentando agregar atomic-agents...${NC}"
    poetry add atomic-agents || echo -e "${YELLOW}No se pudo agregar atomic-agents automáticamente. Puede ser necesario instalarlo manualmente desde GitHub.${NC}"
    
    # Agregar dependencias de desarrollo
    echo -e "${BLUE}Agregando dependencias de desarrollo...${NC}"
    poetry add --group dev pytest pytest-asyncio black isort mypy
else
    echo -e "${GREEN}Proyecto Poetry ya inicializado.${NC}"
fi

# Crear entorno virtual e instalar dependencias
echo -e "${BLUE}Instalando dependencias con Poetry...${NC}"
poetry install

# Mensaje final
echo -e "${GREEN}¡Configuración completa!${NC}"
echo -e "${BLUE}Para activar el entorno virtual:${NC}"
echo -e "  ${YELLOW}poetry shell${NC}"
echo -e "${BLUE}Para ejecutar el ejemplo:${NC}"
echo -e "  ${YELLOW}poetry run python example.py${NC}"
echo -e "${BLUE}Si atomic-agents no se pudo instalar automáticamente, puedes instalarlo con:${NC}"
echo -e "  ${YELLOW}poetry shell${NC}"
echo -e "  ${YELLOW}pip install git+https://github.com/BrainBlend-AI/atomic-agents.git${NC}"
echo -e "${BLUE}No olvides editar el archivo .env con tus propias claves API.${NC}"

# Hacer ejecutable el script
chmod +x "$0"
