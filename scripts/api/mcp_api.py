"""
Antigravity IDX Orchestrator — FastAPI Backend.

Provides REST and WebSocket endpoints for:
- Workflow CRUD (Antigravity .md + LangGraph/CrewAI generation)
- Agent, Skill, and Script catalogs
- MCP server management
- LangSmith trace streaming (real-time thought tracing)
- LLM chat via aisuite (Gemini)
"""

import os
import json
import logging
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import service modules (same package)
from workflow_service import (
    list_workflows,
    get_workflow,
    save_workflow,
    list_agents,
    get_agent,
    save_agent,
    list_skills,
    get_skill,
    save_skill,
    list_scripts,
    get_script,
    save_script,
    list_rules,
    list_blueprints,
    list_knowledge_files,
    list_patterns,
    get_generic_artifact,
    save_generic_artifact,
    get_agent_config,
    save_agent_config,
    PROJECT_ROOT,
)
from llm_config import chat_with_aisuite, get_langchain_llm


# ---------------------------------------------------------------------------
# Globals & State
# ---------------------------------------------------------------------------
event_clients: list[WebSocket] = []


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown logic."""
    # Ensure LangSmith tracing is on
    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGSMITH_PROJECT", "antigravity-idx")

    # Start file watcher for Hot Reload
    asyncio.create_task(watch_artifacts())
    yield


async def watch_artifacts():
    """Watch for changes in task.md and walkthrough.md to trigger UI refresh."""
    brain_dir = Path.home() / ".gemini" / "antigravity" / "brain"
    if not brain_dir.exists():
        return

    mtimes = {}
    while True:
        try:
            for artifact in brain_dir.rglob("*.md"):
                if artifact.name in ["task.md", "walkthrough.md"]:
                    mtime = artifact.stat().st_mtime
                    if mtimes.get(str(artifact)) != mtime:
                        mtimes[str(artifact)] = mtime
                        # Broadcast event
                        await broadcast_event(
                            {
                                "type": "file_change",
                                "file": artifact.name,
                                "path": str(artifact),
                            }
                        )
        except Exception:
            pass
        await asyncio.sleep(2)


async def broadcast_event(data: dict):
    """Send JSON data to all connected event clients."""
    for ws in event_clients[:]:
        try:
            await ws.send_json(data)
        except Exception:
            event_clients.remove(ws)


app = FastAPI(title="Antigravity IDX Orchestrator", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Schemas ---


@app.get("/api/schemas/{name}")
async def api_get_schema(name: str):
    """Serve a JSON schema from the schemas directory."""
    if not name.endswith(".json"):
        name += ".schema.json"
    schema_path = PROJECT_ROOT / "schemas" / name
    if not schema_path.exists():
        # Try without .schema
        schema_path = PROJECT_ROOT / "schemas" / name.replace(".schema.json", ".json")

    if not schema_path.exists():
        raise HTTPException(status_code=404, detail=f"Schema {name} not found")

    return json.loads(schema_path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "langsmith_tracing": os.environ.get("LANGSMITH_TRACING", "false"),
        "langsmith_project": os.environ.get("LANGSMITH_PROJECT", ""),
    }


# ---------------------------------------------------------------------------
# Workflows
# ---------------------------------------------------------------------------
@app.get("/api/workflows")
async def api_list_workflows():
    """List all Antigravity workflows."""
    return list_workflows()


@app.get("/api/workflows/{filename}")
async def api_get_workflow(filename: str):
    """Get a specific workflow by filename."""
    result = get_workflow(filename)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


class WorkflowSaveRequest(BaseModel):
    description: str = ""
    tags: list[str] = []
    version: str = "1.0.0"
    title: str = ""
    phases: list[dict] = []
    raw_body: str = ""


@app.put("/api/workflows/{filename}")
async def api_save_workflow(filename: str, data: WorkflowSaveRequest):
    """Save/update a workflow."""
    return save_workflow(filename, data.model_dump())


@app.post("/api/workflows/{filename}")
async def api_create_workflow(filename: str, data: WorkflowSaveRequest):
    """Create a new workflow."""
    return save_workflow(filename, data.model_dump())


# ---------------------------------------------------------------------------
# Agents, Skills, Scripts
# ---------------------------------------------------------------------------
@app.get("/api/agents")
async def api_list_agents():
    """List all agent definitions."""
    return list_agents()


@app.get("/api/agents/{name}")
async def api_get_agent(name: str):
    """Get agent detail and content."""
    result = get_agent(name)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


class ContentSaveRequest(BaseModel):
    path: str
    content: str


@app.put("/api/agents/{name}")
async def api_save_agent(name: str, data: ContentSaveRequest):
    """Save agent content."""
    return save_agent(data.path, data.content)


@app.get("/api/skills")
async def api_list_skills():
    """List all skill definitions."""
    return list_skills()


@app.get("/api/skills/{name}")
async def api_get_skill(name: str):
    """Get skill detail and content."""
    result = get_skill(name)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.put("/api/skills/{name}")
async def api_save_skill(name: str, data: ContentSaveRequest):
    """Save skill content."""
    return save_skill(data.path, data.content)


@app.get("/api/scripts")
async def api_list_scripts():
    """List all Python scripts."""
    return list_scripts()


@app.get("/api/scripts/{path:path}")
async def api_get_script(path: str):
    """Get script content."""
    result = get_script(path)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.put("/api/scripts/{path:path}")
async def api_save_script(path: str, data: ContentSaveRequest):
    """Save script content."""
    return save_script(data.path, data.content)


# --- Generic Artifacts ---


@app.get("/api/artifacts/{path:path}")
async def api_get_artifact(path: str):
    """Get any supported artifact (.md/.json) content."""
    result = get_generic_artifact(path)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.put("/api/artifacts")
async def api_save_artifact(data: ContentSaveRequest):
    """Save any supported artifact content."""
    return save_generic_artifact(data.path, data.content)


# --- Specialized Lists ---


@app.get("/api/rules")
async def api_list_rules():
    return list_rules()


@app.get("/api/blueprints")
async def api_list_blueprints():
    return list_blueprints()


@app.get("/api/knowledge-files")
async def api_list_knowledge_files():
    return list_knowledge_files()


@app.get("/api/patterns")
async def api_list_patterns():
    return list_patterns()


@app.get("/api/agent-config")
async def api_get_agent_config():
    return get_agent_config()


@app.put("/api/agent-config")
async def api_save_agent_config(data: dict):
    return save_agent_config(data)


# ---------------------------------------------------------------------------
# MCP Servers
@app.get("/api/mcp/servers")
async def api_list_mcp_servers():
    """List all available MCP servers from mcp_config.json."""
    mcp_config_path = Path.home() / ".gemini" / "antigravity" / "mcp_config.json"
    servers = []
    if mcp_config_path.exists():
        try:
            config = json.loads(mcp_config_path.read_text(encoding="utf-8"))
            for name, details in config.get("mcpServers", {}).items():
                servers.append(
                    {
                        "id": name,
                        "name": name,
                        "status": "connected",  # Mock status for now
                        "command": details.get("command", ""),
                        "args": details.get("args", []),
                    }
                )
        except Exception:
            pass
    return servers


@app.get("/api/mcp/servers/{name}")
async def api_get_mcp_server(name: str):
    """Get a single MCP server config."""
    mcp_config_path = Path.home() / ".gemini" / "antigravity" / "mcp_config.json"
    if mcp_config_path.exists():
        config = json.loads(mcp_config_path.read_text(encoding="utf-8"))
        if name in config.get("mcpServers", {}):
            details = config["mcpServers"][name]
            return {
                "id": name,
                "name": name,
                "command": details.get("command", ""),
                "args": details.get("args", []),
                "env": details.get("env", {}),
            }
    raise HTTPException(status_code=404, detail=f"MCP Server {name} not found")


class McpServerCreate(BaseModel):
    name: str
    command: str
    args: list[str] = []
    env: dict[str, str] = {}


@app.post("/api/mcp/servers")
async def api_create_mcp_server(req: McpServerCreate):
    """Add a new MCP server to mcp_config.json."""
    mcp_config_path = Path.home() / ".gemini" / "antigravity" / "mcp_config.json"
    config = {"mcpServers": {}}
    if mcp_config_path.exists():
        try:
            config = json.loads(mcp_config_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    config.setdefault("mcpServers", {})[req.name] = {
        "command": req.command,
        "args": req.args,
        "env": req.env,
    }

    mcp_config_path.parent.mkdir(parents=True, exist_ok=True)
    mcp_config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return {"status": "created", "name": req.name}


@app.delete("/api/mcp/servers/{name}")
async def api_delete_mcp_server(name: str):
    """Remove an MCP server from mcp_config.json."""
    mcp_config_path = Path.home() / ".gemini" / "antigravity" / "mcp_config.json"
    if mcp_config_path.exists():
        config = json.loads(mcp_config_path.read_text(encoding="utf-8"))
        if name in config.get("mcpServers", {}):
            del config["mcpServers"][name]
            mcp_config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
            return {"status": "deleted"}
    raise HTTPException(status_code=404, detail=f"MCP Server {name} not found")


@app.post("/api/mcp/servers/{name}/test")
async def api_test_mcp_server(name: str):
    """Test an MCP server by performing a real handshake."""
    mcp_config_path = Path.home() / ".gemini" / "antigravity" / "mcp_config.json"
    if not mcp_config_path.exists():
        raise HTTPException(status_code=404, detail="Config not found")

    config = json.loads(mcp_config_path.read_text(encoding="utf-8"))
    details = config.get("mcpServers", {}).get(name)
    if not details:
        raise HTTPException(status_code=404, detail=f"Server {name} not found")

    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from mcp.client.sse import sse_client

    try:
        print(f"DEBUG: Testing MCP server: {name}")
        # Check if it's an SSE server or stdio server
        server_url = details.get("serverUrl")

        if server_url:
            print(f"DEBUG: Connecting via SSE to {server_url}")
            # SSE Test
            async with sse_client(url=server_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    tool_names = [t.name for t in tools.tools]
                    return {
                        "status": "success",
                        "stdout": f"Connected to SSE server. Available tools: {len(tool_names)}",
                    }
        else:
            print(
                f"DEBUG: Connecting via stdio: {details['command']} {details.get('args', [])}"
            )
            # Stdio Test
            params = StdioServerParameters(
                command=details["command"],
                args=details.get("args", []),
                env={**os.environ, **details.get("env", {})},
            )
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    print("DEBUG: Client connected, initializing...")
                    await session.initialize()
                    print("DEBUG: Handshake successful, listing tools...")
                    tools = await session.list_tools()
                    tool_names = [t.name for t in tools.tools]
                    print(f"DEBUG: Found {len(tool_names)} tools")
                    return {
                        "status": "success",
                        "stdout": f"Handshake OK. Found tools: {', '.join(tool_names[:10])}{' ...' if len(tool_names) > 10 else ''}",
                    }

    except Exception as e:
        print(f"DEBUG: MCP Test Error for {name}: {str(e)}")
        return {"status": "error", "error": f"{type(e).__name__}: {str(e)}"}


# ---------------------------------------------------------------------------
# LLM Chat (aisuite)
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    messages: list[dict]
    model: str = "google:gemini-2.5-flash-lite"


@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    """Chat with an LLM via aisuite."""
    try:
        result = chat_with_aisuite(req.messages, model=req.model)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# LangSmith Traces (Thought Tracer data source)
# ---------------------------------------------------------------------------
@app.get("/api/traces")
async def api_get_traces(project: str = "antigravity-idx", limit: int = 20):
    """Fetch recent LangSmith traces for the Thought Tracer panel."""
    try:
        from langsmith import Client

        client = Client()
        runs = list(
            client.list_runs(
                project_name=project,
                limit=limit,
            )
        )
        return [
            {
                "id": str(run.id),
                "name": run.name,
                "run_type": run.run_type,
                "status": run.status,
                "start_time": run.start_time.isoformat() if run.start_time else None,
                "end_time": run.end_time.isoformat() if run.end_time else None,
                "latency_ms": getattr(run, "latency_ms", None),
                "total_tokens": getattr(run, "total_tokens", None),
                "error": run.error,
                "inputs": str(run.inputs)[:200] if run.inputs else None,
                "outputs": str(run.outputs)[:200] if run.outputs else None,
            }
            for run in runs
        ]
    except ImportError:
        return {"error": "langsmith package not installed"}
    except Exception as e:
        return {"error": str(e), "traces": []}


# ---------------------------------------------------------------------------
# WebSocket: Real-time Thought Streaming
# ---------------------------------------------------------------------------
@app.websocket("/ws/thoughts")
async def thought_stream(websocket: WebSocket):
    """Stream agent thoughts in real-time via WebSocket.

    Polls LangSmith for new traces and forwards them to connected clients.
    Falls back to local log file if LangSmith is unavailable.
    """
    await websocket.accept()
    seen_ids: set[str] = set()

    try:
        while True:
            # Try LangSmith first
            try:
                from langsmith import Client

                client = Client()
                runs = list(
                    client.list_runs(
                        project_name=os.environ.get(
                            "LANGSMITH_PROJECT", "antigravity-idx"
                        ),
                        limit=5,
                    )
                )
                for run in runs:
                    run_id = str(run.id)
                    if run_id not in seen_ids:
                        seen_ids.add(run_id)
                        await websocket.send_json(
                            {
                                "type": "trace",
                                "id": run_id,
                                "name": run.name,
                                "run_type": run.run_type,
                                "status": run.status,
                                "latency_ms": getattr(run, "latency_ms", None),
                                "error": run.error,
                            }
                        )
            except Exception:
                # Fallback: tail local thoughts.log
                log_path = PROJECT_ROOT / "thoughts.log"
                if log_path.exists():
                    try:
                        with open(log_path, "r", encoding="utf-8") as f:
                            # Read all lines to find new ones
                            lines = f.readlines()
                            for line in lines:
                                line = line.strip()
                                if not line:
                                    continue
                                try:
                                    data = json.loads(line)
                                    line_id = data.get("id", f"hash_{hash(line)}")
                                    if line_id not in seen_ids:
                                        seen_ids.add(line_id)
                                        await websocket.send_json(data)
                                except json.JSONDecodeError:
                                    pass
                    except Exception as e:
                        logging.error(f"Error reading thoughts.log: {e}")

            await asyncio.sleep(2)
    except Exception:
        pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass


@app.websocket("/ws/events")
async def event_stream(websocket: WebSocket):
    """General event stream for hot-reloading and UI notifications."""
    await websocket.accept()
    event_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep alive
    except Exception:
        pass
    finally:
        if websocket in event_clients:
            event_clients.remove(websocket)


# ---------------------------------------------------------------------------
# Agent Workflow Generation (LangGraph / CrewAI)
# ---------------------------------------------------------------------------
class AgentWorkflowRequest(BaseModel):
    """Request to generate an executable agent workflow."""

    name: str
    description: str
    framework: str = "langgraph"  # langgraph | crewai
    steps: list[dict] = []
    tools: list[str] = []


@app.post("/api/agent-workflows/generate")
async def generate_agent_workflow(req: AgentWorkflowRequest):
    """Use LLM to generate a LangGraph or CrewAI workflow Python file."""
    llm = get_langchain_llm()

    framework_instructions = {
        "langgraph": "Generate a LangGraph StateGraph workflow with typed state, nodes for each step, and conditional edges.",
        "crewai": "Generate a CrewAI workflow with Agent and Task definitions, using a Crew with sequential or hierarchical process.",
    }

    prompt = f"""You are an expert AI engineer. Generate a production-ready Python file for the following workflow:

**Name**: {req.name}
**Description**: {req.description}
**Framework**: {req.framework}
**Steps**: {json.dumps(req.steps, indent=2)}
**Tools to integrate**: {req.tools}

{framework_instructions.get(req.framework, '')}

Include proper imports, type hints, docstrings, and error handling.
Use langchain_google_genai.ChatGoogleGenerativeAI as the LLM with model="gemini-2.5-flash-lite".
Include LangSmith tracing setup at the top of the file (LANGSMITH_TRACING=true, LANGSMITH_PROJECT=antigravity-idx).
Return ONLY the Python code, no markdown fences."""

    response = llm.invoke(prompt)
    code = response.content

    # Save the generated file
    output_dir = PROJECT_ROOT / "scripts" / "ai" / "agents" / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{req.name.replace(' ', '_').lower()}.py"
    output_path.write_text(code, encoding="utf-8")

    return {
        "status": "generated",
        "path": str(output_path.relative_to(PROJECT_ROOT)),
        "framework": req.framework,
        "code_preview": code[:500],
    }


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
