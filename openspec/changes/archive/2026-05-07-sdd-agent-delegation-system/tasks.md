## 1. Index Update

- [x] 1.1 Add `13. [SDD Multi-Agent Delegation System](#sdd-multi-agent-delegation-system)` to the AGENTS.md index after line 16 (`12. Gemas del Proyecto`)

## 2. Section 13 — Content Insertion

- [x] 2.1 Insert section 13 between the Glosario (line 504) and the footer (line 507), preserving the existing `---` separator and footer text

### 2.1 Subsection: 13.1 Principio Fundamental (permanente)

- [x] 2.1.1 Write the opening with `<!-- jr-stack:sdd-agent-delegation -->` marker
- [x] 2.1.2 State the permanent principle: all important tasks MUST delegate to internal subagents

### 2.2 Subsection: 13.2 Workflow de Delegación (permanente)

- [x] 2.2.1 Document the 7-step mandatory delegation workflow as an ASCII diagram
- [x] 2.2.2 Specify that each step is tool-agnostic (task/delegate/skill)

### 2.3 Subsection: 13.3 Subagentes Actuales (temporal)

- [x] 2.3.1 Add ⚠️ notice that this subsection is the current implementation, replaceable when migrating to Copilot
- [x] 2.3.2 Document the 4 subagents (BigPickle, Nemotron, DeepSeek, Hy3) with roles, purposes, and mandatory triggers
- [x] 2.3.3 Map each subagent to real tools (task/delegate/skill)

### 2.4 Subsection: 13.4 Reglas de Optimización de Tokens (permanente)

- [x] 2.4.1 Document token optimization rules (delegation, surgical edits, context reduction)

### 2.5 Subsection: 13.5 Integración con OPSX (permanente)

- [x] 2.5.1 Document how the delegation system integrates within each OPSX phase
- [x] 2.5.2 Clarify that user-facing OPSX commands remain unchanged

## 3. Final Verification

- [x] 3.1 Verify AGENTS.md renders correctly with the new section
- [x] 3.2 Confirm no existing content was modified or removed
- [x] 3.3 Confirm footer and `---` separators are intact
