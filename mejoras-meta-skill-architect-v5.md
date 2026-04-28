# Plan de Mejoras — meta-skill-architect v5.0.0 → v5.1.0

> **Autor del análisis:** Ingeniero Senior  
> **Fecha:** 2026-04-28  
> **Fuente:** Auditoría externa (Deepseek) + revisión propia del código fuente  
> **Veredicto base:** APROBAR con mejoras de robustez — la arquitectura es sólida, los cambios son de hardening, no de rediseño.

---

## Resumen ejecutivo

La skill está en nivel de producción. El análisis externo identificó 5 áreas de mejora; mi revisión del código confirma 4 de ellas y agrega 3 propias que el análisis no detectó. Los cambios propuestos son todos quirúrgicos: ninguno toca la arquitectura central ni el ciclo de 5 pasos.

**Prioridad de aplicación recomendada:**

| Prioridad | Cambios | Impacto |
|-----------|---------|---------|
| P1 — Aplicar ahora | C1, C2, C5, C6 | Corrección de bugs reales o ambigüedad que ya causa fallos |
| P2 — Próximo ciclo | C3, C4 | Mejoras de robustez en edge cases |
| P3 — Opcional | C7 | Pulido estético, sin impacto funcional |

---

## C1 — Rúbrica con criterio de ejecutabilidad (P1)

**Archivo:** `SKILL.md`  
**Problema confirmado:** El criterio "Densidad semántica" en la Rúbrica usa "Secciones ejecutables vs Vacías/placeholders" — definición circular. Un SKILL.md con `[PENDIENTE: pregunta X]` no está vacío, pero tampoco es ejecutable. El criterio generaría un falso positivo.

El análisis externo detectó esto. Revisando el código confirmo que `validate_structure.py` ya tiene `check_no_placeholder()` que detecta `[PENDIENTE:]`, pero la **Rúbrica del SKILL.md no lo refleja**. Hay inconsistencia entre lo que valida el script y lo que declara la rúbrica.

**Cambio en `SKILL.md`, sección `## Rúbrica`:**

```markdown
# ANTES
| Densidad semántica | Secciones ejecutables | Vacías/placeholders |

# DESPUÉS
| Ejecutabilidad | Toda instrucción cumple: es autónoma, tiene criterio de terminación, no compite con otra instrucción, y no tiene narrowing excesivo (ver Análisis de Ejecutabilidad en references/protocols-core.md) | Alguna instrucción requiere inferencia del agente, o contiene [PENDIENTE:] sin resolver |
```

**Por qué:** Alinea la rúbrica con los checks reales de `validate_structure.py` y con el Protocolo de Ejecutabilidad ya documentado en `protocols-core.md`. Elimina la ambigüedad sin añadir nueva lógica.

---

## C2 — Algoritmo de enrutamiento determinista (P1)

**Archivo:** `task.md`  
**Problema confirmado:** La tabla de "Punto de entrada según la solicitud" tiene 7 situaciones más el caso de migración. El criterio para distinguir "audita" de "mejora" es léxico (literalmente depende de qué palabra use el usuario), lo cual falla ante frases como "¿qué mejorarías de esta skill?", "dale un vistazo", o "¿está bien así?".

Adicionalmente, la distinción entre ir al Paso 3 o al Paso 5 para una skill existente no es mutuamente excluyente — una skill existente puede necesitar ambos.

**Cambio en `task.md`, sección `## Punto de entrada`:**

Reemplazar la tabla actual por un algoritmo explícito con criterio de decisión basado en estado del artefacto, no en palabras clave:

```markdown
## Algoritmo de Enrutamiento (Punto de Entrada)

Ejecuta en orden. Detente en el primer match:

1. ¿El usuario proporciona texto que empieza con `---` (frontmatter YAML)?  
   → Es una skill existente. Ejecuta **Reporte de Auditoría** (Paso 5).  
   → Si el usuario también pide cambios → continúa con Paso 3 → Paso 4 → Paso 5.

2. ¿El usuario proporciona un archivo o texto sin frontmatter `---`?  
   → Es un prompt informal. **Modo Migración** (S9 en references/protocols-advanced.md).

3. ¿La interacción tiene ≥2 iteraciones de modificación sobre la misma skill?  
   → Ejecuta **Análisis Post-Modificación** (references/protocols-core.md) ANTES de proponer cualquier cambio adicional.

4. ¿El usuario describe un problema en lenguaje natural sin adjuntar archivo?  
   → **Nueva skill.** Inicia desde Paso 1.

5. Ambigüedad total (no encaja en ningún caso anterior):  
   → Pregunta única: "¿Traes una skill existente para revisar, o empezamos desde cero?"  
   → No generes hasta recibir respuesta.
```

**Por qué:** El enrutamiento basado en estado del artefacto (`---` presente o no) es determinista y no depende de que el usuario use la palabra exacta "audita" o "mejora". Elimina la ambigüedad de 7 ramas a 5, con criterio objetivo en cada una.

---

## C3 — Modo contexto ultra-limitado en el Fallback (P2)

**Archivo:** `SKILL.md`, sección `## Fallback de contexto`  
**Problema detectado (análisis externo, confirmado):** El Fallback actual declara qué hacer si `system.md` no está disponible, pero no cubre el caso donde el contexto total es insuficiente para cargar `system.md` + `task.md` + referencias. En Kilocode/Opencode con ventanas de 8k tokens, cargar la estructura completa puede provocar truncamiento silencioso.

**Cambio en `SKILL.md`, sección `## Fallback de contexto`:**

Añadir bloque al final de la sección existente:

```markdown
## Fallback de contexto ultra-limitado (< 8k tokens disponibles)

Si la ventana de contexto no permite cargar task.md o references/:
- Opera solo con las instrucciones de este SKILL.md
- Ignora referencias a protocolos avanzados (S1, S6, S7, etc.)
- Usa la plantilla mínima para todo output
- Declara al usuario: "Operando en modo mínimo por límite de contexto. 
  Funciones avanzadas (auditoría estructurada, comparación A/B, autoevaluación) 
  no disponibles en esta sesión."
- El ciclo de 5 pasos sigue siendo obligatorio
```

**Por qué:** Establece un contrato explícito de degradación graceful en lugar de truncamiento silencioso. El usuario sabe qué funcionalidades tiene disponibles.

---

## C4 — Validación cruzada description↔cuerpo en validate_structure.py (P2)

**Archivo:** `scripts/validate_structure.py`  
**Problema detectado (revisión propia, no en análisis externo):** El script valida que `description` tenga formato correcto (longitud, sin `<>`), pero no valida que lo que promete la description sea implementado en el cuerpo. Esto ya está cubierto como Paso 0 del protocolo de Trigger Optimization en `protocols-core.md`, pero es manual.

El análisis externo no lo detectó, pero revisando `validate_structure.py` veo que tiene 10 checks y ninguno compara description vs body.

**Cambio en `scripts/validate_structure.py`:**

Añadir función `check_description_body_coherence()` después de los checks existentes:

```python
def check_description_body_coherence(content: str, frontmatter: dict) -> tuple[bool, str]:
    """
    Check semántico básico: palabras clave de la description deben aparecer en el cuerpo.
    No es un check semántico completo — detecta solo inconsistencias obvias.
    """
    description = frontmatter.get("description", "")
    if not description:
        return True, ""  # Ya validado en otro check
    
    # Extrae sustantivos clave (palabras de más de 5 chars, no stopwords)
    stopwords = {"para", "como", "desde", "hasta", "sobre", "entre", "cuando", "donde"}
    desc_words = [w.lower() for w in description.split() if len(w) > 5 and w.lower() not in stopwords]
    
    # El cuerpo es el contenido después del frontmatter
    body = "\n".join(content.split("\n")[content.split("\n").index("---", 1) + 1:]) if "---" in content else content
    body_lower = body.lower()
    
    # Si más del 60% de las palabras clave no aparecen en el cuerpo → incoherencia probable
    missing = [w for w in desc_words if w not in body_lower]
    if len(desc_words) > 0 and (len(missing) / len(desc_words)) > 0.6:
        return False, (
            f"description menciona términos ausentes en el cuerpo: {missing[:3]}. "
            "Posible incoherencia description↔cuerpo. Revisar manualmente."
        )
    return True, ""
```

Y registrar en `validate_structure()`:

```python
# Check 11: Coherencia description↔cuerpo (heurístico)
valid, msg = check_description_body_coherence(content, frontmatter)
if not valid:
    errors.append(f"coherencia: {msg}")  # Warning, no bloqueante
```

**Por qué:** Automatiza parcialmente el Paso 0 de Trigger Optimization. Es heurístico (60% de threshold), explícitamente marcado como tal, y emite warning en lugar de bloquear. El check no reemplaza la revisión manual — la complementa.

---

## C5 — mcp_server.py: versión alineada con v5.0.0 (P1)

**Archivo:** `scripts/mcp_server.py`  
**Problema detectado (revisión propia):** El `get_skill_metadata()` retorna `"version": "3.0.0"` y el `main()` también emite `"version": "3.0.0"` en el evento `ready`. La skill ya está en v5.0.0. Esta inconsistencia no es cosmética — si otro agente consulta los metadatos vía MCP, recibe información de versión incorrecta.

Adicionalmente, el README dice que `execute_skill()` ya lanza `NotImplementedError`, lo cual es correcto, pero la versión del archivo es la que falla.

**Cambio en `scripts/mcp_server.py`:**

```python
# ANTES (línea ~18)
def get_skill_metadata() -> dict:
    return {
        "name": "meta-skill-architect",
        "version": "3.0.0",   # ← bug
        ...
    }

# DESPUÉS
def get_skill_metadata() -> dict:
    return {
        "name": "meta-skill-architect",
        "version": "5.0.0",   # ← alineado con SKILL.md
        ...
    }
```

```python
# ANTES (línea ~105, en main())
"result": {
    "event": "ready",
    "server": "meta-skill-architect_mcp",
    "version": "3.0.0",   # ← bug
},

# DESPUÉS
"result": {
    "event": "ready",
    "server": "meta-skill-architect_mcp",
    "version": "5.0.0",   # ← alineado
},
```

**Por qué:** Inconsistencia de versión en metadatos MCP puede causar que agentes clientes rechacen o malinterpreten la skill. Es un bug de 2 líneas con impacto real en integraciones.

---

## C6 — test_runner.py: fecha hardcoded (P1)

**Archivo:** `scripts/test_runner.py`  
**Problema detectado (revisión propia, no en análisis externo):** La función `run_evaluations()` hardcodea `"evaluation_date": "2025-05-26"` en el output. Cada vez que se ejecuta el script, el reporte dice que fue ejecutado el 26 de mayo de 2025, independientemente de cuándo se ejecute realmente.

```python
# ANTES (línea ~180 aprox)
output = {
    "evaluation_date": "2025-05-26",   # ← hardcoded

# DESPUÉS
import datetime
output = {
    "evaluation_date": datetime.date.today().isoformat(),   # ← dinámico
```

El import de `datetime` ya existe en el archivo (línea 8), así que no es un cambio de dependencias.

**Por qué:** Un reporte de evaluación con fecha incorrecta invalida el valor del registro histórico. Bug de 1 línea, sin riesgo de regresión.

---

## C7 — knowledge-log.md: registrar cambios de esta sesión (P3)

**Archivo:** `data/knowledge-log.md`  
**Problema detectado:** El knowledge-log tiene la última entrada el 2026-04-27. Los cambios de v4.1.0 y v5.0.0 (2026-04-28) no están registrados. La tabla "Actualizaciones de Estándar" dice que la última versión fue v4.0.0 → v4.1.0 (aproximado).

**Cambio en `data/knowledge-log.md`, tabla "Actualizaciones de Estándar":**

```markdown
| 2026-04-28 | v4.1.0: correcciones producción (P1-P5): orden auditoría+mejora, visibilidad S1, rúbrica código, historial siempre, trigger knowledge-log | task.md, SKILL.md | ✅ |
| 2026-04-28 | v5.0.0: refactoring estructural — task.md reducido a ~200 líneas, protocolos movidos a references/protocols-advanced.md y protocols-core.md | task.md, references/ | ✅ |
```

**Añadir en tabla "Patrones de Fallo Recurrentes":**

```markdown
| P07 | Versión hardcoded en scripts | mcp_server.py en v3.0.0 cuando skill era v5.0.0 | Sincronizar versión de scripts con SKILL.md en cada release | 2026-04-28 |
| P08 | Fecha hardcoded en reportes | evaluation_date fija en test_runner.py | Usar datetime.date.today().isoformat() | 2026-04-28 |
```

**Por qué:** El knowledge-log es el mecanismo de memoria entre sesiones. Si no se actualiza, los futuros ciclos de automejoramiento (S7) no tienen registro de qué ya fue corregido.

---

## Tabla de impacto consolidada

| ID | Archivo | Tipo | Riesgo si no se aplica | Esfuerzo |
|----|---------|------|------------------------|----------|
| C1 | SKILL.md | Corrección rúbrica | Falso positivo en auditorías | 5 min |
| C2 | task.md | Refactor enrutamiento | Enrutamiento incorrecto ante frases no estándar | 20 min |
| C3 | SKILL.md | Adición fallback | Truncamiento silencioso en contexto limitado | 10 min |
| C4 | validate_structure.py | Nueva función | Incoherencia description↔cuerpo no detectada | 30 min |
| C5 | mcp_server.py | Bug fix versión | Metadatos MCP incorrectos en producción | 2 min |
| C6 | test_runner.py | Bug fix fecha | Reportes con fecha inválida en histórico | 1 min |
| C7 | knowledge-log.md | Actualización registro | Historial incompleto, sesiones futuras sin contexto | 10 min |

---

## Lo que NO cambio (y por qué)

**Ejemplo 3 y 4 en `examples.md` sin fixture específico:**  
El análisis externo sugirió anclar el Ejemplo 3 a un fixture de skill "broken". Revisando los fixtures existentes en `data/validate_fixtures/` (broken-frontmatter.md, missing-rubrica.md, short-errors.md), el material ya existe. Lo que falta es que el Ejemplo 3 los referencie explícitamente. Sin embargo, hacer ese cambio requeriría editar `examples.md` para acoplar ejemplos a fixtures, lo cual introduce dependencia frágil (si alguien renombra un fixture, el ejemplo queda roto). El riesgo de acoplamiento supera el beneficio de anclaje. **No aplicar.**

**Reescritura de description de la skill para trigger optimization:**  
La description actual tiene 487 chars (dentro del límite de 1024) y cubre los contextos principales. El análisis externo no reportó undertriggering. Optimizar description sin evidencia de fallos reales es premature optimization. **No aplicar sin datos de fallos.**

**Cambios a `system.md`:**  
El system prompt es la capa invariante. Modificarlo sin evidencia de fallo en las Reglas Invariantes viola el principio de cambio mínimo. El análisis externo no reportó ningún fallo en la capa de seguridad. **No tocar.**

---

## Historial de esta sesión (para añadir al SKILL.md)

```markdown
## Historial de cambios

| Versión | Cambio | Criterio que resuelve | Fecha |
|---------|--------|----------------------|-------|
| 5.0.0 | Refactoring estructural: task.md a ~200 líneas, protocolos a references/ | Mantenibilidad | 2026-04-28 |
| 5.1.0 | C1: Rúbrica con criterio de ejecutabilidad; C2: Algoritmo de enrutamiento determinista; C3: Fallback ultra-limitado; C4: Check coherencia description↔cuerpo; C5: Versión MCP alineada; C6: Fecha dinámica en test_runner; C7: knowledge-log actualizado | Consistencia rúbrica, robustez enrutamiento, degradación graceful, detección automática incoherencias, metadatos correctos, histórico válido | 2026-04-28 |
```

---

*Plan generado desde revisión directa de archivos fuente + análisis externo Deepseek.*  
*Todos los cambios son aditivos o correcciones de bugs. Ninguno modifica la arquitectura de defensa.*
