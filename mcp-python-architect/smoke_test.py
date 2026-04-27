import sys
import subprocess
import os

def run_smoke_test():
    print("🚀 Iniciando Smoke Test para el Servidor MCP...")
    
    # 1. Verificar dependencias
    try:
        import mcp
        print("✅ SDK de MCP encontrado.")
    except ImportError:
        print("❌ Error: SDK de MCP no instalado. Ejecuta 'pip install -r requirements.txt'")
        sys.exit(1)

    # 2. Verificar que el archivo server.py existe
    if os.path.exists("server.py"):
        print("✅ Archivo server.py encontrado.")
    else:
        print("❌ Error: server.py no encontrado.")
        sys.exit(1)

    # 3. Intento de carga simbólica (verificar sintaxis)
    try:
        from server import mcp as server_instance
        tools = server_instance.list_tools()
        print(f"✅ Servidor cargado correctamente. Herramientas detectadas: {[t.name for t in tools]}")
    except Exception as e:
        print(f"❌ Error al cargar el servidor: {e}")
        sys.exit(1)

    print("\n✨ El entorno de la skill está configurado correctamente.")

if __name__ == "__main__":
    run_smoke_test()
