# -*- coding: utf-8 -*-

"""A command line interface for BioKEEN.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:
- When you run ``python3 -m biokeen`` python will execute``__main__.py`` as a script. That means there won't be any
  ``biokeen.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``biokeen.__main__`` in ``sys.modules``.
.. seealso:: http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import json
import logging
import os
from typing import List, Optional, TextIO

import click

from bio2bel.constants import get_global_connection
from biokeen.constants import DATA_DIR, iterate_source_paths

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
    """Start the BioKEEN training pipeline."""
    import pykeen

    if config is not None:
        config = json.load(config)
    else:
        from .prompts import prompt_config
        config = prompt_config(connection=connection, rebuild=rebuild)

    pykeen.run(config)


@main.command()
@click.option('-m', '--model-directory', type=click.Path(file_okay=False, dir_okay=True))
@click.option('-d', '--data-directory', type=click.Path(file_okay=False, dir_okay=True))
def predict(model_directory: str, data_directory: str):
    """Use a trained model to make predictions."""
    from pykeen.predict import start_predictions_pipeline
    start_predictions_pipeline(model_directory, data_directory)


@main.group()
def data():
    """Commands for data acquisition."""


@data.command(help=f'Data stored in {DATA_DIR}')
def ls():
    """List built data."""
    for path in iterate_source_paths():
        click.echo(path)


@data.command()
@click.confirmation_option()
def clear():
    """Remove all built data."""
    for path in iterate_source_paths():
        os.remove(path)


@data.command()
@click.argument('names', nargs=-1)
@connection_option
@click.option('-r', '--rebuild', is_flag=True)
@click.option('-v', '--verbose', is_flag=True)
def get(names: List[str], connection: str, rebuild: bool, verbose: bool):
    """Install, populate, and build Bio2BEL repository."""
    if verbose:
        logging.basicConfig(level=logging.INFO)

    from biokeen.content import install_bio2bel_module

    for name in names:
        install_bio2bel_module(name, connection, rebuild)


if __name__ == '__main__':
    main()
