import sys
import os

def run_smoke_test():
    print("🛡️ Iniciando Smoke Test para Conservative-Dev-Protocol (v1.0.0)...")
    
    # 1. Verificar existencia de la skill
    if os.path.exists("SKILL.md"):
        print("✅ SKILL.md encontrado.")
    else:
        print("❌ Error: SKILL.md no encontrado.")
        sys.exit(1)

    # 2. Verificar secciones clave
    with open("SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()
        required = ["CHANGELOG_SESSION.md", "ask_user", "Preferencias del Proyecto", "No Borrar"]
        for item in required:
            if item in content:
                print(f"✅ Regla '{item}' detectada.")
            else:
                print(f"❌ Error: Falta la regla crítica '{item}' en SKILL.md.")
                sys.exit(1)

    print("\n✨ El protocolo conservador está configurado y listo para proteger el código.")

if __name__ == "__main__":
    run_smoke_test()
