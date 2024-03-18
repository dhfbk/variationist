import math
import numpy as np
import pandas as pd
import sys
from collections import Counter
from transformers import AutoTokenizer
from typing import List

from variationist.metrics import utils


# From: https://github.com/dhfbk/hate-speech-artifacts/blob/main/lexartifacts-package/src/lexartifacts/lexical_artifacts.py


def compute_pmi(
    w_count: Counter, 
    l_count: Counter, 
    w_l_count: Counter, 
    num_texts: int
) -> pd.core.frame.DataFrame:
    """
    A function that computes positive reweighted pointwise mutual information between tokens and 
    labels, following the implementation by [1].
    [1] Alan Ramponi and Sara Tonelli. 2022. Features or Spurious Artifacts? Data-centric Baselines 
    for Fair and Robust Hate Speech Detection. In Proceedings of the 2022 Conference of the North 
    American Chapter of the Association for Computational Linguistics: Human Language Technologies.
    Parameters
    ----------
    w_count: Counter[str:int]
        Token counts over the whole dataset (i.e., {"token1": 123, "token2": 20, ...})
    l_count: Counter[str:int]
        Label counts over the whole dataset (i.e., {"label1": 42, "label2": 21, ...})
    w_l_count: Counter[(str,str):int]
        Token and label counts over the whole dataset (i.e., {("token1", label1"): 12, ...})
    num_texts: int
        Total number of texts in the dataset
    Returns
    -------
    pd.core.frame.DataFrame
        Pandas dataframe with tokens as rows and classes as columns (namely, label_of_interest and 
        "other"). Values in this matrix are PMI scores.
    """
    pmi_scores = {l:{} for l in l_count.keys()}

    for l in l_count.keys():
        for w in w_count.keys():
            # P(w): occurrences of "w" in texts over the total number of texts (across labels)
            p_w = w_count[w] / float(num_texts)

            if (w, l) in w_l_count.keys():
                # P(w|l): co-occurrences of "w" and "l" in texts over the number of texts with label l
                p_w_l = w_l_count[(w, l)] / float(l_count[l])

                # PMI(w,l) = P(w|l)/P(w): pointwise mutual information
                pmi = math.log2(p_w_l / float(p_w))

                # Adjustment factor; co-occurrences of "w" and "l" in texts
                adj_factor = w_l_count[(w, l)]

                # Reweighted PMI(w,l) = PMI(w,l)*adj_factor: reweighted PMI to account for low-frequency terms
                rpmi = pmi * adj_factor

                # Positive reweighted PMI(w,l): all values below 0 are normalized to EPSILON
                if rpmi <= 0.0: rpmi = utils.EPSILON

                # Add the scores to the dictionary
                pmi_scores[l][w] = rpmi

    return pd.DataFrame(pmi_scores)


def get_counts(
    texts: List[str], 
    curr_label: str, 
    label_of_interest: str, 
    tokenizer: AutoTokenizer, 
    tokenizer_type: str,
    stopwords: str = "en"
) -> (Counter, Counter, Counter):
    """
    A function that calculates relevant counts about a specific label after tokenizing the text 
    according to a given pretrained tokenizer.
    Parameters
    ----------
    texts: List[str]
        Input texts belonging to a specific label "curr_label"
    curr_label: str
        Label whose examples will be counted and to which "texts" belong to
    label_of_interest: str
        Label that is the focus of the artifacts calculation
    tokenizer: AutoTokenizer
        HuggingFace's pretrained tokenizer to use
    tokenizer_type: str
        Name of the pretrained tokenizer according to HuggingFace (e.g., "bert-base-uncased")
    stopwords: str
        Language for the stopwords to be removed from lexical artifacts. Default: en (English)
        If None, all stopwords are instead retained in the list of lexical artifacts
        For now, only "en" is supported (with a default stopword list), more on next releases
    Returns
    -------
    token_counter: Counter
        Token counts for the given label "curr_label"
    label_counter: Counter
        Label counts for the given label "curr_label"
    token_label_counter: Counter
        Token and label counts for the given label "curr_label"
    """
    token_counter, label_counter, token_label_counter = Counter(), Counter(), Counter()

    for i in range(len(texts)):
        tokens = tokenizer.tokenize(texts[i])
        label = label_of_interest if (curr_label == label_of_interest) else "other"

        label_counter[label] += 1
        for token in set(tokens):
            if stopwords == "en":
                # Retain all tokens except stopwords
                if token.lstrip("Ġ") not in utils.EN_STOP_WORDS:
                    if token != "":
                        token_counter[token] += 1
                        token_label_counter[(token, label)] += 1
            else:
                if token != "":
                    token_counter[token] += 1
                    token_label_counter[(token, label)] += 1

    return token_counter, label_counter, token_label_counter


def normalize_pmi(pmi_scores: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """
    A function that normalize a dataframe of PMI scores in [0,1], following the implementation by [1].
    [1] Alan Ramponi and Sara Tonelli. 2022. Features or Spurious Artifacts? Data-centric Baselines 
    for Fair and Robust Hate Speech Detection. In Proceedings of the 2022 Conference of the North 
    American Chapter of the Association for Computational Linguistics: Human Language Technologies.
    Parameters
    ----------
    pmi_scores: pd.core.frame.DataFrame
        Pandas dataframe with tokens as rows and classes as columns (namely, label_of_interest and 
        "other"). Values in this matrix are PMI scores.
    Returns
    -------
    pmi_normalized: pd.core.frame.DataFrame
        Normalized pandas dataframe with tokens as rows and classes as columns (namely, label_of_interest 
        and "other"). Values in this matrix are normalized PMI scores.
    """

    def min_max_normalization(dataframe: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        An auxiliary function that performs the min-max normalization over log2 PMI scores.
        Parameters
        ----------
        dataframe: pd.core.frame.DataFrame
            Pandas dataframe with tokens as rows and classes as columns (namely, label_of_interest and 
            "other"). Values in this matrix are log2 PMI scores.
        Returns
        -------
        df_normalized: pd.core.frame.DataFrame
            Normalized pandas dataframe with tokens as rows and classes as columns (namely, label_of_interest 
            and "other"). Values in this matrix are min-max normalized log2 PMI scores.
        """
        df_normalized = dataframe.copy()

        for column in df_normalized.columns:
            curr_column = df_normalized[column]
            column_min = df_normalized[column].min()
            column_max = df_normalized[column].max()
            df_normalized[column] = (curr_column - column_min) / (column_max - column_min)
            
        return df_normalized

    # Fill missing values with epsilon for calculating the log2
    pmi_scores = pmi_scores.fillna(utils.EPSILON)

    # Normalize log2 PMI values in [0,1] (flattening negative values to zero)
    pmi_scores = np.log2(pmi_scores)
    pmi_scores[pmi_scores < 0.0] = 0.0
    pmi_normalized = min_max_normalization(pmi_scores)

    return pmi_normalized


def compute(
    texts: List[str], 
    labels: List[str], 
    label_of_interest: str, 
    method: str = "pmi", 
    special_tokens: List[str] = [],
    add_emojis: bool = True, 
    stopwords: str = "",
    pretrained_tokenizer: str = "bert-base-uncased", 
) -> pd.core.frame.DataFrame:
    """
    A function that computes lexical artifacts given an input dataset (texts and labels) and a label 
    of interest. Additional parameters can be specified to e.g., exclude emojis from the computation of
    lexical artifacts, add special tokens to the tokenizer's vocabulary, and in the near future changing the method and the
    pretrained tokenizer.
    [1] Alan Ramponi and Sara Tonelli. 2022. Features or Spurious Artifacts? Data-centric Baselines 
    for Fair and Robust Hate Speech Detection. In Proceedings of the 2022 Conference of the North 
    American Chapter of the Association for Computational Linguistics: Human Language Technologies.
    
    Parameters
    ----------
    texts: List[str]
        Input texts (note: the ith text of "texts" must match the ith label of "labels")
    labels: List[str]
        Input labels (note: the ith label of "labels" must match the ith text of "texts")
    label_of_interest: str
        Label that is the focus of the artifacts calculation (note: it must be in "labels")
    method: str
        Algorithm to compute the contribution strength of each token to each label. Default: "pmi"
        For now, we support "pmi" as implemented in [1], more on next releases
    special_tokens: List[str]
        List of special tokens to add to the tokenizer's vocabulary. Default: []
    add_emojis: bool
        Whether or not adding emojis to the tokenizer's vocabulary. Default: True
        If this is set to False, a special token "[EMOJI]" will be used for all emojis
    stopwords: str
        The language for the stopwords to be removed from lexical artifacts. Default: en (English)
        If None, all stopwords are instead retained in the list of lexical artifacts
        For now, only "en" is supported (with a default stopword list), more on next releases
    pretrained_tokenizer: str
        Name of the HuggingFace's pretrained tokenizer to use (e.g., "bert-base-uncased")
        For now, BPE-based tokenizers (e.g., RoBERTa-base, GPT2) would not filter stopword correctly,
        if requested, due to the "Ġ" special character. Thorough support on next releases
    Returns
    -------
    sorted_pmi_scores: pd.core.frame.DataFrame
        Pandas dataframe with tokens as rows and label_of_interest as column. Values in this matrix 
        are PMI scores following the implementation by [1].
    """

    # Ensure texts and labels are of the same size
    if len(texts) != len(labels):
        sys.exit(f"ERROR: The number of texts and labels do not match! Exit.")

    # Ensure the label of interest is actually in the label set
    if label_of_interest not in labels:
        sys.exit(f"ERROR: {label_of_interest} is not present in \"labels\"! Exit.")

    # Print a warning in case of very few examples
    if len(texts) <= 100:
        print(f"WARNING. It seems the dataset is so small ({len(texts)} examples). Note that this \
            may affect the reliability of artifacts computation.")

    # Convert labels to string and keep track of unique labels
    labels = [str(label) for label in labels]
    unique_labels = list(Counter(labels).keys())
    label_of_interest = str(label_of_interest)

    # Create a mapping dictionary label -> {text1, ..., textN}
    label_to_texts = {}
    for i in range(len(labels)):
        if labels[i] not in label_to_texts.keys():
            label_to_texts[labels[i]] = [texts[i]]
        else:
            label_to_texts[labels[i]].append(texts[i])

    # Initialize the pretrained tokenizer with special tokens
    tokenizer = AutoTokenizer.from_pretrained(pretrained_tokenizer, use_fast=True)
    tok_special_tokens = (special_tokens+utils.EMOJIS_TOKENS) if (add_emojis == True) else (special_tokens+[utils.EMOJI_TOKEN])
    special_tokens_dict = {'additional_special_tokens': tok_special_tokens}
    num_added_toks = tokenizer.add_special_tokens(special_tokens_dict)

    # Tokenize text, normalize labels, and count token/label/token-label occurrences
    token_counter, label_counter, token_label_counter = Counter(), Counter(), Counter()
    for curr_label in unique_labels:
        curr_token_counters, curr_label_counters, curr_token_label_counters = get_counts(
            label_to_texts[curr_label], curr_label, label_of_interest, tokenizer, pretrained_tokenizer, stopwords)
        token_counter += curr_token_counters
        label_counter += curr_label_counters
        token_label_counter += curr_token_label_counters
    
    # Get the total count of texts according to the labels that are taken into consideration
    texts_count = sum(label_counter.values())

    # Calculate the contribution strength of each token to each label
    if method == "pmi":
        # Calculate pointwise mutual information and normalize scores in [0,1]
        pmi_scores = compute_pmi(token_counter, label_counter, token_label_counter, texts_count)
        pmi_scores_norm = normalize_pmi(pmi_scores)
    else:
        sys.exit("The method {method} is not supported. Exit.")

    # Sort results by label (in descending order)
    sorted_pmi_scores = pmi_scores_norm[label_of_interest].to_frame().sort_values(
        by=[label_of_interest], ascending=False)
    
    return sorted_pmi_scores

