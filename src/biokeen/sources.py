# -*- coding: utf-8 -*-

"""Functions for ensuring data sources."""

import logging
import os
from typing import Optional

import bio2bel_drugbank
import bio2bel_hippie
from pybel import from_pickle, to_pickle
from .constants import DATA_DIR
from .convert import to_keen_file

__all__ = [
    'ensure_hippie',
    'ensure_drugbank',
]

logger = logging.getLogger(__name__)

hippie_bel_path = os.path.join(DATA_DIR, 'hippie.bel.pickle')
hippie_keen_path = os.path.join(DATA_DIR, 'hippie.keen.tsv')

drugbank_bel_path = os.path.join(DATA_DIR, 'drugbank.bel.pickle')
drugbank_keen_path = os.path.join(DATA_DIR, 'drugbank.keen.tsv')


def ensure_hippie(connection: Optional[str] = None):
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
    to_keen_file(hippie_graph, hippie_keen_path)


def ensure_drugbank(connection: Optional[str] = None):
    if os.path.exists(drugbank_bel_path):
        drugbank_graph = from_pickle(drugbank_bel_path)
    else:
        drugbank_manager = bio2bel_drugbank.Manager(connection=connection)
        if not drugbank_manager.is_populated():
            drugbank_manager.populate()
        drugbank_graph = drugbank_manager.to_bel()
        to_pickle(drugbank_graph, drugbank_bel_path)

    to_keen_file(drugbank_graph, drugbank_keen_path)
