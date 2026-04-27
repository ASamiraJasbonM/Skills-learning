# Skills Learning

Colección de skills instalables para agentes IA (OpenCode, Claude, etc.)

## Skills Incluidos

### 1. Code Analysis
- **Descripción:** Analiza código fuente para identificar bugs, vulnerabilidades de seguridad (CWE/OWASP), code smells y oportunidades de optimización.
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill code-analysis`
- **Versión:** 2.0.0

### 2. Django-Shield
- **Descripción:** Auditor de ciberseguridad senior especializado en Django 5.x/6.x. Análisis de Taint Flow, auditoría de configuración y validación de autorización.
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill django-shield`
- **Versión:** 3.0.0

### 3. FastAPI-Shield
- **Descripción:** Auditor de ciberseguridad para aplicaciones FastAPI. Especializado en validación Pydantic, seguridad en Dependency Injection y OAuth2/JWT.
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill fastapi-shield`
- **Versión:** 1.0.0

### 4. Architecture Diagram Architect
- **Descripción:** Transforma requerimientos técnicos en código ejecutable de Python usando la librería `diagrams` para visualizar arquitecturas.
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill architecture-diagram-architect`
- **Versión:** 1.0.0

### 5. Git Master Architect
- **Descripción:** Experto en Git para analizar cambios, redactar commits descriptivos y gestionar flujos de trabajo con branches y rebases.
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill git-master-architect`
- **Versión:** 1.0.0

### 6. MCP Python Architect
- **Descripción:** Diseña y construye servidores Model Context Protocol (MCP) robustos en Python con validación Pydantic.
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill mcp-python-architect`
- **Versión:** 1.1.0

### 7. Meta-Skill Architect
- **Descripción:** Sistema de ingeniería de prompts para diseñar, auditar y mejorar skills SKILL.md para agentes IA.
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill meta-skill-architect`
- **Versión:** 3.0.0
- **Última actualización:** 2026-04-26 (post-evaluación senior)

---

## Cómo Instalar un Skill

### Opción 1: Usando npx skills (recomendado)

```bash
# Instalar un skill específico
npx skills add ASamiraJasbonM/Skills-learning --skill <nombre-skill>

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
├── code-analysis/          # Code analysis skill
├── django-shield/         # Django security audit
├── fastapi-shield/        # FastAPI security audit
├── architecture-diagram-architect/  # Diagram generation
├── git-master-architect/  # Git expertise
├── mcp-python-architect/ # MCP server builder
├── meta-skill-architect/  # SKILL.md architect
└── README.md
```

---

## Categorías por Dominio

| Dominio | Skills |
|--------|-------|
| **Seguridad** | django-shield, fastapi-shield |
| **Ingeniería de Código** | code-analysis, mcp-python-architect |
| **Arquitectura** | architecture-diagram-architect |
| **DevOps** | git-master-architect |
| **Diseño de Skills** | meta-skill-architect |

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