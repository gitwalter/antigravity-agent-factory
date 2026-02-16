---
description: Answer process and configuration questions for FI (incl. FI-CAX, VIM),
  SD, MM, EWM, LE, CO, WM, AIF, and logistics chain. Supports ABAP development patterns.
  Output EN or DE.
name: guiding-s4-processes
type: skill
---
# S4 Process Guide

Answer process and configuration questions for FI (incl. FI-CAX, VIM), SD, MM, EWM, LE, CO, WM, AIF, and logistics chain. Supports ABAP development patterns. Output EN or DE.

Answers process and configuration questions for **FI (incl. FI-CAX, VIM), SD, MM, EWM, LE, CO, WM, AIF**, and the full logistics chain. Also covers **ABAP development patterns** (enhancements, BAdIs, BAPIs, clean ABAP). Supports **both consultants and developers**. Output in **English or German** (per user/locale preference).

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Query Knowledge Files
Query relevant S/4 knowledge files based on the user's question:
- **FI questions**: Query sap-fi-patterns.json, sap-fi-cax-patterns.json, sap-vim-patterns.json
- **SD questions**: Query sap-sd-patterns.json
- **MM questions**: Query sap-mm-patterns.json
- **EWM questions**: Query sap-ewm-patterns.json
- **LE questions**: Query sap-le-patterns.json
- **CO questions**: Query sap-co-patterns.json
- **WM questions**: Query sap-wm-patterns.json
- **AIF questions**: Query sap-aif-patterns.json
- **ABAP development questions**: Query sap-abap-dev-patterns.json
- **Cross-module questions**: Query sap-logistics-chain.json

### Step 2: Ground with SAP Help (if needed)
If knowledge files don't provide sufficient detail, use SAP Help MCP:
- Call `sap_help_search` with relevant query terms
- Retrieve specific help pages using `sap_help_get` with result IDs
- Verify table/field information against official SAP documentation

### Step 3: Format Response
Return a concise answer with:
- **Process**: 1–2 sentence description
- **Tables/fields**: Bullet list with table names and purposes
- **R/3 vs S/4**: Note differences where applicable (e.g., ACDOCA only in S/4)
- **Citation**: Reference to knowledge file or SAP Help topic

### Step 4: Language Selection
Output in **English** or **German** based on:
- User's explicit language preference
- LOCALE variable if available
- Default to English if not specified

## Behavior

1. **Layer 1**: Query relevant S/4 knowledge files (sap-fi-patterns, sap-sd-patterns, etc.) for process, tables, and key fields.
2. **Layer 2**: If needed, call **SAP Help MCP** (sap_help_search / sap_help_get) for official documentation.
3. Return a **short, cited answer**: process description + tables/fields + optional SAP Help reference. Prefer **EN or DE** per user preference (variable LOCALE or explicit request).

## Output Format

- Process: 1–2 sentences.
- Tables/fields: Bullet list with purpose.
- R/3 vs S/4: Note where applicable (e.g. ACDOCA only in S/4).
- Citation: "See SAP Help: [topic]" or knowledge file name.

## Knowledge Files (required)

- sap-fi-patterns.json, sap-fi-cax-patterns.json, sap-vim-patterns.json
- sap-sd-patterns.json, sap-mm-patterns.json, sap-ewm-patterns.json, sap-le-patterns.json
- sap-logistics-chain.json, common-table-patterns.json
- sap-co-patterns.json, sap-wm-patterns.json, sap-aif-patterns.json, sap-abap-dev-patterns.json

## Best Practices

- Always verify table/field information via SAP Help MCP when uncertain
- Distinguish between R/3/ECC and S/4HANA table availability
- Use knowledge files as primary source, SAP Help as secondary verification
- Provide concise answers (1–2 sentences for process, bullet lists for tables)
- Include citations to knowledge files or SAP Help topics
- Note S/4-specific features (e.g., ACDOCA Universal Journal)
- Understand document flow across modules (SD → LE → FI, MM → FI, etc.)
- Consider integration points between modules when answering questions

## References

- Research briefs: {directories.blueprints}/sap-s4-enterprise/research/s4-research-brief-*.md
- SAP_GROUNDING_DESIGN.md for Layer 1/2 grounding

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
