# -*- coding: utf-8 -*-

"""Constants for BioKEEN."""

import os

HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR_ENVVAR = 'KEEN_DATA'
DATA_DIR = os.environ.get(DATA_DIR_ENVVAR) or os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, 'data'))
