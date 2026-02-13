# MCP Server Installation & Configuration Guide

This guide provides setup instructions for specialized MCP servers.

> [!IMPORTANT]
> **Prerequisite: Install `uv`** (required for `uvx` commands):
> ```powershell
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
> ```

## 1. LangChain & LangGraph Documentation (mcpdoc)
Official specialized documentation server using official `llms.txt` grounding.

*   **Repository**: [langchain-ai/mcpdoc](https://github.com/langchain-ai/mcpdoc)
*   **Installation (uvx)**: `uvx --from mcpdoc mcpdoc`
*   **Cursor Configuration**:
    ```json
    "langgraph-docs-mcp": {
      "command": "uvx",
      "args": [
        "--from", "mcpdoc", "mcpdoc",
        "--urls", "LangGraph:https://langchain-ai.github.io/langgraph/llms.txt LangChain:https://python.langchain.com/llms.txt",
        "--transport", "stdio"
      ]
    }
    ```

---

## 2. LangSmith MCP
Official server for tracing, prompt management, and dataset access.

*   **Repository**: [langchain-ai/langsmith-mcp-server](https://github.com/langchain-ai/langsmith-mcp-server)
*   **Cloud (Hosted)**: `https://langsmith-mcp-server.onrender.com/mcp`
*   **Local (uvx)**: `uvx langsmith-mcp-server`
*   **Local Windows (Anaconda)**: `C:\App\Anaconda\envs\langgraph\Scripts\langsmith-mcp-server.exe`

---

## 3. SAP Documentation MCP
Broad documentation coverage (CAP, RAP, CPI, ABAP, UI5) via the Marian Zeis implementation.

*   **Repository**: [marianfoo/mcp-sap-docs](https://github.com/marianfoo/mcp-sap-docs)
*   **Cloud (Recommended)**: `https://mcp-sap-docs.marianzeis.de/mcp`
*   **Cursor Configuration (CRITICAL)**:
    1.  Open Cursor Settings -> MCP servers.
    2.  Click **Add New MCP Server**.
    3.  Set Name: `mcp-sap-docs`.
    4.  Set Type: **SSE** (Important: Do not use command).
    5.  Set URL: `https://mcp-sap-docs.marianzeis.de/mcp`

---

## 4. Specialized Excel & Word Tools
These are dedicated tools distinct from the general Microsoft 365 MCP.

### Excel (excel-mcp-server)
Dedicated tool for local Excel file manipulation without requiring Excel installed.
*   **Repository**: [haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server)
*   **Official Installation**: `uvx excel-mcp-server stdio`
*   **Local Python**: `pip install excel-mcp-server`
*   **Local Windows (Anaconda)**: `C:\App\Anaconda\envs\langgraph\Scripts\excel-mcp-server.exe`
*   **Configuration**:
    ```json
    "excel": {
      "command": "uvx",
      "args": ["excel-mcp-server", "stdio"]
    }
    ```

### Doc-Tools (Word Doc Manipulation)
A specialized tool for handling Word document structures.
*   **Installation**: `npx @puchunjie/doc-tools-mcp`
*   **Configuration (Robust Fix for 'invalid character W')**:
    We use a local adapter script to silence the Chinese startup message that breaks the protocol.
    ```json
    "doc-tools": {
      "command": "node",
      "args": ["${workspaceFolder}/scripts/mcp-adapters/doc_tools_adapter.js"]
    }
    ```
    > [!NOTE]
    > This adapter automatically runs `npx -y @puchunjie/doc-tools-mcp` and filters the output for compatibility.

### Famano Office (Word Doc Manipulation)
A specialized tool for interacting with Word documents (.docx).
*   **Website**: [Famano Office](https://www.pulsemcp.com/servers/famano-office)
*   **Installation (uvx)**: `uvx mcp-server-office`
*   **Configuration**:
    ```json
    "famano-office": {
      "command": "uvx",
      "args": ["mcp-server-office"]
    }
    ```

---

## 5. System Utilities
### SQLite Manager
*   **Local Executable**: `C:\App\Anaconda\envs\langgraph\Scripts\mcp-sqlite-manager.exe`
*   **Args**: `["start", "--db", "${workspaceFolder}/data/demo.db"]`

### Search & Fetch
*   **Sequential Thinking**: `https://remote.mcpservers.org/sequentialthinking/mcp`
*   **Fetch**: `https://remote.mcpservers.org/fetch/mcp`

---
## 6. Google Workspace (Gmail, Calendar, Drive)
Integration with Google Workspace services using the official Anthropic MCP server.

*   **Repository**: [anthropics/mcp-server-gsuite](https://github.com/anthropics/mcp-server-gsuite)
*   **Installation (npx)**: `npx -y @anthropics/mcp-server-gsuite`
*   **Configuration**:
    ```json
    "google-workspace": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropics/mcp-server-gsuite"
      ],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
      }
    }
    ```

### Setup Instructions
1.  **Create Google Cloud Project**: Go to [Google Cloud Console](https://console.cloud.google.com) and create a new project.
2.  **Enable APIs**: Enable **Gmail API**, **Google Calendar API**, and **Google Drive API**.
3.  **Configure OAuth Consent**:
    *   Go to **APIs & Services > OAuth consent screen**.
    *   Choose **External** (unless you have a Google Workspace organization).
    *   Fill in required fields (App name, support email, etc.).
    *   Add yourself as a **Test User**.
4.  **Create Credentials**:
    *   Go to **APIs & Services > Credentials**.
    *   Click **Create Credentials > OAuth client ID**.
    *   Application type: **Desktop app**.
    *   Name: `MCP Client`.
    *   Download JSON or copy **Client ID** and **Client Secret**.
5.  **Configure Environment**: Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in your environment or directly in the config (env vars recommended).

> [!NOTE]
> On the first run, a browser window will open asking you to authenticate and authorize the app. This will generate a token file in your working directory.

---
*Generated by Antigravity Agent Factory Research*
