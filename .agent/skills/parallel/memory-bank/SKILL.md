---
description: Foundational skill for managing the memory context protocol (MCP) knowledge
  graph
name: memory-bank
type: skill
---
# Memory Bank

Manage the system's persistent knowledge graph using the `memory` MCP server.

## When to Use
This skill should be used when building persistent knowledge graphs, managing entities and relationships across agent interactions, and maintaining a searchable repository of facts and observations.

## Prerequisites
- Access to the Memory MCP server instance.
- Understanding of entity-relationship models and knowledge graph concepts.
- Familiarity with the knowledge node structure (entities, relations, observations).

## Process

1. Review the current context and entities.
2. Search, Create, or Update nodes as needed.
3. Maintain referential integrity between the graph and file-based KIs.

### Step 1: Context Grounding
Before any knowledge operation, search for existing entities in the graph.
```python
# Use MCP tool: search_nodes
search_nodes(query="{{topic}}")
```

### Step 2: Entity & Relation Creation
When a new concept or fact is discovered:
```python
# Use MCP tools: create_entities, create_relations
create_entities(entities=[{"name": "{{concept}}", "entityType": "{{type}}", "observations": ["{{fact}}"]}])
create_relations(relations=[{"from": "{{source}}", "to": "{{target}}", "relationType": "{{predicate}}"}])
```

### Step 3: Wisdom Storage
When capturing wisdom from logs (via `wisdom-harvest`):
```python
# Use MCP tool: add_observations
add_observations(observations=[{"entityName": "{{topic}}", "contents": ["{{wisdom_insight}}"]}])
```

## Best Practices
- **Atomic Nodes**: Keep entities focused (e.g., specific technologies or patterns).
- **Active Verbs**: Use active voice for relation types (e.g., "implements", "solves", "extends").
- **Observation History**: Add dates to observations when they represent temporal facts.

## Related
- Skill: `knowledge-generation`
- Skill: `wisdom-harvest`
- Agent: `knowledge-operations-specialist`
