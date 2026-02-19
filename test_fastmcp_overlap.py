from mcp.server.fastmcp import FastMCP
from starlette.testclient import TestClient
import asyncio

# Setup FastMCP with overlapping paths
try:
    print("Initializing FastMCP with overlapping /sse paths...")
    # Attempt to set both to /sse
    mcp = FastMCP("Test Server", sse_path="/sse", message_path="/sse")

    # Get the underlying Starlette app
    app = mcp.sse_app()
    client = TestClient(app)

    print("\n--- Testing GET /sse (Should be SSE endpoint) ---")
    response_get = client.get("/sse")
    print(f"GET /sse Status: {response_get.status_code}")
    # SSE usually returns 200 OK (stream started) or equivalent

    print("\n--- Testing POST /sse (Should be Message endpoint) ---")
    # Send a dummy message without session_id (should fail validation but NOT be 405)
    response_post = client.post(
        "/sse", json={"jsonrpc": "2.0", "method": "ping", "id": 1}
    )
    print(f"POST /sse Status: {response_post.status_code}")
    print(f"Body: {response_post.text}")

    if response_post.status_code == 405:
        print("FAIL: POST /sse returned 405 Method Not Allowed (Route conflict)")
    elif response_post.status_code in [200, 202, 400]:
        print(
            f"PASS: POST /sse returned {response_post.status_code} (Handled by Message endpoint)"
        )
    else:
        print(f"WARN: Unexpected status {response_post.status_code}")

except Exception as e:
    print(f"Error during test: {e}")
