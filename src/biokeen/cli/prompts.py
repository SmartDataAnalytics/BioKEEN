# -*- coding: utf-8 -*-

"""Prompts for the BioKEEN command line interface."""

from collections import OrderedDict
from typing import Dict, Iterable

import click

from biokeen.constants import ID_TO_DATABASE_MAPPING
from pykeen.cli.prompt import prompt_config
from pykeen.cli.utils.cli_print_msg_helper import print_section_divider
from pykeen.constants import TRAINING_SET_PATH
from .messages import print_intro, print_welcome_message
from ..content import install_bio2bel_module

__all__ = [
    'prompt_biokeen_config',
]


def prompt_biokeen_config(*, connection: str, rebuild: bool) -> Dict:
    """Configure experiments."""
    config = OrderedDict()

    # Step 1: Welcome + Intro
    print_welcome_message()
    print_section_divider()
    print_intro()
    print_section_divider()

    # Step 2: Ask for data source
    do_prompt_bio2bel = click.confirm('Do you want to use one of the databases provided by BioKEEN?', default=True)
    print_section_divider()

    do_prompt_training = True

    if do_prompt_bio2bel:
        do_prompt_training = False
        config[TRAINING_SET_PATH] = [
            install_bio2bel_module(name=name, connection=connection, rebuild=rebuild)
            for name in select_bio2bel_repository()
        ]

    print_section_divider()

    return prompt_config(
        config=config,
        show_welcome=False,
        do_prompt_training=do_prompt_training,
    )


def select_bio2bel_repository() -> Iterable[str]:
    """Prompt the user for a Bio2BEL database."""
    click.secho("Current Step: Please select the database you want to train on:", fg='blue')

    number_width = 1 + round(len(ID_TO_DATABASE_MAPPING) / 10)
    for model, model_id in sorted(ID_TO_DATABASE_MAPPING.items()):
        click.echo(f'{model: >{number_width}}: {model_id}')

    while True:
        try:
            user_input = click.prompt('> Please select one of the options', value_proc=process_selection)
        except ValueError as e:
            click.secho(str(e), fg='red')
        else:
            return user_input


def process_selection(values: str) -> Iterable[str]:
    for value in values.split(' '):
        try:
            value = int(value)
        except ValueError:
            if value not in ID_TO_DATABASE_MAPPING.values():
                raise ValueError(f'{value} is an invalid database')
            yield value
        else:
            if value not in ID_TO_DATABASE_MAPPING:
                raise ValueError(f'{value} is an invalid index')
            yield ID_TO_DATABASE_MAPPING[value]
