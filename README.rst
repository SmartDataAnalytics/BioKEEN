BioKEEN |build| |coverage| |docs| |zenodo|
==========================================
BioKEEN (Biological KnowlEdge EmbeddiNgs) is a package for training and evaluating biological knowledge graph
embeddings built on `PyKEEN <https://github.com/SmartDataAnalytics/PyKEEN>`_.

Citation
--------
If you find BioKEEN useful in your work, please consider citing:

.. [1] Ali, M., *et al.* (2018). `BioKEEN: A library for learning and evaluating biological knowledge graph embeddings
       <https://doi.org/10.1101/475202>`_. bioRxiv 475202.

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
1. ``biokeen`` can be installed with the following commands:

.. code-block:: sh

    python3 -m pip install git+https://github.com/SmartDataAnalytics/BioKEEN.git@master

2. or in editable mode with:

.. code-block:: sh

    $ git clone https://github.com/SmartDataAnalytics/BioKEEN.git biokeen
    $ cd biokeen
    $ python3 -m pip install -e .

Usage
-----
Code examples can be found in the `notebooks directory
<https://github.com/SmartDataAnalytics/BioKEEN/tree/master/notebooks>`_.

CLI Usage
---------
To show BioKEEN's available commands, please run following command:

.. code-block:: sh

    biokeen

Starting the Training/HPO Pipeline
**********************************
To configure an experiment, please run following command:

.. code-block:: sh

    biokeen start

To start BioKEEN with an existing configuration file, please run the following command:

.. code-block:: sh

    biokeen start -f /path/to/config.json

Starting the Prediction Pipeline
********************************
To make prediction based on a trained model, please run following command:

.. code-block:: sh

    biokeen predict -m /path/to/model/directory -d /path/to/data/directory

Summarize the Results of All Experiments
****************************************
To summarize the results of all experiments, please run following command:

.. code-block:: sh

    biokeen-summarize -d /path/to/experiments/directory -o /path/to/output/file.csv

Getting Bio2BEL Data
********************
To download and structure the data from a `Bio2BEL <https://github.com/bio2bel>`_ repository, run:

.. code-block:: sh

    biokeen get <name>

Where ``<name>`` can be any repository name in Bio2BEL such as ``hippie``, ``mirtarbase``.

.. |build| image:: https://travis-ci.org/SmartDataAnalytics/BioKEEN.svg?branch=master
    :target: https://travis-ci.org/SmartDataAnalytics/BioKEEN

.. |zenodo| image:: https://zenodo.org/badge/150270965.svg
    :target: https://zenodo.org/badge/latestdoi/150270965

.. |docs| image:: http://readthedocs.org/projects/biokeen/badge/?version=latest
    :target: https://biokeen.readthedocs.io/en/latest/
    :alt: Documentation Status

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/biokeen.svg
    :alt: Stable Supported Python Versions

.. |pypi_version| image:: https://img.shields.io/pypi/v/biokeen.svg
    :alt: Current version on PyPI

.. |pypi_license| image:: https://img.shields.io/pypi/l/biokeen.svg
    :alt: MIT License

.. |coverage| image:: https://codecov.io/gh/SmartDataAnalytics/BioKEEN/branch/master/graphs/badge.svg
    :target: https://codecov.io/gh/SmartDataAnalytics/BioKEEN
    :alt: Coverage Status on CodeCov
