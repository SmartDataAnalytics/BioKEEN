# -*- coding: utf-8 -*-

"""CLI utils."""

from collections import OrderedDict
from typing import Dict

import click

from biokeen.cli_utils.bio_2_bel_utils import install_bio2bel_module
from biokeen.cli_utils.cli_print_msg_helper import print_intro, print_welcome_message
from biokeen.cli_utils.cli_query_helper import select_database
from pykeen.cli.prompt import (
    prompt_device, prompt_embedding_model, prompt_evaluation_parameters, prompt_execution_parameters,
    prompt_output_directory, prompt_random_seed, prompt_training_file,
)
from pykeen.cli.utils.cli_print_msg_helper import print_execution_mode_message, print_section_divider
from pykeen.constants import EXECUTION_MODE, HPO_MODE, TRAINING_MODE, TRAINING_SET_PATH

__all__ = [
    'prompt_config',
]


def prompt_config(connection: str, rebuild: bool) -> Dict:
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
