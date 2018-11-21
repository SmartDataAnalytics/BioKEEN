# -*- coding: utf-8 -*-

"""Constants for BioKEEN."""

import os

HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR_ENVVAR = 'BioKEEN_DATA'
DATA_DIR = os.environ.get(DATA_DIR_ENVVAR) or os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, 'data'))
os.makedirs(DATA_DIR, exist_ok=True)

VERSION = '0.0.4'

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
