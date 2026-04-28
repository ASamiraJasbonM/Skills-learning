import ast
import sys
from pathlib import Path

class DjangoSettingsAuditor(ast.NodeVisitor):
    def __init__(self):
        self.findings = []
        self.has_security_mw = False
        self.has_csrf_mw = False

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                # Check DEBUG
                if target.id == 'DEBUG':
                    if isinstance(node.value, ast.Constant) and node.value.value is True:
                        self.findings.append("CRÍTICO: DEBUG está activo (True). Riesgo de exposición de trazas.")
                
                # Check SECRET_KEY
                if target.id == 'SECRET_KEY':
                    if isinstance(node.value, ast.Constant) and len(str(node.value.value)) > 0:
                        if not os.environ.get('DJANGO_SECRET_KEY'):
                            self.findings.append("ADVERTENCIA: SECRET_KEY parece estar hardcodeada. Usar variables de entorno.")

                # Check ALLOWED_HOSTS
                if target.id == 'ALLOWED_HOSTS':
                    if isinstance(node.value, ast.List) and any(isinstance(elt, ast.Constant) and elt.value == '*' for elt in node.value.elts):
                        self.findings.append("CRÍTICO: ALLOWED_HOSTS contiene '*'. Riesgo de ataques de cabecera Host.")

                # Check MIDDLEWARE
                if target.id == 'MIDDLEWARE':
                    if isinstance(node.value, (ast.List, ast.Tuple)):
                        mws = [elt.value for elt in node.value.elts if isinstance(elt, ast.Constant)]
                        if 'django.middleware.security.SecurityMiddleware' in mws:
                            self.has_security_mw = True
                        if 'django.middleware.csrf.CsrfViewMiddleware' in mws:
                            self.has_csrf_mw = True

def audit_settings(file_path):
    import os
    try:
        tree = ast.parse(file_path.read_text())
        auditor = DjangoSettingsAuditor()
        auditor.visit(tree)
        
        if not auditor.has_security_mw:
            auditor.findings.append("CRÍTICO: SecurityMiddleware no detectado en MIDDLEWARE.")
        if not auditor.has_csrf_mw:
            auditor.findings.append("CRÍTICO: CsrfViewMiddleware no detectado en MIDDLEWARE.")
            
        return auditor.findings
    except Exception as e:
        return [f"Error procesando {file_path.name}: {str(e)}"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/check_settings.py <settings.py>")
        sys.exit(1)
    
    import os
    path = Path(sys.argv[1])
    results = audit_settings(path)
    
    if results:
        print(f"✗ Hallazgos de seguridad en {path.name}:")
        for f in results:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"✓ {path.name}: Configuración básica conforme.")
        sys.exit(0)
