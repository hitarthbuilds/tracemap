from tracemap.graph.node import ExecutionNode

def _serialize_value(value):
    """
    Convert runtime values into JSON-safe representations.
    """
    if value is None:
        return None

    if isinstance(value, (int, float, str, bool)):
        return value

    if isinstance(value, (list, tuple)):
        return [_serialize_value(v) for v in value]

    if isinstance(value, dict):
        return {str(k): _serialize_value(v) for k, v in value.items()}

    # Fallback: represent, don't serialize
    return repr(value)


def _node_to_dict(node: ExecutionNode) -> dict:
    return {
        "id": node.id,
        "function": node.function,
        "file": node.file,
        "lines": {
            "start": node.line_start,
            "end": node.line_end,
        },
        "timing": {
            "duration_ms": round(node.duration_ms, 6),
        },
        "locals_diff": {
            name: (
                _serialize_value(old),
                _serialize_value(new),
            )
            for name, (old, new) in node.locals_diff.items()
        },  
        "exception": node.exception,
        "children": [_node_to_dict(child) for child in node.children],
    }


def export_snapshot(graph) -> dict:
    """
    Export the execution graph as a deterministic snapshot.

    This is the canonical output contract of TraceMap.
    """
    if graph.root is None:
        return {}

    return {
        "root": _node_to_dict(graph.root),
        "node_count": len(graph.nodes),
    }
