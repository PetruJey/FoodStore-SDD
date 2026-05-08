# Agent Delegation System

Este cambio no modifica capacidades del sistema Food Store. Es una extensión al
`AGENTS.md` que define el comportamiento interno del agente IA (delegación multi-agente).

## No-OP Requirements

Este spec existe únicamente para satisfacer la dependencia del artifact `tasks`.
No hay requerimientos ADDED, MODIFIED ni REMOVED sobre las capacidades del sistema.

### Requirement: Process-only documentation change
El sistema Food Store SHALL NOT ver cambios en sus capacidades, APIs, modelo de datos,
ni comportamiento como resultado de este cambio.

#### Scenario: No system capabilities affected
- **WHEN** se aplica el cambio `sdd-agent-delegation-system`
- **THEN** las capabilities existentes del sistema Food Store permanecen inalteradas
