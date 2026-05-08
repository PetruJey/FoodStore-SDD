## Context

El archivo `AGENTS.md` es la fuente de verdad para el comportamiento del agente IA en el proyecto Food Store. Actualmente contiene 12 secciones que cubren stack, arquitectura, convenciones, workflow SDD y reglas de negocio. Sin embargo, no especifica **cómo** el agente debe organizar su trabajo internamente: no hay un patrón de delegación, no hay separación de roles (arquitecto vs revisor vs implementador), y no hay optimización de tokens.

BigPickle (el agente actual) tiende a centralizar todo en un solo contexto: analiza, diseña, implementa y revisa sin delegar. Esto funciona para cambios pequeños pero escala mal. Cuando el orchestrador migre a GitHub Copilot, el problema se agrava porque Copilot tiene un contexto diferente.

## Goals / Non-Goals

**Goals:**
- Establecer el principio permanente de que **toda tarea importante delega a subagentes internos**
- Definir 4 roles de subagentes con propósitos y triggers de uso claros
- Separar explícitamente el **patrón permanente** (workflow, optimización, integración OPSX) de la **implementación temporal** (BigPickle, Nemotron, DeepSeek, Hy3)
- Agregar la sección 13 al AGENTS.md sin modificar ninguna línea existente
- Marcar la extensión con `<!-- jr-stack:... -->` para identificarla como manual en caso de regeneración

**Non-Goals:**
- NO cambiar el workflow OPSX existente (`/opsx:explore → propose → apply → archive`)
- NO modificar backend, frontend, specs del sistema, ni configuración del proyecto
- NO cambiar el footer de regeneración automática
- NO implementar la lógica de los subagentes — solo documentar el patrón

## Decisions

| Decisión | Opción A | Opción B | Elegida | Razón |
|----------|----------|----------|---------|-------|
| Ubicación de la nueva sección | Después de Workflow SDD (sección 9) | **Antes del footer (final del archivo)** | B | No requiere renumerar secciones existentes. El footer de regeneración queda intacto |
| Separación permanente/temporal | Secciones separadas | **Subsecciones dentro de una misma sección** | Subsecciones | Más cohesivo. El lector ve el sistema completo en un solo lugar |
| Mapeo de subagentes a tools | Solo nombres conceptuales | **Mapeo explícito a task/delegate/skill** | Mapeo explícito | El agente actual necesita saber QUÉ herramienta usar para cada rol |
| Formato de marcador | Comentario HTML simple | `<!-- jr-stack:... -->` | `<!-- jr-stack:sdd-agent-delegation -->` | Sigue el mismo patrón que las secciones del system prompt del agente |

## Implementation Plan

La implementación es puramente editorial — modificar un solo archivo (AGENTS.md) con dos cambios quirúrgicos:

1. **Índice**: Agregar línea `13. [SDD Multi-Agent Delegation System](#sdd-multi-agent-delegation-system)` después de la línea 16
2. **Sección 13**: Insertar el contenido completo (aproximadamente 100 líneas) entre el Glosario (línea 504) y el footer (línea 507)

El contenido de la sección 13 se divide en 5 subsecciones:
- **13.1 Principio Fundamental** (permanente)
- **13.2 Workflow de Delegación** (permanente)
- **13.3 Subagentes Actuales** (temporal — reemplazar al migrar a Copilot)
- **13.4 Reglas de Optimización de Tokens** (permanente)
- **13.5 Integración con OPSX** (permanente)

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|-----------|
| El AGENTS.md se regenera desde `docs/` y pierde la extensión manual | La sección está marcada con `<!-- jr-stack:... -->` y el workflow de implementación debe respetar ese marcador al regenerar |
| Los subagentes específicos (Nemotron, DeepSeek, Hy3) pueden no existir como tools en el futuro | Sección 13.3 marcada como TEMPORAL. Al migrar a Copilot solo se reemplaza esa subsección |
| El workflow de 7 pasos puede sentirse pesado para cambios triviales | El principio dice "para TODA tarea IMPORTANTE". Cambios triviales (typo, rename) no requieren el workflow completo |
