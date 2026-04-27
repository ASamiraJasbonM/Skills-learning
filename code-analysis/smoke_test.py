import sys
import os

def run_smoke_test():
    print("🚀 Iniciando Smoke Test para Code-Analysis (v2.1.0)...")
    
    # 1. Verificar existencia de la skill
    if os.path.exists("SKILL.md"):
        print("✅ SKILL.md encontrado.")
    else:
        print("❌ Error: SKILL.md no encontrado.")
        sys.exit(1)

    # 2. Verificar secciones clave
    with open("SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()
        required_sections = ["Matriz de Severidad Técnica", "Big O", "<code_to_analyze>", "CWE"]
        for section in required_sections:
            if section in content:
                print(f"✅ Sección '{section}' detectada.")
            else:
                print(f"❌ Error: Falta la sección '{section}' en SKILL.md.")
                sys.exit(1)

    print("\n✨ La skill Code-Analysis v2.1.0 está validada estructuralmente.")

if __name__ == "__main__":
    run_smoke_test()
