# 🕵️‍♀️ `variationist`

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![v0.1.0](https://img.shields.io/badge/pypi-v0.1.0-orange)](https://pypi.org/project/variationist/0.1.0/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue)](#)

*Description will go here*


## Installation

[!WARNING]
The python library is currently work in progress (not available).

🕵️‍♀️ Variationist can be installed as a python package from [PyPI](https://pypi.org/) using the `pip` command as follows:

```
pip install variationist
```

Alternatively, for development purposes it can be installed from source as follows:

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


## Usage

### Using the library: minimal example

[!WARNING]
The example may change and it will be tested when the python library will be available.

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

### Using the app

[!CAUTION]
The app needs to be refactored and will need to include all the new features.

```
streamlit run main.py
```

### Run from code (for development only)

```
python example.py
```
The `example.py` file contains a sample usage of Variationist. 


### Documentation

[!WARNING]
The documentation is currently work in progress (not available).

The documentation will be available at: [https://variationist.readthedocs.io/en/latest/](https://variationist.readthedocs.io/en/latest/)
