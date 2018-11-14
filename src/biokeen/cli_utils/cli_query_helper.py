# -*- coding: utf-8 -*-

"""Helper script to query parameters needed in training mode."""

import click

from biokeen.constants import ID_TO_DATABASE_MAPPING


def select_database():
    """Select database."""
    click.secho("Current Step: Please select the database you want to train on:", fg='blue')
    for model, model_id in sorted(ID_TO_DATABASE_MAPPING.items()):
        click.echo(f'{model}: {model_id}')

    ids = list(ID_TO_DATABASE_MAPPING.keys())

    while True:
        user_input = click.prompt('> Please select one of the options: ', type=int)

        if user_input in ID_TO_DATABASE_MAPPING:
            return ID_TO_DATABASE_MAPPING[user_input]

        elif user_input in ID_TO_DATABASE_MAPPING.values():
            return user_input

        click.echo(
            f"Invalid input, please type in a number between 1 and {len(ID_TO_DATABASE_MAPPING)} indicating the "
            f"database id.\nFor example, type {ids[0]} to select {ID_TO_DATABASE_MAPPING[ids[0]]} and press enter\n"
        )
