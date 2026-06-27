"""Python wrappers for FlaUI C# automation identifiers.

These thin wrappers expose the C# ``FlaUI.Core.Identifiers`` types (``PropertyId``, ``EventId``,
``PatternId``, ``TextAttributeId``) with Pythonic ``id``/``name`` access, value-equality by id, and
a readable ``repr``. The ids are sourced from the C# registry, so there is no risk of drift.
"""

from flaui.core.identifiers.event_id import EventId
from flaui.core.identifiers.identifier_base import IdentifierBase
from flaui.core.identifiers.pattern_id import PatternId
from flaui.core.identifiers.property_id import PropertyId
from flaui.core.identifiers.text_attribute_id import TextAttributeId

__all__ = [
    "IdentifierBase",
    "PropertyId",
    "EventId",
    "PatternId",
    "TextAttributeId",
]
