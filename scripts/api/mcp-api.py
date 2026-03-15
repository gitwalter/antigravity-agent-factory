from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

app = FastAPI(title="Antigravity IDX Orchestrator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/api/mcp/servers")
async def get_mcp_servers():
    return [
        {"id": "fs", "name": "filesystem", "status": "online", "type": "Core"},
        {"id": "mem", "name": "memory", "status": "online", "type": "Core"},
        {"id": "git", "name": "git", "status": "online", "type": "Core"},
        {"id": "tav", "name": "tavily", "status": "online", "type": "Intelligence"},
    ]


@app.get("/api/traffic")
async def get_traffic():
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    log_path = os.path.join(base_dir, "traffic.log")
    try:
        traffic = []
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                for line in f:
                    if line.strip():
                        traffic.append(json.loads(line))
        return traffic[-10:] if isinstance(traffic, list) else []
    except Exception as e:
        print(f"Traffic error: {e}")
        return []


@app.websocket("/ws/thoughts")
async def thought_stream(websocket: WebSocket):
    await websocket.accept()
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    log_path = os.path.join(base_dir, "thoughts.log")
    try:
        # Read existing thoughts first
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                for line in f:
                    if line.strip():
                        await websocket.send_json(json.loads(line))

        # Tail the file for new thoughts
        if os.path.exists(log_path):
            with open(log_path, "r") as file:
                file.seek(0, 2)  # Go to end
                while True:
                    line = file.readline()
                    if not line:
                        await asyncio.sleep(0.5)
                        continue
                    if line.strip():
                        await websocket.send_json(json.loads(line))
        else:
            print(f"Log path not found: {log_path}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        try:
            await websocket.close()
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
