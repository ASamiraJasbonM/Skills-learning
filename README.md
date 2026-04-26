# Skills Learning

Colección de skills instalables para agentes IA (OpenCode, Claude, etc.)

## Skills Incluidos

### 1. Code Analysis
- **Descripción:** Analiza código fuente para identificar bugs, vulnerabilidades de seguridad, code smells y oportunidades de optimización.
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill code-analysis`

### 2. Django-Shield 2026
- **Descripción:** Auditor de ciberseguridad senior para Django 5.x/6.x. Identifica vulnerabilidades lógicas y de configuración, analiza superficie de ataque (Taint Flow).
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill django-shield`

### 3. Prompt v22 (Meta-Skill Architect)
- **Descripción:** Sistema de ingeniería de prompts para diseñar, auditar y mejorar skills SKILL.md para agentes IA. Diseña skills nuevas, audita existentes,改进 iterativamente, adapta a plataformas específicas.
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill prompt_v22`
- **Versión:** 3.0.0
- **Runtimes:** Claude, Gemini, GPT, Opencode, Kilocode

---

## Cómo Instalar un Skill

### Opción 1: Usando npx skills (recomendado)

```bash
# Instalar un skill específico
npx skills add ASamiraJasbonM/Skills-learning --skill <nombre-skill>

# Ejemplo: code-analysis
npx skills add ASamiraJasbonM/Skills-learning --skill code-analysis

# Ejemplo: django-shield
npx skills add ASamiraJasbonM/Skills-learning --skill django-shield

# Ejemplo: prompt_v22
npx skills add ASamiraJasbonM/Skills-learning --skill prompt_v22

# Instalar todos los skills
npx skills add ASamiraJasbonM/Skills-learning --skill '*'
```

### Opción 2: Manual

```bash
# Clonar el repositorio
git clone https://github.com/ASamiraJasbonM/Skills-learning.git

# Copiar el skill deseado a tu directorio de skills
cp -r Skills-learning/<skill-name> ~/.config/opencode/skills/
```

---

## Estructura del Repositorio

```
Skills-learning/
├── .gitignore                     # Ignora skill-creator/
├── code-analysis/
│   └── SKILL.md                   # Code analysis skill
├── django-shield/
│   └── SKILL.md                   # Django security audit skill
├── prompt_v22/
│   ├── system.md                   # Identidad v3.0.0
│   ├── task.md                    # Instrucciones v3.0.0
│   ├── scripts/
│   │   ├── validate.sh            # Validador seguridad
│   │   ├── validate_structure.py  # Validador estructura v2
│   │   ├── test_runner.py        # Suite evaluación v2
│   │   └── mcp_server.py       # Servidor MCP
│   ├── references/
│   │   ├── schemas.md           # Esquemas JSON
│   │   ├── writing-patterns.md # Patrones escritura
│   │   └── examples.md        # Ejemplos canónicos
│   └── data/
│       └── examples.json        # 8 evals, 28 expectations
├── mejoras_v23_scripts_y_modificacion.md
├── mejoras_v24_senior_engineer.md
├── prompt_v22-analisis.md
├── prompt_v22-cumplimiento.md
├── prompt_v22_system.md
├── prompt_v22_task.md
├── sugerencias_prompt_v22.md
└── README.md
```

---

## Acerca de prompt_v22

prompt_v22 (Meta-Skill Architect v3.0.0) es un **arquitecto autónomo de skills** que:

- ✅ Diseña skills nuevas desde cero
- ✅ Audita skills existentes
- ✅ Mejora skills iterativamente
- ✅ Adapta a 5 plataformas (Claude, Gemini, GPT, Opencode, Kilocode)
- ✅ Protocolo de Generalización (diagnóstico de problemas)
- ✅ Análisis de Ejecutabilidad (instrucciones autonome)
- ✅ Comparación A/B inline (sin subagentes)
- ✅ Trigger Optimization (por razonamiento)
- ✅ Metacrítica de Expectations

** scripts:**
- `validate.sh` — Validador seguridad (Capa 2)
- `validate_structure.py` — Validador estructura YAML (8+ checks)
- `test_runner.py` — Suite evaluación con grading.json
- `mcp_server.py` — Servidor MCP para integración

**Comparación con skill-creator:**
| Aspecto | skill-creator | prompt_v22 v3.0.0 |
|---------|--------------|-------------------|
| Requiere Claude Code | ✅ | ❌ |
| Patrones escritura | Implícitos | **Explícitos** |
| Comparación A/B | Subagentes | **Inline** |
| Multiplataforma | ❌ | **5 runtimes** |

---

## Crear un Nuevo Skill

```bash
# Inicializar un nuevo skill
npx skills init my-new-skill

# Editar el archivo SKILL.md generado
# Push a GitHub y usar:
npx skills add TU_USUARIO/my-new-skill
```

---

## Requisitos

- Node.js 18+
- Agente IA compatible (OpenCode, Claude Code, etc.)

---

## License

MIT