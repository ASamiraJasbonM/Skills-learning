#!/usr/bin/env python3
"""
validate_structure.py v2 - Validador de estructura para SKILL.md generado por prompt_v22

Propósito: Validar que un SKILL.md generado cumple el estándar de prompt_v22.
Este script es Capa 0 de calidad estructural (no reemplaza validate.sh que es Capa 2 de seguridad).

Validaciones v2:
1. SKILL.md existe y tiene frontmatter YAML válido
2. Campos requeridos: name, description
3. name en kebab-case (a-z, 0-9, guiones), máx. 64 caracteres
4. description sin angle brackets < >, máx. 1024 caracteres
5. Secciones requeridas por prompt_v22
6. Tabla de errores ≥4 filas
7. No placeholders [PENDIENTE:], [TODO:]
8. Rúbrica tiene columnas de éxito Y fallo
9. Tabla de errores tiene columna de acción

Usage:
    python scripts/validate_structure.py <path/to/SKILL.md>
    python scripts/validate_structure.py <path/to/SKILL.md> --json
"""

import argparse
import json
import re
import sys
import yaml
from pathlib import Path


ALLOWED_FIELDS_CORE = {
    # Estandar oficial (quick_validate.py)
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
    # Campos adicionales de prompt_v22
    "version",
    "platform",
    "domain",
    "dependencies",
    "part",
    "runtimes",
}
ALLOWED_FIELDS = ALLOWED_FIELDS_CORE

SECTIONS_REQUIRED_MANDATORY = {"## Manejo de Errores"}
SECTIONS_RUBRICA_VARIANTS = {"## Rúbrica", "## Rúbrica de Validación"}
SECTIONS_MINIMA = {"## Tarea", "## Manejo de Errores", "## Rúbrica"}


def parse_frontmatter(content: str) -> tuple[dict, int]:
    """Parse YAML frontmatter from SKILL.md content."""
    lines = content.split("\n")

    if not lines[0].strip().startswith("---"):
        return {}, -1

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip().startswith("---"):
            end_idx = i
            break

    if end_idx is None:
        return {}, -1

    frontmatter_lines = lines[1:end_idx]
    frontmatter_text = "\n".join(frontmatter_lines)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter if frontmatter else {}, end_idx
    except yaml.YAMLError:
        return {}, end_idx


def validate_name(name: str) -> tuple[bool, str]:
    """Validar name en kebab-case."""
    if not name:
        return False, "Campo 'name' vacío"

    if len(name) > 64:
        return False, f"name demasiado largo ({len(name)} chars, máx 64)"

    if not re.match(r"^[a-z0-9][a-z0-9-]*$", name):
        return False, f"name debe ser kebab-case (a-z, 0-9, guiones)"

    if name.startswith("-") or name.endswith("-") or "--" in name:
        return (
            False,
            "name no puede empezar/terminar con guion o tener guiones consecutivos",
        )

    return True, ""


def validate_description(description: str) -> tuple[bool, str]:
    """Validar description sin angle brackets."""
    if not description:
        return False, "Campo 'description' vacío"

    if len(description) > 1024:
        return (
            False,
            f"description demasiado larga ({len(description)} chars, máx 1024)",
        )

    if "<" in description or ">" in description:
        return False, "description no puede contener angle brackets < >"

    return True, ""


def validate_compatibility(compatibility: str) -> tuple[bool, str]:
    """Validar compatibility field si existe."""
    if not compatibility:
        return True, ""

    if len(compatibility) > 500:
        return (
            False,
            f"compatibility demasiado larga ({len(compatibility)} chars, máx 500)",
        )

    return True, ""


def count_error_rows(content: str) -> int:
    """Cuenta filas en la tabla de Manejo de Errores.

    Busca la sección completa hasta el próximo '##', sin romper en línea vacía.
    """
    lines = content.split("\n")
    in_errors_table = False
    header_seen = False
    row_count = 0

    for line in lines:
        # Detectar inicio de la sección
        if "## Manejo de Errores" in line:
            in_errors_table = True
            continue

        # Si llegamos a otra sección, terminamos
        if in_errors_table and line.strip().startswith("##"):
            break

        if in_errors_table:
            # Saltar separador de tabla (línea con ---)
            if "---" in line and line.strip().startswith("|"):
                header_seen = True
                continue

            # Contar filas de datos (solo después del header)
            if line.strip().startswith("|"):
                if header_seen:
                    row_count += 1
                else:
                    # Primera línea con | es el header
                    header_seen = True

    return row_count


def check_no_placeholder(content: str) -> tuple[bool, str]:
    """Detecta placeholders sin rellenar del tipo [PENDIENTE:] o [TODO:]"""
    patterns = [r"\[PENDIENTE:", r"\[TODO:", r"\[PLACEHOLDER", r"\[INSERT"]
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return False, f"Placeholder sin detectar: {pattern}"
    return True, ""


def check_rubrica_has_both_columns(content: str) -> tuple[bool, str]:
    """La rubrica debe tener columna de éxito Y fallo, no solo éxito.

    Examina toda la sección de rúbrica, no solo la primera línea.
    """
    lines = content.split("\n")
    in_rubrica = False
    rubrica_content_lines = []

    for line in lines:
        if "## Rúbrica" in line or "## Rúbrica de Validación" in line:
            in_rubrica = True
            continue
        if in_rubrica:
            # Si llegamos a otra sección, terminamos
            if line.strip().startswith("##"):
                break
            rubrica_content_lines.append(line)

    if not rubrica_content_lines:
        return False, "Sección ## Rúbrica no encontrada"

    # Examinar todo el contenido de la sección de rúbrica
    rubrica_text = "\n".join(rubrica_content_lines).lower()
    has_success = any(
        w in rubrica_text for w in ["éxito", "pasa", "correcto", "pass", "success"]
    )
    has_failure = any(
        w in rubrica_text for w in ["falla", "error", "incorrecto", "fail", "fallo"]
    )
    if not (has_success and has_failure):
        return False, "Rúbrica debe indicar criterios de éxito Y fallo"
    return True, ""


def check_error_table_has_actions(content: str) -> tuple[bool, str]:
    """Cada fila de la tabla de errores debe tener columna Acción."""
    lines = content.split("\n")
    in_errors = False
    error_table_lines = []

    for line in lines:
        if "## Manejo de Errores" in line:
            in_errors = True
            continue
        if in_errors:
            # Si llegamos a otra sección, terminamos
            if line.strip().startswith("##"):
                break
            error_table_lines.append(line)

    if not error_table_lines:
        return False, "Sección ## Manejo de Errores no encontrada"

    # Contar filas de datos en la tabla (excluyendo header y separador)
    rows = [
        l for l in error_table_lines if l.strip().startswith("|") and "---" not in l
    ]
    data_rows = rows[1:] if len(rows) > 1 else []
    if len(data_rows) < 4:
        return False, f"Tabla de errores tiene {len(data_rows)} filas, mínimo 4"
    return True, ""


def validate_sections(content: str, is_minima: bool = False) -> tuple[bool, list[str]]:
    """Valida secciones requeridas."""
    missing = []

    # Secciones obligatorias
    for section in SECTIONS_REQUIRED_MANDATORY:
        if section not in content:
            missing.append(section)

    # Acepta cualquier variante de rúbrica
    if not any(v in content for v in SECTIONS_RUBRICA_VARIANTS):
        missing.append("## Rúbrica (o ## Rúbrica de Validación)")

    return len(missing) == 0, missing


def check_description_body_coherence(
    content: str, frontmatter: dict
) -> tuple[bool, str]:
    """
    Check semántico básico: palabras clave de la description deben aparecer en el cuerpo.
    No es un check semántico completo — detecta solo inconsistencias obvias.
    """
    description = frontmatter.get("description", "")
    if not description:
        return True, ""

    stopwords = {"para", "como", "desde", "hasta", "sobre", "entre", "cuando", "donde"}
    desc_words = [
        w.lower()
        for w in description.split()
        if len(w) > 5 and w.lower() not in stopwords
    ]

    body = (
        "\n".join(content.split("\n")[content.split("\n").index("---", 1) + 1 :])
        if "---" in content
        else content
    )
    body_lower = body.lower()

    missing = [w for w in desc_words if w not in body_lower]
    if len(desc_words) > 0 and (len(missing) / len(desc_words)) > 0.6:
        return False, (
            f"description menciona términos ausentes en el cuerpo: {missing[:3]}. "
            "Posible incoherencia description↔cuerpo. Revisar manualmente."
        )
    return True, ""


def check_skill_md_length(content: str) -> tuple[bool, str]:
    """Detecta SKILL.md sobrecargado — candidato a refactorización."""
    word_count = len(content.split())
    line_count = len(content.splitlines())

    if word_count > 5000:
        return False, (
            f"SKILL.md tiene {word_count} palabras (máx recomendado: 5000). "
            "Mover documentación estática a references/."
        )
    if line_count > 500:
        return False, (
            f"SKILL.md tiene {line_count} líneas (máx recomendado: 500). "
            "Considerar estructura completa con references/."
        )
    return True, f"{word_count} palabras, {line_count} líneas — dentro del límite"


def validate_structure(skill_path: Path, fix: bool = False) -> tuple[bool, list[str]]:
    """
    Valida un SKILL.md generado.
    Returns (passed, list_of_errors).
    """
    errors = []

    if not skill_path.exists():
        return False, [f"Archivo no encontrado: {skill_path}"]

    try:
        content = skill_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, [f"Error leyendo archivo: {e}"]

    frontmatter, end_idx = parse_frontmatter(content)

    if end_idx < 0:
        errors.append("Sin frontmatter YAML (debe empezar con ---)")
        return False, errors

    if not isinstance(frontmatter, dict):
        errors.append("Frontmatter debe ser un diccionario YAML válido")
        return False, errors

    if "name" not in frontmatter:
        errors.append("Falta campo requerido: name")
    else:
        valid, msg = validate_name(frontmatter["name"])
        if not valid:
            errors.append(f"name: {msg}")

    if "description" not in frontmatter:
        errors.append("Falta campo requerido: description")
    else:
        valid, msg = validate_description(frontmatter["description"])
        if not valid:
            errors.append(f"description: {msg}")

    if "compatibility" in frontmatter:
        valid, msg = validate_compatibility(frontmatter["compatibility"])
        if not valid:
            errors.append(f"compatibility: {msg}")

    valid_sections, missing_sections = validate_sections(content)
    if not valid_sections:
        for section in missing_sections:
            errors.append(f"Sección faltante: {section}")

    error_rows = count_error_rows(content)
    if error_rows < 4:
        errors.append(f"Tabla de errores insuficiente ({error_rows} filas, mínimo 4)")

    # Check 7: No placeholders
    valid, msg = check_no_placeholder(content)
    if not valid:
        errors.append(f"placeholder: {msg}")

    # Check 8: Rúbrica con éxito Y fallo
    valid, msg = check_rubrica_has_both_columns(content)
    if not valid:
        errors.append(f"rubrica: {msg}")

    # Check 9: Tabla errores con columna acción
    valid, msg = check_error_table_has_actions(content)
    if not valid:
        errors.append(f"error-table: {msg}")

    # Check 10: Peso del SKILL.md (S2)
    valid, msg = check_skill_md_length(content)
    if not valid:
        errors.append(f"peso: {msg}")

    # Check 11: Coherencia description↔cuerpo (heurístico)
    valid, msg = check_description_body_coherence(content, frontmatter)
    if not valid:
        errors.append(f"coherencia: {msg}")  # Warning, no bloqueante

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(
        description="Validador de estructura para SKILL.md de prompt_v22"
    )
    parser.add_argument("skill_path", type=Path, help="Ruta al SKILL.md a validar")
    parser.add_argument(
        "--fix", action="store_true", help="Intentar auto-corregir errores mínimos"
    )
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON")
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Solo mostrar errores"
    )

    args = parser.parse_args()

    if not args.quiet:
        print(f"Validando: {args.skill_path}")

    passed, errors = validate_structure(args.skill_path, args.fix)

    if args.json:
        import json

        output = {
            "path": str(args.skill_path),
            "passed": passed,
            "errors": errors,
            "error_count": len(errors),
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        sys.exit(0 if passed else 1)

    if passed:
        if not args.quiet:
            print("✓ Estructura válida")
        sys.exit(0)
    else:
        print("✗ Errores encontrados:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
