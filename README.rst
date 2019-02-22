BioKEEN |build| |coverage| |docs| |zenodo|
==========================================
BioKEEN (Biological KnowlEdge EmbeddiNgs) is a package for training and evaluating biological knowledge graph
embeddings built on `PyKEEN <https://github.com/SmartDataAnalytics/PyKEEN>`_.

Because we use PyKEEN as the underlying software package, implementations of 10 knowledge graph embedding models are
currently available for BioKEEN. Furthermore, BioKEEN can be run in *training mode* in which users provide their own set
of hyper-parameter values, or in *hyper-parameter optimization mode* to find suitable hyper-parameter values from set
of user defined values.

Through the integration of the `Bio2BEL <https://github.com/bio2bel>`_ software numerous biomedical databases are
directly accessible within BioKEEN.

BioKEEN can also be run without having experience in programing by using its interactive command line interface that can
be started with the command “biokeen” from a terminal.

Tutorial
--------
A brief tutorial on how to get started with BioKEEN is available `here <https://vimeo.com/314252656>`_.

.. image:: https://i.vimeocdn.com/video/755767182.jpg?mw=1100&mh=619&q=70
    :width: 300px
    :target: https://vimeo.com/314252656

Citation
--------
If you find BioKEEN useful in your work, please consider citing:

.. [1] Ali, M., *et al.* (2019). `BioKEEN: A library for learning and evaluating biological knowledge graph embeddings
       <https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz117/5320556>`_. *Bioinformatics* , btz117.

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
``biokeen`` can be installed on any system running Python 3.6+  with the following commands:

.. code-block:: sh

    $ pip install git+https://github.com/SmartDataAnalytics/BioKEEN.git

Alternatively, it can be installed from the source for development with:

.. code-block:: sh

    $ git clone https://github.com/SmartDataAnalytics/BioKEEN.git biokeen
    $ cd biokeen
    $ pip install -e .

Usage
-----
Code examples can be found in the `notebooks directory <https://github.com/SmartDataAnalytics/BioKEEN/tree/master/notebooks>`_.

CLI Usage
---------
To show BioKEEN's available commands, please run following command:

.. code-block:: sh

    biokeen

Starting the Training/HPO Pipeline - Set Up Your Experiment within 60 seconds
*****************************************************************************
To configure an experiment via the CLI, please run following command:

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

    biokeen summarize -d /path/to/experiments/directory -o /path/to/output/file.csv

Getting Bio2BEL Data
********************
To download and structure the data from a `Bio2BEL <https://github.com/bio2bel>`_ repository, run:

.. code-block:: sh

    biokeen data get <name>

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
