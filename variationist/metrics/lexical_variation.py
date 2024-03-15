import math
from statistics import stdev, mean
from tqdm import tqdm


def safe_divide(numerator, denominator):
    """Utility function to avoid zero division errors."""
    if denominator == 0 or denominator == 0.0:
        result = 0
    else:
        result = numerator / denominator

    return result


def ttr(label_values_dict, subsets_of_interest, args):
    """Calculates Type Token Ratio.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
    
    Returns
    -------
    values_dict (`dict`):
        A dictionary with the mean TTR score for each subset and its standard deviation.
    """
    values_dict = dict()
    for column in label_values_dict:
        for l in tqdm(range(len(label_values_dict[column]))):
            values_list = []
            curr_label = subsets_of_interest[column][l].name
            for sentence in subsets_of_interest[column][l]:
                if len(sentence) == 0:
                    continue
                tok = len(sentence)
                typ = len(list(dict.fromkeys(sentence)))
                values_list.append(safe_divide(typ,tok))
            values_dict[curr_label] = dict()
            if len(values_list) == 0:
                values_dict[curr_label]["mean"] = 0
            else:
                values_dict[curr_label]["mean"] = mean(values_list)
            if len(values_list) < 2:
                values_dict[curr_label]["stdev"] = 0
            else:
                values_dict[curr_label]["stdev"] = stdev(values_list)

    # print("TTR: ",values_dict)

    return values_dict


def rttr(label_values_dict, subsets_of_interest, args):
    """Calculates Root Type Token Ratio.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
    
    Returns
    -------
    values_dict (`dict`):
        A dictionary with the mean RTTR score for each subset and its standard deviation.
    """
    values_dict = dict()
    for column in label_values_dict:
        for l in tqdm(range(len(label_values_dict[column]))):
            values_list = []
            curr_label = subsets_of_interest[column][l].name
            for sentence in subsets_of_interest[column][l]:
                if len(sentence) == 0:
                    continue
                tok = len(sentence)
                typ = len(list(dict.fromkeys(sentence)))
                values_list.append(safe_divide(typ,math.sqrt(tok)))
            values_dict[curr_label] = dict()
            if len(values_list) == 0:
                values_dict[curr_label]["mean"] = 0
            else:
                values_dict[curr_label]["mean"] = mean(values_list)
            if len(values_list) < 2:
                values_dict[curr_label]["stdev"] = 0
            else:
                values_dict[curr_label]["stdev"] = stdev(values_list)

    # print("RTTR: ",values_dict)

    return values_dict


def maas(label_values_dict, subsets_of_interest, args):
    """Calculates Maas's index (Maas, 1972).
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
    
    Returns
    -------
    values_dict (`dict`):
        A dictionary with the mean Maas index score for each subset and its standard deviation.
    """
    values_dict = dict()
    for column in label_values_dict:
        for l in tqdm(range(len(label_values_dict[column]))):
            values_list = []
            curr_label = subsets_of_interest[column][l].name
            for sentence in subsets_of_interest[column][l]:
                if len(sentence) == 0:
                    continue
                tok = len(sentence)
                typ = len(list(dict.fromkeys(sentence)))
                values_list.append(safe_divide((math.log10(tok)-math.log10(typ)), math.pow(math.log10(tok),2)))
            values_dict[curr_label] = dict()
            if len(values_list) == 0:
                values_dict[curr_label]["mean"] = 0
            else:
                values_dict[curr_label]["mean"] = mean(values_list)
            if len(values_list) < 2:
                values_dict[curr_label]["stdev"] = 0
            else:
                values_dict[curr_label]["stdev"] = stdev(values_list)

    # print("MAAS: ",values_dict)

    return values_dict


def lttr(label_values_dict, subsets_of_interest, args):
    """Calculates Log Type Token Ratio.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
    
    Returns
    -------
    values_dict (`dict`):
        A dictionary with the mean LTTR score for each subset and its standard deviation.
    """
    values_dict = dict()
    for column in label_values_dict:
        for l in tqdm(range(len(label_values_dict[column]))):
            values_list = []
            curr_label = subsets_of_interest[column][l].name
            for sentence in subsets_of_interest[column][l]:
                if len(sentence) == 0:
                    continue
                tok = len(sentence)
                typ = len(list(dict.fromkeys(sentence)))
                values_list.append(safe_divide(math.log10(typ), math.log10(tok)))
            values_dict[curr_label] = dict()
            if len(values_list) == 0:
                values_dict[curr_label]["mean"] = 0
            else:
                values_dict[curr_label]["mean"] = mean(values_list)
            if len(values_list) < 2:
                values_dict[curr_label]["stdev"] = 0
            else:
                values_dict[curr_label]["stdev"] = stdev(values_list)

    # print("LTTR: ",values_dict)
    
    return values_dict

