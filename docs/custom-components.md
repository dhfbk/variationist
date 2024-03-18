# Custom components

🕵️‍♀️ Variationist supports custom components set by the users. In particular, there are two customizable components: tokenizers and metrics.

## Custom tokenizers

While 🕵️‍♀️ Variationist natively supports different types of language [units](https://github.com/dhfbk/variationist/tree/main/docs/units.md) through its build-in [tokenization](https://github.com/dhfbk/variationist/edit/main/docs/tokenizers.md) module, users can also plug in their own custom tokenizers, as they may be interested in analyzing different types of units from traditional ones.

Just like with the built-in tokenizer options, custom tokenizers are defined with the `tokenizer` argument in `InspectorArgs`. You just have to have your own tokenization function first.

Tokenization functions in 🕵️‍♀️ Variationist are supposed to take as input a `pandas.Series` containing a text column and the `InspectorArgs` (as some functions might need some of the args for certain operations). They are then supposed to return a `pandas.Series` containing the tokenized texts. If your function works for each text, you can use `apply()` to run it on the entire series.

For **example**, if we want to use characters as units, we can simply turn our text strings into lists with the Python built-in function `list()`:
```
def char_tokenization_fn(text_column, inspector_args):
    tok_lines = text_column.apply(list)
    return tok_lines
```
We can then tell 🕵️‍♀️ Variationist to use this function for tokenizing texts as we would define any other tokenizer in 🕵️‍♀️ Variationist, through the **`tokenizer`** parameter of the `InspectorArgs` class.

```
ins_args = InspectorArgs(text_names=["text"],
                         var_names=["label"],
                         metrics=["npw_pmi"],
                         tokenizer=char_tokenization_fn)
```

## Custom metrics

🕵️‍♀️ Variationist can also accept any custom metric defined by the user in addition to the built-in [metrics](https://github.com/dhfbk/variationist/blob/main/docs/metrics.md). Metrics, including custom ones, are called with the following 3 arguments:
- `label_values_dict`: A `dict` containing all of the possible values each variable (or combination thereof) can take in the input dataset.
- `subsets_of_interest`: A `dict` containing a `pandas.Series` for each subset to be analyzed, i.e. for each combination of text columns or variable values.
- `args`: The `InspectorArgs` defined before running the `Inspector`.

They should return a Python `dict` with the calculated metric for each subset.

For an example of how to define and use custom metrics in 🕵️‍♀️ Variationist, check out this [notebook](https://github.com/dhfbk/variationist/blob/main/examples/Variationist%20-%20Example%202%3A%20Custom%20Metrics.ipynb).
