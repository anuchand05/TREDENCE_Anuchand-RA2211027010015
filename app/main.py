from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import asyncio

from app.models import GraphSpec, RunRequest
from app.engine.tools import ToolRegistry, extract_functions, check_complexity, detect_basic_issues, suggest_improvements
from app.engine.graph import GraphEngine
from app.engine.workflows import make_code_review_graph

app = FastAPI(title="Mini Workflow Engine")

from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# setup tools and engine
tool_registry = ToolRegistry()
tool_registry.register("extract_functions", extract_functions)
tool_registry.register("check_complexity", check_complexity)
tool_registry.register("detect_basic_issues", detect_basic_issues)
tool_registry.register("suggest_improvements", suggest_improvements)

engine = GraphEngine(tool_registry)

# create a sample graph on startup
@app.on_event("startup")
async def _startup():
    sample = make_code_review_graph()
    engine.create_graph(sample)

@app.post("/graph/create")
async def create_graph(spec: GraphSpec):
    gid = engine.create_graph(spec.dict())
    return {"graph_id": gid}

@app.post("/graph/run")
async def run_graph(req: RunRequest):
    if not engine.get_graph(req.graph_id):
        raise HTTPException(status_code=404, detail="graph not found")
    # If a threshold isn't provided, set a default for the workflow
    state = dict(req.initial_state)
    state.setdefault("threshold", 80)

    run_id = await engine.run_graph(req.graph_id, state)
    return {"run_id": run_id}

@app.get("/graph/state/{run_id}")
async def get_run_state(run_id: str):
    run = engine.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    # return state, status, last log entries
    logs = [entry.dict() for entry in run["log"]]
    return {
        "status": run["status"],
        "state": run["state"],
        "current_node": run.get("current_node"),
        "log": logs
    }

# optional endpoint to wait for completion synchronously (for convenience)
@app.post("/graph/wait/{run_id}")
async def wait_for_completion(run_id: str):
    task = engine.run_tasks.get(run_id)
    if not task:
        raise HTTPException(status_code=404, detail="run task not found")
    await task
    run = engine.get_run(run_id)
    return {
        "status": run["status"],
        "state": run["state"],
        "log": [l.dict() for l in run["log"]]
    }

# endpoint to cancel a running workflow
@app.post("/graph/cancel/{run_id}")
async def cancel_run(run_id: str):
    task = engine.run_tasks.get(run_id)
    if not task:
        raise HTTPException(status_code=404, detail="Run not found")
    task.cancel()
    return {"status": "cancelled"}

from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/run/{run_id}")
async def websocket_logs(websocket: WebSocket, run_id: str):
    await websocket.accept()

    run = engine.get_run(run_id)
    if not run:
        await websocket.send_text("Invalid run_id")
        await websocket.close()
        return

    last_index = 0  # Tracks what parts of the log have already been sent

    try:
        while True:
            await asyncio.sleep(0.1)

            logs = run["log"]
            new_logs = logs[last_index:]

            # Send all new logs
            for entry in new_logs:
                await websocket.send_json(entry.dict())

            last_index = len(logs)

            # Stop streaming when workflow finishes
            if run["status"] in ("completed", "cancelled", "error"):
                await websocket.send_text(f"Run finished with status: {run['status']}")
                await websocket.close()
                return

    except WebSocketDisconnect:
        print("WebSocket disconnected")

