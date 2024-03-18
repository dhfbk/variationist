Variationist's documentation
============================

|license| |pypi| |python| |documentation| |tutorials|

.. |license| image:: https://img.shields.io/badge/license-MIT-green.svg
    :target: https://github.com/dhfbk/variationist/blob/main/LICENSE
    :alt: MIT license

.. |pypi| image:: https://img.shields.io/badge/pypi-v0.1.3-orange
    :target: https://pypi.org/project/variationist/0.1.3/
    :alt: v0.1.3

.. |python| image:: https://img.shields.io/badge/python-3.9+-blue
    :target: https://www.python.org/downloads/
    :alt: Python 3.9+

.. |documentation| image:: https://img.shields.io/readthedocs/:packageName/:version
    :target: https://variationist.readthedocs.io/en/latest/
    :alt: Documentation

.. |tutorials| image:: https://img.shields.io/badge/tutorials-colab-orange
    :target: https://github.com/dhfbk/variationist/tree/main/examples
    :alt: Tutorials


**Variationist** is a highly-modular, flexible, and customizable tool to analyze and explore language variation and bias in written language data. It allows researchers, from NLP practitioners to linguists and social scientists, to seamlessly investigate language use across many dimensions and a wide range of use cases.


Installation
------------

**Python package**

Variationist can be installed as a python package from `PyPI`_ using the :code:`pip` command as follows:

.. code-block:: console

    pip install variationist


**Installing from source**

Alternatively, Variationist can be installed from source as follows:

1) Clone the `GitHub repository`_ on your own path:

.. code-block:: console

    git clone https://github.com/dhfbk/variationist.git

2) Create an environment with your own preferred package manager. We used `python 3.9`_ and dependencies listed in `requirements.txt`_. If you use `conda`_, you can just run the following commands from the root of the project:

.. code-block:: console

    conda create --name variationist python=3.9         # create the environment
    conda activate variationist                         # activate the environment
    pip install --user -r requirements.txt              # install the required packages


Getting started
---------------

For getting started, please refer to our `GitHub repository`_ for materials such as a `quickstart`_, extra `documentation`_, and `tutorials`_.


Citation
--------

A preprint will be available soon! In the meanwhile, if you use Variationist in your work please cite:

.. code-block:: console

    @misc{ramponi-etal-2024-variationist,
      author = {Ramponi, Alan and Casula, Camilla and Menini, Stefano},
      title = {Variationist: {E}xploring Multifaceted Variation and Bias in Written Language Data},
      year = {2024},
      publisher = {GitHub repository},
      howpublished = {\url{https://github.com/dhfbk/variationist}}
    }




.. _PyPi: https://pypi.org/
.. _GitHub repository: https://github.com/dhfbk/variationist
.. _python 3.9: https://www.python.org/downloads/release/python-390/
.. _requirements.txt: https://github.com/dhfbk/variationist/blob/main/requirements.txt
.. _conda: https://docs.conda.io/en/latest/
.. _quickstart: https://github.com/dhfbk/variationist?tab=readme#quickstart
.. _extra documentation: https://github.com/dhfbk/variationist?tab=readme#documentation
.. _tutorials: https://github.com/dhfbk/variationist?tab=readme#tutorials


.. toctree::