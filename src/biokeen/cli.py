# -*- coding: utf-8 -*-

"""A command line interface for BioKEEN."""

import json
from collections import OrderedDict

import click
from bio2bel.constants import get_global_connection
from pykeen import run
from pykeen.cli import prompt_config, _configure_evaluation_specific_parameters, training_file_prompt, \
    execution_mode_prompt, model_selection_prompt, execution_mode_specific_prompt, device_prompt, output_direc_prompt
from pykeen.constants import TRAINING_SET_PATH, EXECUTION_MODE
from pykeen.utilities.cli_utils.cli_print_msg_helper import print_section_divider, print_training_set_message

from biokeen.cli_utils.bio_2_bel_utils import install_bio2bel_module
from biokeen.cli_utils.cli_print_msg_helper import print_welcome_message, print_intro
from biokeen.cli_utils.cli_query_helper import ask_for_data_source, select_database
from biokeen.constants import CONFIG_PATH
from .build import ensure_drugbank, ensure_hippie, iterate_source_paths

connection_option = click.option(
    '-c',
    '--connection',
    default=get_global_connection(),
    show_default=True,
    help='Bio2BEL database connection string',
)


def prompt_config():
    """

    :return:
    """
    config = OrderedDict()

    # Step 1: Welcome + Intro
    print_welcome_message()
    print_section_divider()
    print_intro()
    print_section_divider()

    # Step 2: Ask for data source
    is_biokeen_data_required = ask_for_data_source()

    if is_biokeen_data_required:
        database_name = select_database()
        config[TRAINING_SET_PATH] = install_bio2bel_module(name=database_name)
    else:
        print_training_set_message()
        config[TRAINING_SET_PATH] = training_file_prompt(config)

    print_section_divider()

    # Step 3: Ask for execution mode
    config = execution_mode_prompt(config=config)
    print_section_divider()

    # Step 4: Ask for model
    model_name = model_selection_prompt()
    print_section_divider()

    # Step 5: Query parameters depending on the selected execution mode
    config = execution_mode_specific_prompt(config=config, model_name=model_name)
    print_section_divider()

    config.update(_configure_evaluation_specific_parameters(config[EXECUTION_MODE]))

    print_section_divider()

    # Step 7: Query device to train on
    config = device_prompt(config=config)
    print_section_divider()

    # Step 8: Define output directory
    config = output_direc_prompt(config=config)
    print_section_divider()

    return config


@click.group()
# @click.command()
# @click.option('-c', '--config', type=click.File(), help='A BioKEEN JSON configuration file')
def main():  # noqa: D401
    """A command line interface for BioKEEN."""



@main.command()
@click.option('-c', '--config', type=click.File(), default=CONFIG_PATH, show_default=True)
@click.option('-o', '--output-directory', help='Output directory', type=click.Path(file_okay=False, dir_okay=True))
@click.option('-p', '--training-path', help='Data path', type=click.Path(file_okay=True, dir_okay=False))
def pykeen(config, output_directory, training_path):
    """Run PyKEEN."""
    config = json.load(config)

    start(
        config,
        output_directory=output_directory,
        training_path=training_path,
    )


@main.command()
def ls():
    """List built data."""
    for path in iterate_source_paths():
        click.echo(path)

@main.command()
def start():
    """Start BioKEEN pipeline."""

    config = prompt_config()

    start(config)



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
    install_bio2bel_module(name, connection, rebuild)
