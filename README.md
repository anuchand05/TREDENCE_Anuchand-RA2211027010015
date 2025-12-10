# Mini Workflow Engine (AI Engineering Internship Assignment)

## What this repo contains
- A minimal workflow/graph engine in Python with:
  - Nodes (simple functions) that read and modify shared state
  - Edges, branching (via conditions), and a looping example (with max_iterations guard)
  - A simple tool registry
  - FastAPI endpoints to create graphs, start runs, and query run state

- Example workflow implemented: **Code Review Mini-Agent** (Option A).

## Files
- `app/main.py` — FastAPI app
- `app/engine/graph.py` — core engine
- `app/engine/tools.py` — tool registry + example tools
- `app/engine/workflows.py` — sample code-review graph generator
- `app/models.py` — Pydantic models
- `requirements.txt`

