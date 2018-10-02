BioKEEN |build|
===============

BioKEEN is a package for training and evaluating biological knowledge graph embeddings.
 
**Currently, the framework is under heavy development.**

Installation
------------
1. ``BioKEEN`` can be installed with the following commmands:

.. code-block:: sh

    python3 -m pip install git+https://github.com/SmartDataAnalytics/BioKEEN.git@master

2. or in editable mode with:

.. code-block:: sh

    git clone https://github.com/SmartDataAnalytics/BioKEEN.git

.. code-block:: sh

    cd BioKEEN

.. code-block:: sh

    python3 -m pip install -e .

How to use
----------

To start BioKEEN, please run the following command:
    
.. code-block:: sh

    keen
    
or alternatively:    

.. code-block:: python

    python3 -m biokeen
    
then the command line interface will assist you to configure your experiments.

.. |build| image:: https://travis-ci.org/SmartDataAnalytics/BioKEEN.svg?branch=master
    :target: https://travis-ci.org/SmartDataAnalytics/BioKEEN
