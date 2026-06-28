"""This module contains the set of custom FlaUI's exceptions.

The Python exceptions mirror the C# ``FlaUI.Core.Exceptions`` inheritance tree so that
``except`` clauses behave the same way they do in FlaUI:

.. code-block:: text

    Exception
    └── FlaUIException
        ├── ElementNotAvailableException
        ├── ElementNotEnabledException
        ├── ElementNotFound                 (Python-only convenience)
        ├── MethodNotSupportedException
        ├── NoClickablePointException
        ├── NotSupportedByFrameworkException
        ├── ProxyAssemblyNotLoadedException
        ├── NotCachedException
        │   ├── PatternNotCachedException    (carries ``pattern_id``)
        │   └── PropertyNotCachedException   (carries ``property_id``)
        └── NotSupportedException
            ├── PatternNotSupportedException  (carries ``pattern_id``)
            └── PropertyNotSupportedException (carries ``property_id``)

``SystemException`` is intentionally kept outside the ``FlaUIException`` tree: it wraps a raw
``System.Exception`` that is not a FlaUI error, so ``except FlaUIException`` should not catch it.
"""

from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Iterator, Optional, Union

from FlaUI.Core.Exceptions import (  # type: ignore
    ElementNotAvailableException as CSharpElementNotAvailableException,
    ElementNotEnabledException as CSharpElementNotEnabledException,
    FlaUIException as CSharpFlaUIException,
    MethodNotSupportedException as CSharpMethodNotSupportedException,
    NoClickablePointException as CSharpNoClickablePointException,
    NotCachedException as CSharpNotCachedException,
    NotSupportedByFrameworkException as CSharpNotSupportedByFrameworkException,
    NotSupportedException as CSharpNotSupportedException,
    PatternNotCachedException as CSharpPatternNotCachedException,
    PatternNotSupportedException as CSharpPatternNotSupportedException,
    PropertyNotCachedException as CSharpPropertyNotCachedException,
    PropertyNotSupportedException as CSharpPropertyNotSupportedException,
    ProxyAssemblyNotLoadedException as CSharpProxyAssemblyNotLoadedException,
)
import System  # type: ignore


# ---------------------------------------------------------------------------
# Exception hierarchy (mirrors FlaUI.Core.Exceptions)
# ---------------------------------------------------------------------------
class FlaUIException(Exception):
    """Base exception for all FlaUI errors (mirrors C# ``FlaUI.Core.Exceptions.FlaUIException``)."""

    def __init__(self, message: str = "FlaUI exception") -> None:
        """Store the message and initialise the base ``Exception``.

        :param message: Human-readable error description.
        """
        self.message = message
        super().__init__(self.message)


class ElementNotAvailableException(FlaUIException):
    """Python equivalent of C# ``ElementNotAvailableException`` (the element is no longer available)."""

    def __init__(self, message: str = "Element not available") -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        """
        super().__init__(message)


class ElementNotEnabledException(FlaUIException):
    """Python equivalent of C# ``ElementNotEnabledException`` (the element is disabled)."""

    def __init__(self, message: str = "Element not enabled") -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        """
        super().__init__(message)


class MethodNotSupportedException(FlaUIException):
    """Python equivalent of C# ``MethodNotSupportedException`` (the method is not supported)."""

    def __init__(self, message: str = "Method not supported") -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        """
        super().__init__(message)


class NoClickablePointException(FlaUIException):
    """Python equivalent of C# ``NoClickablePointException`` (no clickable point was found)."""

    def __init__(self, message: str = "No clickable point") -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        """
        super().__init__(message)


class NotSupportedByFrameworkException(FlaUIException):
    """Python equivalent of C# ``NotSupportedByFrameworkException`` (unsupported by the chosen UIA framework)."""

    def __init__(self, message: str = "Not supported by framework") -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        """
        super().__init__(message)


class ProxyAssemblyNotLoadedException(FlaUIException):
    """Python equivalent of C# ``ProxyAssemblyNotLoadedException`` (the UIA proxy assembly is missing)."""

    def __init__(self, message: str = "Proxy assembly not loaded") -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        """
        super().__init__(message)


class NotCachedException(FlaUIException):
    """Python equivalent of C# ``NotCachedException`` (requested data was not in the cache)."""

    def __init__(self, message: str = "Not cached") -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        """
        super().__init__(message)


class NotSupportedException(FlaUIException):
    """Python equivalent of C# ``NotSupportedException`` (the requested feature is not supported)."""

    def __init__(self, message: str = "Not supported") -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        """
        super().__init__(message)


class PropertyNotSupportedException(NotSupportedException):
    """Python equivalent of C# ``PropertyNotSupportedException``; carries the offending ``property_id``."""

    def __init__(
        self, message: str = "The requested property is not supported", property_id: Optional[Any] = None
    ) -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        :param property_id: The C# ``PropertyId`` that is not supported, when known.
        """
        self.property_id = property_id
        super().__init__(message)


class PatternNotSupportedException(NotSupportedException):
    """Python equivalent of C# ``PatternNotSupportedException``; carries the offending ``pattern_id``."""

    def __init__(
        self, message: str = "The requested pattern is not supported", pattern_id: Optional[Any] = None
    ) -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        :param pattern_id: The C# ``PatternId`` that is not supported, when known.
        """
        self.pattern_id = pattern_id
        super().__init__(message)


class PropertyNotCachedException(NotCachedException):
    """Python equivalent of C# ``PropertyNotCachedException``; carries the offending ``property_id``."""

    def __init__(
        self, message: str = "The requested property is not cached", property_id: Optional[Any] = None
    ) -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        :param property_id: The C# ``PropertyId`` that is not cached, when known.
        """
        self.property_id = property_id
        super().__init__(message)


class PatternNotCachedException(NotCachedException):
    """Python equivalent of C# ``PatternNotCachedException``; carries the offending ``pattern_id``."""

    def __init__(self, message: str = "The requested pattern is not cached", pattern_id: Optional[Any] = None) -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        :param pattern_id: The C# ``PatternId`` that is not cached, when known.
        """
        self.pattern_id = pattern_id
        super().__init__(message)


class ElementNotFound(FlaUIException):
    """Raised when an automation element cannot be found (Python-only convenience, no C# equivalent)."""

    def __init__(self, message: str = "Element not found") -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        """
        super().__init__(message)


class SystemException(Exception):
    """Wraps a raw C# ``System.Exception`` that is not a FlaUI error (kept outside the ``FlaUIException`` tree)."""

    def __init__(self, message: str = "System exception") -> None:
        """Initialise the exception.

        :param message: Human-readable error description.
        """
        self.message = message
        super().__init__(self.message)


# ---------------------------------------------------------------------------
# C# -> Python translation decorator
# ---------------------------------------------------------------------------
def _identifier(csharp_exception: Any, attr: str) -> Optional[Any]:
    """Return the ``PropertyId``/``PatternId`` carried by a C# exception, if present.

    :param csharp_exception: The caught C# exception instance.
    :param attr: The C# attribute name to read (``"Property"`` or ``"Pattern"``).
    :return: The C# identifier object, or ``None`` when it is absent.
    """
    return getattr(csharp_exception, attr, None)


def _raise_translated(exception: Any, context: str) -> None:
    """Re-raise a caught C# exception as its Python equivalent from the FlaUI hierarchy.

    Checks are ordered most-derived first so a subclass is never swallowed by its base. The C#
    exception text is preserved and the offending ``PropertyId``/``PatternId`` is forwarded where
    available. This is the shared translation core used by both :func:`handle_csharp_exceptions`
    and :func:`translate_exceptions`.

    :param exception: The caught C# (``System.Exception``-derived) exception instance.
    :param context: Human-readable description of the failing operation (e.g. a method name).
    :raises PropertyNotSupportedException: When the C# call raises ``PropertyNotSupportedException``.
    :raises PatternNotSupportedException: When the C# call raises ``PatternNotSupportedException``.
    :raises NotSupportedException: When the C# call raises ``NotSupportedException``.
    :raises PropertyNotCachedException: When the C# call raises ``PropertyNotCachedException``.
    :raises PatternNotCachedException: When the C# call raises ``PatternNotCachedException``.
    :raises NotCachedException: When the C# call raises ``NotCachedException``.
    :raises NotSupportedByFrameworkException: When the C# call raises ``NotSupportedByFrameworkException``.
    :raises ProxyAssemblyNotLoadedException: When the C# call raises ``ProxyAssemblyNotLoadedException``.
    :raises NoClickablePointException: When the C# call raises ``NoClickablePointException``.
    :raises MethodNotSupportedException: When the C# call raises ``MethodNotSupportedException``.
    :raises ElementNotEnabledException: When the C# call raises ``ElementNotEnabledException``.
    :raises ElementNotAvailableException: When the C# call raises ``ElementNotAvailableException``.
    :raises FlaUIException: When the C# call raises any other ``FlaUIException``.
    :raises SystemException: When the C# call raises a non-FlaUI ``System.Exception``.
    """
    e = exception
    if isinstance(e, CSharpPropertyNotSupportedException):
        raise PropertyNotSupportedException(
            f"The property or method '{context}' is not supported: {e}",
            property_id=_identifier(e, "Property"),
        ) from e
    if isinstance(e, CSharpPatternNotSupportedException):
        raise PatternNotSupportedException(
            f"The pattern for '{context}' is not supported: {e}",
            pattern_id=_identifier(e, "Pattern"),
        ) from e
    if isinstance(e, CSharpNotSupportedException):
        raise NotSupportedException(f"The property or method '{context}' is not supported: {e}") from e
    if isinstance(e, CSharpPropertyNotCachedException):
        raise PropertyNotCachedException(
            f"The property or method '{context}' is not cached: {e}",
            property_id=_identifier(e, "Property"),
        ) from e
    if isinstance(e, CSharpPatternNotCachedException):
        raise PatternNotCachedException(
            f"The pattern for '{context}' is not cached: {e}",
            pattern_id=_identifier(e, "Pattern"),
        ) from e
    if isinstance(e, CSharpNotCachedException):
        raise NotCachedException(f"The property or method '{context}' is not cached: {e}") from e
    if isinstance(e, CSharpNotSupportedByFrameworkException):
        raise NotSupportedByFrameworkException(
            f"The property or method '{context}' is not supported by the framework: {e}"
        ) from e
    if isinstance(e, CSharpProxyAssemblyNotLoadedException):
        raise ProxyAssemblyNotLoadedException(
            f"The property or method '{context}' caused a ProxyAssemblyNotLoadedException: {e}"
        ) from e
    if isinstance(e, CSharpNoClickablePointException):
        raise NoClickablePointException(
            f"The property or method '{context}' caused a NoClickablePointException: {e}"
        ) from e
    if isinstance(e, CSharpMethodNotSupportedException):
        raise MethodNotSupportedException(f"The property or method '{context}' is not supported: {e}") from e
    if isinstance(e, CSharpElementNotEnabledException):
        raise ElementNotEnabledException(
            f"The property or method '{context}' caused an ElementNotEnabledException: {e}"
        ) from e
    if isinstance(e, CSharpElementNotAvailableException):
        raise ElementNotAvailableException(
            f"The property or method '{context}' caused an ElementNotAvailableException: {e}"
        ) from e
    if isinstance(e, CSharpFlaUIException):
        raise FlaUIException(f"The property or method '{context}' caused a FlaUIException: {e}") from e
    raise SystemException(f"The property or method '{context}' caused an exception: {e}") from e


@contextmanager
def _translate_exceptions_block(context: str) -> Iterator[None]:
    """Context manager body that translates C# exceptions raised inside the block.

    :param context: Human-readable description used in the raised exception message.
    :yield: None.
    """
    try:
        yield
    except System.Exception as e:  # noqa: F821 - C# base exception type
        _raise_translated(e, context)


def translate_exceptions(arg: Union[Callable[..., Any], str, None] = None) -> Any:
    """Translate C# FlaUI exceptions into their Python equivalents (decorator or context manager).

    This is the Pythonic, user-facing entry point. It supports three forms:

    .. code-block:: python

        # 1. Bare decorator
        @translate_exceptions
        def do_thing(): ...

        # 2. Decorator with a context label
        @translate_exceptions("clicking the button")
        def click(): ...

        # 3. Context manager around an arbitrary block of interop code
        with translate_exceptions("reading the value"):
            value = element.raw_element.Value

    :param arg: When used as a bare decorator this is the wrapped function; when used as a context
        manager (or parametrized decorator) this is an optional human-readable context label.
    :return: The wrapped function (bare-decorator form) or a context manager that doubles as a
        parametrized decorator.
    """
    if callable(arg):
        # Form 1: used directly as @translate_exceptions
        return handle_csharp_exceptions(arg)
    # Forms 2 & 3: the contextmanager result is also usable as a decorator (ContextDecorator).
    return _translate_exceptions_block(arg or "operation")


def handle_csharp_exceptions(func):
    """Wrap a function so C# FlaUI exceptions are re-raised as their Python equivalents.

    The C# exception text is preserved in the re-raised message, and the offending
    ``PropertyId``/``PatternId`` is forwarded to ``property_id``/``pattern_id`` where available.
    ``except`` clauses are ordered most-derived first so subclasses are not swallowed by their base.

    :param func: The function to wrap.
    :return: The wrapped function.
    :raises PropertyNotSupportedException: When the C# call raises ``PropertyNotSupportedException``.
    :raises PatternNotSupportedException: When the C# call raises ``PatternNotSupportedException``.
    :raises NotSupportedException: When the C# call raises ``NotSupportedException``.
    :raises PropertyNotCachedException: When the C# call raises ``PropertyNotCachedException``.
    :raises PatternNotCachedException: When the C# call raises ``PatternNotCachedException``.
    :raises NotCachedException: When the C# call raises ``NotCachedException``.
    :raises NotSupportedByFrameworkException: When the C# call raises ``NotSupportedByFrameworkException``.
    :raises ProxyAssemblyNotLoadedException: When the C# call raises ``ProxyAssemblyNotLoadedException``.
    :raises NoClickablePointException: When the C# call raises ``NoClickablePointException``.
    :raises MethodNotSupportedException: When the C# call raises ``MethodNotSupportedException``.
    :raises ElementNotEnabledException: When the C# call raises ``ElementNotEnabledException``.
    :raises ElementNotAvailableException: When the C# call raises ``ElementNotAvailableException``.
    :raises FlaUIException: When the C# call raises any other ``FlaUIException``.
    :raises SystemException: When the C# call raises a non-FlaUI ``System.Exception``.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        """Invoke ``func`` and translate any C# exception into its Python equivalent."""
        try:
            return func(*args, **kwargs)
        except System.Exception as e:
            _raise_translated(e, func.__name__)

    return wrapper
