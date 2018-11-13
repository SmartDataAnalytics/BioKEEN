# -*- coding: utf-8 -*-

"""Functions for ensuring data sources."""

import logging
import os
from typing import Iterable, Optional

import numpy as np

from pybel import from_pickle, to_pickle
from .constants import DATA_DIR
from .convert import to_pykeen_file

__all__ = [
    'iterate_source_paths',
    'ensure_hippie',
    'ensure_drugbank',
    'ensure_compath',
]

logger = logging.getLogger(__name__)

hippie_bel_path = os.path.join(DATA_DIR, 'hippie.bel.pickle')
hippie_keen_path = os.path.join(DATA_DIR, 'hippie.keen.tsv')

drugbank_bel_path = os.path.join(DATA_DIR, 'drugbank.bel.pickle')
drugbank_keen_path = os.path.join(DATA_DIR, 'drugbank.keen.tsv')

compath_bel_path = os.path.join(DATA_DIR, 'compath.bel.pickle')
compath_keen_path = os.path.join(DATA_DIR, 'compath.keen.tsv')


def get_full_matrix():
    """Get all built data as a matrix."""
    return np.concatenate([
        np.loadtxt(fname, dtype=str, delimiter='\t')
        for fname in iterate_source_paths()
    ])


def iterate_source_paths() -> Iterable[str]:
    """Iterate over the source paths."""
    for file_name in os.listdir(DATA_DIR):
        if 'keen.tsv' in file_name:
            yield os.path.join(DATA_DIR, file_name)


def ensure_hippie(connection: Optional[str] = None):
    """Ensure the HIPPIE database is built."""
    import bio2bel_hippie

    if os.path.exists(hippie_bel_path):
        logger.info('loading from pickle')
        hippie_graph = from_pickle(hippie_bel_path)
    else:
        logger.info('getting from manager')
        hippie_manager = bio2bel_hippie.Manager(connection=connection)
        if not hippie_manager.is_populated():
            hippie_manager.populate()
        hippie_graph = hippie_manager.to_bel()

        to_pickle(hippie_graph, hippie_bel_path)

    logger.info('outputting')
    to_pykeen_file(hippie_graph, hippie_keen_path)


def ensure_drugbank(connection: Optional[str] = None):
    """Ensure the DrugBank database is built."""
    import bio2bel_drugbank

    if os.path.exists(drugbank_bel_path):
        drugbank_graph = from_pickle(drugbank_bel_path)
    else:
        drugbank_manager = bio2bel_drugbank.Manager(connection=connection)
        if not drugbank_manager.is_populated():
            drugbank_manager.populate()
        drugbank_graph = drugbank_manager.to_bel()
        to_pickle(drugbank_graph, drugbank_bel_path)

    to_pykeen_file(drugbank_graph, drugbank_keen_path)


def ensure_compath():
    """Ensure the ComPath mappings are retrieved."""
    import compath_resources
    graph = compath_resources.get_bel()
    to_pickle(graph, compath_bel_path)
    to_pykeen_file(graph, compath_keen_path)
