class TraceContext:
    """
    Single source of truth for all mutable tracing state.

    There must be exactly ONE TraceContext per trace run.
    """

    __slots__ = (
        "graph",
        "_call_stack",
        "_frames",
    )

    def __init__(self, graph):
        self.graph = graph          # ExecutionGraph
        self._call_stack = []       # stack of node_ids
        self._frames = {}           # frame_id -> FrameRuntime

    # -------------------------
    # Call lifecycle
    # -------------------------

    def enter_call(self, frame_runtime):
        """
        Register a new function call.
        """
        node = frame_runtime.node

        self.graph.attach(node)
        self._call_stack.append(node.id)
        self._frames[frame_runtime.frame_id] = frame_runtime

    def exit_call(self, frame_id: int, line_end: int):
        """
        Close the current function call.
        Enforces stack discipline.
        """
        frame_rt = self._frames.pop(frame_id, None)
        if frame_rt is None:
            return

        node_id = frame_rt.node.id

        if not self._call_stack or self._call_stack[-1] != node_id:
            # Defensive: out-of-order return (should not happen)
            return

        self._call_stack.pop()
        self.graph.close(node_id, line_end)

    # -------------------------
    # Runtime helpers
    # -------------------------

    def current_node(self):
        """
        Return the currently executing node, if any.
        """
        if not self._call_stack:
            return None
        return self.graph.nodes[self._call_stack[-1]]

    def frame_runtime(self, frame_id: int):
        """
        Get FrameRuntime for a live frame.
        """
        return self._frames.get(frame_id)
