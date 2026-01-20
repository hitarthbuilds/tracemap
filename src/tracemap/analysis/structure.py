from tracemap.graph.node import ExecutionNode


def analyze_structure(root: ExecutionNode) -> dict:
    """
    Analyze execution structure:
    - max depth
    - deepest call chain
    - fanout per node
    - recursion detection
    """

    max_depth = 0
    deepest_chain = []
    recursion_nodes = set()
    fanout = {}

    def dfs(node: ExecutionNode, path):
        nonlocal max_depth, deepest_chain

        path.append(node)

        # Depth
        depth = len(path)
        if depth > max_depth:
            max_depth = depth
            deepest_chain = [n.function for n in path]

        # Fanout
        fanout[node.id] = len(node.children)

        # Recursion detection (function-level)
        names = [n.function for n in path]
        if len(names) != len(set(names)):
            recursion_nodes.add(node.function)

        for child in node.children:
            dfs(child, path)

        path.pop()

    dfs(root, [])

    return {
        "max_depth": max_depth,
        "deepest_chain": deepest_chain,
        "fanout": fanout,
        "recursive_functions": sorted(recursion_nodes),
    }
