import sys
import os

def run_smoke_test():
    print("🛡️ Iniciando Smoke Test para Django-Shield (v3.1.0)...")
    
    # 1. Verificar existencia de la skill
    if os.path.exists("SKILL.md"):
        print("✅ SKILL.md encontrado.")
    else:
        print("❌ Error: SKILL.md no encontrado.")
        sys.exit(1)

    # 2. Verificar estructura de carpetas (assets/references si existieran)
    # Por ahora solo SKILL.md es obligatorio, pero validamos que no esté vacío
    with open("SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()
        if "NIST AI RMF" in content and "Taint Flow" in content:
            print("✅ Secciones críticas (NIST, Taint Flow) detectadas en la skill.")
        else:
            print("❌ Error: Faltan secciones clave en SKILL.md.")
            sys.exit(1)

    print("\n✨ La skill Django-Shield está lista para auditar.")

if __name__ == "__main__":
    run_smoke_test()
