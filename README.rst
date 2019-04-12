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

Share Your Experimental Artifacts
---------------------------------
You can share you trained KGE models along the other experimental artifacts through the `KEEN-Model-Zoo <https://github.com/SmartDataAnalytics/KEEN-Model-Zoo>`_.

Tutorials
---------
A brief tutorial on how to get started with BioKEEN is available `here <https://vimeo.com/314252656>`_.

.. image:: https://i.vimeocdn.com/video/755767182.jpg?mw=1100&mh=619&q=70
    :width: 300px
    :target: https://vimeo.com/314252656


.. |br| raw:: html

   <br />

|br| Further tutorials are can be found in the `notebooks directory <https://github.com/SmartDataAnalytics/BioKEEN/tree/master/notebooks>`_ and in our `documentation <https://biokeen.readthedocs.io/en/latest/>`_.

Citation
--------
If you find BioKEEN useful in your work, please consider citing:

.. [1] Ali, M., *et al.* (2019). `BioKEEN: A library for learning and evaluating biological knowledge graph embeddings
       <https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz117/5320556>`_. *Bioinformatics* , btz117.

**Note**: ComPath has been updated, for this reason we have uploaded the dataset version that we have used for
our experiments: `dataset <https://github.com/SmartDataAnalytics/KEEN-Model-Zoo/blob/master/bioinformatics/ComPath/compath.keen.tsv>`_



Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
To install biokeen, Python 3.6+ is required, and we recommend to install it on Linux or Mac OS systems.
Please run following command:

.. code-block:: sh

    $ pip install git+https://github.com/SmartDataAnalytics/BioKEEN.git

Alternatively, it can be installed from the source for development with:

.. code-block:: sh

    $ git clone https://github.com/SmartDataAnalytics/BioKEEN.git biokeen
    $ cd biokeen
    $ pip install -e .

Contributing
------------
Contributions, whether filing an issue, making a pull request, or forking, are appreciated.
See `CONTRIBUTING.rst <https://github.com/SmartDataAnalytics/BioKEEN/blob/master/CONTRIBUTING.rst>`_ for more
information on getting involved.

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

where the value for the argument **-m** is the directory containing the model, in more detail following files must be
contained in the directory:

* configuration.json
* entities_to_embeddings.json
* relations_to_embeddings.json
* trained_model.pkl

These files are created automatically created after model is trained (and evaluated) and exported in your
specified output directory.

The value for the argument **-d** is the directory containing the data for which inference should be applied, and it
needs to contain following files:

* entities.tsv
* relations.tsv

where *entities.tsv* contains all entities of interest, and relations.tsv all relations. Both files should contain
should contain a single column containing all the entities/relations. Based on these files, PyKEEN will create all
triple permutations, and computes the predictions for them, and saves them in data directory
in *predictions.tsv*.

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
