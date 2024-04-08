"""This module contains the set of custom FlaUi's exceptions."""

class FlaUiException(ValueError):
    """Base class for exceptions in this module."""

    pass


class ElementNotFoundError(FlaUiException):
    """Exception raised when an element is not found."""

    pass
