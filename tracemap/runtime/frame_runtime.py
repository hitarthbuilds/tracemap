from tracemap.semantics.locals import diff_locals


class FrameRuntime:
    """
    Runtime state for a live Python frame.

    This object exists only while the frame is executing.
    It is the ONLY place where frame-local mutation is tracked.
    """

    __slots__ = (
        "frame_id",
        "frame",
        "node",
        "_prev_locals",
    )

    def __init__(self, frame, node):
        self.frame_id = id(frame)
        self.frame = frame
        self.node = node
        self._prev_locals = dict(frame.f_locals)

    def on_line(self):
        """
        Called on every 'line' trace event.
        Computes variable diffs and attaches them to the node.
        """
        current = dict(self.frame.f_locals)
        changes = diff_locals(self._prev_locals, current)

        if changes:
            self.node.locals_diff.update(changes)

        self._prev_locals = current

    def close(self, line_end: int):
        """
        Finalize the execution node for this frame.
        """
        self.node.close(line_end)
