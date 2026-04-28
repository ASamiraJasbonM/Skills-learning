# Protocolos Core — Meta-Skill Architect v5.0.0

Este archivo contiene los protocolos de análisis y optimización: Generalización, Ejecutabilidad, Comparación A/B, Trigger Optimization y Metacrítica.

Cárgalo bajo demanda cuando el usuario necesite estos protocolos específicos.

---

## Protocolo de Generalización (antes de modificar)

Cuando el usuario reporta que algo "no funciona", sigue este orden de razonamiento:

### 1. Diagnostica el nivel del problema

| Síntoma | Causa probable | Solución correcta |
|---------|---------------|-------------------|
| El agente ignora una instrucción específica | Instrucción ambigua o enterrada | Reubica o reformula, explica el why |
| El agente hace algo diferente cada vez | Instrucciones que compiten | Elimina la contradicción, no añadas más reglas |
| El agente funciona en los ejemplos del usuario pero falla en producción | Overfitting a los ejemplos | Generaliza: escribe el principio, no el caso |
| El agente produce output correcto pero el usuario no queda satisfecho | Mal definición de éxito | Revisa la rúbrica, no las instrucciones |

### 2. Aplica el principio de lean prompt

Antes de añadir cualquier instrucción nueva, pregúntate:
- ¿Qué instrucción existente está fallando? → repárala
- ¿Hay algo que pueda eliminar y que no esté contribuyendo? → elimínalo
- ¿El problema es de instrucciones o de ejemplos insuficientes? → añade un ejemplo, no una regla

### 3. Umbral para cambio de metáfora

Si después de 2 iteraciones quirúrgicas el mismo comportamiento sigue fallando, el problema no es la instrucción — es el modelo mental que el prompt transmite. Reescribe la sección desde cero con una metáfora diferente y explica el why. No acumules reglas sobre un modelo mental roto.

---

## Análisis de Ejecutabilidad de Instrucciones

Al auditar o mejorar un SKILL.md, evalúa cada instrucción con estas 4 preguntas:

### Pregunta 1: ¿Es la instrucción autónoma?

Una instrucción es autónoma si un agente puede ejecutarla sin preguntar nada más.
- ❌ "Procesa el documento apropiadamente" → no autónoma
- ✅ "Extrae el texto, identifica las secciones con headers H2, formatea según plantilla" → autónoma

### Pregunta 2: ¿Existe un criterio de terminación?

El agente necesita saber cuándo ha completado cada paso.
- ❌ "Analiza los riesgos" → ¿cuándo está completo?
- ✅ "Evalúa los 4 vectores de riesgo (inyección, sesgo, scope, herramienta). Cuando hayas documentado mitigación para cada uno, avanza al Paso 4." → tiene criterio

### Pregunta 3: ¿Hay instrucciones que compiten?

Busca pares de instrucciones que pidan comportamientos contradictorios:
- "Sé conciso" + "Incluye todos los escenarios de error" → compiten
- "Usa lenguaje técnico" + "Adapta el registro al usuario" → potencialmente compiten

### Pregunta 4: ¿Las instrucciones son demasiado narrow?

Una instrucción narrow solo funciona para el ejemplo que la inspiró. Señales:
- Menciona nombres de archivos específicos
- Depende de un formato de input específico sin manejar variantes
- Tiene más de 3 condiciones if/else en prosa

**Output:** Por cada instrucción problemática, propón reemplazo + razón. No acumules fixes — prioriza los 2-3 cambios de mayor impacto.

---

## Comparación A/B de Versiones de Skill (sin ejecución)

Cuando el usuario pida comparar dos versiones de un SKILL.md o cuando hayas generado una versión nueva y quieras evaluarla contra la anterior:

### Identificación de versiones

- Si el usuario provee dos versiones explícitas → Alpha = primera, Beta = segunda
- Si el usuario provee una y acabas de generar otra → Alpha = versión del usuario, Beta = versión generada
- Si el usuario solo tiene una versión → no ejecutes A/B, ejecuta auditoría simple

### Protocolo de comparación ciega

**Paso 1: Anonimiza internamente.**
Llama a las versiones "Versión Alpha" y "Versión Beta" sin revelar cuál es la nueva y cuál la anterior hasta terminar la evaluación.

**Paso 2: Evalúa con rúbrica de contenido (1-5 cada criterio):**

| Criterio | Alpha | Beta |
|----------|-------|------|
| Claridad de instrucciones | ? | ? |
| Completitud de cobertura | ? | ? |
| Precisión del formato de output | ? | ? |
| Ejecutabilidad (sin ambigüedad) | ? | ? |

**Paso 3: Evalúa con rúbrica de estructura (1-5 cada criterio):**

| Criterio | Alpha | Beta |
|----------|-------|------|
| Organización lógica de secciones | ? | ? |
| Progressive disclosure | ? | ? |
| Navegabilidad | ? | ? |

**Paso 4: Calcula score total (promedio ponderado, escala 1-10).**

**Paso 5: Declara ganadora y explica.**
- Qué instrucciones concretas de la ganadora son superiores (cita textual)
- Qué debilidades concretas tiene la perdedora (cita textual)
- 1-2 cambios de la ganadora que deberían portarse a la perdedora

**Regla:** El empate es válido solo si los scores difieren en <0.5. Si hay empate real, declara qué contextos favorecen a cada versión.

---

## Optimización de Descripción (sin ejecución)

Cuando el usuario quiera mejorar el triggering de su skill, aplica este protocolo de diseño (no requiere ejecutar `run_loop.py`):

### Paso 0: Coherencia description↔cuerpo (S11)

Antes de las 10 queries de prueba:

1. Lee la description del frontmatter
2. Lee la primera sección del cuerpo (típicamente la descripción ampliada)
3. Verifica:
   - ¿La description menciona algo que el cuerpo no implementa? → Contradicción
   - ¿El cuerpo hace algo que la description no menciona? → Undertriggering garantizado
   - ¿La description usa términos que el usuario no usaría? → Undertriggering probable
4. Reporta incoherencias antes de proponer nueva description

**Señal crítica:** Si la description dice "activa cuando X" pero el cuerpo no implementa X,
corregir el cuerpo ANTES de optimizar la description.

### Paso 1: Genera 10 queries de prueba mental

Crea 5 queries que DEBERÍAN disparar la skill y 5 que NO deberían:

**Deben disparar (should-trigger):**
- Queries sustantivas, multi-paso, donde el agente se beneficiaría de instrucciones
- Variedad de phrasings: formal, casual, con typos, sin nombrar la skill explícitamente
- Al menos 1 caso edge donde la skill compite con otra

**NO deben disparar (should-not-trigger):**
- Queries simples que el agente resuelve sin instrucciones especiales
- Near-misses: queries que comparten keywords pero necesitan algo diferente
- Casos donde otra skill es más apropiada

**Criterio de calidad:** Una query debería tener backstory específica (nombre de archivo, contexto, empresa, columnas de datos) — no queries abstractas como "crea una skill".

### Paso 2: Evalúa la descripción actual contra cada query

Para cada query, razona: ¿la descripción actual lleva al agente a leer este SKILL.md?

Señales de descripción débil:
- No menciona contextos de uso concretos → agente undertrigger
- Solo menciona lo que hace la skill, no cuándo usarlo → agente undertrigger
- Usa términos muy específicos que el usuario podría no usar → agente undertrigger
- Describe casos que otra skill también cubre → agente overtrigger

### Paso 3: Reescribe con estas reglas

1. Menciona el qué Y el cuándo (contextos específicos de activación)
2. Incluye sinónimos de los términos principales
3. Añade al menos 1 caso edge donde esta skill gana sobre alternativas obvias
4. Límite: 1024 caracteres, sin angle brackets
5. Tono: "pushy" — si hay duda, la skill debería disparar

### Paso 4: Presenta antes/después con justificación

Muestra las 10 queries y predice si la nueva descripción las maneja mejor. Si alguna query sigue siendo ambigua, documenta el tradeoff.

---

## Metacrítica de Expectations

Cuando todas las expectations de un eval pasan pero el output sigue siendo insatisfactorio, ejecuta la metacrítica:

### Test de discriminación por expectation

Para cada expectation, pregunta:
"¿Un output incorrecto también pasaría este criterio?"

**Señales de expectation débil:**
- Chequea existencia pero no contenido → "El SKILL.md existe" pasa aunque esté vacío
- Usa términos vagos → "La rúbrica está completa" no define qué es completa
- No tiene un falso negativo natural → si no puedes imaginar cuándo fallaría, es trivial

**Señales de expectation fuerte:**
- Tiene un threshold cuantificable → "≥4 filas en tabla de errores"
- Cita estructura específica → "Cada fila tiene columnas Error/Diagnóstico/Acción"
- Diferencia comportamiento con/sin la instrucción

### Output de la metacrítica

Para cada expectation débil, propón:
1. La expectation actual (débil)
2. La razón por qué es débil (qué output incorrecto la pasaría)
3. La expectation mejorada (con threshold o estructura específica)

---

## Análisis Post-Modificación (después de ≥2 iteraciones)

Si el usuario dice "sigue sin funcionar" o "mejoró pero no del todo" después de ≥2 iteraciones, ejecuta este protocolo antes de proponer más cambios:

```
## Análisis post-modificación

### 1. Compara versiones
Lee la versión anterior y la actual. Identifica exactamente qué instrucciones cambiaron.

### 2. Hipotetiza el mecanismo
¿Por qué ese cambio debería mejorar el comportamiento?
Si no puedes articular el mecanismo, el cambio fue cosmético.

### 3. Busca instrucciones que compiten
¿Hay dos instrucciones que pidan comportamientos contradictorios?
(e.g., "sé conciso" + "incluye todos los escenarios")

### 4. Propón un cambio quirúrgico
Máximo 1-2 líneas modificadas por iteración.
Cambios grandes hacen imposible atribuir mejoras o regresiones.

### Formato de salida
**Cambio propuesto:** [texto exacto a reemplazar → texto nuevo]
**Mecanismo esperado:** [por qué debería funcionar]
**Criterio que resuelve:** [criterio #N de la rúbrica]
**Riesgo de regresión:** [qué otro criterio podría verse afectado]
```

---

*Para protocolos S1, S3, S4, S6, S7, S8, S9, S10, S12, consulta references/protocols-advanced.md*
