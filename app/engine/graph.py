from typing import Dict, Any, Callable, List, Optional
import asyncio
import uuid
from copy import deepcopy
from app.engine.tools import ToolRegistry
from app.models import ExecutionLogEntry
from app.engine.safe_eval import safe_eval  # ✅ NEW IMPORT


# Engine: maintains in-memory graphs and runs
class GraphEngine:
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry
        self.graphs: Dict[str, Dict] = {}
        self.runs: Dict[str, Dict] = {}  # run_id -> {state, log, status}
        self.run_tasks: Dict[str, asyncio.Task] = {}

    def create_graph(self, graph_spec: Dict) -> str:
        graph_id = graph_spec.get("id") or str(uuid.uuid4())
        self.graphs[graph_id] = deepcopy(graph_spec)
        return graph_id

    def get_graph(self, graph_id: str):
        return self.graphs.get(graph_id)

    def get_run(self, run_id: str):
        return self.runs.get(run_id)

    async def _exec_node(self, node_cfg: Dict, state: Dict[str, Any], run_ctx: Dict) -> ExecutionLogEntry:
        fn_name = node_cfg["fn"]
        tool_fn = self.tool_registry.get(fn_name)
        if not tool_fn:
            msg = f"tool '{fn_name}' not found"
            entry = ExecutionLogEntry(node=node_cfg["id"], message=msg, state_snapshot=deepcopy(state))
            run_ctx["log"].append(entry)
            return entry

        if asyncio.iscoroutinefunction(tool_fn):
            result = await tool_fn(state)
        else:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: tool_fn(state))

        msg = result.get("message") if isinstance(result, dict) and "message" in result else str(result)
        entry = ExecutionLogEntry(node=node_cfg["id"], message=msg, state_snapshot=deepcopy(state))
        run_ctx["log"].append(entry)
        return entry

    async def run_graph(self, graph_id: str, initial_state: Dict[str, Any]) -> str:
        graph = self.get_graph(graph_id)
        if not graph:
            raise ValueError("graph not found")

        run_id = str(uuid.uuid4())
        run_ctx = {
            "state": deepcopy(initial_state),
            "log": [],
            "status": "running",
            "current_node": None,
            "iter_counters": {},
        }
        self.runs[run_id] = run_ctx

        task = asyncio.create_task(self._execute(graph, run_ctx, run_id))
        self.run_tasks[run_id] = task
        return run_id

    async def _execute(self, graph: Dict, run_ctx: Dict, run_id: str):
        try:
            nodes_by_id = {n["id"]: n for n in graph["nodes"]}
            current = graph["nodes"][0]["id"]
            edges = graph.get("edges", {})

            while current:
                run_ctx["current_node"] = current
                node_cfg = nodes_by_id[current]

                run_ctx["iter_counters"].setdefault(current, 0)
                run_ctx["iter_counters"][current] += 1

                await self._exec_node(node_cfg, run_ctx["state"], run_ctx)

                next_node = edges.get(current)
                condition = node_cfg.get("condition")
                max_iter = node_cfg.get("max_iterations")

                took_branch = False

                if condition:
                    try:
                        cond_result = safe_eval(condition, run_ctx["state"])  # ✅ SAFE NOW
                    except ValueError as e:
                        run_ctx["log"].append(ExecutionLogEntry(
                            node=current,
                            message=f"condition error: {e}",
                            state_snapshot=deepcopy(run_ctx["state"]),
                        ))
                        cond_result = False

                    if isinstance(cond_result, str):
                        next_node = cond_result
                        took_branch = True
                    elif cond_result:
                        took_branch = True

                if max_iter and run_ctx["iter_counters"].get(current, 0) >= max_iter:
                    run_ctx["log"].append(ExecutionLogEntry(
                        node=current,
                        message=f"max_iterations reached ({max_iter}), breaking loop",
                        state_snapshot=deepcopy(run_ctx["state"]),
                    ))

                current = next_node
                await asyncio.sleep(0)

            run_ctx["status"] = "completed"

        except asyncio.CancelledError:
            run_ctx["status"] = "cancelled"
            run_ctx["log"].append(ExecutionLogEntry(
                node=run_ctx.get("current_node", "unknown"),
                message="run cancelled",
                state_snapshot=deepcopy(run_ctx["state"])
            ))

        except Exception as exc:
            run_ctx["status"] = "error"
            run_ctx["log"].append(ExecutionLogEntry(
                node=run_ctx.get("current_node", "unknown"),
                message=f"error: {exc}",
                state_snapshot=deepcopy(run_ctx["state"])
            ))
