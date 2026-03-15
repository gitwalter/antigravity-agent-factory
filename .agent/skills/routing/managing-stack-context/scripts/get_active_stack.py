import json
import os
import sys


def get_config_path():
    root_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
            )
        )
    )
    return os.path.join(root_dir, ".agent", "config", "stack-configurations.json")


def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_active_stack():
    config_path = get_config_path()
    config = load_config(config_path)

    # We write a local '.active-stack' file in the root if overwritten, otherwise use config default
    root_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
            )
        )
    )
    active_tracker = os.path.join(root_dir, ".agent", "config", ".active-stack")

    active_key = config.get("default_stack", "python_fastapi")

    if os.path.exists(active_tracker):
        with open(active_tracker, "r", encoding="utf-8") as f:
            active_key = f.read().strip()

    if active_key not in config.get("stacks", {}):
        print(
            f"Error: Active stack '{active_key}' is not defined in stack-configurations.json"
        )
        sys.exit(1)

    stack_data = config["stacks"][active_key]

    print("=== Active SDLC Stack ===")
    print(f"Key: {active_key}")
    print(f"Name: {stack_data.get('display_name')}")
    print(f"Language: {stack_data.get('primary_language')}")
    print(f"Memory Entity: {stack_data.get('memory_entity')}")
    print("\n[Mapped Workflows]")
    for phase, workflow in stack_data.get("workflows", {}).items():
        print(f"- {phase}: {workflow}")

    print("\n[Execution Commands]")
    for cmd_type, cmd in stack_data.get("commands", {}).items():
        print(f"- {cmd_type}: {cmd}")


if __name__ == "__main__":
    get_active_stack()
