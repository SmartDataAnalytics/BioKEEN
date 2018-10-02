# -*- coding: utf-8 -*-

"""A command line interface for BioKEEN."""

import sys

import click

from bio2bel.constants import get_global_connection
from bio2bel.manager.bel_manager import BELManagerMixin
from .build import ensure_drugbank, ensure_hippie, iterate_source_paths
from .convert import to_keen_file

EMOJI = '🍩'


@click.group()
def main():
    """A command line interface for BioKEEN."""


@main.command()
def ls():
    """List built data."""
    for path in iterate_source_paths():
        click.echo(path)


@main.group()
def build():
    """Build Bio2BEL resources."""


connection_option = click.option(
    '-c',
    '--connection',
    default=get_global_connection(),
    show_default=True,
    help='Database connection string.',
)


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
@click.option("-f", "--file", type=click.File("w"), default=sys.stdout)
@click.argument("name")
def get(name, file):
    """Install, populate, and build Bio2BEL repository."""
    import importlib

    package = f"bio2bel_{name}"

    try:
        b_module = importlib.import_module(package)
    except ImportError:
        click.secho(f'{EMOJI} pip install {package}', bold=True)
        # Install this package using pip
        # https://stackoverflow.com/questions/12332975/installing-python-module-within-code
        from pip._internal import main as pip_main
        pip_main(['install', package])

        try:
            b_module = importlib.import_module(package)
        except ImportError:
            click.secho(f'{EMOJI} failed to import {package}', bold=True)
            sys.exit(1)
    else:
        click.secho(f'{EMOJI} imported {package}', bold=True)

    if not issubclass(b_module.Manager, BELManagerMixin):
        click.secho(f'{EMOJI} {package} does not produce BEL', bold=True, fg='red')
        sys.exit(1)

    manager = b_module.Manager()

    if not manager.is_populated():
        click.secho(f'{EMOJI} populating {package}', bold=True)
        manager.populate()
    else:
        click.secho(f'{EMOJI} {package} has already been populated', bold=True)

    graph = manager.to_bel()
    to_keen_file(graph, file)
