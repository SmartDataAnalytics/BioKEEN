# -*- coding: utf-8 -*-

"""Input and output for BEL conversion."""

import logging
from pathlib import Path
from typing import Optional, TextIO, Tuple, Union

import pandas as pd
from tqdm import tqdm

from pybel import BELGraph
from pybel.dsl import BaseEntity
from .converters import (
    AssociationConverter, CorrelationConverter, DecreasesAmountConverter, DrugIndicationConverter,
    DrugSideEffectConverter, EquivalenceConverter, IncreasesAmountConverter, IsAConverter,
    MiRNADecreasesExpressionConverter, MiRNADirectlyDecreasesExpressionConverter, NamedComplexHasComponentConverter,
    PartOfNamedComplexConverter, RegulatesActivityConverter, RegulatesAmountConverter, PartOfBiologicalProcess
)

__all__ = [
    'to_pykeen_file',
    'to_pykeen_df',
    'get_triple',
]

logger = logging.getLogger(__name__)


def to_pykeen_file(graph: BELGraph, file: Union[str, Path, TextIO]) -> bool:
    """Write the relationships in the BEL graph to a KEEN TSV file."""
    df = to_pykeen_df(graph)

    if len(df.index) == 0:
        return False

    df.to_csv(file, sep='\t', index=None, header=None)
    return True


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
        NamedComplexHasComponentConverter,
        PartOfNamedComplexConverter,
        PartOfBiologicalProcess,
        RegulatesActivityConverter,
        MiRNADecreasesExpressionConverter,
        MiRNADirectlyDecreasesExpressionConverter,
        IsAConverter,
        EquivalenceConverter,
        CorrelationConverter,
        AssociationConverter,
        DrugIndicationConverter,
        DrugSideEffectConverter,
        RegulatesAmountConverter,
        IncreasesAmountConverter,
        DecreasesAmountConverter,
    ]

    for converter in converters:
        if converter.predicate(u, v, key, data):
            return converter.convert(u, v, key, data)

    logger.info(f'unhandled: {graph.edge_to_bel(u, v, data)}')
    return None
