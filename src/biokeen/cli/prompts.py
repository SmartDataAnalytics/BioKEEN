# -*- coding: utf-8 -*-

"""Prompts for the BioKEEN command line interface."""

import os
import re
from collections import OrderedDict
from typing import Dict, Iterable, Optional

import click

from pykeen.cli.prompt import prompt_config
from pykeen.cli.utils.cli_print_msg_helper import print_section_divider
from pykeen.constants import TRAINING_SET_PATH
from .messages import print_intro, print_welcome_message
from ..constants import ID_TO_DATABASE_MAPPING
from ..content import install_bio2bel_module

__all__ = [
    'prompt_biokeen_config',
]


def prompt_biokeen_config(*, connection: str, rebuild: bool, do_prompt_bio2bel: Optional[bool] = None) -> Dict:
    """Configure experiments."""
    config = OrderedDict()

    # Step 1: Welcome + Intro
    print_welcome_message()
    print_section_divider()
    print_intro()
    print_section_divider()

    # Step 2: Ask for data source
    if do_prompt_bio2bel is None:
        do_prompt_bio2bel = click.confirm('Do you want to use one of the databases provided by BioKEEN?', default=True)
        print_section_divider()

    do_prompt_training = True

    if do_prompt_bio2bel:
        do_prompt_training = False
        config[TRAINING_SET_PATH] = []
        for name in select_bio2bel_repository():
            try:
                path = install_bio2bel_module(name=name, connection=connection, rebuild=rebuild)
            except Exception:
                click.secho(f'failed: {name}', fg='red')
            else:
                if os.path.exists(path):
                    config[TRAINING_SET_PATH].append(f'bio2bel:{name}')
                else:
                    click.secho(f'failed: {name}: {path}', fg='red')

        # TODO replace this with less safe code that assumes everything installs no problemo
        """
        config[TRAINING_SET_PATH] = [
            f'bio2bel:{name}'
            for name in select_bio2bel_repository()
        ]
        """

    print_section_divider()

    return prompt_config(
        config=config,
        show_welcome=False,
        do_prompt_training=do_prompt_training,
    )


def select_bio2bel_repository() -> Iterable[str]:
    """Prompt the user for a Bio2BEL database."""
    click.secho("Current Step: Please select the database(s) you want to train on:", fg='blue')

    number_width = 1 + round(len(ID_TO_DATABASE_MAPPING) / 10)
    for model, model_id in sorted(ID_TO_DATABASE_MAPPING.items()):
        click.echo(f'{model: >{number_width}}: {model_id}')

    while True:
        try:
            user_input = click.prompt('> Please select one or more of the options', value_proc=process_selection)
        except ValueError as e:
            click.secho(str(e), fg='red')
        else:
            return user_input


def process_selection(values: str) -> Iterable[str]:
    for value in re.split(r'\s|,', values):
        value = value.strip()
        if not value:
            continue

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
