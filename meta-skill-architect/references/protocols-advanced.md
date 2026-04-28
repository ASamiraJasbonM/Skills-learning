# Protocolos Avanzados — Meta-Skill Architect v5.0.0

Este archivo contiene los protocolos S1, S3, S4, S6, S7, S8, S9, S10, S12.
Cárgalo bajo demanda cuando el usuario necesite funcionalidad específica.

---

## S1: Protocolo de Enriquecimiento Estructural

Ejecuta DESPUÉS del Paso 4 (Artefacto), si la skill lo requiere:

### 1. Diagnóstico de necesidades

Para cada recurso, evalúa:

| Señal en el SKILL.md | Recurso a generar |
|----------------------|------------------|
| Menciona una API, esquema o estándar externo | references/[nombre].md |
| Contiene pasos determinísticos repetibles | scripts/[nombre].py o .sh |
| Produce un output con estructura fija | assets/template.[ext] |
| SKILL.md supera 400 líneas | Refactorizar → referencias externas |

### 2. Generación por recurso

**references/[nombre].md:**
- Mueve toda documentación estática (APIs, esquemas, guías) fuera del SKILL.md
- El SKILL.md queda con punteros: "Para detalles del API, consulta references/api-docs.md"
- Cada archivo references/: < 10.000 palabras, kebab-case, con tabla de contenidos

**scripts/[nombre].py:**
- Genera cuando hay ≥3 pasos secuenciales determinísticos (transformar, validar, formatear)
- Incluye: docstring, argparse, manejo de errores, exit codes explícitos
- El SKILL.md incluye: `Ejecutar: python scripts/nombre.py --input X --output Y`

**assets/template.[ext]:**
- Genera cuando el output tiene estructura fija (JSON, Markdown, YAML)
- Usa placeholders `{{ campo }}` para valores dinámicos
- El SKILL.md incluye: "Cargar assets/template.json y sustituir placeholders"

### 3. Árbol de salida (SIEMPRE visible)

ANTES de generar archivos, presenta al usuario:
"Voy a generar/actualizar estos archivos:"
```
nombre-skill/
├── SKILL.md
├── references/
│   └── [generados]
├── scripts/
│   └── [generados]
└── assets/
    └── [generados]
```
"¿Confirmas?"

Tras la confirmación, genera los archivos.

**Criterio de terminación:** Cuando todos los recursos identificados en el diagnóstico tienen un archivo generado o una decisión explícita de no generarlo.

---

## S3: Catálogo de Scripts por Dominio

Al generar o auditar una skill, evalúa si alguno de estos scripts aplica:

| Dominio | Script típico | Propósito |
|---------|--------------|-----------|
| Validación de datos | validate_input.py | Verifica formato, tipos, rangos antes de procesar |
| Procesamiento de texto | transform.py | Normaliza, limpia, reformatea texto |
| Integración de API | call_api.py | Wrapper con retry, timeout, manejo de errores HTTP |
| Generación de reportes | generate_report.py | Produce output desde plantilla + datos |
| Testing de la skill | test_skill.py | Ejecuta casos de prueba contra el SKILL.md |
| Instalación de dependencias | setup.sh | Instala requirements, verifica entorno |
| Validación de estructura | validate_structure.py | (ya existe en tu skill) |

Para cada script identificado:
1. Genera el esqueleto con docstring, argparse, exit codes
2. Referencialo desde SKILL.md con el comando exacto de ejecución
3. Documenta el contrato (input esperado, output, exit codes)

---

## S4: Protocolo de Generación de Plantillas

Cuando el ## Formato de Salida del SKILL.md describe una estructura fija:

1. Identifica el formato: JSON, YAML, Markdown, CSV, HTML
2. Extrae los campos del formato de salida
3. Genera assets/template.[ext] con placeholders `{{ campo }}`
4. Actualiza el SKILL.md para referenciar la plantilla:
   "Cargar assets/template.json, sustituir {{ campo }} con valor real"

Ejemplo: Si el formato es:
```
Urgencia: [P1/P2/P3/P4]
Sistema: [sistema]
Resumen: [texto]
```

Genera `assets/output-template.md`:
```
Urgencia: {{ urgencia }}
Sistema: {{ sistema }}
Resumen: {{ resumen }}
```

---

## S6: Modo Autoevaluación

Cuando el usuario diga "audítate a ti mismo", "evalúa tu propio SKILL.md",
o "¿cumples tus propios estándares?":

1. Carga @SKILL.md (este archivo)
2. Ejecuta el Paso 5 (Validación) completo sobre él, con evidencia textual
3. Aplica el Análisis de Ejecutabilidad a cada instrucción de las Instrucciones Operativas
4. Produce un reporte con:
   - Criterios que pasan (con cita textual como evidencia)
   - Criterios que fallan (con propuesta de corrección)
   - Score: N/5 criterios formales
5. Si el score < 5/5: propón la corrección y pregunta al usuario si la aplica

**Criterio de terminación:** El reporte está completo cuando cubre los 5 criterios
formales con evidencia textual, no con declaraciones generales.

---

## S7: Ciclo de Automejoramiento

Cuando la autoevaluación detecta un criterio que falla:

1. **Diagnostica:** ¿Es instrucción ambigua, competing instructions, o modelo mental roto?
2. **Propón cambio quirúrgico:**
   - Texto exacto a reemplazar (cita del SKILL.md actual)
   - Texto de reemplazo propuesto
   - Mecanismo esperado: por qué este cambio resuelve el fallo
   - Criterio que resuelve: criterio #N de la rúbrica
   - Riesgo de regresión: qué otro criterio podría verse afectado
3. **Solicita aprobación:** "¿Aplico este cambio al SKILL.md? (sí/no)"
4. **Si aprobado:** genera el SKILL.md actualizado con versión incrementada (x.y → x.y+1)
   y añade fila al ## Historial de cambios

**Límite:** Máximo 2 cambios por ciclo de automejoramiento.
Más cambios hacen imposible atribuir mejoras o regresiones.

---

## S8: Protocolo de Actualización de Estándar

Cuando el usuario diga "el estándar cambió", "ahora el campo X es requerido",
o proporcione documentación nueva del formato SKILL.md:

1. Identifica qué cambió: campo nuevo, campo deprecado, nueva regla de validación
2. Evalúa impacto en:
   - Frontmatter de las plantillas (template-full.md, template-minimal.md)
   - Checks en validate_structure.py
   - Ejemplos en examples.md y data/examples.json
3. Produce diff de los cambios propuestos para cada archivo afectado
4. Solicita aprobación antes de generar los archivos actualizados
5. Registra el cambio en data/knowledge-log.md bajo "Actualizaciones de Estándar"

**Señales de obsolescencia a monitorear:**
- El usuario reporta que validate_structure.py rechaza skills válidas → check puede estar desactualizado
- El usuario reporta que openskills install rechaza skills generadas por la skill → frontmatter obsoleto
- El usuario menciona un campo nuevo en la documentación oficial

---

## S9: Modo Migración de Skill

Cuando el usuario trae un archivo que NO es un SKILL.md estándar:

1. Lee el archivo proporcionado
2. Identifica el formato origen:
   - Sin frontmatter YAML → skill informal / prompt sin estructura
   - Frontmatter con campos no estándar → skill de otra plataforma
   - JSON → posible Action de GPT o configuración de Gemini
3. Extrae: intención, pasos, restricciones, errores, criterios de éxito
4. Mapea al estándar SKILL.md:
   - Intención → description en frontmatter
   - Pasos → ## Instrucciones Operativas / ## Tarea
   - Restricciones → MoSCoW en ## Restricciones
   - Errores detectables → ## Manejo de Errores
   - Criterios de éxito → ## Rúbrica
5. Genera SKILL.md estándar
6. Ejecuta Paso 5 (Validación) sobre el resultado
7. Reporta qué información faltaba en el original y qué supuestos aplicaste

---

## S10: Protocolo de Generación de Evals

Cuando el usuario diga "genera evals para esta skill" o después de crear una skill nueva:

1. Lee la ## Rúbrica: cada criterio de éxito se convierte en una expectation
2. Lee el ## Manejo de Errores: cada escenario se convierte en un eval de categoría "robustez"
3. Lee los ## Riesgos Identificados: cada riesgo se convierte en un eval de categoría "seguridad"
4. Genera entre 4 y 8 evals con este formato:

```json
{
  "id": N,
  "category": "calidad|seguridad|robustez|ambiguedad",
  "prompt": "[prompt que debería disparar el comportamiento]",
  "expected_output": "[descripción del output esperado]",
  "expectations": [
    "[expectation cuantificable 1]",
    "[expectation cuantificable 2]"
  ]
}
```

5. Aplica la Metacrítica de Expectations a cada expectation generada antes de mostrarlas.
   Toda expectation débil se fortalece antes de incluirla.

**Criterio de calidad para las expectations generadas:**
- Cada una tiene threshold cuantificable o estructura específica citada
- Ninguna pasa si el output está vacío
- Al menos 1 eval de seguridad si la skill procesa inputs del usuario

---

## S12: Modo Suite de Skills

Cuando el usuario quiera crear múltiples skills relacionadas:

1. Identifica las skills candidatas:
   - ¿Hay un flujo principal que orquesta subskills? → skill orquestadora + subskills
   - ¿Hay comportamientos mutuamente excluyentes? → skills separadas con descriptions distintas
   - ¿Hay conocimiento compartido? → references/ compartido entre skills

2. Propón arquitectura:
   ```
   mi-suite/
   ├── orchestrator/
   │   └── SKILL.md (decide cuál subskill usar)
   ├── subskill-a/
   │   └── SKILL.md
   ├── subskill-b/
   │   └── SKILL.md
   └── shared/
       └── references/
           └── common-docs.md
   ```

3. Genera cada skill en orden: primero las subskills, luego la orquestadora

4. Verifica que las descriptions no se solapen entre skills de la suite
   (aplica Trigger Optimization a cada una por separado)

---

## Patrones de Escritura

Al escribir o revisar cualquier SKILL.md, consulta `references/writing-patterns.md` para los patrones de escritura. No los cargues automáticamente — solo cuando estés generando instrucciones y quieras verificar que son ejecutables.

---

## Ejemplos Canónicos

Consulta `references/examples.md` cuando necesites:
- Ver un SKILL.md completo generado correctamente (Ejemplo 1: ticket triage)
- Ver el protocolo de clarificación en acción (Ejemplo 2: solicitud ambigua)
- Ver flujo de auditoría de skill existente (Ejemplo 3: auditoría)

No los cargues automáticamente — solo cuando el usuario pida un ejemplo o cuando detectes confusión sobre la estructura.

---

*Para el ciclo core de 5 pasos y punto de entrada, consulta task.md*
