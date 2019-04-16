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
from click_default_group import DefaultGroup

from bio2bel.constants import get_global_connection
from biokeen.constants import EMOJI, VERSION, biokeen_config
from pykeen.constants import VERSION as PYKEEN_VERSION

connection_option = click.option(
    '-c',
    '--connection',
    default=get_global_connection(),
    show_default=True,
    help='Bio2BEL database connection string',
)


@click.group(cls=DefaultGroup, default_if_no_args=False)
@click.version_option()
def main():  # noqa: D401
    """A command line interface for BioKEEN."""


@main.command()
@connection_option
@click.option('-f', '--config', type=click.File())
@click.option('-r', '--rebuild', is_flag=True)
@click.option('-x', '--no-prompt-bio2bel', is_flag=True)
def start(config: Optional[TextIO], connection: str, rebuild: bool, no_prompt_bio2bel: bool):
    """Start the BioKEEN training pipeline."""
    import pykeen

    if config is not None:
        config = json.load(config)
    else:
        from .prompts import prompt_biokeen_config
        config = prompt_biokeen_config(
            connection=connection,
            rebuild=rebuild,
            do_prompt_bio2bel=(not no_prompt_bio2bel),
        )

    config['pykeen-version'] = PYKEEN_VERSION
    config['biokeen-version'] = VERSION
    pykeen.run(config)


@main.command()
@click.option('-m', '--model-directory', type=click.Path(file_okay=False, dir_okay=True, exists=True), required=True)
@click.option('-d', '--data-directory', type=click.Path(file_okay=False, dir_okay=True, exists=True), required=True)
def predict(model_directory: str, data_directory: str):
    """Use a trained model to make predictions."""
    from pykeen.predict import start_predictions_pipeline
    start_predictions_pipeline(model_directory, data_directory)


@main.group()
def data():
    """Commands for data acquisition."""


@data.command(help=f'Data stored in {biokeen_config.data_directory}')
def ls():
    """List built data."""
    for path in biokeen_config.iterate_source_paths():
        click.echo(path)


@data.command()
@click.confirmation_option()
def clear():
    """Remove all built data."""
    for path in biokeen_config.iterate_source_paths():
        os.remove(path)


@data.command()
@click.argument('names', nargs=-1)
@connection_option
@click.option('-r', '--rebuild', is_flag=True)
@click.option('-v', '--verbose', count=True)
def get(names: List[str], connection: str, rebuild: bool, verbose: bool):
    """Install, populate, and build Bio2BEL repository."""
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    elif verbose == 2:
        logging.basicConfig(level=logging.DEBUG)

    from biokeen.content import install_bio2bel_module

    for name in names:
        click.secho(f'{EMOJI} Getting {name}', fg='cyan')
        install_bio2bel_module(name, connection, rebuild)


if __name__ == '__main__':
    main()
