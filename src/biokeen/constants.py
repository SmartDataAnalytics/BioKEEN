# -*- coding: utf-8 -*-

"""Constants for BioKEEN."""

import os

DATA_DIR_ENVVAR = 'KEEN_DATA'
DATA_DIR = os.environ.get(DATA_DIR_ENVVAR) or os.path.join(os.path.expanduser('~'), '.keen')
