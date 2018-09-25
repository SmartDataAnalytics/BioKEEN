# -*- coding: utf-8 -*-

"""CLI for BioKEEN."""

import click

from bio2bel.constants import get_global_connection
from .sources import ensure_drugbank, ensure_hippie


@click.group()
def main():
    """BioKEEN Command Line Interface."""


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
