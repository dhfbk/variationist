# Tokenizers

Since the driver for the computation is a language [unit](https://github.com/dhfbk/variationist/tree/main/docs/units.md), we need ways to segment texts into desired units.

A tokenizer can be defined through the **`tokenizer`** parameter of the `InspectorArgs` class. For defining custom tokenizers, see [custom components](https://github.com/dhfbk/variationist/tree/main/docs/custom-components.md). Off-the-shelf choices are the following:

- A default whitespace tokenizer that goes beyond Latin characters (i.e., `whitespace`, by default)
- Any tokenizer from 🤗 [Hugging Face](https://huggingface.co/), represented by a string `hf::$TOKENIZER_NAME`, where `$TOKENIZER_NAME` is the name of a model's tokenizer as indicated in the Hugging Face repository

This ample choice (including custom tokenizers) avoids any assumptions on what actually *is* a language [unit](https://github.com/dhfbk/variationist/tree/main/docs/units.md), also broaden the applicability of 🕵️‍♀️ Variationist to a wide range of language varieties.