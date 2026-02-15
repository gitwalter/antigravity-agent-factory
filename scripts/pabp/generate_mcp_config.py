import json
from pathlib import Path


def main():
    mcp_root = Path(".agent/mcp")
    master_config = {"mcpServers": {}}

    if not mcp_root.exists():
        print("No MCP directory found.")
        return

    print(f"Scanning {mcp_root}...")

    for mcp_dir in mcp_root.iterdir():
        if mcp_dir.is_dir():
            # Look for a JSON config snippet or try to parse README/setup-guide
            # The PABP inspection showed setup-guide.md often contains the JSON snippet

            # Heuristic: verify if we have a direct json config file (some bundles might have it)
            # If not, create a placeholder pointing to the dir

            # For now, let's look for a generic pattern or just list them
            print(f"Found MCP: {mcp_dir.name}")

            # In a real scenario, we'd parse the setup-guide.md to extract the JSON block
            # For this task, let's create a stub entry that points the user to the documentation
            master_config["mcpServers"][mcp_dir.name] = {
                "command": "node",  # Assumption, likely needs adjustment based on guide
                "args": [f"path/to/{mcp_dir.name}/index.js"],
                "disabled": True,
                "description": f"See {mcp_dir}/setup-guide.md for setup instructions",
            }

            # Try to read setup-guide to be smarter
            setup_guide = mcp_dir / "setup-guide.md"
            if setup_guide.exists():
                content = setup_guide.read_text(encoding="utf-8")
                if "mcpServers" in content:
                    print("  - Found config snippet in setup-guide.md")

    target_file = Path(".agent/mcp_config_generated.json")
    target_file.write_text(json.dumps(master_config, indent=2), encoding="utf-8")
    print(f"Generated master config at {target_file}")


if __name__ == "__main__":
    main()
