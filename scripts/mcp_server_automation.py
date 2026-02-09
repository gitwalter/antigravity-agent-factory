import json
import logging
import sys
import subprocess
from pathlib import Path

# Configure logging to stderr to avoid polluting stdout (which is used for JSON-RPC)
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("mcp-automation")

ROOT = Path(__file__).parent.parent

def run_script(script_path, args=None):
    if args is None:
        args = []
    
    full_path = ROOT / script_path
    cmd = [sys.executable, str(full_path)] + args
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}\n\nExit Code: {result.returncode}"
                }
            ],
            "isError": result.returncode != 0
        }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error executing script: {e}"
                }
            ],
            "isError": True
        }

def handle_initialize(request):
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "antigravity-automation",
            "version": "1.0.0"
        }
    }

def handle_list_tools(request):
    return {
        "tools": [
            {
                "name": "run_pre_commit_check",
                "description": "Run the pre-commit validation runner in check mode.",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "generate_test_catalog",
                "description": "Generate the test catalog documentation.",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
             {
                "name": "fetch_updates",
                "description": "Fetch updates from a PABP source.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string", "description": "URL or path to source"}
                    },
                    "required": ["source"]
                }
            }
        ]
    }

def handle_call_tool(request):
    params = request.get("params", {})
    name = params.get("name")
    args = params.get("arguments", {})
    
    if name == "run_pre_commit_check":
        return run_script("scripts/git/pre_commit_runner.py", ["--check"])
    elif name == "generate_test_catalog":
        return run_script("scripts/docs/generate_test_catalog.py")
    elif name == "fetch_updates":
        source = args.get("source")
        if not source:
             return {"content": [{"type": "text", "text": "Missing source argument"}], "isError": True}
        return run_script("scripts/pabp/fetch_updates.py", ["--source", source])
    else:
        return {
            "content": [{"type": "text", "text": f"Unknown tool: {name}"}],
            "isError": True
        }

def main():
    logger.info("Starting Automation MCP Server...")
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line)
            logger.info(f"Received request: {request.get('method')}")
            
            response = {"jsonrpc": "2.0", "id": request.get("id")}
            method = request.get("method")
            
            if method == "initialize":
                response["result"] = handle_initialize(request)
            elif method == "tools/list":
                response["result"] = handle_list_tools(request)
            elif method == "tools/call":
                response["result"] = handle_call_tool(request)
            elif method == "notifications/initialized":
                 # No response needed for notifications
                 continue
            else:
                 # Ignore other messages for simple implementation
                 continue
                 
            print(json.dumps(response), flush=True)
            
        except Exception as e:
            logger.error(f"Error handling request: {e}", exc_info=True)
            # Try to send error response if possible
            continue

if __name__ == "__main__":
    main()
