#Mini Workflow Engine — Tredence AI Engineering Internship Assignment

A lightweight, extensible agent workflow engine built using FastAPI, showcasing Python backend design, async execution, state management, conditional branching, looping logic, and live run inspection.

This project demonstrates the core backend engineering skills required for the Tredence AI Engineering Internship — including API design, workflow orchestration, structured state handling, and clean code architecture.

What This Project Does

This engine allows you to:

Define nodes (steps) that execute Python functions

Maintain a shared state dictionary flowing through the workflow

Define edges to control transitions between nodes

Perform conditional branching using safe rule evaluation

Support loops with max_iterations

Register and call custom tools

Run workflows asynchronously

Track progress via:

/graph/state/{run_id} (live state)

/graph/wait/{run_id} (block until completion)

Cancel running workflows (/graph/cancel/{run_id})
