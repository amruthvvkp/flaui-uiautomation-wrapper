"""Wrapper for a UI Automation pattern identifier (``FlaUI.Core.Identifiers.PatternId``)."""

from typing import Optional

from flaui.core.identifiers.identifier_base import IdentifierBase
from flaui.core.identifiers.property_id import PropertyId


class PatternId(IdentifierBase):
    """Python wrapper around a C# ``PatternId`` (identifies an automation pattern)."""

    @property
    def availability_property(self) -> Optional[PropertyId]:
        """Return the property indicating whether the pattern is available, if any.

        :return: A :class:`PropertyId` wrapping the C# availability property, or ``None`` when the
            pattern declares no availability property.
        """
        raw_property = self.raw.AvailabilityProperty
        return None if raw_property is None else PropertyId(raw=raw_property)
