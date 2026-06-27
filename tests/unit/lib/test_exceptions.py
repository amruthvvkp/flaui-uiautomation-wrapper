"""Unit tests for the FlaUI exception hierarchy and the C# -> Python translation decorator."""

from FlaUI.Core.Exceptions import (  # type: ignore
    FlaUIException as CSharpFlaUIException,
    PatternNotSupportedException as CSharpPatternNotSupportedException,
)
import pytest
import System  # type: ignore

from flaui.lib.exceptions import (
    ElementNotAvailableException,
    ElementNotEnabledException,
    ElementNotFound,
    FlaUIException,
    handle_csharp_exceptions,
    MethodNotSupportedException,
    NoClickablePointException,
    NotCachedException,
    NotSupportedByFrameworkException,
    NotSupportedException,
    PatternNotCachedException,
    PatternNotSupportedException,
    PropertyNotCachedException,
    PropertyNotSupportedException,
    ProxyAssemblyNotLoadedException,
    SystemException,
)


class TestExceptionHierarchy:
    """Validate the Python inheritance tree mirrors ``FlaUI.Core.Exceptions``."""

    @pytest.mark.parametrize(
        "exc",
        [
            ElementNotAvailableException,
            ElementNotEnabledException,
            MethodNotSupportedException,
            NoClickablePointException,
            NotSupportedByFrameworkException,
            ProxyAssemblyNotLoadedException,
            NotCachedException,
            NotSupportedException,
            ElementNotFound,
        ],
    )
    def test_direct_flaui_children(self, exc: type) -> None:
        """Each of these extends ``FlaUIException``."""
        assert issubclass(exc, FlaUIException)

    def test_not_supported_subtree(self) -> None:
        """Property/Pattern not-supported exceptions extend ``NotSupportedException``."""
        assert issubclass(PropertyNotSupportedException, NotSupportedException)
        assert issubclass(PatternNotSupportedException, NotSupportedException)

    def test_not_cached_subtree(self) -> None:
        """Property/Pattern not-cached exceptions extend ``NotCachedException``."""
        assert issubclass(PropertyNotCachedException, NotCachedException)
        assert issubclass(PatternNotCachedException, NotCachedException)

    def test_system_exception_outside_tree(self) -> None:
        """``SystemException`` is a plain ``Exception``, not a ``FlaUIException``."""
        assert not issubclass(SystemException, FlaUIException)
        assert issubclass(SystemException, Exception)

    def test_derived_caught_by_base(self) -> None:
        """A derived exception is catchable via its base class (Pythonic ``except``)."""
        with pytest.raises(FlaUIException):
            raise PropertyNotSupportedException()
        with pytest.raises(NotSupportedException):
            raise PatternNotSupportedException()
        with pytest.raises(NotCachedException):
            raise PropertyNotCachedException()


class TestExceptionMetadata:
    """Validate the identifier metadata carried by the relevant exceptions."""

    def test_property_id_carried(self) -> None:
        """``property_id`` defaults to ``None`` and is stored when provided."""
        sentinel = object()
        assert PropertyNotSupportedException().property_id is None
        assert PropertyNotSupportedException(property_id=sentinel).property_id is sentinel
        assert PropertyNotCachedException(property_id=sentinel).property_id is sentinel

    def test_pattern_id_carried(self) -> None:
        """``pattern_id`` defaults to ``None`` and is stored when provided."""
        sentinel = object()
        assert PatternNotSupportedException().pattern_id is None
        assert PatternNotSupportedException(pattern_id=sentinel).pattern_id is sentinel
        assert PatternNotCachedException(pattern_id=sentinel).pattern_id is sentinel


class TestHandleCsharpExceptions:
    """Validate the ``handle_csharp_exceptions`` translation decorator."""

    def test_translates_flaui_exception_with_chaining(self) -> None:
        """A C# ``FlaUIException`` becomes the Python ``FlaUIException`` with the original as ``__cause__``."""

        @handle_csharp_exceptions
        def boom() -> None:
            """Raise a C# FlaUIException."""
            raise CSharpFlaUIException("kaboom")

        with pytest.raises(FlaUIException) as info:
            boom()
        assert "boom" in str(info.value)  # the wrapped function name is included
        assert isinstance(info.value.__cause__, CSharpFlaUIException)

    def test_pattern_not_supported_not_swallowed_by_base(self) -> None:
        """A C# ``PatternNotSupportedException`` maps to its own type, not the base ``NotSupportedException``."""

        @handle_csharp_exceptions
        def boom() -> None:
            """Raise a C# PatternNotSupportedException."""
            raise CSharpPatternNotSupportedException()

        with pytest.raises(PatternNotSupportedException):
            boom()

    def test_translates_system_exception(self) -> None:
        """A non-FlaUI ``System.Exception`` becomes ``SystemException``."""

        @handle_csharp_exceptions
        def boom() -> None:
            """Raise a raw C# System exception."""
            raise System.InvalidOperationException("sys")

        with pytest.raises(SystemException):
            boom()
