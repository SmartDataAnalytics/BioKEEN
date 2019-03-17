# -*- coding: utf-8 -*-

"""Constants for BioKEEN."""

import os
from typing import Iterable

import easy_config

HERE = os.path.abspath(os.path.dirname(__file__))
HOME = os.path.expanduser('~')


class BiokeenConfig(easy_config.EasyConfig):
    """Configuration for BioKEEN."""

    NAME = 'biokeen'
    FILES = [
        os.path.join(HOME, '.config', 'biokeen.cfg'),
        os.path.join(HOME, '.config', 'config.ini'),
    ]

    #: the data directory where TSVs get exported
    data: str = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, 'data'))


biokeen_config = BiokeenConfig.load()

DATA_DIR = biokeen_config.data
os.makedirs(DATA_DIR, exist_ok=True)


def iterate_source_paths() -> Iterable[str]:
    """Iterate over the source paths."""
    for file_name in os.listdir(DATA_DIR):
        if 'keen.tsv' in file_name:
            yield os.path.join(DATA_DIR, file_name)


VERSION = '0.0.13-dev'

EMOJI = '🍩'

# Available databases
COMPATH_NAME = 'compath'
HIPPIE_NAME = 'hippie'
KEGG_NAME = 'kegg'
MIRTARBASE_NAME = 'mirtarbase'
MSIG_NAME = 'msig'
REACTOME_NAME = 'reactome'
SIDER_NAME = 'sider'
WIKIPATHWAYS_NAME = 'wikipathways'
DRUGBANK_NAME = 'drugbank'
ADEPTUS_NAME = 'adeptus'
HSDN_NAME = 'hsdn'
INTERPRO_NAME = 'interpro'
DDR_NAME = 'ddr'

# ToDo: Add databases
DATABASES = [
    COMPATH_NAME,
    HIPPIE_NAME,
    KEGG_NAME,
    MIRTARBASE_NAME,
    MSIG_NAME,
    REACTOME_NAME,
    SIDER_NAME,
    WIKIPATHWAYS_NAME,
    DRUGBANK_NAME,
    ADEPTUS_NAME,
    HSDN_NAME,
    INTERPRO_NAME,
    DDR_NAME,
]

ID_TO_DATABASE_MAPPING = dict(enumerate(DATABASES, start=1))
