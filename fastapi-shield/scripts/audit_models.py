import ast
import sys
from pathlib import Path

class PydanticAuditor(ast.NodeVisitor):
    def __init__(self):
        self.findings = []

    def visit_ClassDef(self, node):
        # Verificar si hereda de BaseModel
        is_pydantic = any(isinstance(base, ast.Name) and base.id == 'BaseModel' for base in node.bases)
        if is_pydantic:
            for item in node.body:
                if isinstance(item, ast.AnnAssign):
                    # Check for 'Any' type
                    if isinstance(item.annotation, ast.Name) and item.annotation.id == 'Any':
                        self.findings.append(f"CLASE {node.name}: Campo '{item.target.id}' usa 'Any' (Validación Débil).")
                    
                    # Check for missing Field() with constraints
                    has_field = False
                    if isinstance(item.value, ast.Call) and isinstance(item.value.func, ast.Name) and item.value.func.id == 'Field':
                        has_field = True
                    
                    if not has_field and isinstance(item.annotation, ast.Name) and item.annotation.id == 'str':
                        self.findings.append(f"CLASE {node.name}: Campo string '{item.target.id}' sin restricciones Field(min_length=...).")
        self.generic_visit(node)

def audit_file(file_path):
    try:
        tree = ast.parse(file_path.read_text())
        auditor = PydanticAuditor()
        auditor.visit(tree)
        return auditor.findings
    except Exception as e:
        return [f"Error procesando {file_path.name}: {str(e)}"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/audit_models.py <archivo.py>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    results = audit_file(path)
    
    if results:
        print(f"✗ Hallazgos de seguridad en {path.name}:")
        for f in results:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"✓ {path.name}: Esquemas Pydantic conformes con la política estricta.")
        sys.exit(0)
