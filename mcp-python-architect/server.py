from mcp.server.fastmcp import FastMCP
import random

# Inicializar FastMCP
mcp = FastMCP("Example MCP Server")

@mcp.tool()
def get_random_fact() -> str:
    """Retorna un dato curioso aleatorio sobre el Model Context Protocol."""
    facts = [
        "MCP permite que los modelos de lenguaje usen herramientas locales de forma segura.",
        "El SDK de Python usa JSON-RPC 2.0 bajo el capó para la comunicación.",
        "FastMCP es la forma más rápida de crear servidores MCP con decoradores de Python.",
        "Los servidores MCP pueden exponer Tools, Resources y Prompts."
    ]
    return random.choice(facts)

@mcp.tool()
def echo_message(message: str) -> str:
    """
    Repite el mensaje enviado por el usuario.
    
    Args:
        message: El texto que se desea repetir.
    """
    return f"Servidor MCP recibió: {message}"

if __name__ == "__main__":
    mcp.run()
