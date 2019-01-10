# -*- coding: utf-8 -*-

"""A command line interface for BioKEEN."""

import json
import logging
from typing import List, Optional, TextIO

import click

import pykeen
from bio2bel.constants import get_global_connection
from biokeen.build import iterate_source_paths
from biokeen.cli_utils.bio_2_bel_utils import install_bio2bel_module
from biokeen.cli_utils.prompt_utils import prompt_config
from pykeen.predict import start_predictions_pipeline

connection_option = click.option(
    '-c',
    '--connection',
    default=get_global_connection(),
    show_default=True,
    help='Bio2BEL database connection string',
)


@click.group()
@click.version_option()
def main():  # noqa: D401
    """A command line interface for BioKEEN."""


@main.command()
@connection_option
@click.option('-f', '--config', type=click.File())
@click.option('-r', '--rebuild', is_flag=True)
def start(config: Optional[TextIO], connection: str, rebuild: bool):
    """Start BioKEEN pipeline."""
    if config is None:
        config = prompt_config(connection, rebuild)
    else:
        config = json.load(config)

    pykeen.run(config)


@main.command()
@click.option('-m', '--model-directory', type=click.Path(file_okay=False, dir_okay=True))
@click.option('-d', '--data-directory', type=click.Path(file_okay=False, dir_okay=True))
def predict(model_directory: str, data_directory: str):
    """Use a trained model to make predictions."""
    start_predictions_pipeline(model_directory, data_directory)


@main.group()
def data():
    """Commands for data acquisition."""


@data.command()
def ls():
    """List built data."""
    for path in iterate_source_paths():
        click.echo(path)


@data.command()
@click.argument('names', nargs=-1)
@connection_option
@click.option('-r', '--rebuild', is_flag=True)
@click.option('-v', '--verbose', is_flag=True)
def get(names: List[str], connection: str, rebuild: bool, verbose: bool):
    """Install, populate, and build Bio2BEL repository."""
    if verbose:
        logging.basicConfig(level=logging.INFO)

    for name in names:
        install_bio2bel_module(name, connection, rebuild)


if __name__ == '__main__':
    main()
