# -*- coding: utf-8 -*-

"""A command line interface for BioKEEN."""

import json
import logging
from collections import OrderedDict

import click

import pykeen
from bio2bel.constants import get_global_connection
from biokeen.build import ensure_compath, ensure_drugbank, ensure_hippie, iterate_source_paths
from biokeen.cli_utils.bio_2_bel_utils import install_bio2bel_module
from biokeen.cli_utils.cli_print_msg_helper import print_intro, print_welcome_message
from biokeen.cli_utils.cli_query_helper import select_database
from pykeen.cli import (
    prompt_device, prompt_embedding_model, prompt_evaluation_parameters, prompt_execution_parameters,
    prompt_output_directory, prompt_random_seed, prompt_training_file,
)
from pykeen.constants import EXECUTION_MODE, HPO_MODE, TRAINING_MODE, TRAINING_SET_PATH
from pykeen.predict import start_predictions_pipeline
from pykeen.utilities.cli_utils.cli_print_msg_helper import (
    print_execution_mode_message, print_section_divider, )

connection_option = click.option(
    '-c',
    '--connection',
    default=get_global_connection(),
    show_default=True,
    help='Bio2BEL database connection string',
)


def prompt_config(connection, rebuild):
    """Configure experiments."""
    config = OrderedDict()

    # Step 1: Welcome + Intro
    print_welcome_message()
    print_section_divider()
    print_intro()
    print_section_divider()

    # Step 2: Ask for data source
    is_biokeen_data_required = click.confirm('Do you want to use one of the databases provided by BioKEEN?',
                                             default=True)
    print_section_divider()

    if is_biokeen_data_required:
        database_name = select_database()
        config[TRAINING_SET_PATH] = install_bio2bel_module(name=database_name, connection=connection, rebuild=rebuild)
    else:
        prompt_training_file(config)

    print_section_divider()

    # Step 3: Ask for execution mode
    print_execution_mode_message()
    config[EXECUTION_MODE] = (
        TRAINING_MODE
        if click.confirm('Do you have hyper-parameters? If not, will begin hyper-parameter search.', default=False) else
        HPO_MODE
    )
    print_section_divider()

    # Step 4: Ask for model
    model_name = prompt_embedding_model()
    print_section_divider()

    # Step 5: Query parameters depending on the selected execution mode
    prompt_execution_parameters(config=config, model_name=model_name)
    print_section_divider()

    prompt_evaluation_parameters(config)

    print_section_divider()

    # Step 6: Please select a random seed
    prompt_random_seed(config)
    print_section_divider()

    # Step 7: Query device to train on
    prompt_device(config)
    print_section_divider()

    # Step 8: Define output directory
    prompt_output_directory(config)
    print_section_divider()

    return config


@click.group()
def main():  # noqa: D401
    """A command line interface for BioKEEN."""


@main.command()
@connection_option
@click.option('-f', '--config', type=click.File())
@click.option('-r', '--rebuild', is_flag=True)
def start(config, connection, rebuild):
    """Start BioKEEN pipeline."""
    if config is None:
        config = prompt_config(connection, rebuild)
    else:
        config = json.load(config)

    pykeen.run(config)


@main.command()
@click.option('-m', '--model_direc', type=click.Path(file_okay=False, dir_okay=True))
@click.option('-d', '--data_direc', type=click.Path(file_okay=False, dir_okay=True))
def predict(model_direc: str, data_direc: str):
    """Use a trained model to make predictions."""
    start_predictions_pipeline(model_direc, data_direc)


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
def get(names, connection, rebuild, verbose):
    """Install, populate, and build Bio2BEL repository."""
    if verbose:
        logging.basicConfig(level=logging.INFO)
    for name in names:
        install_bio2bel_module(name, connection, rebuild)


@data.group()
def build():
    """Build suggested Bio2BEL resources."""


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


@build.command()
def compath():
    """Build ComPath."""
    ensure_compath()
