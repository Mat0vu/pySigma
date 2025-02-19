from dataclasses import dataclass, field
from typing import Optional, List, Type
from uuid import UUID
from enum import Enum, auto
import sigma.exceptions as sigma_exceptions
from sigma.exceptions import (
    SigmaRuleLocation,
)


class EnumLowercaseStringMixin:
    def __str__(self) -> str:
        return self.name.lower()


class SigmaStatus(EnumLowercaseStringMixin, Enum):
    UNSUPPORTED = auto()
    DEPRECATED = auto()
    EXPERIMENTAL = auto()
    TEST = auto()
    STABLE = auto()

    def __eq__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value == other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __ge__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value >= other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __gt__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value > other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __ne__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value != other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __le__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value <= other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __lt__(self, other):
        if isinstance(other, SigmaStatus):
            return self.value < other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaStatus", source=other)

    def __hash__(self):
        return self.value.__hash__()


class SigmaLevel(EnumLowercaseStringMixin, Enum):
    INFORMATIONAL = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

    def __eq__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value == other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __ge__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value >= other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __gt__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value > other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __ne__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value != other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __le__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value <= other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __lt__(self, other):
        if isinstance(other, SigmaLevel):
            return self.value < other.value

        raise sigma_exceptions.SigmaTypeError("Must be a SigmaLevel", source=other)

    def __hash__(self):
        return self.value.__hash__()


class SigmaRelatedType(EnumLowercaseStringMixin, Enum):
    CORRELATION = auto()
    DERIVED = auto()
    MERGED = auto()
    OBSOLETE = auto()
    RENAMED = auto()
    SIMILAR = auto()


@dataclass
class SigmaRelatedItem:
    id: UUID
    type: SigmaRelatedType

    @classmethod
    def from_dict(cls, value: dict) -> "SigmaRelatedItem":
        """Returns Related item from dict with fields."""
        try:
            id = UUID(value["id"])
        except ValueError:
            raise sigma_exceptions.SigmaRelatedError(f"Sigma related identifier must be an UUID")

        try:
            type = SigmaRelatedType[value["type"].upper()]
        except:
            raise sigma_exceptions.SigmaRelatedError(
                f"{value['type']} is not a Sigma related valid type"
            )

        return cls(
            id,
            type,
        )


@dataclass
class SigmaRelated:
    related: List[Type[SigmaRelatedItem]]

    @classmethod
    def from_dict(cls, val: list) -> "SigmaRelated":
        """Returns Related object from dict with fields."""

        list_ret = []
        for v in val:
            if not "id" in v.keys():
                raise sigma_exceptions.SigmaRelatedError("Sigma related must have an id field")
            elif not "type" in v.keys():
                raise sigma_exceptions.SigmaRelatedError("Sigma related must have a type field")
            else:
                list_ret.append(SigmaRelatedItem.from_dict(v))  # should rise the SigmaRelatedError

        return cls(list_ret)


@dataclass(unsafe_hash=True)
class SigmaRuleTag:
    namespace: str
    name: str
    source: Optional[SigmaRuleLocation] = field(default=None, compare=False)

    @classmethod
    def from_str(cls, tag: str, source: Optional[SigmaRuleLocation] = None) -> "SigmaRuleTag":
        """Build SigmaRuleTag class from plain text tag string."""
        try:
            ns, n = tag.split(".", maxsplit=1)
        except ValueError:
            raise sigma_exceptions.SigmaValueError(
                "Sigma tag must start with namespace separated with dot from remaining tag."
            )
        return cls(ns, n)

    def __str__(self) -> str:
        return f"{self.namespace}.{self.name}"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return other == self.__str__()
        elif type(self) is type(other):
            return self.name == other.name and self.namespace == other.namespace
