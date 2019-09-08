# -*- coding: utf-8 -*-

"""Input and output for BEL conversion."""

import json
import logging
from collections import Counter
from typing import Dict, TextIO, Union

import itertools as itt
import pandas as pd
from networkx.utils import open_file
from pybel import BELGraph
from pybel.io.tsv import get_triples

__all__ = [
    'to_pykeen_path',
    'to_pykeen_df',
    'get_pykeen_summary',
    'to_pykeen_summary_path',
]

logger = logging.getLogger(__name__)


def to_pykeen_path(df: pd.DataFrame, path: str) -> bool:
    """Write the relationships in the BEL graph to a KEEN TSV file.

    If you have a BEL graph, first do:

    >>> from biokeen.convert import to_pykeen_df, to_pykeen_path
    >>> graph = ...  # Something from PyBEL
    >>> df = to_pykeen_df(graph)
    >>> to_pykeen_path(df, 'graph.keen.tsv')
    """
    if len(df.index) == 0:
        return False
    df.to_csv(path, sep='\t', index=None, header=None)
    return True


def get_pykeen_summary(df: pd.DataFrame) -> Dict:
    """Summarize a KEEN dataframe."""
    entity_count = Counter(itt.chain(df[df.columns[0]], df[df.columns[2]]))
    return {
        'namespaces': Counter(
            element.split(':')[0]
            for element in itt.chain(df[df.columns[0]], df[df.columns[2]])
        ),
        'entities': len(entity_count),
        'relations': len(df.index),
    }


@open_file(1, mode='w')
def to_pykeen_summary_path(df: pd.DataFrame, file: Union[str, TextIO], indent=2, **kwargs):
    """Write the summary of a KEEN dataframe to a file."""
    json.dump(get_pykeen_summary(df), file, indent=indent, **kwargs)


def to_pykeen_df(graph: BELGraph, use_tqdm: bool = True) -> pd.DataFrame:
    """Get a DataFrame representing the triples."""
    triples = get_triples(graph=graph, use_tqdm=use_tqdm)
    return pd.DataFrame(triples, columns=['subject', 'predicate', 'object'])
