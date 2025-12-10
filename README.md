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

## How to run
1. Create a venv and install:

Mini Workflow Engine – AI Engineering Internship Assignment

A lightweight, extensible workflow/graph engine inspired by LangGraph.
Built using Python, FastAPI, and async execution, it allows you to define:

Nodes → Python functions that read & modify shared state

Edges → connections defining execution flow

Conditional branching

Looping based on state

A shared state dictionary flowing between nodes

This project includes a fully functional example workflow:

Code Review Mini-Agent

A simple rule-based agent that analyzes Python code and iteratively improves its “quality score”.