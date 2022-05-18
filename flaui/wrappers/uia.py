from abc import ABC


class UIA(ABC):
    """UIAutomation base wrapper

    Abstract Class that works with UIA2 and UIA3.
    """

    def __init__(self, automation: str, timeout: int = 1000) -> None:
        self._automation = None  # TODO Add UIA2, UIA3 switcher here
        self.timeout = timeout
