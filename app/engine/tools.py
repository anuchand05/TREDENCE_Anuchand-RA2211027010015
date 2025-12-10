from typing import Callable, Dict, Any
import asyncio

Tool = Callable[[dict], dict]

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, name: str, fn: Tool):
        self._tools[name] = fn

    def get(self, name: str):
        return self._tools.get(name)

# Example tools for Code Review workflow (rule-based)
def extract_functions(state: dict) -> dict:
    # pretend to parse code in state['code'] and count functions
    code = state.get("code", "")
    # very naive: count "def " occurrences
    functions = code.count("def ")
    state.setdefault("meta", {})["functions"] = functions
    return {"message": f"extracted {functions} functions"}

def check_complexity(state: dict) -> dict:
    # naive complexity: functions * 2 + len(code) // 100
    functions = state.get("meta", {}).get("functions", 0)
    code_len = len(state.get("code", ""))
    complexity = functions * 2 + code_len // 100
    state.setdefault("meta", {})["complexity"] = complexity
    return {"message": f"computed complexity={complexity}"}

def detect_basic_issues(state: dict) -> dict:
    # naive issues: number of "TODO" and "print(" occurrences
    code = state.get("code", "")
    issues = code.count("TODO") + code.count("print(")
    state.setdefault("meta", {})["issues"] = issues
    return {"message": f"detected {issues} issues"}

def suggest_improvements(state: dict) -> dict:
    # produce a quality_score (higher is better)
    complexity = state.get("meta", {}).get("complexity", 0)
    issues = state.get("meta", {}).get("issues", 0)
    # naive scoring: start 100, subtract complexity*3 and issues*10
    score = max(0, 100 - complexity * 3 - issues * 10)
    state["quality_score"] = score
    return {"message": f"suggested improvements, quality_score={score}"}

def simple_sleep(state: dict) -> dict:
    # Example of async-like long running tool (we'll await this in engine)
    import time
    time.sleep(0.1)
    return {"message": "slept briefly"}
