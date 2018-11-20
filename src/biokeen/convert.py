# -*- coding: utf-8 -*-

"""Conversion utilities for BEL."""

import logging
from pathlib import Path
from typing import TextIO, Tuple, Union

import pandas as pd
from tqdm import tqdm

from pybel import BELGraph
from pybel.constants import (
    ACTIVITY, DIRECTLY_DECREASES, EQUIVALENT_TO, HAS_COMPONENT, IS_A, MODIFIER, OBJECT, PART_OF, REGULATES, RELATION,
    TRANSCRIBED_TO, TRANSLATED_TO,
)
from pybel.dsl import BaseEntity, MicroRna, Rna

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


def get_triple(graph: BELGraph, u: BaseEntity, v: BaseEntity, key: str) -> Tuple[str, str, str]:
    """Get the triples' strings that should be written to the file."""
    data = graph[u][v][key]
    relation = data[RELATION]
    # subject_modifier = data.get(SUBJECT)
    object_modifier = data.get(OBJECT)

    if relation in HAS_COMPONENT:
        return (
            f'{v.namespace}:{v.identifier or v.name}',
            'partOf',
            str(u),
        )

    elif relation == PART_OF:
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            'partOf',
            f'{v.namespace}:{v.identifier or v.name}',
        )

    elif relation == REGULATES and object_modifier and object_modifier.get(MODIFIER) == ACTIVITY:
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            'activityDirectlyNegativelyRegulatesActivityOf',
            f'{v.namespace}:{v.identifier or v.name}',
        )

    elif relation == DIRECTLY_DECREASES and isinstance(u, MicroRna) and isinstance(v, Rna):
        # this is a mircoRNA regulation
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            'repressesExpressionOf',
            f'{v.namespace}:{v.identifier or v.name}',
        )

    elif relation == TRANSLATED_TO:
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            'ribosomallyTranslatesTo',
            f'{v.namespace}:{v.identifier or v.name}',
        )

    elif relation == TRANSCRIBED_TO:
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            'transcribedTo',
            f'{v.namespace}:{v.identifier or v.name}',
        )

    elif relation == IS_A:
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            'isA',
            f'{v.namespace}:{v.identifier or v.name}',
        )

    elif relation == EQUIVALENT_TO:
        return (
            f'{u.namespace}:{u.identifier or u.name}',
            'equivalentTo',
            f'{v.namespace}:{v.identifier or v.name}',
        )

    else:
        logger.info(f'unhandled: {graph.edge_to_bel(u, v, data)}')
