# -*- coding: utf-8 -*-

"""Conversion base classes."""

from abc import ABC, abstractmethod
from typing import Tuple

from pybel.constants import (
    ACTIVITY, ASSOCIATION, CORRELATIVE_RELATIONS, DECREASES, DIRECTLY_DECREASES, DIRECTLY_INCREASES, EQUIVALENT_TO,
    HAS_COMPONENT, INCREASES, IS_A, MODIFIER, OBJECT, PART_OF, REGULATES, RELATION,
)
from pybel.dsl import Abundance, BaseEntity, MicroRna, NamedComplexAbundance, Pathology, Protein, Rna
from pybel.typing import EdgeData


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


class _ConvertOnRelation(Converter):
    relation = ...

    @classmethod
    def predicate(cls, u, v, key, edge_data):
        """Test a BEL edge has a given relation."""
        return edge_data[RELATION] == cls.relation


class PartOfNamedComplexConverter(SimpleTypedPredicate, TypedConverter):
    """Converts BEL statements like ``p(X) partOf complex(Y)``."""
    subject_type = Protein
    relation = PART_OF
    object_type = NamedComplexAbundance
    target_relation = 'partOf'


class NamedComplexHasComponentConverter(SimpleTypedPredicate):
    """Converts BEL statements like ``complex(X) hasComponent p(Y)``."""
    subject_type = NamedComplexAbundance
    relation = HAS_COMPONENT
    object_type = Protein

    @staticmethod
    def convert(u: BaseEntity, v: BaseEntity, key: str, data: EdgeData):
        return (
            f'{v.namespace}:{v.identifier or v.name}',
            'partOf',
            f'{u.namespace}:{u.identifier or u.name}',
        )


'''
class TranslationConverter(TypedConverter):
    relation = TRANSLATED_TO
    target_relation = 'ribosomallyTranslatesTo'


class TranscriptionConverter(TypedConverter):
    relation = TRANSCRIBED_TO
    target_relation = 'ribosomallyTranslatesTo'
'''


class IsAConverter(_ConvertOnRelation):
    relation = IS_A
    target_relation = 'isA'


class EquivalenceConverter(_ConvertOnRelation):
    relation = EQUIVALENT_TO
    target_relation = 'equivalentTo'


class CorrelationConverter(SimpleConverter):
    @staticmethod
    def predicate(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return edge_data[RELATION] in CORRELATIVE_RELATIONS


class AssociationConverter(Converter):
    """Converts BEL statements like ``a(X) -- path(Y)``."""

    @staticmethod
    def predicate(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return edge_data[RELATION] == ASSOCIATION

    @staticmethod
    def convert(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            edge_data.get('association_type', ASSOCIATION),  # allow more specific association to be defined
            f'{v.namespace}:{v.identifier or v.name}',
        )


class DrugEffectConverter(SimpleConverter, SimpleTypedPredicate):
    """Converts BEL statements like ``a(X) ? path(Y)``."""
    subject_type = Abundance
    relation = ...
    object_type = Pathology


class DrugIndicationConverter(DrugEffectConverter):
    """Converts BEL statements like ``a(X) -| path(Y)``."""
    relation = DECREASES


class DrugSideEffectConverter(DrugEffectConverter):
    """Converts BEL statements like ``a(X) -> path(Y)``."""
    relation = INCREASES


class RegulatesAmountConverter(TypedConverter):
    relation = REGULATES
    target_relation = 'regulatesAmountOf'

    @classmethod
    def predicate(cls, u, v, key, data):
        object_modifier = data.get(OBJECT)
        return data[RELATION] == cls.relation and (not object_modifier or not object_modifier.get(MODIFIER))


class IncreasesAmountConverter(RegulatesAmountConverter):
    relation = INCREASES
    target_relation = 'increasesAmountOf'


class DecreasesAmountConverter(RegulatesAmountConverter):
    relation = DECREASES
    target_relation = 'decreasesAmountOf'


class RegulatesActivityConverter(TypedConverter):
    relation = REGULATES
    target_relation = 'activityDirectlyRegulatesActivityOf'

    @classmethod
    def predicate(cls, u, v, key, data):
        object_modifier = data.get(OBJECT)
        return data[RELATION] == cls.relation and object_modifier and object_modifier.get(MODIFIER) == ACTIVITY


class IncreasesActivityConverter(RegulatesActivityConverter):
    relation = INCREASES
    target_relation = 'activityDirectlyPositivelyRegulatesActivityOf'


class DecreasesActivityConverter(RegulatesActivityConverter):
    relation = DECREASES
    target_relation = 'activityDirectlyNegativelyRegulatesActivityOf'


class MiRNARegulatesExpressionConverter(TypedConverter, SimpleTypedPredicate):
    """Converts BEL statements like ``m(X) reg r(Y)``."""
    subject_type = MicroRna
    relation = REGULATES
    object_type = Rna
    target_relation = 'regulatesExpressionOf'


class MiRNAIncreasesExpressionConverter(MiRNARegulatesExpressionConverter):
    """Converts BEL statements like ``m(X) -> r(Y)``."""
    relation = INCREASES
    target_relation = 'increasesExpressionOf'


class MiRNADirectlyIncreasesExpressionConverter(MiRNARegulatesExpressionConverter):
    """Converts BEL statements like ``m(X) => r(Y)``."""
    relation = DIRECTLY_INCREASES
    target_relation = 'increasesExpressionOf'


class MiRNADecreasesExpressionConverter(MiRNARegulatesExpressionConverter):
    """Converts BEL statements like ``m(X) -| r(Y)``."""
    relation = DECREASES
    target_relation = 'repressesExpressionOf'


class MiRNADirectlyDecreasesExpressionConverter(MiRNARegulatesExpressionConverter):
    """Converts BEL statements like ``m(X) =| r(Y)``."""
    relation = DIRECTLY_DECREASES
    target_relation = 'repressesExpressionOf'
