import sys
import importlib

REQUIRED_PACKAGES = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'sklearn']

def check_dependencies():
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"✗ ERROR: Faltan los siguientes paquetes: {', '.join(missing)}")
        print("Sugerencia: pip install pandas numpy matplotlib seaborn scikit-learn")
        sys.exit(1)
    else:
        print("✓ Entorno de Ciencia de Datos verificado correctamente.")
        sys.exit(0)

if __name__ == "__main__":
    check_dependencies()
