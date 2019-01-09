# -*- coding: utf-8 -*-

"""Conversion utilities for BEL."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, TextIO, Tuple, Union

import pandas as pd
from tqdm import tqdm

from pybel import BELGraph
from pybel.constants import (
    ACTIVITY, ASSOCIATION, CORRELATIVE_RELATIONS, DECREASES, DIRECTLY_DECREASES, EQUIVALENT_TO, HAS_COMPONENT, IS_A,
    MODIFIER, OBJECT, PART_OF, REGULATES, RELATION, TRANSCRIBED_TO, TRANSLATED_TO,
)
from pybel.dsl import BaseEntity, MicroRna, Rna
from pybel.typing import EdgeData

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
        HasComponentConverter,
        PartOfConverter,
        RegulatesActivityConverter,
        DecreasesExpressionConverter,
        TranscriptionConverter,
        TranscriptionConverter,
        IsAConverter,
        EquivalenceConverter,
        CorrelationConverter,
        AssociationConverter,
        DecreasesConverter,
    ]

    for converter in converters:
        if converter.predicate(u, v, key, data):
            return converter.convert(u, v, key, data)

    logger.info(f'unhandled: {graph.edge_to_bel(u, v, data)}')
    return None


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


class _ConvertOnRelation(Converter):
    relation = ...

    @classmethod
    def predicate(cls, u, v, key, edge_data):
        """Test a BEL edge has a given relation."""
        return edge_data[RELATION] == cls.relation


class HasComponentConverter(_ConvertOnRelation):
    relation = HAS_COMPONENT

    @staticmethod
    def convert(u: BaseEntity, v: BaseEntity, key: str, data: EdgeData):
        return (
            f'{v.namespace}:{v.identifier or v.name}',
            'partOf',
            str(u),
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


class PartOfConverter(_BoringConvertOnRelation):
    relation = PART_OF
    target_relation = 'partOf'


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


class CorrelationConverter(Converter):

    @staticmethod
    def predicate(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return edge_data[RELATION] in CORRELATIVE_RELATIONS

    @staticmethod
    def convert(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            edge_data[RELATION],
            f'{v.namespace}:{v.identifier or v.name}',
        )


class AssociationConverter(Converter):

    @staticmethod
    def predicate(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return edge_data[RELATION] in CORRELATIVE_RELATIONS

    @staticmethod
    def convert(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            edge_data.get('association_type', ASSOCIATION),  # allow more specific association to be defined
            f'{v.namespace}:{v.identifier or v.name}',
        )


class DecreasesConverter(Converter):
    @staticmethod
    def predicate(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return edge_data[RELATION] == DECREASES

    @staticmethod
    def convert(u: BaseEntity, v: BaseEntity, key: str, edge_data: EdgeData):
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            edge_data[RELATION],
            f'{v.namespace}:{v.identifier or v.name}',
        )


class RegulatesActivityConverter(Converter):
    @classmethod
    def predicate(cls, u, v, key, data):
        object_modifier = data.get(OBJECT)
        return data[RELATION] == REGULATES and object_modifier and object_modifier.get(MODIFIER) == ACTIVITY

    @staticmethod
    def convert(u: BaseEntity, v: BaseEntity, key: str, data: EdgeData):
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            'activityDirectlyNegativelyRegulatesActivityOf',
            f'{v.namespace}:{v.identifier or v.name}',
        )


class DecreasesExpressionConverter(Converter):
    @classmethod
    def predicate(cls, u, v, key, data):
        return data[RELATION] == DIRECTLY_DECREASES and isinstance(u, MicroRna) and isinstance(v, Rna)

    @staticmethod
    def convert(u: BaseEntity, v: BaseEntity, key: str, data: EdgeData):
        # this is a mircoRNA regulation
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            'repressesExpressionOf',
            f'{v.namespace}:{v.identifier or v.name}',
        )
