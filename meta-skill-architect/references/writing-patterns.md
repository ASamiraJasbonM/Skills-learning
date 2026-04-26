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

Una instrucción es autónoma si un agente puede ejecutarla sin preguntar nada más.

### Autónoma
"Extrae el texto, identifica las sesiones con headers H2, formatea según plantilla."

### No autónoma
"Procesa el documento apropiadamente."

---

## Patrón 7: Criterio de terminación

Cada paso debe tener un criterio claro de cuándo está completo.

### Con criterio
"Evalúa los 4 vectores de riesgo (inyección, sesgo, scope, herramienta).
Cuando hayas documentado mitigación para cada uno, avanza al Paso 4."

### Sin criterio
"Analiza los riesgos."

---

*Referencia:-task.md dice "consulta references/writing-patterns.md al escribir o revisar habilidades"*
*No cargues automáticamente.*