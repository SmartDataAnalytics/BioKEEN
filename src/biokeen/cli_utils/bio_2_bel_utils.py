# -*- coding: utf-8 -*-

"""Utilities for BioKEEN."""

import importlib
import os
import sys

import click

from bio2bel.manager.bel_manager import BELManagerMixin
from biokeen.constants import DATA_DIR, EMOJI
from biokeen.convert import to_pykeen_file
from pybel import from_pickle, to_pickle


def _import_bio2bel_module(package: str):
    """Import a package, or install it."""
    try:
        b_module = importlib.import_module(package)

    except ImportError:
        click.secho(f'{EMOJI} pip install {package}', bold=True)
        # Install this package using pip
        # https://stackoverflow.com/questions/12332975/installing-python-module-within-code
        from pip._internal import main as pip_main
        pip_main(['install', package])

        try:
            return importlib.import_module(package)
        except ImportError:
            click.secho(f'{EMOJI} failed to import {package}', bold=True)
            sys.exit(1)

    return b_module


def install_bio2bel_module(name, connection, rebuild):
    """Install Bio2BEL module."""
    bio2bel_module_name = f"bio2bel_{name}"
    pykeen_df_path = os.path.join(DATA_DIR, f'{name}.keen.tsv')
    pickle_path = os.path.join(DATA_DIR, f'{name}.bel.pickle')

    if os.path.exists(pykeen_df_path) and not rebuild:
        click.secho(f'{EMOJI} {bio2bel_module_name} has already been retrieved. See: {pykeen_df_path}', bold=True)
        return pykeen_df_path

    if os.path.exists(pickle_path):
        click.secho(f'{EMOJI} loaded {bio2bel_module_name} pickle: {pickle_path}', bold=True)
        graph = from_pickle(pickle_path)
        to_pykeen_file(graph, pykeen_df_path)
        return pykeen_df_path

    bio2bel_module = _import_bio2bel_module(bio2bel_module_name)
    click.secho(f'{EMOJI} imported {bio2bel_module_name}', bold=True)

    if not issubclass(bio2bel_module.Manager, BELManagerMixin):
        click.secho(f'{EMOJI} {bio2bel_module_name} does not produce BEL', bold=True, fg='red')
        sys.exit(1)

    manager = bio2bel_module.Manager(connection=connection)

    if not manager.is_populated():
        click.secho(f'{EMOJI} populating {bio2bel_module_name}', bold=True)
        manager.populate()
    else:
        click.secho(f'{EMOJI} {bio2bel_module_name} has already been populated', bold=True)

    click.secho(f'{EMOJI} generating BEL for {bio2bel_module_name}', bold=True)
    graph = manager.to_bel()
    click.echo(f'Summary: {graph.number_of_nodes()} nodes / {graph.number_of_edges()} edges')
    to_pickle(graph, pickle_path)
    click.secho(f'{EMOJI} generating PyKEEN TSV for {bio2bel_module_name}', bold=True)
    to_pykeen_file(graph, pykeen_df_path)

    return pykeen_df_path
