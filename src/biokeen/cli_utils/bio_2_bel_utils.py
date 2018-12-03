# -*- coding: utf-8 -*-

"""Utilities for BioKEEN."""

import importlib
import os
import sys

import click
import pkg_resources

from bio2bel import AbstractManager
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
        r = pip_main(['install', package])
        if r != 0:  # command failed
            click.secho(f'{EMOJI} could not find {package} on PyPI. Try installing from GitHub with:', bold=True)
            name = package.split("_")[-1]
            click.echo(f'\n   pip install git+https://github.com/bio2bel/{name}.git\n')
            sys.exit(1)

        try:
            return importlib.import_module(package)
        except ImportError:
            click.secho(f'{EMOJI} failed to import {package}', bold=True)
            sys.exit(1)

    return b_module


def install_bio2bel_module(name, connection, rebuild):
    """Install Bio2BEL module."""
    if name == 'compath':  # special case for compath
        module_name = 'compath_resources'
    else:
        module_name = f"bio2bel_{name}"

    pykeen_df_path = os.path.join(DATA_DIR, f'{name}.keen.tsv')
    pickle_path = os.path.join(DATA_DIR, f'{name}.bel.pickle')

    if os.path.exists(pykeen_df_path) and not rebuild:
        click.secho(f'{EMOJI} {module_name} has already been retrieved. See: {pykeen_df_path}', bold=True)
        return pykeen_df_path

    if os.path.exists(pickle_path) and not rebuild:
        click.secho(f'{EMOJI} loaded {module_name} pickle: {pickle_path}', bold=True)
        graph = from_pickle(pickle_path)
        to_pykeen_file(graph, pykeen_df_path)
        return pykeen_df_path

    bio2bel_module = _import_bio2bel_module(module_name)
    click.secho(f'{EMOJI} imported {module_name}', bold=True)

    manager_cls = bio2bel_module.Manager

    if not issubclass(manager_cls, BELManagerMixin):
        version = pkg_resources.get_distribution(module_name).version
        click.secho(f'{EMOJI} {module_name} v{version} does not produce BEL', bold=True, fg='red')
        sys.exit(1)

    manager = manager_cls(connection=connection)

    if issubclass(manager_cls, AbstractManager):
        if not manager.is_populated():
            click.secho(f'{EMOJI} populating {module_name}', bold=True)
            manager.populate()
        else:
            click.secho(f'{EMOJI} {module_name} has already been populated', bold=True)

    click.secho(f'{EMOJI} generating BEL for {module_name}', bold=True)
    graph = manager.to_bel()
    click.echo(f'Summary: {graph.number_of_nodes()} nodes / {graph.number_of_edges()} edges')
    to_pickle(graph, pickle_path)
    click.secho(f'{EMOJI} generating PyKEEN TSV for {module_name}', bold=True)
    to_pykeen_file(graph, pykeen_df_path)
    click.secho(f'{EMOJI} wrote PyKEEN TSV to {pykeen_df_path}', bold=True)

    return pykeen_df_path
