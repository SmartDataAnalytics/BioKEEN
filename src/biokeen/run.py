# -*- coding: utf-8 -*-

"""Script for starting the pipeline and saving the results."""

from dataclasses import dataclass
from typing import Dict, Mapping, Optional

import pykeen
from pykeen.utilities.pipeline import Pipeline


@dataclass
class Results:
    """Results from PyKEEN."""

    config: Mapping
    pipeline: Pipeline
    results: Mapping


def run(config: Dict,
        output_directory: Optional[str] = None) -> Results:
    """Run PyKEEN using a given configuration."""
    results = pykeen.run(
        config=config,
        output_directory=output_directory,
    )

    return results
