def diff_locals(prev: dict, curr: dict) -> dict:
    """
    Compute variable changes between two locals snapshots.
    Returns {var: (old, new)}
    """
    changes = {}

    for key, value in curr.items():
        if prev.get(key) != value:
            changes[key] = (prev.get(key), value)

    return changes
