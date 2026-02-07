# Porting Guide: Cursor to Antigravity

This guide helps you transition your existing **Cursor Agent Factory** projects to the **Antigravity Agent Factory** architecture.

## Primary Changes

| Concept | Cursor (Old) | Antigravity (New) |
|---------|--------------|-------------------|
| Config Folder | `.agent/` | `.agent/` |
| Rules File | `.agentrules` | `.agentrules` |
| Default Agent | `cursor-agent` | `antigravity-agent` |
| Branding | Cursor Factory | Antigravity Factory |

## Migration Steps

1. **Rename the Configuration Directory**
   Rename your `.agent/` folder to `.agent/`:
   ```bash
   mv .agent .agent
   ```

2. **Update the Rules File**
   Rename `.agentrules` to `.agentrules`:
   ```bash
   mv .agentrules .agentrules
   ```

3. **Update Internal References**
   Search and replace "Cursor" with "Antigravity" in your agents and skills descriptions. The `.agentrules` markers should also be updated from `factory:cursor` to `factory:antigravity`.

4. **Verify Tool Paths**
   If you have hardcoded paths to `.agent/` in your custom scripts or tools, update them to point to `.agent/`.

## Why Antigravity?

Antigravity focuses on **grounded intelligence**—ensuring that AI agents are not just generating code, but are operating within the ethical and technical boundaries defined by your project's Purpose, Principles, and Axioms.
