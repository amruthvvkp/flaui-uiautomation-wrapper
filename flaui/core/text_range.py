"""Python wrapper for the C# ``FlaUI.Core.ITextRange`` type.

A text range represents a contiguous span of text within a control that supports the Text pattern.
The wrapper mirrors ``ITextRange`` one-to-one; the native object stays reachable via
:attr:`TextRange.raw_text_range`.
"""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from flaui.core.definitions import TextPatternRangeEndpoint, TextUnit
from flaui.lib.exceptions import ElementNotFound, handle_csharp_exceptions
from flaui.lib.system.drawing import Rectangle


class TextRange(BaseModel):
    """Represents a span of text within a Text-pattern control (mirrors C# ``ITextRange``)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw_text_range: Any = Field(..., description="The underlying C# ITextRange object")

    @field_validator("raw_text_range")
    def validate_text_range_exists(cls, v: Any, info: ValidationInfo) -> Any:
        """Validate the native text range exists.

        :param v: Raw C# ITextRange object.
        :param info: Pydantic validation info.
        :raises ElementNotFound: If the text range is ``None``.
        :return: The validated raw text range.
        """
        if v is None:
            raise ElementNotFound("Text range does not exist")
        return v

    @handle_csharp_exceptions
    def add_to_selection(self) -> None:
        """Add the text range to the current selection."""
        self.raw_text_range.AddToSelection()

    @handle_csharp_exceptions
    def clone(self) -> "TextRange":
        """Return a copy of the text range.

        :return: A new :class:`TextRange` with the same span.
        """
        return TextRange(raw_text_range=self.raw_text_range.Clone())

    @handle_csharp_exceptions
    def compare(self, range: "TextRange") -> bool:
        """Return whether this range spans the same text as another.

        :param range: The range to compare against.
        :return: ``True`` if both ranges have identical endpoints.
        """
        return self.raw_text_range.Compare(range.raw_text_range)

    @handle_csharp_exceptions
    def compare_endpoints(
        self,
        src_endpoint: TextPatternRangeEndpoint,
        target_range: "TextRange",
        target_endpoint: TextPatternRangeEndpoint,
    ) -> int:
        """Compare an endpoint of this range with an endpoint of another range.

        :param src_endpoint: The endpoint of this range to compare.
        :param target_range: The other range.
        :param target_endpoint: The endpoint of the other range to compare.
        :return: Negative, zero, or positive if this endpoint is before, at, or after the target.
        """
        return self.raw_text_range.CompareEndpoints(
            src_endpoint.value, target_range.raw_text_range, target_endpoint.value
        )

    @handle_csharp_exceptions
    def expand_to_enclosing_unit(self, text_unit: TextUnit) -> None:
        """Expand the range to the nearest enclosing unit boundary.

        :param text_unit: The text unit to expand to.
        """
        self.raw_text_range.ExpandToEnclosingUnit(text_unit.value)

    @handle_csharp_exceptions
    def find_attribute(self, attribute: Any, value: Any, backward: bool) -> Optional["TextRange"]:
        """Find a sub-range with the given text attribute value.

        :param attribute: The C# ``TextAttributeId`` to search for.
        :param value: The attribute value to match.
        :param backward: Search backward from the end when ``True``.
        :return: The matching :class:`TextRange`, or ``None`` if not found.
        """
        result = self.raw_text_range.FindAttribute(attribute, value, backward)
        return None if result is None else TextRange(raw_text_range=result)

    @handle_csharp_exceptions
    def find_text(self, text: str, backward: bool, ignore_case: bool) -> Optional["TextRange"]:
        """Find a sub-range containing the given text.

        :param text: The text to find.
        :param backward: Search backward from the end when ``True``.
        :param ignore_case: Match case-insensitively when ``True``.
        :return: The matching :class:`TextRange`, or ``None`` if not found.
        """
        result = self.raw_text_range.FindText(text, backward, ignore_case)
        return None if result is None else TextRange(raw_text_range=result)

    @handle_csharp_exceptions
    def get_attribute_value(self, attribute: Any) -> Any:
        """Return the value of a text attribute over the range.

        :param attribute: The C# ``TextAttributeId`` to read.
        :return: The attribute value (a mixed value if the attribute varies over the range).
        """
        return self.raw_text_range.GetAttributeValue(attribute)

    @handle_csharp_exceptions
    def get_bounding_rectangles(self) -> List[Rectangle]:
        """Return the bounding rectangles of the text in the range.

        :return: A list of :class:`Rectangle` for each line in the range.
        """
        return [Rectangle(raw_value=_) for _ in self.raw_text_range.GetBoundingRectangles()]

    @handle_csharp_exceptions
    def get_children(self) -> List[Any]:
        """Return the embedded child elements within the range.

        :return: A list of child automation elements.
        """
        from flaui.core.automation_elements import AutomationElement

        return [AutomationElement(raw_element=_) for _ in self.raw_text_range.GetChildren()]

    @handle_csharp_exceptions
    def get_enclosing_element(self) -> Any:
        """Return the innermost element that encloses the range.

        :return: The enclosing :class:`~flaui.core.automation_elements.AutomationElement`.
        """
        from flaui.core.automation_elements import AutomationElement

        return AutomationElement(raw_element=self.raw_text_range.GetEnclosingElement())

    @handle_csharp_exceptions
    def get_text(self, max_length: int = -1) -> str:
        """Return the plain text of the range.

        :param max_length: Maximum number of characters to return, or ``-1`` for all.
        :return: The text of the range.
        """
        return self.raw_text_range.GetText(max_length)

    @handle_csharp_exceptions
    def move(self, unit: TextUnit, count: int) -> int:
        """Move the range by the given number of text units.

        :param unit: The unit to move by.
        :param count: The number of units to move (negative moves backward).
        :return: The number of units actually moved.
        """
        return self.raw_text_range.Move(unit.value, count)

    @handle_csharp_exceptions
    def move_endpoint_by_range(
        self,
        src_endpoint: TextPatternRangeEndpoint,
        target_range: "TextRange",
        target_endpoint: TextPatternRangeEndpoint,
    ) -> None:
        """Move an endpoint of this range to an endpoint of another range.

        :param src_endpoint: The endpoint of this range to move.
        :param target_range: The range whose endpoint becomes the new position.
        :param target_endpoint: The endpoint of the target range to move to.
        """
        self.raw_text_range.MoveEndpointByRange(src_endpoint.value, target_range.raw_text_range, target_endpoint.value)

    @handle_csharp_exceptions
    def move_endpoint_by_unit(self, endpoint: TextPatternRangeEndpoint, unit: TextUnit, count: int) -> int:
        """Move an endpoint of the range by the given number of text units.

        :param endpoint: The endpoint to move.
        :param unit: The unit to move by.
        :param count: The number of units to move (negative moves backward).
        :return: The number of units actually moved.
        """
        return self.raw_text_range.MoveEndpointByUnit(endpoint.value, unit.value, count)

    @handle_csharp_exceptions
    def remove_from_selection(self) -> None:
        """Remove the text range from the current selection."""
        self.raw_text_range.RemoveFromSelection()

    @handle_csharp_exceptions
    def scroll_into_view(self, align_to_top: bool) -> None:
        """Scroll the range into view.

        :param align_to_top: Align the range to the top of the viewport when ``True``.
        """
        self.raw_text_range.ScrollIntoView(align_to_top)

    @handle_csharp_exceptions
    def select(self) -> None:
        """Select the text range, replacing any existing selection."""
        self.raw_text_range.Select()
