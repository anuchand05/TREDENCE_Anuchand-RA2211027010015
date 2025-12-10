# This file exports a helper to build the sample graph for Option A (Code Review)
def make_code_review_graph():
    # nodes: id, fn, optional condition / max_iterations
    nodes = [
        {"id": "extract", "fn": "extract_functions"},
        {"id": "complexity", "fn": "check_complexity"},
        {"id": "issues", "fn": "detect_basic_issues"},
        {"id": "suggest", "fn": "suggest_improvements", 
         # We'll loop on 'suggest' until quality_score >= threshold
         # use condition to decide whether to continue: if quality_score < threshold -> return node id 'complexity' to loop
         "condition": "state.get('quality_score', 0) < state.get('threshold', 80)",
         "max_iterations": 5  # safety guard
        },
    ]
    # edges simple linear, but condition on 'suggest' can return name to continue loop
    edges = {
        "extract": "complexity",
        "complexity": "issues",
        "issues": "suggest",
        # when suggest condition is false, it will fall through to None (end)
    }
    return {"id": "code_review_sample", "nodes": nodes, "edges": edges}
