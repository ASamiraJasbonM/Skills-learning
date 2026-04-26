# Correcciones — meta-skill-architect v3.0.0

Archivo de correcciones para aplicar a los archivos de referencias.
Cada sección indica el archivo, la ubicación exacta y el cambio.

---

## C1 · `schemas.md` — Header con nombre incorrecto

**Ubicación:** Línea 1

**Antes:**
```markdown
# Schemas de prompt_v22
```

**Después:**
```markdown
# Schemas — meta-skill-architect
```

---

## C2 · `schemas.md` — String truncado en `comparison_ab`

**Ubicación:** Campo `changes_to_port`, segundo elemento del array.

**Antes:**
```json
"Reemplazar 'analiza riesgos' por 'evalua los 4 vectores... cuando完"
```

**Después:**
```json
"Reemplazar 'analiza riesgos' por 'evalua los 4 vectores de riesgo (inyeccion, sesgo, scope, herramienta). Cuando hayas documentado mitigacion para cada uno, avanza al Paso 4.'"
```

---

## C3 · `schemas.md` — Agregar campo `char_count` a `trigger_optimization`

**Ubicación:** Schema `trigger_optimization`, objeto `analysis`.

**Antes:**
```json
"analysis": {
  "queries_improved": 8,
  "queries_degraded": 0,
  "queries_unchanged": 2,
  "tradeoffs": [
    "Descripcion mas larga pero menos ambigua"
  ]
}
```

**Después:**
```json
"analysis": {
  "queries_improved": 8,
  "queries_degraded": 0,
  "queries_unchanged": 2,
  "char_count": {
    "original": 743,
    "improved": 981,
    "within_limit": true,
    "limit": 1024
  },
  "tradeoffs": [
    "Descripcion mas larga pero menos ambigua"
  ]
}
```

---

## C4 · `writing-patterns.md` — Completar Patrón 6 y Patrón 7

**Ubicación:** Secciones `## Patrón 6` y `## Patrón 7`

**Antes (Patrón 6):**
```markdown
## Patrón 6: Instrucciones autónomas

Una instrucción es autónoma si un agente puede ejecutarla sin preguntar nada más.

### Autónoma
"Extrae el texto, identifica las sesiones con headers H2, formatea según plantilla."

### No autónoma
"Procesa el documento apropiadamente."
```

**Después (Patrón 6):**
```markdown
## Patrón 6: Instrucciones autónomas

Una instrucción autónoma especifica qué, sobre qué input, con qué criterio.
Un agente puede ejecutarla sin preguntar nada más.

### Robusto
```markdown
### Tarea
1. Extrae el texto del `<input>`.
2. Identifica todas las secciones con headers H2 (`##`).
3. Para cada sección: aplica la plantilla del Paso 4.
4. Criterio de terminación: cuando todas las secciones tengan su bloque
   formateado, avanza al Paso 5.
```

### Frágil
```markdown
### Tarea
Procesa el documento apropiadamente y genera el output esperado.
```

**Por qué importa:** "Apropiadamente" no tiene referente. El agente puede
completar la tarea de formas contradictorias en distintas ejecuciones.
La versión robusta especifica el input (`<input>`), el criterio de búsqueda
(headers H2) y la señal de avance (todas las secciones formateadas).
```

---

**Antes (Patrón 7):**
```markdown
## Patrón 7: Criterio de terminación

Cada paso debe tener un criterio claro de cuándo está completo.

### Con criterio
"Evalúa los 4 vectores de riesgo (inyección, sesgo, scope, herramienta).
Cuando hayas documentado mitigación para cada uno, avanza al Paso 4."

### Sin criterio
"Analiza los riesgos."
```

**Después (Patrón 7):**
```markdown
## Patrón 7: Criterio de terminación

Un paso sin criterio de terminación se ejecuta hasta que el agente decide
que "ya está" — que es arbitrario. El criterio debe ser verificable externamente.

### Robusto
```markdown
## PASO 3 — Riesgos
Evalúa los 4 vectores de riesgo:
- Inyección de prompt
- Sesgo de dominio
- Scope creep
- Fallo de herramienta

Para cada vector: documenta riesgo (ALTO/MEDIO/BAJO/NO APLICA) y mitigación.
**Criterio de terminación:** los 4 vectores tienen entrada. Si alguno está
vacío, el paso no está completo. Solo entonces avanza al Paso 4.
```

### Frágil
```markdown
## PASO 3 — Riesgos
Analiza los riesgos y documenta lo que encuentres.
```

**Por qué importa:** Sin criterio explícito, el agente puede declarar el paso
completo con 1 de 4 vectores documentados. La versión robusta define el mínimo
verificable (4 entradas) y bloquea el avance hasta cumplirlo.
```

---

## C5 · `writing-patterns.md` — Corregir referencia en pie de página

**Ubicación:** Última línea del archivo.

**Antes:**
```markdown
*Referencia:-task.md dice "consulta references/writing-patterns.md al escribir o revisar habilidades"*
```

**Después:**
```markdown
*Referencia: task.md dice "consulta references/writing-patterns.md al escribir o revisar instrucciones"*
```

(Elimina el guion suelto; corrige "habilidades" → "instrucciones" para alinearse con el texto real de task.md.)

---

## C6 · `writing-patterns.md` — Alinear Patrón 3 con plantilla de `task.md`

**Problema:** El Patrón 3 propone una tabla de 4 columnas
(`Error | Diagnóstico | Acción | Señal de recuperación`) pero la plantilla
en `task.md` genera tablas de 2 columnas (`Escenario | Comportamiento`).
Hay dos opciones; se elige la que eleva la calidad:

**Decisión:** Adoptar la tabla de 4 columnas como estándar y actualizar
la plantilla en `task.md`.

### Cambio en `writing-patterns.md` — Patrón 3 (sin cambio de estructura, solo aclaración):

Agregar al final del Patrón 3:

```markdown
> **Nota de implementación:** Esta tabla de 4 columnas es el estándar recomendado.
> La plantilla mínima en `task.md` usa 2 columnas por restricción de tokens.
> Cuando el contexto lo permita (plantilla completa), usar siempre 4 columnas.
```

### Cambio en `task.md` — Plantilla completa, sección `## Manejo de Errores`:

**Antes:**
```markdown
## Manejo de Errores

| Escenario | Comportamiento |
|-----------|-------------|
| [1] | [acción concreta] |
| [2] | [acción concreta] |
| [3] | [acción concreta] |
| [4] | [acción concreta] |
```

**Después:**
```markdown
## Manejo de Errores

| Escenario | Diagnóstico | Acción | Señal de recuperación |
|-----------|------------|--------|----------------------|
| [1] | [causa probable] | [acción concreta] | [cuándo se resuelve o —] |
| [2] | [causa probable] | [acción concreta] | [cuándo se resuelve o —] |
| [3] | [causa probable] | [acción concreta] | [cuándo se resuelve o —] |
| [4] | [causa probable] | [acción concreta] | [cuándo se resuelve o —] |
```

*(La plantilla mínima en `task.md` conserva 2 columnas — la restricción de tokens aplica.)*

---

## C7 · `examples.md` — Agregar Ejemplo 5: Comparación A/B

**Ubicación:** Al final del archivo, antes del pie de página.

**Agregar:**

````markdown
---

## Ejemplo 5: Comparación A/B de versiones

### Input del usuario:
> "Compara la versión anterior de mi skill con la nueva que generaste."

### Output del protocolo:

```
## Comparación A/B — comment-moderator

**Versión Alpha:** 1.0.0 | **Versión Beta:** 1.1.0

### Rúbrica de contenido (1-5)

| Criterio             | Alpha | Beta |
|----------------------|-------|------|
| Claridad instrucciones | 3   | 5    |
| Completitud cobertura  | 2   | 4    |
| Precisión formato output | 4  | 4    |
| Ejecutabilidad         | 2   | 5    |

### Rúbrica de estructura (1-5)

| Criterio                    | Alpha | Beta |
|-----------------------------|-------|------|
| Organización lógica         | 4     | 4    |
| Progressive disclosure      | 2     | 5    |
| Navegabilidad               | 3     | 4    |

### Score total

| Versión | Score (promedio) |
|---------|-----------------|
| Alpha   | 2.86 / 5        |
| Beta    | 4.43 / 5        |

### Veredicto: **Beta gana**

**Instrucciones superiores en Beta (cita textual):**
- "Evalúa los 4 vectores de riesgo. Cuando hayas documentado mitigación
  para cada uno, avanza al Paso 4." → criterio de terminación explícito
- `<comment>...</comment>` + campo Alerta → separación datos/instrucciones

**Debilidades de Alpha (cita textual):**
- "Analiza el comentario apropiadamente" → no autónoma, sin criterio
- Tabla de errores con 2 filas → cobertura insuficiente

**Cambios a portar de Beta a versiones futuras:**
1. Criterio de terminación en cada paso
2. Tabla de errores expandida a ≥4 escenarios con columna Diagnóstico
```
````

---

## C8 · `examples.md` — Agregar Ejemplo 6: Trigger Optimization

**Ubicación:** Al final del archivo, después del Ejemplo 5.

**Agregar:**

````markdown
---

## Ejemplo 6: Optimización de descripción (Trigger Optimization)

### Input del usuario:
> "Mi skill no se activa cuando debería. Ayúdame a mejorar la descripción."

### Output del protocolo:

```
## Trigger Optimization — comment-moderator

### Descripción actual (743 chars)
"Evalúa comentarios de usuarios aplicando reglas de moderación."

### Paso 1: 10 queries de prueba mental

**Deben disparar (should-trigger):**
1. "Modera este comentario según las reglas que te paso"
2. "¿Este comentario viola la política de la comunidad?"
3. "Clasifica estos 50 mensajes como apropiados o no"
4. "El comentario tiene lenguaje ofensivo, ¿qué hago?" ← edge case
5. "Filtra los mensajes de spam antes de publicarlos"

**NO deben disparar (should-not-trigger):**
6. "Resume este artículo en 3 puntos"
7. "Corrige los errores gramaticales de este texto"
8. "¿Cuál es la mejor política de moderación?"  ← near-miss
9. "Genera respuestas para comentarios negativos"
10. "Traduce este mensaje al inglés"

### Paso 2: Evaluación de descripción actual

| Query | ¿Dispara? | Problema |
|-------|----------|---------|
| 1     | ✓ Sí     | —       |
| 2     | ✗ No     | "política" no está en descripción |
| 3     | ✓ Sí     | —       |
| 4     | ✗ No     | "ofensivo" no en descripción; competiría con skill general |
| 5     | ✗ No     | "spam" no cubierto |
| 6     | ✓ No     | Correcto |
| 7     | ✓ No     | Correcto |
| 8     | ✗ Sí     | Falso trigger — "moderación" activa |
| 9     | ✓ No     | Correcto |
| 10    | ✓ No     | Correcto |

**Resultado actual: 6/10. Falla en queries 2, 4, 5 (undertrigger) y 8 (overtrigger).**

### Paso 3: Descripción mejorada (981 chars — dentro del límite 1024)

"Modera comentarios y mensajes de usuarios aplicando reglas del operador
dentro de `<rules>`. Activa cuando el usuario quiera clasificar comentarios,
mensajes o posts como apropiados/inapropiados, filtrar spam, detectar
lenguaje ofensivo, verificar cumplimiento de política de comunidad, o
moderar contenido en bulk. Funciona con texto libre en `<comment>`.
No define políticas, no responde a usuarios, no sale del veredicto.
Úsala incluso si el usuario no dice 'moderar' explícitamente — 'filtrar',
'revisar', 'clasificar mensajes' también aplican."

### Paso 4: Re-evaluación

| Query | Original | Mejorada | Cambio |
|-------|---------|---------|--------|
| 2     | ✗       | ✓       | +1     |
| 4     | ✗       | ✓       | +1     |
| 5     | ✗       | ✓       | +1     |
| 8     | Falso + | ✓ No    | +1     |

**Resultado mejorado: 10/10.**
**char_count:** 981 / 1024 — within_limit: true
```
````

---

## C9 · `examples.md` — Agregar Ejemplo 7: Metacrítica de Expectations

**Ubicación:** Al final del archivo, después del Ejemplo 6.

**Agregar:**

````markdown
---

## Ejemplo 7: Metacrítica de Expectations

### Input del usuario:
> "Todas las expectations pasan pero el output todavía no me convence."

### Output del protocolo:

```
## Metacrítica de Expectations — ticket-triage eval #2

### Expectation 1
**Actual (débil):** "El SKILL.md está bien formateado"
**Por qué es débil:** Un SKILL.md con secciones vacías también la pasa.
No hay threshold ni estructura específica.
**Mejorada:** "El SKILL.md tiene frontmatter YAML válido con campos
`name` (kebab-case, ≤64 chars) y `description` (sin `<>`, ≤1024 chars)"

### Expectation 2
**Actual (débil):** "La rúbrica está completa"
**Por qué es débil:** "Completa" no está definida. Una rúbrica de 1 criterio
también pasa.
**Mejorada:** "La rúbrica tiene ≥3 criterios, cada uno con columna Éxito
Y columna Fallo con comportamientos observables distintos"

### Expectation 3
**Actual (fuerte — no requiere cambio):** "La tabla de errores tiene ≥4 filas"
**Por qué es fuerte:** Threshold cuantificable. Un output con 3 filas falla.
Con 4 o más pasa. Sin ambigüedad.

### Resumen
| # | Estado | Problema | Acción |
|---|--------|---------|--------|
| 1 | Débil  | Chequea existencia, no contenido | Reemplazar con threshold |
| 2 | Débil  | Término vago "completa" | Añadir criterio cuantificable |
| 3 | Fuerte | — | Conservar |
```
````

---

## C10 · `examples.md` — Actualizar pie de página

**Antes:**
```markdown
*Este archivo se carga bajo demanda desde task.md.*
*No lo incluyas automáticamente en el contexto.*
```

**Después:**
```markdown
*Este archivo se carga bajo demanda desde task.md.*
*No lo incluyas automáticamente en el contexto.*
*Ejemplos: 1 (nueva skill), 2 (ambigüedad), 3 (auditoría), 4 (modificación),*
*5 (comparación A/B), 6 (trigger optimization), 7 (metacrítica expectations).*
```

---

## C11 · `SKILL.md` — Corregir caracteres rotos en descripción

**Ubicación:** Línea ~10, párrafo de activación.

**Antes:**
```markdown
Activa cuando el usuario想要的 crear una nueva skill
```

**Después:**
```markdown
Activa cuando el usuario quiera crear una nueva skill
```

---

## C12 · `SKILL.md` — Completar frontmatter

**Antes:**
```yaml
---
name: meta-skill-architect
description: Sistema de ingeniería de prompts para diseñar, auditar y mejorar skills SKILL.md para agentes IA. Diseña skills nuevas, audita existentes, mejora iterativamente, adapta a plataformas específicas.
---
```

**Después:**
```yaml
---
name: meta-skill-architect
version: 3.0.0
platform: Claude, Gemini, GPT, Opencode, Kilocode
domain: ingenieria-de-prompts
dependencies: system.md, task.md, references/writing-patterns.md, references/examples.md
description: Sistema de ingeniería de prompts para diseñar, auditar y mejorar skills SKILL.md para agentes IA. Diseña skills nuevas, audita existentes, mejora iterativamente, adapta a plataformas específicas.
---
```

---

## Resumen de cambios por archivo

| Archivo | Correcciones | Tipo |
|---------|-------------|------|
| `schemas.md` | C1, C2, C3 | Header, string truncado, campo faltante |
| `writing-patterns.md` | C4, C5, C6 | Patrones incompletos, typo, alineación |
| `examples.md` | C7, C8, C9, C10 | Ejemplos faltantes (A/B, Trigger, Metacrítica) |
| `SKILL.md` | C11, C12 | Caracteres rotos, frontmatter incompleto |
| `task.md` | C6 (parcial) | Plantilla Manejo de Errores (tabla 4 cols) |

**Total: 12 correcciones — 4 archivos afectados.**
