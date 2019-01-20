# -*- coding: utf-8 -*-

"""BioKEEN's command line interface helper."""

import click


def print_welcome_message():
    """Print welcome message."""
    click.secho('#################################################')
    click.secho("#\t\tWelcome to " + click.style("BioKEEN", bold=True) + "\t\t#")
    click.secho('#################################################')


def print_intro():
    """Print intro."""
    click.secho("This interface will assist you to configure your experiment.")
    click.secho("")
    click.secho(
        "BioKEEN can be run in two modes: \n"
        "1.) Training mode: BioKEEN trains a model based on a set of user-defined hyper-parameters.\n"
        "2.) Hyper-parameter optimization mode: "
        "Apply Random Search to determine the most appropriate set of hyper-parameter values"
    )
