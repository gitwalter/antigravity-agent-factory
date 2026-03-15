import json
import os
import sys
import argparse


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
    return root_dir, os.path.join(
        root_dir, ".agent", "config", "stack-configurations.json"
    )


def set_active_stack():
    parser = argparse.ArgumentParser(
        description="Set the active SDLC stack for the factory environment."
    )
    parser.add_argument(
        "--stack",
        required=True,
        help="The key of the stack from stack-configurations.json",
    )
    args = parser.parse_args()

    target_stack = args.stack

    root_dir, config_path = get_config_path()

    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    if target_stack not in config.get("stacks", {}):
        print(
            f"Error: Target stack '{target_stack}' is not defined in stack-configurations.json"
        )
        print("Available stacks:")
        for k in config.get("stacks", {}).keys():
            print(f"  - {k}")
        sys.exit(1)

    # Write to local environment memory file
    tracker_path = os.path.join(root_dir, ".agent", "config", ".active-stack")

    with open(tracker_path, "w", encoding="utf-8") as f:
        f.write(target_stack)

    print(f"Success! The active factory SDLC stack has been set to: {target_stack}")
    print(
        f"Memory Entity for Orchestrator Context: {config['stacks'][target_stack]['memory_entity']}"
    )


if __name__ == "__main__":
    set_active_stack()
