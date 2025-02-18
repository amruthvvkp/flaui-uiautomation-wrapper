"""This module contains the set of custom FlaUi's exceptions."""

from functools import wraps
from typing import Any

from FlaUI.Core.Exceptions import (  # type: ignore
    ElementNotAvailableException as CSharpElementNotAvailableException,
    ElementNotEnabledException as CSharpElementNotEnabledException,
    FlaUIException as CSharpFlaUIException,
    MethodNotSupportedException as CSharpMethodNotSupportedException,
    NoClickablePointException as CSharpNoClickablePointException,
    NotCachedException as CSharpNotCachedException,
    NotSupportedByFrameworkException as CSharpNotSupportedByFrameworkException,
    NotSupportedException as CSharpNotSupportedException,
    PropertyNotCachedException as CSharpPropertyNotCachedException,
    PropertyNotSupportedException as CSharpPropertyNotSupportedException,
    ProxyAssemblyNotLoadedException as CSharpProxyAssemblyNotLoadedException,
)
import System  # type: ignore


def handle_csharp_exceptions(
    func,
):
    """Wraps the function to handle C# FlaUI exceptions and raise the equivalent Python exceptions.

    :param func: The function to wrap.
    :raises ProxyAssemblyNotLoadedException: Raises ProxyAssemblyNotLoadedException if the C# FlaUI exception is raised.
    :raises PropertyNotSupportedException: Raises PropertyNotSupportedException if the C# FlaUI exception is raised.
    :raises PropertyNotCachedException: Raises PropertyNotCachedException if the C# FlaUI exception is raised.
    :raises NotSupportedException: Raises NotSupportedException if the C# FlaUI exception is raised.
    :raises NotSupportedByFrameworkException: Raises NotSupportedByFrameworkException if the C# FlaUI exception is raised.
    :raises NotCachedException: Raises NotCachedException if the C# FlaUI exception is raised.
    :raises NoClickablePointException: Raises NoClickablePointException if the C# FlaUI exception is raised.
    :raises MethodNotSupportedException: Raises MethodNotSupportedException if the C# FlaUI exception is raised.
    :raises FlaUIException: Raises FlaUIException if the C# FlaUI exception is raised.
    :raises ElementNotEnabledException: Raises ElementNotEnabledException if the C# FlaUI exception is raised.
    :raises ElementNotAvailableException: Raises ElementNotAvailableException if the C# FlaUI exception is raised.
    :return: The wrapped function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except CSharpProxyAssemblyNotLoadedException as e:
            raise ProxyAssemblyNotLoadedException(
                f"The property or method '{func.__name__}' caused a ProxyAssemblyNotLoadedException: {e}"
            )
        except CSharpPropertyNotSupportedException as e:
            raise PropertyNotSupportedException(f"The property or method '{func.__name__}' is not supported: {e}")
        except CSharpPropertyNotCachedException as e:
            raise PropertyNotCachedException(f"The property or method '{func.__name__}' is not cached: {e}")
        except CSharpNotSupportedException as e:
            raise NotSupportedException(f"The property or method '{func.__name__}' is not supported: {e}")
        except CSharpNotSupportedByFrameworkException as e:
            raise NotSupportedByFrameworkException(
                f"The property or method '{func.__name__}' is not supported by the framework: {e}"
            )
        except CSharpNotCachedException:
            raise NotCachedException(f"The property or method '{func.__name__}' is not cached.")
        except CSharpNoClickablePointException as e:
            raise NoClickablePointException(
                f"The property or method '{func.__name__}' caused a NoClickablePointException: {e}"
            )
        except CSharpMethodNotSupportedException as e:
            raise MethodNotSupportedException(f"The property or method '{func.__name__}' is not supported.: {e}")
        except CSharpFlaUIException as e:
            raise FlaUIException(f"The property or method '{func.__name__}' caused a FlaUIException: {e}")
        except CSharpElementNotEnabledException as e:
            raise ElementNotEnabledException(
                f"The property or method '{func.__name__}' caused an ElementNotEnabledException: {e}"
            )
        except CSharpElementNotAvailableException as e:
            raise ElementNotAvailableException(
                f"The property or method '{func.__name__}' caused an ElementNotAvailableException: {e}"
            )
        except System.Exception as e:
            raise SystemException(f"The property or method '{func.__name__}' caused an exception: {e}")

    return wrapper


class ProxyAssemblyNotLoadedException(Exception):
    """Raises a Python equivalent exception for ProxyAssemblyNotLoadedException from C# FlaUI."""

    def __init__(self, message="Proxy assembly not loaded") -> None:
        self.message = message
        super().__init__(self.message)


class PropertyNotSupportedException(Exception):
    """Raises a Python equivalent exception for PropertyNotSupportedException from C# FlaUI."""

    def __init__(self, message="Property not supported") -> None:
        self.message = message
        super().__init__(self.message)


class PropertyNotCachedException(Exception):
    """Raises a Python equivalent exception for PropertyNotCachedException from C# FlaUI."""

    def __init__(self, message="Property not cached") -> None:
        self.message = message
        super().__init__(self.message)


class NotSupportedException(Exception):
    """Raises a Python equivalent exception for NotSupportedException from C# FlaUI."""

    def __init__(self, message="Not supported") -> None:
        self.message = message
        super().__init__(self.message)


class NotSupportedByFrameworkException(Exception):
    """Raises a Python equivalent exception for NotSupportedByFrameworkException from C# FlaUI."""

    def __init__(self, message="Not supported by framework") -> None:
        self.message = message
        super().__init__(self.message)


class NotCachedException(Exception):
    """Raises a Python equivalent exception for NotCachedException from C# FlaUI."""

    def __init__(self, message="Not cached") -> None:
        self.message = message
        super().__init__(self.message)


class NoClickablePointException(Exception):
    """Raises a Python equivalent exception for NoClickablePointException from C# FlaUI."""

    def __init__(self, message="No clickable point") -> None:
        self.message = message
        super().__init__(self.message)


class MethodNotSupportedException(Exception):
    """Raises a Python equivalent exception for MethodNotSupportedException from C# FlaUI."""

    def __init__(self, message="Method not supported") -> None:
        self.message = message
        super().__init__(self.message)


class FlaUIException(Exception):
    """Raises a Python equivalent exception for FlaUIException from C# FlaUI."""

    def __init__(self, message="FlaUI exception") -> None:
        self.message = message
        super().__init__(self.message)


class ElementNotEnabledException(Exception):
    """Raises a Python equivalent exception for ElementNotEnabledException from C# FlaUI."""

    def __init__(self, message="Element not enabled") -> None:
        self.message = message
        super().__init__(self.message)


class ElementNotAvailableException(Exception):
    """Raises a Python equivalent exception for ElementNotAvailableException from C# FlaUI."""

    def __init__(self, message="Element not available") -> None:
        self.message = message
        super().__init__(self.message)


class ElementNotFound(Exception):
    """Exception raised when an automation element is not found."""

    def __init__(self, message="Element not found") -> None:
        self.message = message
        super().__init__(self.message)


class SystemException(Exception):
    """Exception raised when an C# system exception is raised."""

    def __init__(self, message="System exception") -> None:
        self.message = message
        super().__init__(self.message)
