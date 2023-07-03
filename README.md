# Create the environment

```
conda create --name variation-explorer python=3.9
conda activate variation-explorer
pip install -r requirements.txt
```


# Run variation explorer

```
streamlit run main.py
```

# Run without interface

```
python3 main.py --dataset_filename data/netflix-toy.tsv  --text_cols text --label_cols label --metrics pmi
```

```
python3 main.py --dataset_filename data/netflix-toy.tsv  --text_cols text --label_cols label --metrics most-frequent
```