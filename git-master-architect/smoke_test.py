import sys
import os
import subprocess

def run_smoke_test():
    print("🚀 Iniciando Smoke Test para Git-Master-Architect (v1.1.0)...")
    
    # 1. Verificar existencia de la skill
    if os.path.exists("SKILL.md"):
        print("✅ SKILL.md encontrado.")
    else:
        print("❌ Error: SKILL.md no encontrado.")
        sys.exit(1)

    # 2. Verificar secciones clave
    with open("SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()
        if "Conventional Commits" in content and "<git_diff>" in content:
            print("✅ Secciones críticas (Conventional Commits, XML Delimiters) detectadas.")
        else:
            print("❌ Error: Faltan secciones de seguridad o semántica en SKILL.md.")
            sys.exit(1)

    # 3. Verificar entorno Git
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git CLI disponible en el sistema.")
    except Exception:
        print("⚠️ Warning: Git CLI no detectado en el entorno local.")

    print("\n✨ La skill Git-Master-Architect está lista para su uso.")

if __name__ == "__main__":
    run_smoke_test()
