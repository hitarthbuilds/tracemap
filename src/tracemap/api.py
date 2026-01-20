import sys

from tracemap.graph.graph import ExecutionGraph
from tracemap.runtime.trace_context import TraceContext
from tracemap.runtime.trace_hook import TraceHook


def trace(code: str) -> ExecutionGraph:
    """
    Execute Python code and return its execution graph.
    """
    graph = ExecutionGraph()
    ctx = TraceContext(graph)
    hook = TraceHook(ctx)

    sys.settrace(hook)
    try:
        exec(code, {})
    except Exception:
    # Swallow user exceptions.
    # They are already recorded in the execution graph.
        pass
    finally:
        sys.settrace(None)

    return graph
