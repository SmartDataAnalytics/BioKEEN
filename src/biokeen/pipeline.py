# -*- coding: utf-8 -*-

"""

1. Hard code all parameters for running the TransE model
2. run it here

"""

import json
import os

from biokeen.constants import DATA_DIR
from keen.run import run

CONFIG_PATH = os.path.join(DATA_DIR, "configuration.json")


def main():
    with open(CONFIG_PATH) as file:
        config = json.load(file)

    run(config)


if __name__ == '__main__':
    main()
