import pandas as pd

def get_all_frequencies(pandas_series):
	freq_dict = dict()
	for sentence in pandas_series:
		for token in sentence:
			if token not in freq_dict:
				freq_dict[token] = 0
			freq_dict[token]+=1
	return(freq_dict)


# TODO add lexical variety metrics (TTR, MTLD)