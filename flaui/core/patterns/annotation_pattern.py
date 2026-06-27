"""Wrapper for the UI Automation Annotation pattern (``IAnnotationPattern``)."""

from __future__ import annotations

from flaui.core.automation_elements import AutomationProperty
from flaui.core.patterns.pattern_base import PatternBase
from flaui.lib.exceptions import handle_csharp_exceptions


class AnnotationPattern(PatternBase):
    """Represents the UI Automation Annotation pattern for annotation elements (comments, etc.)."""

    @property
    @handle_csharp_exceptions
    def annotation_type(self) -> AutomationProperty:
        """Return the annotation type identifier.

        :return: An :class:`AutomationProperty` wrapping the ``AnnotationType`` value.
        """
        return AutomationProperty(raw_property=self.raw_pattern.AnnotationType)

    @property
    @handle_csharp_exceptions
    def annotation_type_name(self) -> AutomationProperty:
        """Return the localized annotation type name.

        :return: An :class:`AutomationProperty` wrapping the type name.
        """
        return AutomationProperty(raw_property=self.raw_pattern.AnnotationTypeName)

    @property
    @handle_csharp_exceptions
    def author(self) -> AutomationProperty:
        """Return the author of the annotation.

        :return: An :class:`AutomationProperty` wrapping the author.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Author)

    @property
    @handle_csharp_exceptions
    def date_time(self) -> AutomationProperty:
        """Return the date and time the annotation was created.

        :return: An :class:`AutomationProperty` wrapping the date/time string.
        """
        return AutomationProperty(raw_property=self.raw_pattern.DateTime)

    @property
    @handle_csharp_exceptions
    def target(self) -> AutomationProperty:
        """Return the element the annotation targets.

        :return: An :class:`AutomationProperty` wrapping the target element.
        """
        return AutomationProperty(raw_property=self.raw_pattern.Target)
