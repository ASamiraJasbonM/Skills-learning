import sys
import os

def run_smoke_test():
    print("🚀 Iniciando Smoke Test para el Servidor MCP (v1.1.0)...")
    
    # 1. Verificar dependencias
    try:
        import mcp
        import pydantic
        print("✅ SDK de MCP y Pydantic encontrados.")
    except ImportError as e:
        print(f"❌ Error: Falta dependencia {e}. Ejecuta 'pip install -r requirements.txt'")
        sys.exit(1)

    # 2. Verificar que el archivo server.py existe
    if os.path.exists("server.py"):
        print("✅ Archivo server.py encontrado.")
    else:
        print("❌ Error: server.py no encontrado.")
        sys.exit(1)

    # 3. Intento de carga simbólica y validación de capacidades
    try:
        from server import mcp as server_instance
        
        # Validar Tools
        tools = server_instance.list_tools()
        print(f"✅ Herramientas detectadas ({len(tools)}): {[t.name for t in tools]}")
        
        # Validar Resources
        resources = server_instance.list_resources()
        print(f"✅ Recursos detectados ({len(resources)}): {[r.uri for r in resources]}")
        
        # Validar Prompts
        prompts = server_instance.list_prompts()
        print(f"✅ Prompts detectados ({len(prompts)}): {[p.name for p in prompts]}")
        
    except Exception as e:
        print(f"❌ Error al cargar o validar el servidor: {e}")
        sys.exit(1)

    print("\n✨ El entorno de la skill v1.1.0 está configurado correctamente.")

if __name__ == "__main__":
    run_smoke_test()
