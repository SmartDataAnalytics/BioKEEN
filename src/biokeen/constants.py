# -*- coding: utf-8 -*-

"""Constants for BioKEEN."""

import os
from collections import OrderedDict

HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR_ENVVAR = 'KEEN_DATA'
DATA_DIR = os.environ.get(DATA_DIR_ENVVAR) or os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, 'data'))

VERSION = 'VERSION = '0.0.3-dev''

CONFIG_PATH = os.path.join(DATA_DIR, "configuration.json")
EMOJI = '🍩'

# Available databases
DRUGBANK_NAME = 'drugbank'
HIPPE_NAME = 'hippie'
MIRTARBASE_NAME = 'mirtarbase'
WIKIPATHSWAYS_NAME = 'wikipathways'
MSIG_NAME = 'msig'
KEGG_NAME = 'kegg'
REACTOME_NAME = 'reactome'

# ToDo: Add databases
ID_TO_DATABASE_MAPPING = OrderedDict({
    '1': MIRTARBASE_NAME,
    '2': DRUGBANK_NAME,
    '3': WIKIPATHSWAYS_NAME,
    '4': HIPPE_NAME,
    '5': MSIG_NAME,
    '6': KEGG_NAME,
    '7': REACTOME_NAME
})