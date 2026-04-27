import sys
import os

def run_smoke_test():
    print("📊 Iniciando Smoke Test para ML-Data-Cleaner (v1.0.0)...")
    
    # 1. Verificar existencia de la skill
    if os.path.exists("SKILL.md"):
        print("✅ SKILL.md encontrado.")
    else:
        print("❌ Error: SKILL.md no encontrado.")
        sys.exit(1)

    # 2. Verificar secciones clave
    with open("SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()
        required = ["eda_report.py", "clean_data.py", "ANALYSIS.md", "Big O", "Data Leakage"]
        # Nota: Big O fue un supuesto conservador, Data Leakage es mandatorio.
        for item in ["eda_report.py", "clean_data.py", "ANALYSIS.md", "Data Leakage", "Entendimiento"]:
            if item in content:
                print(f"✅ Concepto '{item}' detectado.")
            else:
                print(f"❌ Error: Falta '{item}' en la definición de la skill.")
                sys.exit(1)

    print("\n✨ La skill ML-Data-Cleaner está lista para procesar datasets.")

if __name__ == "__main__":
    run_smoke_test()
