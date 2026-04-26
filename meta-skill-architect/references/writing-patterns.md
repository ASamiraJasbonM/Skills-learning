# Patrones de Escritura de Skills

Este archivo contiene los 5 patrones de escritura para generar SKILLS robustos.
Consulta este archivo cuando estés escribiendo o revisando instrucciones.

---

## Patrón 1: Definición de formato de output

El output format más resistente especifica la plantilla exacta, no una descripción.

### Robusto
```markdown
## Formato de salida
USA EXACTAMENTE esta estructura:
# [Nombre de la skill en kebab-case]
## Rol
[Una oración: qué hace el agente]
## Tarea
[Pasos numerados]
## Manejo de Errores
| Error | Acción |
```

### Frágil
```markdown
El output debe ser un SKILL.md bien formateado con las secciones estándar.
```

---

## Patrón 2: Instrucciones con ejemplos input→output

Para comportamientos precisos, un ejemplo vale más que tres reglas.

### Robusto
```markdown
## Formato de veredicto de auditoría
Ejemplo de veredicto APROBAR:
"Criterio #2 Cobertura errores: PASA — 6 escenarios documentados (líneas 45-67),
todos con acción concreta, ninguno genérico."

Ejemplo de veredicto RECHAZAR:
"Criterio #2 Cobertura errores: FALLA — Solo 2 escenarios. La tabla existe
pero los escenarios #3 y #4 dicen 'manejar apropiadamente' sin acción concreta."
```

### Frágil
```markdown
El veredicto debe indicar si el criterio pasa o falla con evidencia.
```

---

## Patrón 3: Manejo de errores con rama de recuperación

Cada error en la tabla debe tener una acción de recuperación, no solo un diagnóstico.

### Robusto
| Error | Diagnóstico | Acción | Señal de recuperación |
|-------|------------|--------|----------------------|
| Input sin delimitadores | El usuario no usó `<input>` | Solicitar con ejemplo concreto | Usuario provee input con delimitadores |
| Plataforma no especificada | 2 rondas sin respuesta | Aplicar supuesto Claude + documentar en `## Supuestos` | — |

### Frágil
| Error | Manejo |
|-------|--------|
| Input inválido | Solicitar aclaración |

> **Nota de implementación:** Esta tabla de 4 columnas es el estándar recomendado.
> La plantilla mínima usa 2 columnas por restricción de tokens.
> Cuando el contexto lo permita, usar siempre 4 columnas.

---

## Patrón 4: Rúbrica con comportamiento observable (no intencional)

La diferencia entre una rúbrica medible y una vaga.

### Observable
"PASA si: la tabla de errores tiene ≥4 filas Y cada fila tiene columnas
Error/Diagnóstico/Acción/Señal — verificable contando filas y columnas."

### Intencional (no verificable)
"PASA si: el manejo de errores es completo y cubre los casos importantes."

---

## Patrón 5: Punto de entrada con detección de contexto

En vez de un único flujo, detectar el estado del usuario y saltar al paso correcto.

### Con detección
```
Lee las primeras 2 interacciones del usuario. Detecta:
- ¿Trae un SKILL.md existente? → Salta a Paso 3 (riesgos) y Paso 5 (auditoría)
- ¿Describe un problema nuevo en ≤2 oraciones? → Ejecuta Paso 1 completo
- ¿Tiene un SKILL.md pero dice "no funciona"? → Salta a Protocolo de Generalización
```

### Sin detección
```
Siempre ejecuta el ciclo de 5 pasos desde el Paso 1.
```

---

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

---

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

---

*Referencia: task.md dice "consulta references/writing-patterns.md al escribir o revisar instrucciones"*
*No cargues automáticamente.*