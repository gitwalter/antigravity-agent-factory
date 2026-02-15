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
*   **Fetch (uvx)**: `uvx mcp-server-fetch`
*   **DeepWiki (SSE)**: `https://mcp.deepwiki.com/mcp`

---
## 6. Google Workspace (Gmail, Calendar, Drive)
Integration with Google Workspace services using the official Anthropic MCP server.

*   **Repository**: [GongRzhe/Gmail-MCP-Server](https://github.com/GongRzhe/Gmail-MCP-Server)
*   **Installation (npx)**: `npx -y @gongrzhe/server-gmail-autoauth-mcp`
*   **Configuration**:
    ```json
    "gmail": {
      "command": "npx",
      "args": [
        "-y",
        "@gongrzhe/server-gmail-autoauth-mcp"
      ]
    }
    ```


### Advanced Workspace (MarkusPfundstein)
*   **Repository**: [markuspfundstein/mcp-gsuite](https://github.com/markuspfundstein/mcp-gsuite)
*   **Installation (npx)**: `npx -y @markuspfundstein/mcp-gsuite`
*   **Configuration**: Requires `.gauth.json` and `.accounts.json` in the working directory.

### Drive & Sheets (IsaacPhi)
*   **Repository**: [isaacphi/mcp-gdrive](https://github.com/isaacphi/mcp-gdrive)
*   **Installation (npx)**: `npx -y @isaacphi/mcp-gdrive`
*   **Configuration**: Requires `GDRIVE_CREDS_DIR`, `CLIENT_ID`, and `CLIENT_SECRET`.

### SAP Documentation (marianfoo)
*   **Repository**: [marianfoo/mcp-sap-docs](https://github.com/marianfoo/mcp-sap-docs)
*   **Installation (npx)**: `npx -y mcp-sap-docs`
*   **Configuration**: No special credentials required for public search.

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
5.  **Run Server**: The browser will open automatically for authentication. A token will be stored securely.

---
## 7. Playwright Browser Automation (Docker)
Official Playwright integration running in a container.

*   **Docker Image**: `mcp/playwright`
*   **Cursor Configuration**:
    ```json
    "playwright": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "mcp/playwright"
      ]
    }
    ```

---
*Generated by Antigravity Agent Factory Research*
