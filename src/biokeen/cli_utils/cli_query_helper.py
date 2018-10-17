# -*- coding: utf-8 -*-

"""Helper script to query parameters needed in training mode."""
import click
from biokeen.constants import ID_TO_DATABASE_MAPPING
from prompt_toolkit import prompt

from pykeen.constants import BINARY_QUESTION_MAPPING


def select_database():
    click.echo('Please select the embedding model you want to train:')
    for model, id in ID_TO_DATABASE_MAPPING.items():
        click.echo("%s: %s" % (model, id))

    ids = list(ID_TO_DATABASE_MAPPING.values())
    available_databases = list(ID_TO_DATABASE_MAPPING.keys())

    while True:
        user_input = prompt('> Please select one of the options: ')

        if user_input not in ids:
            click.echo(
                "Invalid input, please type in a number between %s and %s indicating the database id.\n"
                "For example type %s to select the database %s and press enter" % (
                    available_databases[0], ids[0], ids[0], available_databases[0]))
            click.echo()
        else:
            return ID_TO_DATABASE_MAPPING[user_input]

def ask_for_data_source():
    click.echo('Do you want to you use one of the databases provided by BioKEEN for your experiment?')

    while True:
        user_input = prompt('> Please type \'yes\' or \'no\': ')
        if user_input != 'yes' and user_input != 'no':
            click.echo('Invalid input, please type \'yes\' or \'no\' and press enter.\n'
                       'If you type \'yes\' it means that you want to evaluate your model after it is trained.')
        else:
            return BINARY_QUESTION_MAPPING[user_input]