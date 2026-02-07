# Test Fixtures

This directory contains fixture files used by the test suite.

## Files

| File | Purpose |
|------|---------|
| `sample_config.yaml` | Valid YAML configuration for testing config loading |
| `sample_config.json` | Valid JSON configuration for testing config loading |
| `minimal_blueprint.json` | Minimal valid blueprint for testing blueprint schema |
| `empty_config.json` | Empty JSON object for testing default handling |
| `invalid_config.json` | Invalid JSON for testing error handling |

## Usage

These fixtures are used by pytest tests in the `tests/` directory. They are loaded
via the fixtures defined in `conftest.py`.

Example:

```python
def test_load_yaml_config(sample_yaml_config):
    config = ProjectConfig.from_yaml_file(str(sample_yaml_config))
    assert config.project_name == "test-yaml-project"
```
