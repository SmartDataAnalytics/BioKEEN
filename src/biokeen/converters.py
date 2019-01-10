# -*- coding: utf-8 -*-

"""Conversion base classes."""

from abc import ABC, abstractmethod
from typing import Tuple

from pybel.constants import RELATION
from pybel.dsl import BaseEntity
from pybel.typing import EdgeData

__all__ = [
    'Converter',
    'SimpleConverter',
    'TypedConverter',
    'SimpleTypedPredicate',
]


class Converter(ABC):
    """A condition and converter for a BEL edge."""

    @staticmethod
    @abstractmethod
    def predicate(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData) -> bool:
        """Test a BEL edge."""

    @staticmethod
    @abstractmethod
    def convert(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData) -> Tuple[str, str, str]:
        """Convert a BEL edge."""


class SimpleConverter(Converter):
    @classmethod
    def convert(cls, u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            edge_data[RELATION],
            f'{v.namespace}:{v.identifier or v.name}',
        )


class TypedConverter(Converter):
    target_relation = None

    @classmethod
    def convert(cls, u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            cls.target_relation,
            f'{v.namespace}:{v.identifier or v.name}',
        )


class SimpleTypedPredicate(Converter):
    """Finds BEL statements like ``A(X) B C(Y)`` where relation B and types A and C are defined in the class."""

    subject_type = ...
    relation = ...
    object_type = ...

    @classmethod
    def predicate(cls, u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return (
            isinstance(u, cls.subject_type) and
            edge_data[RELATION] == cls.relation and
            isinstance(v, cls.object_type)
        )
