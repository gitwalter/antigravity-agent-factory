@echo off
REM Start the Antigravity RAG MCP Server (SSE Mode)
REM This server must be running for the IDE/Agent to access RAG tools.

echo Starting Antigravity RAG MCP Server...
echo URL: http://localhost:8000/sse
echo.

call scripts\maintenance\detect_env.bat
set PYTHONPATH=%CD%
set MCP_TRANSPORT=sse

python scripts\mcp\servers\rag\rag_mcp_server.py

pause
