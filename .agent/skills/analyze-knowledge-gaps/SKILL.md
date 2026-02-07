---
name: analyze-knowledge-gaps
description: Analyze Factory knowledge base to identify missing, shallow, or stale content
type: skill
agents: [knowledge-extender, knowledge-evolution]
knowledge: [manifest.json, agent-taxonomy]
---

# Analyze Knowledge Gaps Skill

Systematically analyze the Factory's knowledge base against the topic taxonomy to identify gaps, shallow coverage, stale content, and cross-reference issues. Produces prioritized recommendations for knowledge extension.

## When to Use

- Before extending knowledge to understand what's missing
- During blueprint development to check topic coverage
- Periodically to assess knowledge base health
- When users ask "what knowledge is missing?"
- After adding new blueprints to identify required knowledge

## Gap Types

| Gap Type | Description | Priority |
|----------|-------------|----------|
| **Missing** | Topic not covered at all | Critical |
| **Shallow** | Covered but below required depth | High |
| **Stale** | References outdated APIs/versions | Medium |
| **Incomplete** | Partially covered, missing subtopics | Medium |
| **Cross-Reference** | Mentioned but no dedicated knowledge | Low |

## Process

### Step 1: Run CLI Gap Analysis

Use the Factory CLI to get a structured gap report:

```bash
python cli/factory_cli.py --analyze-gaps
```

For scoped analysis:

```bash
# Analyze gaps for a specific blueprint
python cli/factory_cli.py --analyze-gaps --gap-scope blueprint --gap-filter python-fastapi

# Analyze gaps for a domain
python cli/factory_cli.py --analyze-gaps --gap-scope domain --gap-filter ai_development

# Analyze a specific topic
python cli/factory_cli.py --analyze-gaps --gap-scope topic --gap-filter constitutional_ai
```

### Step 2: Interpret Results

The analyzer outputs a prioritized list:

```
Gap Analysis Results
====================

CRITICAL (Missing):
  - constitutional_ai (ai_development > safety_alignment)
    Required depth: 3, Current: 0
    Recommendation: Create knowledge/constitutional-ai-patterns.json

HIGH (Shallow):
  - prompt_injection (ai_development > safety_alignment)
    Required depth: 2, Current: 1
    Source: security-patterns.json (1 mention)
    Recommendation: Expand with dedicated section

MEDIUM (Incomplete):
  - function_calling (ai_development > tool_use)
    Required depth: 2, Current: 1
    Missing: error handling, parallel execution
```

### Step 3: Check Blueprint Coverage

For blueprint-specific analysis:

```bash
python cli/factory_cli.py --coverage-report ai-agent-development
```

Output shows:
- Topics covered by the blueprint's knowledge files
- Required topics from taxonomy that are missing
- Coverage percentage
- Specific recommendations

### Step 4: Prioritize Extensions

Based on gap analysis, prioritize by:

1. **Critical gaps** - Block blueprint functionality
2. **High gaps** - Degrade blueprint quality
3. **Blueprint alignment** - Gaps in popular blueprints
4. **User requests** - Topics users have asked about

## Using the Python API

For programmatic access:

```python
from scripts.analysis.knowledge_gap_analyzer import KnowledgeGapAnalyzer, GapPriority
from pathlib import Path

# Initialize analyzer
factory_root = Path(".")
analyzer = KnowledgeGapAnalyzer(
    knowledge_dir=factory_root / "knowledge",
    taxonomy_dir=factory_root / "scripts" / "taxonomy"
)

# Run full analysis
result = analyzer.analyze("agent_taxonomy.json")

# Get gaps by priority
critical_gaps = [g for g in result.gaps if g.priority == GapPriority.CRITICAL]
high_gaps = [g for g in result.gaps if g.priority == GapPriority.HIGH]

# Show what's missing
for gap in critical_gaps:
    print(f"{gap.topic.name}: {gap.gap_type.value}")
    print(f"  Required depth: {gap.coverage.required_depth}")
    print(f"  Target file: knowledge/{gap.topic.name.replace('_', '-')}-patterns.json")
```

## Output Format

When reporting gaps to the user:

```markdown
## Knowledge Gap Analysis

### Summary
- **Total topics analyzed**: 45
- **Adequate coverage**: 32 (71%)
- **Gaps identified**: 13

### Critical Gaps (Missing)

| Topic | Domain | Required Depth | Recommendation |
|-------|--------|----------------|----------------|
| constitutional_ai | ai_development | 3 | Create new knowledge file |
| prompt_caching | ai_development | 2 | Create new knowledge file |

### High Priority Gaps (Shallow)

| Topic | Current Depth | Required | Source File | Action |
|-------|---------------|----------|-------------|--------|
| function_calling | 1 | 2 | mcp-patterns.json | Expand section |

### Recommendations

1. **Immediate**: Create `constitutional-ai-patterns.json` for safety alignment
2. **Short-term**: Expand `mcp-patterns.json` with function calling patterns
3. **Long-term**: Add cross-references between related knowledge files
```

## Integration with extend-knowledge

After gap analysis, trigger the `extend-knowledge` skill:

```
Identified gap: constitutional_ai (priority: CRITICAL)

→ Invoke extend-knowledge skill with topic "constitutional_ai"
→ Use web search to gather current best practices
→ Create knowledge/constitutional-ai-patterns.json
→ Update manifest and documentation
```

## Fallback Procedures

| Scenario | Fallback |
|----------|----------|
| Taxonomy file not found | Use default taxonomy embedded in analyzer |
| Knowledge directory empty | Report and suggest running quickstart |
| No gaps found | Report healthy status, suggest maintenance |
| Python analyzer fails | Fall back to manual file inspection |

## References

- `scripts/analysis/knowledge_gap_analyzer.py` - Core analyzer implementation
- `scripts/taxonomy/agent_taxonomy.json` - Topic definitions and required depths
- `knowledge/manifest.json` - Current knowledge file registry
- `.agent/skills/extend-knowledge/SKILL.md` - Follow-up skill for gap filling
