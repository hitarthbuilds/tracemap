import sys
import os


def should_trace(filename: str) -> bool:
    """
    Decide whether a file should be traced.

    Rules:
    - Ignore stdlib
    - Ignore site-packages
    - Trace only user code
    """
    if not filename:
        return False

    filename = os.path.abspath(filename)

    if "site-packages" in filename:
        return False

    if filename.startswith(sys.prefix):
        return False

    return True
