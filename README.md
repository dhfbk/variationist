<p align="center"><img src="docs/img/logo.png" width="60%" height="60%"></img></p>

<div align="center">

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![v0.1.0](https://img.shields.io/badge/pypi-v0.1.0-orange)](https://pypi.org/project/variationist/0.1.0/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/readthedocs/:packageName/:version)](https://variationist.readthedocs.io/en/latest/)
[![Tutorials](https://img.shields.io/badge/tutorials-colab-orange)](https://github.com/dhfbk/variationist/tree/main/examples)

</div>

🕵️‍♀️ **Variationist** is a highly-modular, flexible, and customizable tool to analyze and explore language variation and bias in written language data. It allows researchers, from NLP practitioners to linguists and social scientists, to seamlessly investigate language use across a wide range of use cases.

- :cd: [**Installation**](#installation)
- :checkered_flag: [**Quickstart**](#quickstart)
- :closed_book: [**Tutorials**](#tutorials)
- :book: [**Documentation**](#documentation)
- :airplane: [**Roadmap**](#roadmap)
- :cyclone: [**Contributors**](#contributors)
- :pencil2: [**Citation**](#citation)


## Installation

### Python package

🕵️‍♀️ Variationist can be installed as a python package from [PyPI](https://pypi.org/) using the `pip` command as follows:

```
pip install variationist
```

### Installing from source

Alternatively, 🕵️‍♀️ Variationist can be installed from source as follows:

1) Clone this repository on your own path:
```
git clone https://github.com/dhfbk/variationist.git
```

2) Create an environment with your own preferred package manager. We used [python 3.9](https://www.python.org/downloads/release/python-390/) and dependencies listed in [`requirements.txt`](requirements.txt). If you use [conda](https://docs.conda.io/en/latest/), you can just run the following commands from the root of the project:

```
conda create --name variationist python=3.9         # create the environment
conda activate variationist                         # activate the environment
pip install --user -r requirements.txt              # install the required packages
```


## Quickstart

🕵️‍♀️ Variationist can be run in a few line of codes. Below is an example on how it can be used to explore variation and bias in a custom dataset `my_dataset.tsv` using `pmi` and `frequency` as metrics on the text column `text` and the `label` variable, using just 1 token and a default whitespace tokenizer, with stopword removal in English. The output charts will be then serialized in `html` and `png` formats.

:warning: Example to be made more concise, explanatory, and shorter.

```python
from variationist import Inspector, InspectorArgs, Visualizer, VisualizerArgs

# Define the inspector arguments
inspector_args = InspectorArgs(
	text_names=["text"], var_names=["label"], metrics=["pmi", "frequency"],
	stopwords="en", n_tokens=1, n_cooc=1)

# Create an inspector instance, run it, and get the results in json
results = Inspector(data_filepath="my_dataset.tsv", inspector_args).inspect()

# Define the visualizer arguments
visualizer_args = VisualizerArgs(
	filterable=True, zoomable=True, ngrams=None, output_formats=["html", "png"])

# Create dynamic visualizations of the results
Visualizer(input_json=results, output_folder="charts", visualizer_args).visualize()
```


## Tutorials

You can find our tutorials to learn how to better leverage 🕵️‍♀️ **Variationist** in the [`examples/`](https://github.com/dhfbk/variationist/tree/main/examples) folder.

There you can also find a set of interesting case studies using real-world datasets! :chart_with_upwards_trend:


## Documentation

The documentation for 🕵️‍♀️ **Variationist** is available at: [https://variationist.readthedocs.io/en/latest/](https://variationist.readthedocs.io/en/latest/).

You can find more information on specific topics in the following documents:
- [Units](https://github.com/dhfbk/variationist/tree/main/docs/units.md)
- [Tokenizers](https://github.com/dhfbk/variationist/tree/main/docs/tokenizers.md)
- [Metrics](https://github.com/dhfbk/variationist/tree/main/docs/metrics.md)
- [Charts](https://github.com/dhfbk/variationist/tree/main/docs/charts.md)
- [Custom components](https://github.com/dhfbk/variationist/tree/main/docs/custom-components.md)


## Roadmap

🕵️‍♀️ **Variationist** aims to be as accessible as possible to researchers from a wide range of fields. We thus aim to provide the following features in the next months:
- An easy to use graphical user interface with [Streamlit](https://streamlit.io/) to be installed locally or used through [Hugging Face Spaces](https://huggingface.co/spaces)
- ...


## Contributors

- **[Alan Ramponi](https://alanramponi.github.io)**, *Fondazione Bruno Kessler*
- **[Camilla Casula](https://dh.fbk.eu/author/camilla/)**, *Fondazione Bruno Kessler*, *University of Trento*
- **[Stefano Menini](https://dh.fbk.eu/author/stefano/)**, *Fondazione Bruno Kessler*


## Citation

A preprint will be available soon! :construction:
