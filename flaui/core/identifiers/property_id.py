"""Wrapper for a UI Automation property identifier (``FlaUI.Core.Identifiers.PropertyId``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flaui.core.identifiers.identifier_base import IdentifierBase
from flaui.lib.exceptions import handle_csharp_exceptions

if TYPE_CHECKING:
    from flaui.core.condition_factory import PropertyCondition


class PropertyId(IdentifierBase):
    """Python wrapper around a C# ``PropertyId`` (identifies an automation property)."""

    @handle_csharp_exceptions
    def get_condition(self, value: Any) -> PropertyCondition:
        """Build a property condition matching this property against ``value`` (C# ``PropertyId.GetCondition``).

        Python enums (e.g. :class:`~flaui.core.definitions.ControlType`) are unwrapped to their C#
        value, so ``property_id.get_condition(ControlType.Button)`` works like the C# call.

        :param value: The value the property must equal.
        :return: A :class:`~flaui.core.condition_factory.PropertyCondition` usable with ``find_*`` methods.
        """
        from enum import Enum

        from flaui.core.condition_factory import PropertyCondition

        raw_value = value.value if isinstance(value, Enum) else value
        return PropertyCondition(cs_condition=self.raw.GetCondition(raw_value))
