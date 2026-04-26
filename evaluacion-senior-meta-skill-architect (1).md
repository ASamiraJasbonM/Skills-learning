# Evaluación Senior — meta-skill-architect v3.0.0

Evaluación estructural, funcional y de diseño desde la perspectiva de un
senior en desarrollo de skills, con foco en decisiones de arquitectura
(estructura mínima vs completa) y calidad de los componentes actuales.

---

## 1. Veredicto general

| Dimensión | Calificación | Nota |
|-----------|-------------|------|
| Arquitectura de archivos | 7/10 | Estructura correcta, decisiones cuestionables |
| Calidad de SKILL.md | 8/10 | Sólido; un error residual en system.md |
| Scripts (validate, test_runner) | 6/10 | Bugs reales en validate_structure.py |
| Referencias (schemas, patterns) | 9/10 | Bien ejecutadas tras correcciones |
| Decisión mínima vs completa | 5/10 | No documentada ni guiada al usuario |

**Veredicto:** REVISAR — la skill está bien diseñada conceptualmente pero
tiene bugs en los scripts que la harían fallar en producción, y no guía
al usuario sobre cuándo usar estructura mínima vs completa.

---

## 2. Arquitectura actual vs criterio mínima/completa

### Tu estructura actual

```
meta-skill-architect/
├── SKILL.md                  ← instrucciones principales
├── system.md                 ← system prompt (separado)
├── task.md                   ← task prompt (separado)
├── scripts/
│   ├── validate.sh
│   ├── validate_structure.py
│   ├── test_runner.py
│   └── mcp_server.py
├── data/
│   └── examples.json
├── references/
│   ├── schemas.md
│   ├── writing-patterns.md
│   └── examples.md
└── README.md
```

### Diagnóstico por carpeta

**`references/` — Justificado ✅**
El contenido supera 5000 palabras combinado y se carga bajo demanda.
`writing-patterns.md` + `schemas.md` + `examples.md` son exactamente
el tipo de documentación que no debe vivir en el SKILL.md principal.

**`scripts/` — Parcialmente justificado ⚠️**
`validate_structure.py` y `validate.sh` son determinísticos y repetibles → justificados.
`test_runner.py` es correcto en principio, pero su implementación actual
simula los outputs en vez de ejecutar la skill → el script no hace lo que
promete (ver Sección 4).
`mcp_server.py` está bien como script auxiliar, pero tiene referencias a
`prompt_v22` (nombre viejo) y versión `2.2.0` desactualizada.

**`data/` — Justificado ✅**
`examples.json` es una plantilla de assets correcta. Pero el `version`
interno dice `"2.3.0"` — desincronizado con v3.0.0.

**`system.md` y `task.md` en raíz — Decisión correcta ✅**
Separarlos del SKILL.md es la decisión correcta para runtimes que soportan
system prompt cacheable. Bien documentado en el frontmatter de system.md.

---

## 3. Correcciones de arquitectura

### C-A1: Añadir `assets/` para las plantillas de output

Las plantillas de SKILL.md (versión completa y mínima) están embebidas
en `task.md` como texto. Según el criterio de estructura completa, deberían
vivir en `assets/`.

**Estructura recomendada:**
```
assets/
├── template-full.md      # Plantilla completa (≥4000 tokens)
└── template-minimal.md   # Plantilla mínima (Kilocode/Opencode)
```

**Cambio en `task.md`:** Reemplazar los bloques de plantilla embebidos por:
```markdown
## Plantillas

Carga bajo demanda desde `assets/`:
- `assets/template-full.md` — cuando tokens disponibles ≥4000
- `assets/template-minimal.md` — cuando tokens <4000 (Kilocode/Opencode)
```

**Por qué:** Las plantillas son assets de output, no instrucciones.
Embebidas en task.md inflaman el context window innecesariamente.

---

### C-A2: Añadir `data/validate_fixtures/` para testear el validador

El validador no tiene casos de prueba propios. Si `validate_structure.py`
tiene un bug (y lo tiene — ver Sección 4), no hay forma de detectarlo.

**Estructura recomendada:**
```
data/
├── examples.json
└── validate_fixtures/
    ├── valid-full.md          # SKILL.md válido completo → debe pasar
    ├── valid-minimal.md       # SKILL.md mínimo válido → debe pasar
    ├── broken-frontmatter.md  # Sin frontmatter → debe fallar check 1
    ├── missing-rubrica.md     # Sin ## Rúbrica → debe fallar check 7
    └── short-errors.md        # Solo 2 filas de errores → debe fallar check 6
```

**Script de smoke test** (añadir como `scripts/smoke_test.sh`):
```bash
#!/bin/bash
# smoke_test.sh — verifica que validate_structure.py funciona correctamente
pass=0; fail=0

for fixture in data/validate_fixtures/valid-*.md; do
    python scripts/validate_structure.py "$fixture" --quiet
    [ $? -eq 0 ] && ((pass++)) || { echo "FAIL (debería pasar): $fixture"; ((fail++)); }
done

for fixture in data/validate_fixtures/broken-*.md data/validate_fixtures/missing-*.md data/validate_fixtures/short-*.md; do
    python scripts/validate_structure.py "$fixture" --quiet
    [ $? -ne 0 ] && ((pass++)) || { echo "FAIL (debería fallar): $fixture"; ((fail++)); }
done

echo "Smoke test: $pass passed, $fail failed"
[ $fail -eq 0 ] && exit 0 || exit 1
```

---

### C-A3: Documentar la decisión mínima/completa en README

El README actual describe la estructura pero no guía al usuario sobre
cuándo usar cada modo. Esto es crítico porque meta-skill-architect
**genera skills para usuarios**, y debe guiarlos sobre qué estructura recomendar.

**Añadir sección al README.md:**

```markdown
## Cuándo recomendar estructura mínima vs completa

### Estructura mínima — un solo SKILL.md
Usar cuando:
- La skill tiene ≤3 pasos en su flujo principal
- No hay documentación de referencia externa (APIs, schemas)
- El SKILL.md completo cabe en ≤5000 palabras
- La plataforma de destino es Kilocode u Opencode (contexto limitado)

Ejemplo:
```
my-skill/
└── SKILL.md
```

### Estructura completa — carpetas separadas
Usar cuando:
- references/: documentación de API, schemas o guías >5000 palabras
- scripts/: tareas determinísticas y repetibles (validación, formateo)
- assets/: plantillas de output, templates JSON, imágenes
- data/: conjuntos de evaluación, fixtures de prueba

Ejemplo:
```
my-skill/
├── SKILL.md
├── references/
│   └── api-docs.md
├── scripts/
│   └── validate.py
├── assets/
│   └── template.json
└── data/
    └── evals.json
```

### Regla de decisión rápida
¿El SKILL.md necesita cargar contexto externo bajo demanda? → completa
¿Funciona autónomamente con un solo archivo? → mínima
```

---

### C-A4: Añadir guía de estructura al ciclo de generación en `task.md`

Cuando meta-skill-architect genera una nueva skill, debe recomendar
la estructura apropiada. Actualmente no lo hace.

**Añadir al Paso 1 (Intención) en `task.md`:**

```markdown
### Recomendación de estructura (al final del Paso 1)

Después de definir la intención, declara qué estructura recomiendas:

| Condición | Estructura |
|-----------|-----------|
| Skill con 1-3 pasos, sin refs externas | Mínima (solo SKILL.md) |
| Skill con docs de referencia extensas | Completa (+ references/) |
| Skill con validación automatizable | Completa (+ scripts/) |
| Skill con plantillas de output | Completa (+ assets/) |

Ejemplo de output del Paso 1:
"Intención: clasificador de emails por urgencia.
Estructura recomendada: **mínima** — flujo de 3 pasos, sin dependencias externas."
```

---

## 4. Bugs reales en scripts

### Bug B1 — `validate_structure.py`: función duplicada (crítico)

`check_rubrica_has_both_columns` está definida **dos veces** (líneas ~130 y ~160).
La segunda definición sobreescribe la primera silenciosamente.
La segunda versión retorna `True, None` en el caso de éxito en vez de
`True, ""` — inconsistente con el tipo `tuple[bool, str]` declarado.
Lo mismo ocurre con `check_error_table_has_actions`.

**Corrección en `validate_structure.py`:** Eliminar las definiciones duplicadas
(las segundas, líneas ~160-185). Conservar solo las primeras.

---

### Bug B2 — `validate_structure.py`: checks 7-9 definidos pero nunca llamados

El docstring dice:
```
7. No placeholders [PENDIENTE:], [TODO:]
8. Rúbrica tiene columnas de éxito Y fallo
9. Tabla de errores tiene columna de acción
```

Las funciones `check_no_placeholder`, `check_rubrica_has_both_columns` y
`check_error_table_has_actions` existen pero **nunca se llaman** en
`validate_structure()`. El validador solo ejecuta checks 1-6.

**Corrección:** Añadir las llamadas en `validate_structure()`:

```python
# Después del bloque de secciones requeridas:

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
```

---

### Bug B3 — `validate_structure.py`: `count_error_rows` puede dar falso positivo

La función sale del bucle cuando encuentra una línea vacía (`elif line.strip() == ""`),
pero las tablas Markdown frecuentemente tienen líneas vacías antes del siguiente header.
Esto puede hacer que el contador se detenga antes de contar todas las filas.

**Corrección:**

```python
def count_error_rows(content: str) -> int:
    lines = content.split("\n")
    in_errors_table = False
    row_count = 0

    for line in lines:
        if "## Manejo de Errores" in line:
            in_errors_table = True
            continue
        if in_errors_table:
            # Solo rompe en nuevo header H2, no en líneas vacías
            if line.strip().startswith("## ") and "Manejo" not in line:
                break
            if line.strip().startswith("|") and "---" not in line:
                row_count += 1

    return max(0, row_count - 1)  # -1 por la fila de headers
```

---

### Bug B4 — `validate_structure.py`: `SECTIONS_REQUIRED` exige ambas variantes de rúbrica

```python
SECTIONS_REQUIRED = {"## Manejo de Errores", "## Rúbrica", "## Rúbrica de Validación"}
```

El validador falla si el SKILL.md tiene `## Rúbrica` pero no
`## Rúbrica de Validación` (o viceversa). Son nombres alternativos para
la misma sección, no secciones distintas.

**Corrección:** Cambiar la lógica de validación de secciones para aceptar
cualquiera de las dos variantes:

```python
SECTIONS_REQUIRED_MANDATORY = {"## Manejo de Errores"}
SECTIONS_RUBRICA_VARIANTS = {"## Rúbrica", "## Rúbrica de Validación"}

def validate_sections(content: str, is_minima: bool = False) -> tuple[bool, list[str]]:
    errors = []
    for section in SECTIONS_REQUIRED_MANDATORY:
        if section not in content:
            errors.append(section)
    # Acepta cualquier variante de rúbrica
    if not any(v in content for v in SECTIONS_RUBRICA_VARIANTS):
        errors.append("## Rúbrica (o ## Rúbrica de Validación)")
    return len(errors) == 0, errors
```

---

### Bug B5 — `mcp_server.py`: referencias al nombre viejo y versión desactualizada

```python
def get_skill_metadata() -> dict:
    return {
        "name": "prompt_v22",          # ← nombre viejo
        "version": "2.2.0",            # ← versión desactualizada
        ...
    }
```

Y en el evento `ready`:
```python
"server": "prompt_v22_mcp",            # ← nombre viejo
"version": "2.2.0",                    # ← versión desactualizada
```

**Corrección:**

```python
def get_skill_metadata() -> dict:
    return {
        "name": "meta-skill-architect",
        "version": "3.0.0",
        ...
    }
```

```python
"server": "meta-skill-architect-mcp",
"version": "3.0.0",
```

---

### Bug B6 — `system.md`: carácter chino residual en Capa 3

```markdown
la regla invariant立即 bloquea la solicitud.
```

El carácter `立即` (chino: "inmediatamente") es un artefacto de generación.

**Corrección:**
```markdown
la regla invariante bloquea la solicitud inmediatamente.
```

---

### Bug B7 — `system.md`: typo en la description del frontmatter

```yaml
o pregunté cómo estructurar un prompt   # ← conjugación incorrecta
```

**Corrección:**
```yaml
o preguntar cómo estructurar un prompt
```

---

### Bug B8 — `examples.json`: versión interna desincronizada

```json
"version": "2.3.0",
"metadata": { "version": "2.3.0" }
```

Debe ser `3.0.0` para ser coherente con el sistema.

---

### Bug B9 — `test_runner.py`: simula outputs en vez de ejecutar la skill

El runner tiene este comentario honesto:
```python
# Simular output (en uso real, llamar a la skill)
skill_output = f"SKILL.md procesado para: {test.input_text[:30]}..."
```

Esto hace que `test_runner.py` siempre genere resultados falsos. Las
expectations se evalúan contra un string simulado, no contra el output real.

Dado que meta-skill-architect es un agente de diseño (no de ejecución),
la solución correcta es documentar esto explícitamente en el script y en
el README, en vez de dejar código que parece funcionar pero no lo hace.

**Corrección en el docstring de `test_runner.py`:**

```python
"""
test_runner.py v2 - LLM-as-a-Judge evaluation suite para meta-skill-architect

NOTA DE USO: Este script requiere outputs reales de la skill para evaluar.
El modo de uso correcto es:
  1. Ejecutar el modelo con cada prompt de examples.json manualmente
  2. Guardar los outputs en data/outputs/<eval_id>.md
  3. Ejecutar: python scripts/test_runner.py --data data/examples.json --outputs data/outputs/

El modo simulado (sin --outputs) es solo para smoke test del pipeline de evaluación.
"""
```

Y añadir el flag `--outputs` al parser:
```python
parser.add_argument("--outputs", type=Path, default=None,
    help="Directorio con outputs reales de la skill (un .md por eval_id)")
```

---

## 5. Correcciones menores (no bugs, calidad)

| ID | Archivo | Problema | Corrección |
|----|---------|---------|-----------|
| M1 | `README.md` | `references/examples.md` listado como "5 ejemplos canónicos" pero ahora tiene 7 | Actualizar a "7 ejemplos canónicos" |
| M2 | `validate.sh` | Solo detecta `SOSPECHOSO` como inyección; debería también detectar `INYECCIÓN:` | Añadir `grep -qi "INYECCIÓN:"` |
| M3 | `SKILL.md` | Typo: "Problema nuovo" en tabla de punto de entrada | Corregir a "Problema nuevo" |
| M4 | `task.md` | `## Ejemplos canónicos` referencia solo 3 ejemplos pero hay 7 | Actualizar la lista |
| M5 | `validate_structure.py` | Comentario `name太长` mezclado en español e indonesio/chino | Corregir a "name demasiado largo" |
| M6 | `validate_structure.py` | `description terlalu panjang` en indonesio | Corregir a "description demasiado larga" |

---

## 6. Resumen priorizado

### Críticos (rompen funcionalidad)
1. **B1** — Función duplicada en validate_structure.py (sobreescritura silenciosa)
2. **B2** — Checks 7-9 nunca se ejecutan (el validador no valida lo que promete)
3. **B4** — SECTIONS_REQUIRED falla con SKILLs válidos que usan variante de rúbrica
4. **B9** — test_runner.py simula outputs (no evalúa nada real)

### Importantes (inconsistencias que confunden)
5. **B5** — mcp_server.py con nombre y versión viejos
6. **B3** — count_error_rows se detiene antes con líneas vacías
7. **C-A1** — Plantillas embebidas en task.md inflaman el contexto innecesariamente
8. **C-A4** — El ciclo no recomienda estructura al generar una skill nueva

### Menores (calidad y mantenibilidad)
9. **B6, B7** — Residuos en system.md (caracteres, typo)
10. **B8** — examples.json con versión desincronizada
11. **C-A2** — Sin fixtures de prueba para el validador
12. **C-A3** — README sin guía de decisión mínima/completa
13. **M1-M6** — Typos y referencias desactualizadas

---

## 7. Estado post-correcciones esperado

| Dimensión | Antes | Después |
|-----------|-------|---------|
| Checks reales del validador | 6/9 | 9/9 |
| Consistencia de nombres | prompt_v22 en 3 lugares | meta-skill-architect en todos |
| Versiones sincronizadas | 3 archivos con v2.x | todos en v3.0.0 |
| Fixtures de validación | 0 | 5 |
| Guía estructura mínima/completa | ausente | en README + Paso 1 |
| Plantillas en task.md | embebidas (inflación) | referenciadas desde assets/ |

---

*Evaluación generada: 2025-04-26*
*Evaluador: análisis estático de archivos — no requiere ejecución*
