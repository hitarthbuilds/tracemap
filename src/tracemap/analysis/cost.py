from tracemap.graph.node import ExecutionNode


def compute_costs(root: ExecutionNode) -> dict:
    """
    Compute inclusive and self time for all nodes in the execution tree.

    Returns:
        dict[node_id] = {
            "inclusive_ms": float,
            "self_ms": float
        }
    """
    costs = {}

    def visit(node: ExecutionNode):
        inclusive = node.duration_ms

        children_time = 0.0
        for child in node.children:
            visit(child)
            children_time += costs[child.id]["inclusive_ms"]

        self_time = max(inclusive - children_time, 0.0)

        costs[node.id] = {
            "inclusive_ms": inclusive,
            "self_ms": self_time,
        }

    visit(root)
    return costs
