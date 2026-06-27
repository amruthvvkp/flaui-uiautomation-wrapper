"""Base wrapper for FlaUI C# automation identifiers (``FlaUI.Core.Identifiers.IdentifierBase``)."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo


class IdentifierBase(BaseModel):
    """Thin Python wrapper around a C# FlaUI identifier.

    The wrapper holds the underlying C# identifier instance and exposes its native ``Id`` and
    ``Name`` Pythonically. Equality and hashing are based on the id, mirroring the C# behaviour, so
    wrapped identifiers can be compared and used as dictionary keys. The wrapper deliberately does
    not re-register identifiers in Python: the ids come straight from the C# registry to avoid drift.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw: Any = Field(..., description="The underlying C# identifier instance (PropertyId/EventId/...).")

    @field_validator("raw")
    @classmethod
    def validate_raw(cls, v: Any, info: ValidationInfo) -> Any:
        """Reject a missing C# identifier reference.

        :param v: The candidate C# identifier.
        :param info: Pydantic validation context.
        :return: The validated C# identifier.
        :raises ValueError: If the identifier reference is ``None``.
        """
        if v is None:
            raise ValueError("raw identifier must not be None")
        return v

    @property
    def id(self) -> int:
        """Return the native identifier id.

        :return: The integer id assigned by the UI Automation framework.
        """
        return self.raw.Id

    @property
    def name(self) -> str:
        """Return the readable identifier name.

        :return: The human-readable identifier name.
        """
        return self.raw.Name

    def __eq__(self, other: object) -> bool:
        """Return whether two identifiers share the same id (mirrors C# ``IEquatable``).

        :param other: The object to compare against.
        :return: ``True`` when both are identifiers with the same id.
        """
        if isinstance(other, IdentifierBase):
            return self.id == other.id
        return NotImplemented

    def __hash__(self) -> int:
        """Hash by id, matching C# ``GetHashCode``.

        :return: The identifier id used as the hash.
        """
        return self.id

    def __repr__(self) -> str:
        """Return ``'Name [#Id]'`` like the C# ``ToString()``.

        :return: A readable representation of the identifier.
        """
        return f"{self.name} [#{self.id}]"
