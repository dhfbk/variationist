# Metrics

Metrics can be defined through the **`metric`** parameter of the `InspectorArgs` class. For defining custom metrics, see [custom components](https://github.com/dhfbk/variationist/tree/main/docs/custom-components.md). Off-the-shelf choices are the following:


## Basic statistics

- `stats`: (**per-variable statistics**). All the following will be calculated:
  - `num_texts` (**number of texts**): the total number of texts in each subset of interest
  - `avg_text_len` (**average text length**): the average length of texts in each subset of interest
  - `num_tokens` (**number of tokens**): the total number of tokens in each subset
  - `vocab_size` (**vocabulary size**): the total number of unique tokens in each subset (i.e., the size of the vocabulary for each subset)
  - `num_duplicates` (**number of duplicates**): the number of duplicate texts in each subset of interest
- `freq` (**token frequencies**): the frequency of tokens in each subset of interest.


## Lexical variation metrics

- `ttr` (**type-token ratio**): the mean TTR [(Johnson, 1944)](https://psycnet.apa.org/doiLanding?doi=10.1037%2Fh0093508) score for each subset and its standard deviation
- `root_ttr` (**root type-token ratio**): the mean RTTR [(Guiraud, 1960)](https://link.springer.com/book/9789027700254) score for each subset and its standard deviation. It is also referred to as Guiraud's index
- `log_ttr` (**log type-token ratio**):  the mean LTTR [(Herdan, 1960)](https://books.google.it/books?id=wfj2zQEACAAJ) score for each subset and its standard deviation. It is also referred to as Herdan's C
- `maas` (**Maas' index**): the mean Maas' index [(Maas, 1972)](#) score for each subset and its standard deviation


## Unit-variables association metrics

- `pmi` (**pointwise mutual information [PMI]**): the PMI for each token in each subset of interest
- `n_pmi` (**normalized PMI**): the normalized PMI for each token in each subset of interest
- `p_pmi` (**positive PMI**): the positive PMI for each token in each subset of interest
- `np_pmi` (**normalized positive PMI**): the normalized positive PMI for each token in each subset of interest
- `w_pmi` (**weighted PMI**): the weighted PMI for each token in each subset of interest
- `nw_pmi` (**normalized weighted PMI**): the normalized weighted PMI for each token in each subset of interest
- `pw_pmi` (**positive weighted PMI**): the positive weighted PMI for each token in each subset of interest
- `npw_pmi` (**normalized positive weighted PMI**): the normalized positive weighted PMI for each token in each subset of interest
- `np_relevance` (**normalized positive class relevance**): the normalized positive class relevance metric for each token in each subset of interest (based on [Ramponi and Tonelli (2022)](https://aclanthology.org/2022.naacl-main.221/))
- `nw_relevance` (**normalized weighted class relevance**): the normalized weighted class relevance metric for each token in each subset of interest (based on [Ramponi and Tonelli (2022)](https://aclanthology.org/2022.naacl-main.221/))
- `npw_relevance` (**normalized positive weighted class relevance**): the normalized positive weighted class relevance metric for each token in each subset of interest (based on [Ramponi and Tonelli (2022)](https://aclanthology.org/2022.naacl-main.221/))

For unit-variables association metrics, it is possible to also set the `freq_cutoff` parameter, i.e., the token frequency, expressed as an integer, below which we do not consider the token in the analysis. It defaults to 3