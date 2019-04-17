# -*- coding: utf-8 -*-

"""Utilities for BioKEEN."""

import importlib
import logging
import os
import sys
from contextlib import redirect_stdout
from typing import Optional, Union

import numpy as np
import pkg_resources

from bio2bel import AbstractManager
from bio2bel.manager.bel_manager import BELManagerMixin
from pybel import from_json_path, from_web, to_json_path
from .constants import EMOJI, biokeen_config
from .convert import to_pykeen_df, to_pykeen_path, to_pykeen_summary_path

_SPECIAL_CASES = {
    'compath': 'compath_resources',
}

logger = logging.getLogger(__name__)


def install_bio2bel_module(name: str, connection: Optional[str] = None, rebuild: bool = False) -> Optional[str]:
    """Install Bio2BEL module.

    :param name: The name of the Bio2BEL module
    :param connection: The optional database connection
    :param rebuild: Should the cache not be used? Defaults to False.
    """
    module_name = _SPECIAL_CASES.get(name, f'bio2bel_{name}')

    pykeen_df_path = os.path.join(biokeen_config.data_directory, f'{name}.{biokeen_config.keen_tsv_ext}')
    pykeen_df_summary_path = os.path.join(biokeen_config.data_directory, f'{name}.keen.summary.json')
    json_path = os.path.join(biokeen_config.data_directory, f'{name}.bel.json')

    if os.path.exists(pykeen_df_path) and not rebuild:
        logger.info(f'{EMOJI} {module_name} has already been retrieved. See: {pykeen_df_path}')
        return pykeen_df_path

    if os.path.exists(json_path) and not rebuild:
        logger.info(f'{EMOJI} loaded {module_name} JSON: {json_path}')
        graph = from_json_path(json_path)
        df = to_pykeen_df(graph)
        to_pykeen_path(df, pykeen_df_path)
        to_pykeen_summary_path(df, pykeen_df_summary_path)
        return pykeen_df_path

    bio2bel_module = ensure_bio2bel_installation(module_name)
    logger.debug(f'{EMOJI} imported {module_name}')

    manager_cls = bio2bel_module.Manager

    if not issubclass(manager_cls, BELManagerMixin):
        version = pkg_resources.get_distribution(module_name).version
        logger.warning(f'{EMOJI} {module_name} v{version} does not produce BEL')
        sys.exit(1)

    manager = manager_cls(connection=connection)

    if issubclass(manager_cls, AbstractManager):
        if not manager.is_populated():
            logger.info(f'{EMOJI} populating {module_name}')
            manager.populate()
        else:
            logger.debug(f'{EMOJI} {module_name} has already been populated')

    logger.debug(f'{EMOJI} generating BEL for {module_name}')
    graph = manager.to_bel()

    logger.debug(f'Summary: {graph.number_of_nodes()} nodes / {graph.number_of_edges()} edges')
    to_json_path(graph, json_path, indent=2)

    logger.debug(f'{EMOJI} generating PyKEEN TSV for {module_name}')
    df = to_pykeen_df(graph)
    to_pykeen_summary_path(df, pykeen_df_summary_path)
    success = to_pykeen_path(df, pykeen_df_path)

    if success:
        logger.debug(f'{EMOJI} wrote PyKEEN TSV to {pykeen_df_path}')
        return pykeen_df_path

    logger.warning(f'{EMOJI} no statements generated')


def ensure_bio2bel_installation(package: str):
    """Import a package, or install it."""
    try:
        b_module = importlib.import_module(package)

    except ImportError:
        logger.info(f'{EMOJI} pip install {package}')
        # Install this package using pip
        # https://stackoverflow.com/questions/12332975/installing-python-module-within-code
        from pip._internal import main as pip_main

        with redirect_stdout(sys.stderr):
            pip_exit_code = pip_main(['install', '-q', package])  # -q means quiet

        if 0 != pip_exit_code:  # command failed
            logger.warning(f'{EMOJI} could not find {package} on PyPI. Try installing from GitHub with:')
            name = package.split("_")[-1]
            logger.warning(f'\n   pip install git+https://github.com/bio2bel/{name}.git\n')
            sys.exit(1)

        try:
            return importlib.import_module(package)
        except ImportError:
            logger.exception(f'{EMOJI} failed to import {package}')
            sys.exit(1)

    return b_module


BIO2BEL_PREFIX = 'bio2bel'


def handle_bio2bel(module_name: str) -> np.ndarray:
    """Load a Bio2BEL repository.

    :param module_name: The name of the bio2bel repository (with no prefix)
    """
    path = install_bio2bel_module(module_name)
    return np.loadtxt(
        fname=path,
        dtype=str,
        comments='@Comment@ Subject Predicate Object',
        delimiter='\t',
    )


def handle_bel_commons(network_id: Union[int, str], host: Optional[str] = None) -> np.ndarray:
    """Load a BEL document from BEL Commons.

    :param network_id: The network identifier in BEL Commons
    :param host: The host for BEL Commons. Defaults to the Fraunhofer SCAI public instance.
    """
    graph = from_web(int(network_id), host=host)
    df = to_pykeen_df(graph)
    return df.to_numpy()
