from tracemap.graph.node import ExecutionNode


class ExecutionGraph:
    """
    Append-only execution graph.
    Responsible only for structure, not tracing.
    """

    __slots__ = ("root", "nodes", "_open")

    def __init__(self):
        self.root = None
        self.nodes = {}      # node_id -> ExecutionNode
        self._open = []      # stack of open node_ids

    def attach(self, node: ExecutionNode):
        if self._open:
            parent = self.nodes[self._open[-1]]
            parent.children.append(node)
        else:
            self.root = node

        self.nodes[node.id] = node
        self._open.append(node.id)

    def close(self, node_id: str, line_end: int):
        if not self._open or self._open[-1] != node_id:
            return  # defensive: invalid close order

        node = self.nodes[node_id]
        node.close(line_end)
        self._open.pop()

    @property
    def depth(self) -> int:
        return len(self._open)
