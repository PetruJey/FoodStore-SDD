## Why

El AGENTS.md del proyecto describe el stack, la arquitectura y el workflow SDD, pero no establece **cómo** el agente IA debe organizar su propio trabajo internamente. Hoy BigPickle tiende a manejar todas las responsabilidades (analizar, diseñar, implementar, revisar) en un solo contexto, lo que genera contaminación de tokens, menor calidad de revisión y falta de separación de concerns.

Al migrar eventualmente a GitHub Copilot como orchestrator, el proyecto necesita un **patrón de delegación multi-agente** permanente que garantice que cualquier IA (hoy BigPickle, mañana Copilot) delegue tareas especializadas a subagentes internos.

Este cambio establece ese patrón como parte fundamental del AGENTS.md.

## What Changes

- **Nueva sección 13 en AGENTS.md**: "SDD Multi-Agent Delegation System" insertada entre el Glosario y el footer
- **+1 entrada en el índice** del AGENTS.md para la nueva sección
- Conclusión: 4 subagentes internos (Orchestrator, Architect, Reviewer, Frontend/UI) con roles, triggers y mapeo a herramientas
- Separación explícita entre **patrón permanente** (workflow de delegación, optimización de tokens, integración OPSX) e **implementación temporal** (BigPickle, Nemotron, DeepSeek, Hy3 como subagentes actuales)
- Footer de regeneración automática se preserva intacto; sección nueva marcada con comentario HTML como extensión manual

## Capabilities

### New Capabilities

*(Ninguna — este cambio no introduce nuevas capacidades del sistema. Es una extensión al AGENTS.md que define el comportamiento interno del agente IA. No requiere archivos de spec nuevos.)*

### Modified Capabilities

*(Ninguna — no hay cambios en requerimientos del sistema existentes.)*

## Impact

- **Archivo modificado**: `AGENTS.md` (índice + nueva sección 13 antes del footer)
- **Ningún otro archivo del proyecto se modifica**: no se tocan backend, frontend, specs, ni configuración
- **Comportamiento del agente**: BigPickle debe seguir el workflow de delegación obligatorio para toda tarea importante
- **Migración futura**: Cuando el orchestrator cambie a GitHub Copilot, solo se reemplaza la subsección 13.3 (Subagentes Actuales); el patrón permanente (13.1, 13.2, 13.4, 13.5) sigue vigente
