"""Fire-and-forget background tasks."""

import asyncio
from collections.abc import Coroutine

# asyncio keeps only a weak reference to a task, so one nobody else holds can be
# garbage-collected mid-flight. Hold each one here until it finishes.
_background_tasks: set = set()


def spawn(coro: Coroutine) -> asyncio.Task:
    """Run `coro` in the background, keeping it alive until it completes."""
    task = asyncio.create_task(coro)
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    return task
