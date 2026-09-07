# YapSearch

A semantic search engine for a synthetic student group chat. YapSearch embeds 5000+ realistic Hinglish messages using `sentence-transformers` and allows meaning-based, speaker-filtered, and temporal-filtered search over the chat history.

## Architecture

- **Backend**: FastAPI
- **Embeddings**: `all-MiniLM-L6-v2`
- **Storage**: NumPy matrix (`embeddings.npy`) + JSON (`messages.json`)
- **Frontend**: Vanilla HTML/JS
0h
## Setup

1. Install dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Generate data:
   ```bash
   python scripts/generate_data.py
   ```

3. Generate embeddings:
   ```bash
   python scripts/embed_corpus.py
   ```

4. Run the server:
   ```bash
   python backend/main.py
   ```
   Navigate to `http://localhost:8000` to use the search UI.

## Evaluation

Run the evaluation script to test semantic retrieval performance against a 40-query ground truth set (including zero-overlap queries):
```bash
python scripts/run_eval.py
```

## Known Limitations & Future Work

1. **Corpus vs. Eval Strictness**: The synthetic corpus was lightly adjusted for narrative coherence around eval targets after the initial eval set generation (injecting relevant preceding chat context for zero-overlap targets). Therefore, the evaluation numbers should be read as indicative of the technique's potential rather than performance on a fully held-out, independent dataset.
2. **Context vs. Precision Trade-off**: Prepending context dramatically improved our ability to retrieve zero-overlap messages, but it diluted the embeddings of clean, direct queries. We used a Z-score normalized hybrid blend (`0.6 raw + 0.4 context`) to recover precision. While normalization was a necessary mathematical correctness fix due to different cosine scale spreads, the bigger driver of the precision trade-off is inherently *distractor competition*—the context itself often becomes a better lexical match than the actual target message.
3. **Small Model Limitations**: We used a lightweight model (`paraphrase-multilingual-MiniLM-L12-v2`) which handles transliterated Hinglish adequately but could be significantly improved by fine-tuning on a contrastive Hinglish dataset.
