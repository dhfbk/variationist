# Units

The language unit of interest, which can be anything from characters to "words" (whatever their definition may be) and longer sequences. 

🕵️‍♀️ Variationist seamlessly supports *n*-grams (i.e., *n* contiguous language units) and co-occurrences of *n* units (not necessarily contiguous) that fall within a user-defined window size, with optional duplicate handling. For creating units, we rely on either built-in, publicly available, or user-defined [tokenizers](https://github.com/dhfbk/variationist/blob/main/docs/tokenizers.md). 

A unit can be defined through the **`n_tokens`** and **`n_cooc`** parameters of the `InspectorArgs` class. 🕵️‍♀️ Variationist currently supports the following:

- **`n_tokens`**: the number of tokens that should be considered for the analysis. 1 corresponds to unigrams, 2 corresponds to bigrams, and so on
- **`n_cooc`**: the number of tokens used for calculating non-consecutive co-occurrences. For example, *n*=2 means we consider as the base units for our analysis any pair of tokens that co-occur in the same sentence. *n*=3 means we consider triplets of tokens, etc. Defaults to n=1, meaning no co-occurrences are taken into consideration, and we only consider **`n_tokens`**. If **`n_cooc`** is set, **`n_tokens`** must be 1
	- **`cooc_window_size`**: the number denoting the size of the context window for co-occurrences. For instance, a value 3 means we use a context window of 3 to calculate co-occurrences, meaning that any token that is within 3 tokens before or after a given token is added as a co-occurrence
	- **`unique_cooc`**: a boolean denoting whether to consider unique co-occurrences or not. Default to *False* (keep duplicate tokens). If *True*, multiple occurrences of the same token in a text will be discarded. This does not affect the co-occurrences window size by design (the window size considers the original number of tokens and therefore the original allowed maximum distance between tokens)


## Optional preprocessing

Units may optionally undergo preprocessing using specific parameters of the `InspectorArgs` class:

- **lowercase**: a boolean denoting whether to lowercase all the texts before tokenization or not. It defaults to *False*
- **stopwords**: a boolean denoting whether to remove stopwords from texts before tokenization or not. It will use default lists from the [stopwords-iso](https://github.com/stopwords-iso) package in a given `language` defined by the user (as ISO 639-1 code strings) and defaults to *False*
    - **custom_stopwords**: a list of stopwords (or a path to a file containing stopwords, one per line) to be removed before tokenization. If `stopwords` is *True*, these stopwords will be added to that list. It defaults to *None*