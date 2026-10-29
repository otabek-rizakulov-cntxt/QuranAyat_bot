"""What the running app holds once background startup has finished."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AppState:
    """Lives on `app.state.runtime`. Both fields stay None until background
    startup fills them, and the webhook acknowledges updates without
    processing them until it has."""

    bot: Any = None  # telegram.Bot — created in startup so a bad TOKEN can't crash import
    data: Optional[dict] = None  # corpora and inline defaults, parsed in startup
