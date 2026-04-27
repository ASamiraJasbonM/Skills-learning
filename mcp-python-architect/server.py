from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import random

# Inicializar FastMCP con el nuevo estándar v1.1.0
mcp = FastMCP("Advanced MCP Server")

# 1. Esquema de Validación con Pydantic
class FactRequest(BaseModel):
    category: str = Field(description="Categoría del dato curioso (mcp, python, general)")

# 2. Herramientas con Validación
@mcp.tool()
def get_random_fact(args: FactRequest) -> str:
    """Retorna un dato curioso aleatorio basado en una categoría."""
    facts = {
        "mcp": ["MCP usa JSON-RPC 2.0.", "FastMCP simplifica la creación de herramientas."],
        "python": ["Python es el lenguaje preferido para servidores MCP.", "Pydantic asegura tipos estrictos."],
        "general": ["La IA se vuelve más útil con herramientas locales."]
    }
    category = args.category.lower()
    options = facts.get(category, facts["general"])
    return random.choice(options)

@mcp.tool()
def echo_message(message: str) -> str:
    """Repite el mensaje enviado por el usuario."""
    return f"Servidor MCP recibió: {message}"

# 3. Recursos (Resources)
@mcp.resource("info://status")
def get_server_status() -> str:
    """Retorna el estado actual del servidor MCP."""
    return "Estado: Activo | Versión Skill: 1.1.0 | Entorno: Producción"

# 4. Prompts
@mcp.prompt("analizar-arquitectura")
def architecture_prompt():
    """Prompt sugerido para analizar la arquitectura del servidor."""
    return "Revisa el código de este servidor MCP y verifica que use Pydantic para la validación de todas las herramientas."

if __name__ == "__main__":
    mcp.run()
