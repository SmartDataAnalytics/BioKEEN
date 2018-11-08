# -*- coding: utf-8 -*-

"""Constants for BioKEEN."""

import os
from collections import OrderedDict

HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR_ENVVAR = 'KEEN_DATA'
DATA_DIR = os.environ.get(DATA_DIR_ENVVAR) or os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, 'data'))
os.makedirs(DATA_DIR, exist_ok=True)

VERSION = '0.0.4-dev'

CONFIG_PATH = os.path.join(DATA_DIR, "configuration.json")
EMOJI = '🍩'

# Available databases
DRUGBANK_NAME = 'drugbank'
HIPPE_NAME = 'hippie'
MIRTARBASE_NAME = 'mirtarbase'
WIKIPATHWAYS_NAME = 'wikipathways'
MSIG_NAME = 'msig'
KEGG_NAME = 'kegg'
REACTOME_NAME = 'reactome'

# ToDo: Add databases
DATABASES = [
    MIRTARBASE_NAME,
    DRUGBANK_NAME,
    WIKIPATHWAYS_NAME,
    HIPPE_NAME,
    MSIG_NAME,
    KEGG_NAME,
    REACTOME_NAME,
]

ID_TO_DATABASE_MAPPING = dict(enumerate(DATABASES, start=1))
