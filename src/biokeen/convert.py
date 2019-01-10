# -*- coding: utf-8 -*-

"""Conversion utilities for BEL."""

import logging
from pathlib import Path
from typing import Optional, TextIO, Tuple, Union

import pandas as pd
from tqdm import tqdm

from pybel import BELGraph
from pybel.constants import (
    ACTIVITY, ASSOCIATION, CORRELATIVE_RELATIONS, DECREASES, DIRECTLY_DECREASES, DIRECTLY_INCREASES, EQUIVALENT_TO,
    HAS_COMPONENT, INCREASES, IS_A, MODIFIER, OBJECT, PART_OF, REGULATES, RELATION, TRANSCRIBED_TO, TRANSLATED_TO,
)
from pybel.dsl import Abundance, BaseEntity, MicroRna, NamedComplexAbundance, Pathology, Protein
from pybel.typing import EdgeData
from .converters import Converter, SimpleConverter, SimpleTypedPredicate, TypedConverter

__all__ = [
    'to_pykeen_file',
    'to_pykeen_df',
    'get_triple',
]

logger = logging.getLogger(__name__)


def to_pykeen_file(graph: BELGraph, file: Union[str, Path, TextIO]) -> None:
    """Write the relationships in the BEL graph to a KEEN TSV file."""
    df = to_pykeen_df(graph)
    df.to_csv(file, sep='\t', index=None, header=None)


def to_pykeen_df(graph: BELGraph) -> pd.DataFrame:
    """Get a pandas DataFrame representing the triples."""
    triples = (
        get_triple(graph, u, v, key)
        for u, v, key in tqdm(graph.edges(keys=True), total=graph.number_of_edges(), desc='preparing TSV')
    )

    # clean duplicates and Nones
    triples = list(sorted({triple for triple in triples if triple is not None}))

    return pd.DataFrame(triples, columns=['subject', 'predicate', 'object'])


def get_triple(graph: BELGraph, u: BaseEntity, v: BaseEntity, key: str) -> Optional[Tuple[str, str, str]]:  # noqa: C901
    """Get the triples' strings that should be written to the file."""
    data = graph[u][v][key]

    # order is important

    converters = [
        ComplexHasComponentConverter,
        PartOfComplexConverter,
        RegulatesActivityConverter,
        DirectlyDecreasesExpressionConverter,
        TranscriptionConverter,
        TranscriptionConverter,
        IsAConverter,
        EquivalenceConverter,
        CorrelationConverter,
        AssociationConverter,
        DrugIndicationConverter,
        DrugSideEffectConverter,
        DecreasesConverter,
    ]

    for converter in converters:
        if converter.predicate(u, v, key, data):
            return converter.convert(u, v, key, data)

    logger.info(f'unhandled: {graph.edge_to_bel(u, v, data)}')
    return None


class _ConvertOnRelation(Converter):
    relation = ...

    @classmethod
    def predicate(cls, u, v, key, edge_data):
        """Test a BEL edge has a given relation."""
        return edge_data[RELATION] == cls.relation


class PartOfComplexConverter(SimpleTypedPredicate, SimpleConverter):
    """Converts BEL statements like ``p(X) partOf complex(Y)``."""
    subject_type = Protein
    relation = PART_OF
    object_type = NamedComplexAbundance
    target_relation = 'partOf'


class ComplexHasComponentConverter(SimpleTypedPredicate):
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


class _BoringConvertOnRelation(_ConvertOnRelation):
    relation = ...
    target_relation = ...

    @classmethod
    def convert(cls, u: BaseEntity, v: BaseEntity, key: str, data: EdgeData):
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            cls.target_relation,
            f'{v.namespace}:{v.identifier or v.name}',
        )


class TranslationConverter(_BoringConvertOnRelation):
    relation = TRANSLATED_TO
    target_relation = 'ribosomallyTranslatesTo'


class TranscriptionConverter(_BoringConvertOnRelation):
    relation = TRANSCRIBED_TO
    target_relation = 'ribosomallyTranslatesTo'


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


class DecreasesConverter(SimpleConverter):
    """Converts BEL statements like ``?(X) -| ?(Y)``."""

    @staticmethod
    def predicate(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return edge_data[RELATION] == DECREASES


class RegulatesAmountConverter(TypedConverter):
    relation = REGULATES
    target_relation = 'regulatesAmountOf'

    @classmethod
    def predicate(cls, u, v, key, data):
        object_modifier = data.get(OBJECT)
        return data[RELATION] == cls.relation and (not object_modifier or not object_modifier.get(MODIFIER))


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


class RegulatesExpressionConverter(TypedConverter, SimpleTypedPredicate):
    """Converts BEL statements like ``m(X) reg r(Y)``."""
    subject_type = MicroRna
    relation = REGULATES
    object_type = RuntimeError
    target_relation = 'regulatesExpressionOf'


class IncreasesExpressionConverter(RegulatesExpressionConverter):
    """Converts BEL statements like ``m(X) -> r(Y)``."""
    relation = INCREASES
    target_relation = 'increasesExpressionOf'


class DirectlyIncreasesExpressionConverter(RegulatesExpressionConverter):
    """Converts BEL statements like ``m(X) => r(Y)``."""
    relation = DIRECTLY_INCREASES
    target_relation = 'increasesExpressionOf'


class DecreasesExpressionConverter(RegulatesExpressionConverter):
    """Converts BEL statements like ``m(X) -| r(Y)``."""
    relation = DIRECTLY_DECREASES
    target_relation = 'repressesExpressionOf'


class DirectlyDecreasesExpressionConverter(RegulatesExpressionConverter):
    """Converts BEL statements like ``m(X) =| r(Y)``."""
    relation = DIRECTLY_DECREASES
    target_relation = 'repressesExpressionOf'
