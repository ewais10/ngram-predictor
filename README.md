# ngram-predictor

Project scaffold for an n-gram language model predictor.

Directory layout:

- `config/` - environment settings
- `data/` - raw, processed, and model artifacts
- `src/` - source code (data_prep, model, inference, ui, evaluation)
- `tests/` - unit tests


## Environment Variables (config/.env)

| Variable | Description | Example Value |
|----------|-------------|----------------|
| `TRAIN_RAW_DIR` | Path to raw training data directory | `data/raw/train/` |
| `EVAL_RAW_DIR` | Path to raw evaluation data directory | `data/raw/eval/` |
| `TRAIN_TOKENS` | Path to processed training tokens file | `data/processed/train_tokens.txt` |
| `EVAL_TOKENS` | Path to processed evaluation tokens file | `data/processed/eval_tokens.txt` |
| `MODELF` | Path to save/load the trained model | `data/model/model.json` |
| `VOCAB` | Path to save/load the vocabulary | `data/model/vocab.json` |
| `UNK_THRESHOLD` | Minimum word frequency threshold (words below this become UNK) | `3` |
| `TOP_K` | Number of top predictions to return | `3` |
| `NGRAM_ORDER` | Maximum n-gram order (2 for bigrams, 3 for trigrams, etc.) | `4` |

## limitations
- Need to handle "underscores"
- Need to check split at punctuations