@echo off
REM Start the Antigravity RAG MCP Server (SSE Mode)
REM This server must be running for the IDE/Agent to access RAG tools.

echo Starting Antigravity RAG MCP Server...
echo URL: http://localhost:8000/sse
echo.

call D:\Anaconda\Scripts\activate.bat D:\Anaconda\envs\cursor-factory
set PYTHONPATH=D:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory
set MCP_TRANSPORT=sse

"D:\Anaconda\envs\cursor-factory\python.exe" "D:\Users\wpoga\Documents\Python Scripts\antigravity-agent-factory\scripts\mcp\servers\rag\rag_mcp_server.py"

pause
