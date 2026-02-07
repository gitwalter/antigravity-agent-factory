# Testing Strategy

The test suite uses **pytest** and consists of **1165 tests** organized into five categories:

| Category | Tests | Purpose |
|----------|-------|---------|
| Unit Tests | ~723 | Test individual components |
| Integration Tests | ~155 | Test component interactions |
| Validation Tests | ~211 | Validate JSON schemas |
| Guardian Tests | ~31 | Test integrity protection |
| Memory Tests | ~45 | Test memory system |

## Running Tests

Run the full suite with:
```bash
pytest
```
