BioKEEN |build| |zenodo|
========================

BioKEEN (Biological KnowlEdge EmbeddiNgs) is a package for training and evaluating biological knowledge graph embeddings built on
`PyKEEN <https://github.com/SmartDataAnalytics/PyKEEN>`_.

Installation
------------
1. ``BioKEEN`` can be installed with the following commands:

.. code-block:: sh

    python3 -m pip install git+https://github.com/SmartDataAnalytics/BioKEEN.git@master

2. or in editable mode with:

.. code-block:: sh

    $ git clone https://github.com/SmartDataAnalytics/BioKEEN.git biokeen
    $ cd biokeen
    $ python3 -m pip install -e .

How to Use
----------
To show BioKEEN's available commands, please run following command:

.. code-block:: sh

    biokeen

or alternatively:

.. code-block:: python

    python3 -m biokeen


Starting BioKEEN's training/HPO pipeline
****************************************
To configure an experiment, please run following command:

.. code-block:: sh

    biokeen start

or alternatively:

.. code-block:: python

    python3 -m biokeen start


To start BioKEEN with an existing configuration file, please run the following command:

.. code-block:: sh

    biokeen start -c /path/to/config.json

or alternatively:

.. code-block:: python

    python3 -m biokeen start -c /path/to/config.json


Starting BioKEEN's prediction pipeline
**************************************
To make prediction based on a trained model, please run following command:

.. code-block:: sh

    biokeen predict -m /path/to/model/directory -d /path/to/data/directory

or alternatively:

.. code-block:: python

    python3 -m biokeen predict -m /path/to/model/directory -d /path/to/data/directory


Getting Bio2BEL Data
********************
To download and structure the data from a `Bio2BEL <https://github.com/bio2bel>`_ repository, run:

.. code-block:: python

    biokeen get <name>
    
Where ``<name>`` can be any repository name in Bio2BEL such as ``hippie``, ``mirtarbase``.

.. |build| image:: https://travis-ci.org/SmartDataAnalytics/BioKEEN.svg?branch=master
    :target: https://travis-ci.org/SmartDataAnalytics/BioKEEN
    
.. |zenodo| image:: https://zenodo.org/badge/150270965.svg
   :target: https://zenodo.org/badge/latestdoi/150270965
