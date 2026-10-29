"""Laying buttons out in rows."""

from typing import List, Sequence, TypeVar

T = TypeVar("T")


def button_rows(buttons: Sequence[T], cols: int) -> List[List[T]]:
    """Pack `buttons` into rows of `cols`, in order; the last row may be shorter."""
    cols = max(1, int(cols))
    return [list(buttons[i : i + cols]) for i in range(0, len(buttons), cols)]
