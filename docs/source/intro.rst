

Intro to Variationist
=====================

.. container::

   |MIT License| |v0.1.4| |Python 3.9+| |Documentation| |Tutorials|

🕵️‍♀️ **Variationist** is a highly-modular, flexible, and customizable tool
to analyze and explore language variation and bias in written language
data. It allows researchers, from NLP practitioners to linguists and
social scientists, to seamlessly investigate language use across many
dimensions and a wide range of use cases.

Alan Ramponi, Camilla Casula and Stefano Menini. 2024. **Variationist:
Exploring Multifaceted Variation and Bias in Written Language Data**. In
*Proceedings of the 62nd Annual Meeting of the Association for
Computational Linguistics (Volume 3: System Demonstrations)* (To
appear), Bangkok, Thailand. ACL. `[cite] <#citation>`__
`[paper] <https://arxiv.org/abs/2406.17647>`__

Installation
------------

Python package
~~~~~~~~~~~~~~

🕵️‍♀️ Variationist can be installed as a python package from
`PyPI <https://pypi.org/>`__ using the `pip` command as follows:

::

   pip install variationist

Installing from source
~~~~~~~~~~~~~~~~~~~~~~

Alternatively, 🕵️‍♀️ Variationist can be installed from source as follows:

1) Clone this repository on your own path:

::

   git clone https://github.com/dhfbk/variationist.git

2) Create an environment with your own preferred package manager. We used `python 3.9 <https://www.python.org/downloads/release/python-390/>`__ and dependencies listed in `requirements.txt <requirements.txt>`__.
   If you use `conda <https://docs.conda.io/en/latest/>`__, you can just
   run the following commands from the root of the project:

::

   conda create --name variationist python=3.9         # create the environment
   conda activate variationist                         # activate the environment
   pip install --user -r requirements.txt              # install the required packages

Quickstart
----------

🕵️‍♀️ Variationist works in a few line of codes and supports a wide variety
of use cases in many dimensions. Below is an introductory example on how
it can be used to explore variation and bias on a very simple dataset
with a single text column and just a variable.

1) Import 🕵️‍♀️ Variationist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We first import the main classes useful for computation and
visualization as follows:

.. code:: python

   from variationist import Inspector, InspectorArgs, Visualizer, VisualizerArgs

A brief description for the classes is the following: -
**Inspector** (and **InspectorArgs**): it takes care of
orchestrating the analysis, from importing and tokenizing the data to
calculating the metrics and creating outputs with all the calculated
metrics for each text column, variable, and combination thereof. It
relies on `InspectorArgs`, a dataclass that allows the user to specify
a variety of arguments that relate to the analysis. - **Visualizer**
(and **VisualizerArgs**): it takes care of orchestrating the
creation of a variety of interactive charts showing up to five
dimensions based on the results and metadata from a prior analysis using
`Inspector`. It relies on `VisualizerArgs`, a class storing the
specific arguments for visualization.

2) Define and run the *Inspector*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now, we aim to **inspect the data**. For this example, we use a column
`text` and just a single `label` variable (with a default *nominal*
`variable
type <https://github.com/dhfbk/variationist/tree/main/docs/variables.md>`__
and a default *general* `variable
semantics <https://github.com/dhfbk/variationist/tree/main/docs/variables.md>`__);
however, note that 🕵️‍♀️ Variationist can seamlessly handle a potentially
unlimited number of variables and up to two text columns during
computation. We just use `npw_pmi` as our association
`metric <https://github.com/dhfbk/variationist/tree/main/docs/metrics.md>`__
and rely on single tokens as our `unit of
information <https://github.com/dhfbk/variationist/tree/main/docs/units.md>`__,
using a default
`tokenizer <https://github.com/dhfbk/variationist/blob/main/docs/tokenizers.md>`__.
We also ask for some
`preprocessing <https://github.com/dhfbk/variationist/tree/main/docs/preprocessing.md>`__
steps (stopwords removal in English and lowercasing). The output is
stored in the `results` variable but it can alternatively be
serialized to a .json file for later use.

.. code:: python

   # Define the inspector arguments
   ins_args = InspectorArgs(text_names=["text"], var_names=["label"], 
       metrics=["npw_pmi"], n_tokens=1, language="en", stopwords=True, lowercase=True)

   # Run the inspector and get the results
   res = Inspector(dataset="data.tsv", args=ins_args).inspect()

3) Define and run the *Visualizer*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, we aim to **visualize the results**. The visualizer currently
handles the creation of interactive
`charts <https://github.com/dhfbk/variationist/tree/main/docs/charts.md>`__
for more than 30 combinations of `variable type and
semantics <https://github.com/dhfbk/variationist/tree/main/docs/variables.md>`__
up to five dimensions, in which two of them are naturally fixed: the
`units <https://github.com/dhfbk/variationist/tree/main/docs/units.md>`__
(*nominal*) and their
`metric <https://github.com/dhfbk/variationist/tree/main/docs/charts.md>`__
scores (*quantitative*). For this example, we output in the output
folder `my_charts` the results in a `html` format (i.e., the default
and suggested one for the sake of interactivity).

.. code:: python

   # Define the visualizer arguments
   vis_args = VisualizerArgs(output_folder="charts", output_formats=["html"])

   # Create interactive charts for all metrics
   charts = Visualizer(input_json=res, args=vis_args).create()

Optionally, interactive charts can be visualized in notebooks by just
taking the object returned from the `create()` function. For instance,
if the object is stored in a variable named `charts`, visualization
would be as simple as writing the following string in the notebook:
`charts[$METRIC][$CHART_TYPE]`, where `$METRIC` is the metric of
interest and `$CHART_TYPE` is a specific chart type associated with
that metric.



Citation
--------

If you use 🕵️‍♀️ **Variationist** in your work, please cite our paper as
follows:

::

   @article{ramponi-etal-2024-variationist,
     author = {Ramponi, Alan and Casula, Camilla and Menini, Stefano},
     title = {Variationist: {E}xploring Multifaceted Variation and Bias in Written Language Data},
     year = {2024},
     journal = {arXiv preprint arxiv:2406.17647},
     url = {https://arxiv.org/abs/2406.17647}
   }

.. |MIT License| image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: LICENSE
.. |v0.1.4| image:: https://img.shields.io/badge/pypi-v0.1.4-orange
   :target: https://pypi.org/project/variationist/0.1.4/
.. |Python 3.9+| image:: https://img.shields.io/badge/python-3.9+-blue
   :target: https://www.python.org/downloads/
.. |Documentation| image:: https://readthedocs.org/projects/variationist/badge/?version=latest
   :target: https://variationist.readthedocs.io/en/latest/
.. |Tutorials| image:: https://img.shields.io/badge/tutorials-colab-orange
   :target: https://github.com/dhfbk/variationist/tree/main/examples



