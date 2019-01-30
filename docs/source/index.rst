BioKEEN
=======
BioKEEN (Biological KnowlEdge EmbeddiNgs) is a package for training and evaluating **biological** knowledge graph
embeddings built on `PyKEEN <https://github.com/SmartDataAnalytics/PyKEEN>`_. Within BioKEEN several biomedical
databases are directly accessible for training and evaluating biological knowledge graph embeddings
(see :ref:`bio2bel_repositories`).

Because we use PyKEEN as the core underlying framework, currently, implementations of 10
knowledge graph emebddings models are avaialble for BioKEEN. Furthermore, it can be run in training mode in
which users provide their own set of hyper-parameter values, or in hyper-parameter optimization mode to find suitable
hyper-parameter values from set of user defined values. BioKEEN can also be run without having experience in programing
by using its interactive command line interface that can be started with the command "biokeen" from a terminal.

Installation is as easy as getting the code from `PyPI <https://pypi.python.org/pypi/biokeen>`_ with
:code:`python3 -m pip install biokeen`.


Citation
--------
If you use BioKEEN in your work, please cite [1]_:

.. [1] Ali, M., *et al.* (2018). `BioKEEN: A library for learning and evaluating biological knowledge graph embeddings
       <https://zenodo.org/badge/latestdoi/136345023>`_.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :name: start

   installation

.. toctree::
   :maxdepth: 2
   :caption: CLI Usage
   :name: cli

   cli/train_and_evaluate
   cli/inference
   cli/summarize

.. toctree::
   :maxdepth: 2
   :caption: Running PyKEEN programmatically
   :name: prog

   train_and_evaluate
   hyper_parameter_optimization

.. toctree::
   :maxdepth: 2
   :caption: Biological Databases
   :name: bio2bel_repositories

   bio2bel_repositories

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
