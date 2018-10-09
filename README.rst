BioKEEN |build|
===============
BioKEEN is a package for training and evaluating biological knowledge graph embeddings built on
`PyKEEN <https://github.com/SmartDataAnalytics/PyKEEN>`_.

**Currently, the framework is under heavy development.**

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
To start BioKEEN, please run the following command:

.. code-block:: sh

    biokeen

or alternatively:

.. code-block:: python

    python3 -m biokeen

then the command line interface will assist you to configure your experiments.

.. |build| image:: https://travis-ci.org/SmartDataAnalytics/BioKEEN.svg?branch=master
    :target: https://travis-ci.org/SmartDataAnalytics/BioKEEN
