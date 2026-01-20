from tracemap.graph.node import ExecutionNode
from tracemap.runtime.frame_runtime import FrameRuntime
from tracemap.filters.files import should_trace


class TraceHook:
    """
    sys.settrace adapter.

    Intentionally thin. All logic lives elsewhere.
    """

    __slots__ = ("_ctx",)

    def __init__(self, context):
        self._ctx = context

    def __call__(self, frame, event, arg):
        if event == "call":
            self._on_call(frame)
        elif event == "line":
            self._on_line(frame)
        elif event == "return":
            self._on_return(frame)
        elif event == "exception":
            self._on_exception(frame, arg)
        return self

    # -------------------------
    # Event handlers
    # -------------------------

    def _on_call(self, frame):
        node = ExecutionNode(
            function=frame.f_code.co_name,
            file=frame.f_code.co_filename,
            line_start=frame.f_lineno,
        )
        fr = FrameRuntime(frame, node)
        self._ctx.enter_call(fr)

    def _on_line(self, frame):
        fr = self._ctx.frame_runtime(id(frame))
        if fr:
            fr.on_line()

    def _on_return(self, frame):
        self._ctx.exit_call(id(frame), frame.f_lineno)

    def _on_exception(self, frame, exc):
        node = self._ctx.current_node()
        if node:
            exc_type, exc_val, _ = exc
            node.exception = f"{exc_type.__name__}: {exc_val}"
