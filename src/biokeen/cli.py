# -*- coding: utf-8 -*-

"""A command line interface for BioKEEN."""

import sys

import click
from bio2bel.constants import get_global_connection

from .build import ensure_drugbank, ensure_hippie, iterate_source_paths
from .convert import to_keen_file


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

    b_name = f"bio2bel_{name}"

    try:
        b_module = importlib.import_module(b_name)
    except ImportError:
        import pip
        pip.main(["install", b_name])
        try:
            b_module = importlib.import_module(b_name)
        except ImportError:
            sys.exit(1)
    manager = b_module.Manager()
    if not manager.is_populated():
        manager.populate()

    graph = manager.to_bel()
    to_keen_file(graph, file)
