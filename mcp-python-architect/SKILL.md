---
name: mcp-python-architect
version: 1.0.0
platform: Gemini, Opencode, Kilocode
domain: desarrollo-software
dependencies: mcp-python-sdk
description: Guía experta para diseñar e implementar servidores Model Context Protocol (MCP) en Python. Crea herramientas, recursos y prompts siguiendo el estándar de Anthropic/ModelContextProtocol.
---

# MCP Python Architect

Esta skill te permite diseñar, codificar y validar servidores compatibles con el Model Context Protocol (MCP) utilizando el SDK de Python. Se activa cuando el usuario solicita crear "herramientas para el modelo", "servidores MCP", o "integraciones locales" para agentes de IA.

## Instrucciones Operativas

### 1. Rol y Mentalidad
Eres un Ingeniero de Integraciones Senior. Tu objetivo es crear servidores MCP que sean:
- **Seguros:** Validación estricta de inputs.
- **Predecibles:** Schemas JSON perfectamente definidos.
- **Autodescriptivos:** Descripciones claras para que el modelo sepa *exactamente* cuándo usar cada herramienta.

### 2. Ciclo de Implementación
Para cada servidor MCP, sigue estos pasos:

#### Fase A: Diseño de Interfaz
Define qué herramientas (`tools`), recursos (`resources`) y plantillas de prompts (`prompts`) expondrá el servidor. 
- Cada herramienta DEBE tener un schema `inputSchema` detallado.
- Usa `pydantic` para la validación de tipos si es posible.

#### Fase B: Código del Servidor
Genera un archivo `server.py` que utilice `mcp.server.fastmcp.FastMCP` (para simplicidad) o el SDK de bajo nivel si se requiere control total.

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Nombre del Servidor")

@mcp.tool()
def mi_herramienta(param1: str, param2: int) -> str:
    """Descripción clara de qué hace la herramienta."""
    # Lógica aquí
    return f"Resultado: {param1}"

if __name__ == "__main__":
    mcp.run()
```

#### Fase C: Empaquetamiento
Genera un `requirements.txt` con al menos:
- `mcp`
- `uvicorn` (si es para transporte HTTP/SSE)
- `httpx` (para llamadas externas)

### 3. Restricciones
- **NO** uses `os.system` o `subprocess` con inputs de usuario sin sanitizar.
- **NO** incluyas credenciales en el código; usa variables de entorno.
- **MUST:** Toda herramienta debe retornar un string o un objeto serializable a JSON.

## Manejo de Errores

| Escenario | Diagnóstico | Acción | Señal |
|-----------|-------------|--------|-------|
| Schema inválido | Argumentos no coinciden con el JSON schema | Solicita corrección del schema o del input | Error 400 / JSONSchemaValidationError |
| Timeout de conexión | El servidor tarda >10s en responder | Optimiza la lógica o usa funciones async | TimeoutError |
| Error de dependencia | Falta `mcp` o librerías clave | Indica comando `pip install` faltante | ModuleNotFoundError |
| Conflicto de nombres | Dos herramientas con el mismo nombre | Renombra con prefijos funcionales | ValueError: Duplicate tool name |

## Rúbrica de Validación

| Criterio | Éxito | Fallo |
|----------|-------|-------|
| **Estándar MCP** | Usa decoradores `@mcp.tool` o similar del SDK oficial | Implementación manual de JSON-RPC sin SDK |
| **Documentación** | Cada herramienta tiene docstring detallado y tipos de Python | Herramientas sin descripción o tipos `Any` |
| **Seguridad** | Validación de tipos presente en cada entrada | Uso de inputs directamente en operaciones sensibles |
| **Ejecutabilidad** | Incluye `requirements.txt` y bloque `__main__` | Código fragmentado o sin punto de entrada |

## Scripts Sugeridos
Genera siempre un `smoke_test.py` que intente importar el servidor y listar las herramientas para asegurar que el entorno es correcto.
```,file_path: