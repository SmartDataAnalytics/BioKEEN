# -*- coding: utf-8 -*-

"""Constants for BioKEEN."""

import os

import easy_config

HERE = os.path.abspath(os.path.dirname(__file__))


class BiokeenConfig(easy_config.EasyConfig):
    """Configuration for BioKEEN."""

    NAME = 'biokeen'
    FILES = [
        os.path.join(os.path.expanduser('~'), '.config', 'biokeen.cfg'),
        os.path.join(os.path.expanduser('~'), '.config', 'config.ini'),
    ]

    #: the data directory where TSVs get exported
    data: str = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, 'data'))


biokeen_config = BiokeenConfig.load()

DATA_DIR = biokeen_config.data
os.makedirs(DATA_DIR, exist_ok=True)


VERSION = '0.0.8'
CONFIG_PATH = os.path.join(DATA_DIR, "configuration.json")

EMOJI = '🍩'

# Available databases
COMPATH_NAME = 'compath'
HIPPIE_NAME = 'hippie'
KEGG_NAME = 'kegg'
MIRTARBASE_NAME = 'mirtarbase'
MSIG_NAME = 'msig'
REACTOME_NAME = 'reactome'
WIKIPATHWAYS_NAME = 'wikipathways'
DRUGBANK_NAME = 'drugbank'
ADEPTUS_NAME = 'adeptus'
HSDN_NAME = 'hsdn'
INTERPRO_NAME = 'interpro'

# ToDo: Add databases
DATABASES = [
    COMPATH_NAME,
    HIPPIE_NAME,
    KEGG_NAME,
    MIRTARBASE_NAME,
    MSIG_NAME,
    REACTOME_NAME,
    WIKIPATHWAYS_NAME,
    DRUGBANK_NAME,
    ADEPTUS_NAME,
    HSDN_NAME,
    INTERPRO_NAME,
]

ID_TO_DATABASE_MAPPING = dict(enumerate(DATABASES, start=1))
