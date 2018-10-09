# -*- coding: utf-8 -*-

"""A command line interface for BioKEEN."""

import importlib
import json
import os
import sys

import click

from bio2bel.constants import get_global_connection
from bio2bel.manager.bel_manager import BELManagerMixin
from biokeen.constants import DATA_DIR
from pybel import from_pickle, to_pickle
from pykeen import run
from .build import ensure_drugbank, ensure_hippie, iterate_source_paths
from .convert import to_keen_file

CONFIG_PATH = os.path.join(DATA_DIR, "configuration.json")
EMOJI = '🍩'

connection_option = click.option(
    '-c',
    '--connection',
    default=get_global_connection(),
    show_default=True,
    help='Bio2BEL database connection string',
)


@click.group()
def main():  # noqa: D401
    """A command line interface for BioKEEN."""


@main.command()
@click.option('-c', '--config', type=click.File(), default=CONFIG_PATH, show_default=True)
@click.option('-o', '--output-directory', help='Output directory', type=click.Path(file_okay=False, dir_okay=True))
@click.option('-p', '--training-path', help='Data path', type=click.Path(file_okay=True, dir_okay=False))
def keen(config, output_directory, training_path):
    """Run KEEN."""
    config = json.load(config)

    run(
        config,
        output_directory=output_directory,
        training_path=training_path,
    )


@main.command()
def ls():
    """List built data."""
    for path in iterate_source_paths():
        click.echo(path)


@main.group()
def build():
    """Build Bio2BEL resources."""


@build.command()
@connection_option
def all(connection):
    """Build all resources."""
    click.secho('HIPPIE', fg='cyan', bold=True)
    ensure_hippie(connection)
    click.secho('DrugBank', fg='cyan', bold=True)
    ensure_drugbank(connection)


@build.command()
@connection_option
def hippie(connection):
    """Build HIPPIE."""
    ensure_hippie(connection)


@build.command()
@connection_option
def drugbank(connection):
    """Build DrugBank."""
    ensure_drugbank(connection)


@main.command()
@click.argument("name")
@connection_option
@click.option('-r', '--rebuild', is_flag=True)
def get(name, connection, rebuild):
    """Install, populate, and build Bio2BEL repository."""
    bio2bel_module_name = f"bio2bel_{name}"
    keen_df_path = os.path.join(DATA_DIR, f'{name}.keen.tsv')
    pickle_path = os.path.join(DATA_DIR, f'{name}.bel.pickle')

    if os.path.exists(keen_df_path) and not rebuild:
        click.secho(f'{EMOJI} {bio2bel_module_name} has already been retrieved. See: {keen_df_path}', bold=True)
        sys.exit(0)

    if os.path.exists(pickle_path):
        click.secho(f'{EMOJI} loaded {bio2bel_module_name} pickle: {pickle_path}', bold=True)
        graph = from_pickle(pickle_path)
        to_keen_file(graph, keen_df_path)
        sys.exit(0)

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
    click.secho(f'{EMOJI} generating KEEN for {bio2bel_module_name}', bold=True)
    to_keen_file(graph, keen_df_path)


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
