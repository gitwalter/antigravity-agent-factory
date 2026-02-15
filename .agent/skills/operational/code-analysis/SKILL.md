---
description: Static code analysis with AST parsing, complexity metrics, dependency
  graphs, and quality scoring
name: code-analysis
type: skill
---
# Code Analysis

Static code analysis with AST parsing, complexity metrics, dependency graphs, and quality scoring

Performs static analysis using AST parsing, computes complexity metrics (cyclomatic, maintainability), maps dependencies, and produces quality scores.

## Process

1. **AST Parsing** – Parse source into AST and extract structure. See REFERENCE.md § AST Parsing.
2. **Complexity Calculation** – Compute cyclomatic complexity and maintainability index with radon. See REFERENCE.md § Complexity Calculation.
3. **Dependency Mapping** – Extract import statements from AST. See REFERENCE.md § Dependency Mapping.
4. **Quality Scoring** – Compute normalized quality score 0.0–1.0. See REFERENCE.md § Quality Scoring.
5. **Report Generation** – Generate full analysis report. See REFERENCE.md § Report Generation.

**CLI:** Run `python scripts/analyze.py --path <file|dir>` for formatted report or `python scripts/report.py --path <dir> --output report.json` for JSON output.

## Best Practices

- Run analysis in CI with thresholds
- Focus on functions with CC > 10
- Track maintainability index over time
- Use dependency maps for impact analysis

## References

- [Radon Documentation](https://radon.readthedocs.io/)
- [Pylint](https://pylint.org/)
- [Python AST](https://docs.python.org/3/library/ast.html)

## Bundled Resources

- **REFERENCE.md** – Code examples (AST parsing, complexity calculation, dependency mapping, quality scoring, report generation)
- **scripts/analyze.py** – Analyze single file or directory, print formatted report (`--path`)
- **scripts/report.py** – Generate JSON report (`--path`, `--output`)

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
