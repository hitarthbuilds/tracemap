import time
import uuid


class ExecutionNode:
    """
    Represents a single function execution.
    Immutable after closure.
    """

    __slots__ = (
        "id",
        "function",
        "file",
        "line_start",
        "line_end",
        "start_ns",
        "end_ns",
        "locals_diff",
        "exception",
        "children",
    )

    def __init__(self, function: str, file: str, line_start: int):
        self.id = uuid.uuid4().hex[:8]
        self.function = function
        self.file = file
        self.line_start = line_start
        self.line_end = None

        self.start_ns = time.perf_counter_ns()
        self.end_ns = None

        self.locals_diff = {}
        self.exception = None
        self.children = []

    def close(self, line_end: int):
        if self.end_ns is not None:
            return  # defensive: node closes once

        self.line_end = line_end
        self.end_ns = time.perf_counter_ns()

    @property
    def duration_ms(self) -> float:
        if self.end_ns is None:
            return 0.0
        return (self.end_ns - self.start_ns) / 1_000_000
