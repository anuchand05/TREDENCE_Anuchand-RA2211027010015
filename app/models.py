from typing import Any, Dict, Optional, List
from pydantic import BaseModel

# Node config (simple)
class NodeConfig(BaseModel):
    id: str
    fn: str  # the registered node function name
    # optional condition expression (applies after node runs) for branching
    condition: Optional[str] = None  # e.g. "state['issues'] > 0"
    # optional max loop iterations for the node
    max_iterations: Optional[int] = None

class GraphSpec(BaseModel):
    id: Optional[str] = None
    nodes: List[NodeConfig]
    edges: Dict[str, str]  # simple mapping node_id -> next_node_id

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

class ExecutionLogEntry(BaseModel):
    node: str
    message: str
    state_snapshot: Dict[str, Any]
