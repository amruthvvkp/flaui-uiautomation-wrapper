"""Unit tests for the FlaUI exception hierarchy and the C# -> Python translation decorator."""

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
from FlaUI.Core.Identifiers import PatternId, PropertyId  # type: ignore
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
    translate_exceptions,
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


class TestTranslateExceptions:
    """Validate the public ``translate_exceptions`` decorator/context-manager (GH-73)."""

    def test_bare_decorator(self) -> None:
        """``@translate_exceptions`` (no args) translates C# exceptions and includes the func name."""

        @translate_exceptions
        def boom() -> None:
            """Raise a C# FlaUIException."""
            raise CSharpFlaUIException("kaboom")

        with pytest.raises(FlaUIException) as info:
            boom()
        assert "boom" in str(info.value)
        assert isinstance(info.value.__cause__, CSharpFlaUIException)

    def test_parametrized_decorator_uses_context_label(self) -> None:
        """``@translate_exceptions("label")`` includes the supplied context in the message."""

        @translate_exceptions("doing the thing")
        def boom() -> None:
            """Raise a raw C# System exception."""
            raise System.InvalidOperationException("sys")

        with pytest.raises(SystemException) as info:
            boom()
        assert "doing the thing" in str(info.value)

    def test_context_manager_translates_and_chains(self) -> None:
        """``with translate_exceptions(...)`` translates exceptions raised inside the block."""
        with pytest.raises(SystemException) as info:
            with translate_exceptions("reading a value"):
                raise System.InvalidOperationException("sys")
        assert "reading a value" in str(info.value)
        assert isinstance(info.value.__cause__, System.InvalidOperationException)

    def test_context_manager_preserves_subtype(self) -> None:
        """A C# ``PatternNotSupportedException`` keeps its specific Python type in a block."""
        with pytest.raises(PatternNotSupportedException):
            with translate_exceptions():
                raise CSharpPatternNotSupportedException()

    def test_context_manager_passes_through_on_success(self) -> None:
        """No exception is raised when the block succeeds."""
        with translate_exceptions("ok"):
            value = 1 + 1
        assert value == 2


def _property_id() -> PropertyId:
    """Build a throwaway C# ``PropertyId`` for exceptions that require one.

    :return: A C# ``PropertyId`` instance.
    """
    return PropertyId(30005, "TestProp")


def _pattern_id() -> PatternId:
    """Build a throwaway C# ``PatternId``.

    :return: A C# ``PatternId`` instance.
    """
    return PatternId(10000, "TestPattern", None)


class TestExceptionInstantiation:
    """Instantiate every Python exception class so default-message ``__init__`` paths run."""

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
            PropertyNotSupportedException,
            PatternNotSupportedException,
            PropertyNotCachedException,
            PatternNotCachedException,
            ElementNotFound,
            FlaUIException,
            SystemException,
        ],
    )
    def test_default_message(self, exc: type) -> None:
        """Each exception is constructible with no args and carries a non-empty message."""
        instance = exc()
        assert str(instance)


class TestTranslationLadder:
    """Exercise every branch of the C# -> Python translation ladder (``_raise_translated``)."""

    @pytest.mark.parametrize(
        "cs_factory, expected",
        [
            (lambda: CSharpPropertyNotSupportedException(_property_id()), PropertyNotSupportedException),
            (lambda: CSharpPatternNotSupportedException(), PatternNotSupportedException),
            (lambda: CSharpNotSupportedException(), NotSupportedException),
            (lambda: CSharpPropertyNotCachedException(), PropertyNotCachedException),
            (lambda: CSharpPatternNotCachedException(), PatternNotCachedException),
            (lambda: CSharpNotCachedException(), NotCachedException),
            (lambda: CSharpNotSupportedByFrameworkException(), NotSupportedByFrameworkException),
            (lambda: CSharpProxyAssemblyNotLoadedException(), ProxyAssemblyNotLoadedException),
            (lambda: CSharpNoClickablePointException(), NoClickablePointException),
            (lambda: CSharpMethodNotSupportedException(), MethodNotSupportedException),
            (lambda: CSharpElementNotEnabledException(), ElementNotEnabledException),
            (lambda: CSharpElementNotAvailableException(), ElementNotAvailableException),
            (lambda: CSharpFlaUIException(), FlaUIException),
        ],
    )
    def test_each_csharp_type_maps_to_python_type(self, cs_factory, expected: type) -> None:
        """Each specific C# exception maps to its specific Python type, with the original chained."""
        cs_instance = cs_factory()

        @handle_csharp_exceptions
        def boom() -> None:
            """Raise the parametrized C# exception."""
            raise cs_instance

        with pytest.raises(expected) as info:
            boom()
        # Most-derived match: the raised type is exactly ``expected``, not merely a base.
        assert type(info.value) is expected
        assert info.value.__cause__ is cs_instance

    def test_property_id_forwarded_from_csharp(self) -> None:
        """A C# ``PropertyNotSupportedException`` forwards its ``PropertyId`` to the Python exception."""

        @handle_csharp_exceptions
        def boom() -> None:
            """Raise a C# PropertyNotSupportedException carrying a PropertyId."""
            raise CSharpPropertyNotSupportedException(_property_id())

        with pytest.raises(PropertyNotSupportedException) as info:
            boom()
        assert info.value.property_id is not None

    def test_pattern_id_forwarded_from_csharp(self) -> None:
        """A C# ``PatternNotSupportedException`` forwards its ``PatternId`` to the Python exception."""

        @handle_csharp_exceptions
        def boom() -> None:
            """Raise a C# PatternNotSupportedException carrying a PatternId."""
            raise CSharpPatternNotSupportedException(_pattern_id())

        with pytest.raises(PatternNotSupportedException) as info:
            boom()
        assert info.value.pattern_id is not None
